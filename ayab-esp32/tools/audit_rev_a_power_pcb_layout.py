#!/usr/bin/env python3
"""Capture KiCad-native placement data before integrating the Rev A power fixes.

This is deliberately read-only.  It inventories the existing two buck stages
and the ESP32 GPIO4 area so U403 and the sense divider can be placed without
guessing at coordinates or disturbing validated copper.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "ayab-esp32.kicad_pcb"
POWER_REFS = {
    "U601", "U602", "D605", "D606", "L601", "L602",
    "C612", "C613", "C614", "C615", "C616", "C617", "C618", "C619", "C620", "C621",
    "R606", "R607", "R608", "R609", "R610", "TP602", "TP603",
}
ANCHORS = {"U601", "U201"}


def mm(value: int) -> float:
    return pcbnew.ToMM(value)


def point(position) -> str:
    return f"({mm(position.x):.3f}, {mm(position.y):.3f})"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    board = pcbnew.LoadBoard(str(PCB))
    if board is None:
        raise RuntimeError(f"could not load {PCB}")
    footprints = {footprint.GetReference(): footprint for footprint in board.GetFootprints()}

    lines = [
        "# KH910 Rev A — Power PCB Placement Preflight",
        "",
        "Read-only KiCad-native inventory used before adding U403 and R215/R216.",
        "",
        "## Existing power-stage footprints and pads",
        "",
    ]
    for ref in sorted(POWER_REFS):
        footprint = footprints.get(ref)
        if footprint is None:
            lines.append(f"- {ref}: **missing**")
            continue
        lines.append(f"### {ref} — `{footprint.GetValue()}` at {point(footprint.GetPosition())}")
        for pad in footprint.Pads():
            lines.append(f"- pad {pad.GetNumber()} {point(pad.GetPosition())}: `{pad.GetNetname()}`")
        lines.append("")

    lines += ["## Nearby placement inventory", ""]
    for anchor_ref in sorted(ANCHORS):
        anchor = footprints[anchor_ref]
        anchor_pos = anchor.GetPosition()
        lines.append(f"### Within 18 mm of {anchor_ref} at {point(anchor_pos)}")
        nearby = []
        for ref, footprint in footprints.items():
            if ref == anchor_ref:
                continue
            pos = footprint.GetPosition()
            dx, dy = mm(pos.x - anchor_pos.x), mm(pos.y - anchor_pos.y)
            distance = (dx * dx + dy * dy) ** 0.5
            if distance <= 18.0:
                nearby.append((distance, ref, footprint.GetValue(), point(pos)))
        for distance, ref, value, pos in sorted(nearby):
            lines.append(f"- {distance:.2f} mm: {ref} `{value}` at {pos}")
        lines.append("")

    lines += [
        "## Required staged edits",
        "",
        "- Place U403 adjacent to the U601 filtered-output cluster, then partition only that output from the existing +5V copper.",
        "- Place R215/R216 beside U201 GPIO4, route the divider locally, and leave the high-voltage +12V segment away from USB/data routing.",
        "- Refill zones and prove DRC, connectivity, and the power-state topology before promotion.",
    ]
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
