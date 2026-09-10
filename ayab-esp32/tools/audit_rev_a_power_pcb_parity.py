#!/usr/bin/env python3
"""Report the physical PCB coverage of the prototype-critical Rev A power path.

KiCad's board DRC intentionally does not compare a board against the schematic.
This audit gets the authoritative netlist from the multi-sheet design, derives
the local support parts electrically attached to the Rev A power seeds, then
checks that every such part has a placed PCB footprint with the same value.
It is read-only: a failed audit is a design-review result, not a board edit.
"""
from __future__ import annotations

import argparse
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT / "ayab-esp32.kicad_sch"
PCB = ROOT / "ayab-esp32.kicad_pcb"

# These are the deliberate Rev A additions that make USB-service power safe
# and allow firmware to recognize machine power.  The complete support set is
# derived from their non-global nets instead of being maintained by hand.
SEEDS = {"U401", "U402", "U403", "R215", "R216", "TP403"}
GLOBAL_NETS = {"", "GND", "+12V", "+5V", "+3V3", "5V", "3V3"}


def export_netlist(destination: Path) -> None:
    command = ["kicad-cli", "sch", "export", "netlist", "-o", str(destination), str(TOP)]
    subprocess.run(command, check=True)


def parse_netlist(path: Path) -> tuple[dict[str, str], dict[str, set[str]]]:
    root = ET.parse(path).getroot()
    values = {
        comp.attrib["ref"]: (comp.findtext("value") or "")
        for comp in root.findall("./components/comp")
    }
    net_members: dict[str, set[str]] = {}
    for net in root.findall("./nets/net"):
        net_members[net.attrib.get("name", "")] = {
            node.attrib["ref"] for node in net.findall("node") if "ref" in node.attrib
        }
    return values, net_members


def board_parts() -> dict[str, str]:
    board = pcbnew.LoadBoard(str(PCB))
    if board is None:
        raise RuntimeError(f"could not load {PCB}")
    return {footprint.GetReference(): footprint.GetValue() for footprint in board.GetFootprints()}


def render_report(values: dict[str, str], net_members: dict[str, set[str]], placed: dict[str, str]) -> str:
    absent_seeds = sorted(SEEDS - set(values))
    if absent_seeds:
        raise RuntimeError(f"power seed(s) absent from authoritative netlist: {', '.join(absent_seeds)}")

    seed_nets = {
        name: members for name, members in net_members.items()
        if name not in GLOBAL_NETS and members & SEEDS
    }
    expected = set(SEEDS)
    for members in seed_nets.values():
        expected.update(members)

    missing = sorted(expected - set(placed))
    mismatched = sorted(
        ref for ref in expected & set(placed) if values.get(ref, "") != placed[ref]
    )
    lines = [
        "# KH910 Rev A — Prototype Power PCB Parity Audit",
        "",
        "Read-only comparison of the schematic-derived Rev A power circuit with the physical PCB.",
        "",
        "## Seed components",
        "",
    ]
    for ref in sorted(SEEDS):
        lines.append(f"- {ref}: schematic `{values[ref]}`; " + ("PCB present" if ref in placed else "**PCB MISSING**"))

    lines += ["", "## Local power nets and directly attached components", ""]
    for net, members in sorted(seed_nets.items()):
        lines.append(f"- `{net}`: " + ", ".join(f"`{ref}`" for ref in sorted(members)))

    lines += ["", "## Required PCB parity", ""]
    for ref in sorted(expected):
        expected_value = values.get(ref, "")
        actual = placed.get(ref)
        if actual is None:
            status = "**MISSING**"
        elif actual != expected_value:
            status = f"**VALUE MISMATCH: PCB `{actual}`**"
        else:
            status = "present"
        lines.append(f"- {ref} `{expected_value}`: {status}")

    lines += ["", "## Result", ""]
    if missing or mismatched:
        lines.append("**BLOCKED:** the prototype power circuit is not fully represented on the PCB.")
        if missing:
            lines.append("- Missing footprints: " + ", ".join(f"`{ref}`" for ref in missing))
        if mismatched:
            lines.append("- Value mismatches: " + ", ".join(f"`{ref}`" for ref in mismatched))
    else:
        lines.append("**PASS:** every schematic-derived local power part has a matching physical footprint.")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as temp_dir:
        netlist = Path(temp_dir) / "rev-a-power.net"
        export_netlist(netlist)
        values, net_members = parse_netlist(netlist)
    report = render_report(values, net_members, board_parts())
    args.output.write_text(report, encoding="utf-8")
    print(args.output)
    if "**BLOCKED:**" in report:
        raise SystemExit("prototype power PCB parity is incomplete")


if __name__ == "__main__":
    main()
