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
# These are the *active project* reference designators.  The source files also
# retain historical labels from an earlier project, for example U401 -> U601
# and TP403 -> TP603.  Only the assembled root netlist resolves those mappings
# correctly, so do not inspect child sheets in isolation for PCB parity.
SEEDS = {"U601", "U602", "U403", "R215", "R216", "TP603"}
GLOBAL_NETS = {"", "GND", "+12V", "+5V", "+3V3", "5V", "3V3"}


def normalized_pin_net(name: str) -> str:
    """Treat KiCad's synthetic unconnected net name as an open PCB pad."""
    return "" if name.startswith("unconnected-(") else name


def export_netlist(destination: Path) -> None:
    command = [
        "kicad-cli", "sch", "export", "netlist", "--format", "kicadxml",
        "-o", str(destination), str(TOP),
    ]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(
            "netlist export failed:\n"
            + " ".join(command)
            + f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def parse_netlist(path: Path) -> tuple[dict[str, str], dict[str, set[str]], dict[tuple[str, str], str]]:
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
    pin_nets = {
        (node.attrib["ref"], node.attrib["pin"]): net.attrib.get("name", "")
        for net in root.findall("./nets/net")
        for node in net.findall("node")
        if "ref" in node.attrib and "pin" in node.attrib
    }
    return values, net_members, pin_nets


def board_parts() -> tuple[dict[str, str], dict[tuple[str, str], str]]:
    board = pcbnew.LoadBoard(str(PCB))
    if board is None:
        raise RuntimeError(f"could not load {PCB}")
    values = {footprint.GetReference(): footprint.GetValue() for footprint in board.GetFootprints()}
    pin_nets = {
        (footprint.GetReference(), pad.GetNumber()): pad.GetNetname()
        for footprint in board.GetFootprints()
        for pad in footprint.Pads()
    }
    return values, pin_nets


def render_report(values: dict[str, str], net_members: dict[str, set[str]],
                  schematic_pins: dict[tuple[str, str], str], placed: dict[str, str],
                  board_pins: dict[tuple[str, str], str]) -> str:
    absent_seeds = sorted(SEEDS - set(values))
    if absent_seeds:
        raise RuntimeError(
            "active-project power seed(s) absent from assembled netlist: "
            + ", ".join(absent_seeds)
        )
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
    topology_mismatches = []
    for key, actual in sorted(board_pins.items()):
        if key[0] not in SEEDS:
            continue
        expected_net = normalized_pin_net(schematic_pins.get(key, ""))
        if actual != expected_net:
            topology_mismatches.append((key[0], key[1], expected_net, actual))
    preserved_checks = [
        ("GPIO4 is machine-power sense", board_pins.get(("U201", "8")) == "/ESP32/MACHINE_PWR_SENSE"),
        ("active right end-stop remains on GPIO17",
         board_pins.get(("U201", "21")) == "/BROTHER-CONNECTORS/EOL_R_N"),
        ("J701.7 remains tied locally to U701.15",
         board_pins.get(("J701", "7")) == board_pins.get(("U701", "15"))
         and board_pins.get(("J701", "7")) not in (None, "", "/ESP32/MACHINE_PWR_SENSE")),
    ]
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

    lines += ["", "## Pin-level power topology", ""]
    for ref in sorted(SEEDS):
        for key, raw_expected_net in sorted(schematic_pins.items()):
            if key[0] != ref:
                continue
            expected_net = normalized_pin_net(raw_expected_net)
            actual = board_pins.get(key, "")
            status = "matches" if actual == expected_net else f"**PCB `{actual or 'unconnected'}`**"
            lines.append(f"- {ref}.{key[1]}: schematic `{expected_net or 'unconnected'}`; {status}")

    lines += ["", "## Preserved GPIO/control topology", ""]
    for label, passed in preserved_checks:
        lines.append(f"- {label}: " + ("**PASS**" if passed else "**FAIL**"))

    lines += ["", "## Result", ""]
    if missing or mismatched or topology_mismatches or not all(passed for _, passed in preserved_checks):
        lines.append("**BLOCKED:** the prototype power circuit is not fully represented on the PCB.")
        if missing:
            lines.append("- Missing footprints: " + ", ".join(f"`{ref}`" for ref in missing))
        if mismatched:
            lines.append("- Value mismatches: " + ", ".join(f"`{ref}`" for ref in mismatched))
        for ref, pin, expected_net, actual in topology_mismatches:
            lines.append(
                f"- Topology mismatch: `{ref}.{pin}` expected `{expected_net or 'unconnected'}`, "
                f"found `{actual or 'unconnected'}`"
            )
    else:
        lines.append("**PASS:** every schematic-derived local power part has a matching physical footprint.")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            netlist = Path(temp_dir) / "rev-a-power.net"
            export_netlist(netlist)
            values, net_members, schematic_pins = parse_netlist(netlist)
        placed, board_pins = board_parts()
        report = render_report(values, net_members, schematic_pins, placed, board_pins)
    except Exception as exc:
        report = (
            "# KH910 Rev A — Prototype Power PCB Parity Audit\n\n"
            "**AUDIT EXECUTION FAILED:** the power circuit was not evaluated.\n\n"
            "```text\n"
            + str(exc)
            + "\n```\n"
        )
        args.output.write_text(report, encoding="utf-8")
        print(args.output)
        raise
    args.output.write_text(report, encoding="utf-8")
    print(args.output)
    if "**BLOCKED:**" in report:
        raise SystemExit("prototype power PCB parity is incomplete")


if __name__ == "__main__":
    main()
