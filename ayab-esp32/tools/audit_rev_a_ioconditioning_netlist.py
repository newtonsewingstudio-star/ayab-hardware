#!/usr/bin/env python3
"""Audit legacy LM393 carriage/Hall conditioning from a KiCad XML netlist.

Usage:
  audit_rev_a_ioconditioning_netlist.py NETLIST_XML [OUTPUT_MD]

The report is intentionally read-only. It identifies every net touching U702/U703,
expands those nets to connected component pins, and maps the complete pin-to-net
topology of the local R715-R738 / C701-C704 network so Rev A can remove only
obsolete comparator circuitry without disturbing retained ADC or encoder paths.
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

TARGET_REFS = {"U702", "U703"}
LEGACY_NAME_TOKENS = (
    "EOL_R", "EOL_L", "HALL", "KH910_R_K", "KH910_R_L", "ENC_",
)


def text(node, tag, default=""):
    child = node.find(tag)
    return child.text.strip() if child is not None and child.text else default


def local_ref(ref: str) -> bool:
    if ref in {"U701", "U702", "U703", "C701", "C702", "C703", "C704", "TP701", "TP702"}:
        return True
    m = re.fullmatch(r"R(\d+)", ref)
    return bool(m and 701 <= int(m.group(1)) <= 738)


def main() -> None:
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: audit_rev_a_ioconditioning_netlist.py NETLIST_XML [OUTPUT_MD]")

    netlist_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) == 3 else Path("KH910_REV_A_IOCONDITIONING_AUDIT.md")
    root = ET.parse(netlist_path).getroot()

    comps = {}
    for comp in root.findall("./components/comp"):
        ref = comp.get("ref", "")
        comps[ref] = {
            "value": text(comp, "value"),
            "footprint": text(comp, "footprint"),
            "datasheet": text(comp, "datasheet"),
        }

    nets = []
    pin_to_nets = defaultdict(list)
    ref_pin_nodes = defaultdict(dict)
    for net in root.findall("./nets/net"):
        name = net.get("name", "")
        code = net.get("code", "")
        nodes = []
        for node in net.findall("node"):
            item = {
                "ref": node.get("ref", ""),
                "pin": node.get("pin", ""),
                "pinfunction": node.get("pinfunction", ""),
                "pintype": node.get("pintype", ""),
            }
            nodes.append(item)
            pin_to_nets[(item["ref"], item["pin"])].append(name)
            ref_pin_nodes[item["ref"]][item["pin"]] = (name, item["pinfunction"], item["pintype"])
        nets.append({"name": name, "code": code, "nodes": nodes})

    comparator_nets = [
        n for n in nets if any(node["ref"] in TARGET_REFS for node in n["nodes"])
    ]
    named_signal_nets = [
        n for n in nets if any(tok in n["name"].upper() for tok in LEGACY_NAME_TOKENS)
    ]

    connected_refs = set(TARGET_REFS)
    for net in comparator_nets:
        connected_refs.update(node["ref"] for node in net["nodes"] if node["ref"])

    lines = [
        "# KH910 Rev A — I/O Conditioning Netlist Audit",
        "",
        "Generated from the full hierarchical KiCad netlist. This is the electrical source of truth for the legacy LM393 section before Rev A removal/rework.",
        "",
        f"- components in netlist: **{len(comps)}**",
        f"- nets in netlist: **{len(nets)}**",
        f"- nets touching U702/U703: **{len(comparator_nets)}**",
        f"- refs electrically adjacent to U702/U703: **{len(connected_refs)}**",
        "",
        "## Comparator devices",
        "",
        "| Ref | Value | Footprint |",
        "|---|---|---|",
    ]
    for ref in sorted(TARGET_REFS):
        c = comps.get(ref, {})
        lines.append(f"| {ref} | {c.get('value','<missing>')} | `{c.get('footprint','')}` |")

    lines += ["", "## Every net touching U702/U703", ""]
    for net in sorted(comparator_nets, key=lambda n: n["name"]):
        lines += [f"### `{net['name'] or '<unnamed>'}` (code {net['code']})", ""]
        lines += ["| Ref | Pin | Function | Type | Value |", "|---|---:|---|---|---|"]
        for node in sorted(net["nodes"], key=lambda x: (x["ref"], x["pin"])):
            c = comps.get(node["ref"], {})
            lines.append(
                f"| {node['ref']} | {node['pin']} | {node['pinfunction']} | {node['pintype']} | {c.get('value','')} |"
            )
        lines.append("")

    lines += ["## Hall / EOL / encoder named nets", ""]
    for net in sorted(named_signal_nets, key=lambda n: n["name"]):
        members = ", ".join(
            f"{node['ref']}:{node['pin']}" for node in sorted(net["nodes"], key=lambda x: (x["ref"], x["pin"]))
        )
        lines.append(f"- `{net['name']}`: {members}")

    lines += ["", "## Local conditioning component topology", ""]
    lines += [
        "This table lists every connected pin for U701-U703, C701-C704, TP701/TP702 and R701-R738. It is the removal decision table.",
        "",
        "| Ref | Value | Pin 1 / net | Pin 2 / net | Other pins / nets |",
        "|---|---|---|---|---|",
    ]
    for ref in sorted((r for r in comps if local_ref(r)), key=lambda r: (r[0], int(re.sub(r'\D', '', r) or 0), r)):
        c = comps.get(ref, {})
        pins = ref_pin_nodes.get(ref, {})
        def desc(pin):
            if pin not in pins:
                return "—"
            net, fn, typ = pins[pin]
            suffix = f" ({fn})" if fn else ""
            return f"`{net or '<unnamed>'}`{suffix}"
        others = []
        for pin in sorted((p for p in pins if p not in {"1", "2"}), key=lambda p: (len(p), p)):
            net, fn, typ = pins[pin]
            others.append(f"{pin}: `{net or '<unnamed>'}`" + (f" ({fn})" if fn else ""))
        lines.append(f"| {ref} | {c.get('value','')} | {desc('1')} | {desc('2')} | {'; '.join(others) if others else '—'} |")

    lines += ["", "## Adjacent component inventory", ""]
    lines += ["| Ref | Value | Footprint |", "|---|---|---|"]
    for ref in sorted(connected_refs):
        c = comps.get(ref, {})
        lines.append(f"| {ref} | {c.get('value','')} | `{c.get('footprint','')}` |")

    lines += [
        "",
        "## Rev A interpretation gate",
        "",
        "Do not delete U702/U703 by reference alone. The removal patch must preserve the passive HALL_L_ADC/HALL_R_ADC dividers and the encoder path, then be verified by ERC plus a regenerated netlist.",
    ]

    out_path.write_text("\n".join(lines) + "\n")
    print(out_path)


if __name__ == "__main__":
    main()
