#!/usr/bin/env python3
"""Audit Rev A Hall/comparator PCB parity using KiCad pcbnew.

This is read-only. It inventories the old LM393 footprint cluster, the retained
raw-Hall test points, current ESP32 Hall-input pad nets, candidate net names,
and nearby board space so the PCB migration can remove obsolete comparator
hardware and add R735-R738 in one controlled edit.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "ayab-esp32.kicad_pcb"
OUT = ROOT / "KH910_REV_A_HALL_PCB_PARITY.md"

OBSOLETE = {
    "U702", "U703", "C703", "C704",
    *(f"R{i}" for i in range(715, 735)),
}
NEW_DIVIDERS = {"R735", "R736", "R737", "R738"}
INTERESTING = OBSOLETE | NEW_DIVIDERS | {"U701", "TP701", "TP702", "U201", "J408", "J409", "J411", "J412", "J414"}


def mm(v: int) -> float:
    return pcbnew.ToMM(v)


def fp_pos(fp) -> str:
    p = fp.GetPosition()
    return f"({mm(p.x):.3f}, {mm(p.y):.3f}) rot {fp.GetOrientationDegrees():.1f}"


def pad_pos(pad) -> str:
    p = pad.GetPosition()
    return f"({mm(p.x):.3f}, {mm(p.y):.3f})"


def main() -> None:
    board = pcbnew.LoadBoard(str(PCB))
    fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
    nets_by_name = {}
    for code, netinfo in board.GetNetInfo().NetsByNetcode().items():
        nets_by_name[netinfo.GetNetname()] = code

    lines = [
        "# KH910 Rev A — Hall / Comparator PCB Parity Audit",
        "",
        "Generated read-only from the current repository PCB using KiCad `pcbnew`.",
        "",
        f"- Board footprints: **{len(fps)}**",
        f"- Board nets: **{len(nets_by_name)}**",
        f"- Obsolete comparator footprints still present: **{len(OBSOLETE & set(fps))}/{len(OBSOLETE)}**",
        f"- New Hall-divider footprints present: **{len(NEW_DIVIDERS & set(fps))}/4**",
        "",
        "## Required parity summary",
        "",
    ]
    for ref in sorted(OBSOLETE):
        lines.append(f"- {ref}: {'PRESENT (remove)' if ref in fps else 'absent'}")
    for ref in sorted(NEW_DIVIDERS):
        lines.append(f"- {ref}: {'PRESENT' if ref in fps else '**MISSING (add)**'}")

    lines += ["", "## Interesting footprints and pads", ""]
    for ref in sorted(INTERESTING):
        fp = fps.get(ref)
        if not fp:
            continue
        lines += [f"### {ref} — {fp.GetValue()}", f"- footprint at: {fp_pos(fp)}"]
        for pad in fp.Pads():
            if ref == "U201" and pad.GetNumber() not in {"5", "6", "17", "18"}:
                continue
            lines.append(
                f"- pad {pad.GetNumber()}: {pad_pos(pad)} net `{pad.GetNetname()}` (#{pad.GetNetCode()})"
            )
        lines.append("")

    lines += ["## Hall-related board nets", ""]
    hall_tokens = ("EOL_L", "EOL_R", "HALL", "KH910_R_K", "KH910_R_L")
    selected_nets = sorted(
        (name, code) for name, code in nets_by_name.items()
        if any(tok in name.upper() for tok in hall_tokens)
    )
    if selected_nets:
        for name, code in selected_nets:
            lines.append(f"- net {code}: `{name}`")
    else:
        lines.append("- No Hall/EOL/KH910-named nets found.")

    lines += ["", "## Raw Hall test points", ""]
    for ref in ("TP701", "TP702"):
        fp = fps.get(ref)
        if not fp:
            lines.append(f"- {ref}: **missing**")
            continue
        pads = list(fp.Pads())
        for pad in pads:
            lines.append(f"- {ref}: {pad_pos(pad)} net `{pad.GetNetname()}`")

    # Inventory route endpoints attached directly to obsolete pads. This is
    # useful for later deterministic copper pruning after footprint removal.
    endpoint_items = defaultdict(list)
    for item in board.GetTracks():
        if isinstance(item, pcbnew.PCB_VIA):
            p = item.GetPosition()
            endpoint_items[(p.x, p.y)].append(
                f"via `{item.GetNetname()}` {board.GetLayerName(item.GetLayer())}"
            )
        elif isinstance(item, pcbnew.PCB_TRACK):
            s, e = item.GetStart(), item.GetEnd()
            desc = (
                f"track `{item.GetNetname()}` {board.GetLayerName(item.GetLayer())} "
                f"({mm(s.x):.3f},{mm(s.y):.3f})->({mm(e.x):.3f},{mm(e.y):.3f})"
            )
            endpoint_items[(s.x, s.y)].append(desc)
            endpoint_items[(e.x, e.y)].append(desc)

    lines += ["", "## Copper ending exactly on obsolete pads", ""]
    attached_count = 0
    for ref in sorted(OBSOLETE):
        fp = fps.get(ref)
        if not fp:
            continue
        for pad in fp.Pads():
            p = pad.GetPosition()
            attached = endpoint_items.get((p.x, p.y), [])
            if not attached:
                continue
            attached_count += len(attached)
            lines.append(
                f"- {ref} pad {pad.GetNumber()} {pad_pos(pad)} net `{pad.GetNetname()}`: "
                + " | ".join(attached)
            )
    if not attached_count:
        lines.append("- No routed track/via endpoints land exactly on obsolete pads.")

    # Free-space inventory around both former comparator clusters. Use centers
    # of U702/U703 if present and list footprints within 15 mm.
    lines += ["", "## Nearby footprint inventory around comparator clusters", ""]
    for anchor_ref in ("U702", "U703"):
        anchor = fps.get(anchor_ref)
        if not anchor:
            continue
        ap = anchor.GetPosition()
        lines += [f"### Around {anchor_ref} at {fp_pos(anchor)}", ""]
        nearby = []
        for ref, fp in fps.items():
            if ref == anchor_ref:
                continue
            p = fp.GetPosition()
            dx = mm(p.x - ap.x)
            dy = mm(p.y - ap.y)
            dist = (dx * dx + dy * dy) ** 0.5
            if dist <= 15.0:
                nearby.append((dist, ref, fp.GetValue(), fp_pos(fp)))
        for dist, ref, value, pos in sorted(nearby):
            lines.append(f"- {dist:.2f} mm: {ref} `{value}` at {pos}")
        lines.append("")

    lines += [
        "## Migration implications",
        "",
        "The PCB migration must remove the obsolete comparator footprint set and add R735-R738 before final parity validation. Net assignment for the new footprints must be derived from the validated schematic netlist, not guessed from legacy PCB net names.",
    ]

    OUT.write_text("\n".join(lines) + "\n")
    print(OUT)


if __name__ == "__main__":
    main()
