#!/usr/bin/env python3
"""Find all-layer-clear through-via escape sites for the staged power circuit.

This is a read-only geometry probe.  A trace may fit on an inner layer while a
through-via at its endpoint still cuts an unrelated F.Cu trace; this probe
rejects those sites before routing is attempted.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "ayab-esp32.kicad_pcb"
VIA_RADIUS = 0.30
CLEARANCE = 0.24
STEP = 0.25


def mm(value: int) -> float:
    return pcbnew.ToMM(value)


def candidates(board: pcbnew.BOARD, name: str, net: str, centre: tuple[float, float],
               radius: float, count: int = 8) -> list[tuple[float, float]]:
    own = board.GetNetcodeFromNetname(net)
    blocked: list[tuple[float, float, float, float]] = []

    def add_box(item) -> None:
        box = item.GetBoundingBox()
        margin = VIA_RADIUS + CLEARANCE
        blocked.append((
            mm(box.GetX()) - margin, mm(box.GetY()) - margin,
            mm(box.GetX() + box.GetWidth()) + margin, mm(box.GetY() + box.GetHeight()) + margin,
        ))

    for item in board.GetTracks():
        if item.GetNetCode() != own:
            add_box(item)
    for footprint in board.GetFootprints():
        for pad in footprint.Pads():
            if pad.GetNetCode() != own:
                add_box(pad)

    viable = []
    cells = int(math.ceil(radius / STEP))
    for ix in range(-cells, cells + 1):
        for iy in range(-cells, cells + 1):
            x, y = centre[0] + ix * STEP, centre[1] + iy * STEP
            if math.hypot(x - centre[0], y - centre[1]) > radius:
                continue
            if any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in blocked):
                continue
            viable.append((x, y))
    viable.sort(key=lambda point: math.hypot(point[0] - centre[0], point[1] - centre[1]))
    print(name, net, "centre=%.3f,%.3f" % centre,
          "sites=" + " ".join("%.3f,%.3f" % point for point in viable[:count]))
    return viable[:count]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    board = pcbnew.LoadBoard(str(PCB))
    if board is None:
        raise RuntimeError(f"could not load {PCB}")
    lines: list[str] = ["# KH910 Rev A Power Via Escape Probe", ""]
    probes = (
        ("GPIO4_F_ESCAPE", "/ESP32/EOL_R_N", (217.125, 129.675), 3.0),
        ("SENSE_B_ESCAPE", "", (206.175, 137.500), 5.0),
        ("PLUS12_B_ESCAPE", "+12V", (207.825, 137.500), 5.0),
        ("GND_B_ESCAPE", "GND", (209.175, 137.500), 5.0),
        ("PLUS12_BUS_ESCAPE", "+12V", (207.000, 163.100), 4.0),
    )
    for name, net, centre, radius in probes:
        sites = candidates(board, name, net, centre, radius)
        lines.append(f"- {name}: " + (", ".join(f"({x:.3f}, {y:.3f})" for x, y in sites) or "**NONE**"))
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
