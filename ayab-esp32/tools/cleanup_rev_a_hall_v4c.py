#!/usr/bin/env python3
"""Clean only the residual copper identified by the v4c KiCad DRC reports.

Input is the staged v4c board after the board-aware A* Hall routes are added.
This script deliberately does not alter either A* route, divider footprint, MCU
pad assignment, or any unrelated net.

Repairs:
1. Remove legacy B.Cu Hall tails. The new A* In1.Cu routes terminate at the
   existing MCU Hall vias, so downstream retagged B.Cu tails are redundant.
2. Remove comparator-era supply stubs explicitly proven dangling by KiCad DRC.
3. Restore the direct GND link between adjacent U701 pads 11 and 12.

KiCad DRC is the final authority; all expected edits are assertion checked.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
import pcbnew

if len(sys.argv) != 2:
    raise SystemExit("usage: cleanup_rev_a_hall_v4c.py BOARD.kicad_pcb")

PATH = Path(sys.argv[1]).resolve()
board = pcbnew.LoadBoard(str(PATH))
if board is None:
    raise RuntimeError(f"could not load {PATH}")

ADC_L = "/ESP32/HALL_L_ADC"
ADC_R = "/ESP32/HALL_R_ADC"
GND = "GND"
P5 = "+5V"
TOL = 0.004


def mm(p):
    return (pcbnew.ToMM(p.x), pcbnew.ToMM(p.y))


def near(a, b, tol=TOL):
    return math.hypot(a[0] - b[0], a[1] - b[1]) <= tol


def endpoints(item):
    return mm(item.GetStart()), mm(item.GetEnd())


def same_ends(item, a, b):
    p, q = endpoints(item)
    return (near(p, a) and near(q, b)) or (near(p, b) and near(q, a))


def touches(item, point):
    p, q = endpoints(item)
    return near(p, point) or near(q, point)


def length_mm(item):
    p, q = endpoints(item)
    return math.hypot(p[0] - q[0], p[1] - q[1])


def net_obj(name):
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetname() == name and hasattr(pad, "GetNet"):
                return pad.GetNet()
    for item in board.GetTracks():
        if item.GetNetname() == name and hasattr(item, "GetNet"):
            return item.GetNet()
    raise RuntimeError(f"cannot resolve net object for {name}")


def add_track(a, b, net_name, layer=pcbnew.F_Cu, width_mm=0.25):
    tr = pcbnew.PCB_TRACK(board)
    tr.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(a[0]), pcbnew.FromMM(a[1])))
    tr.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(b[0]), pcbnew.FromMM(b[1])))
    tr.SetLayer(layer)
    tr.SetWidth(pcbnew.FromMM(width_mm))
    tr.SetNet(net_obj(net_name))
    board.Add(tr)


removed_adc = {ADC_L: 0, ADC_R: 0}
remove = []

# All B.Cu TRACK segments on the two ADC nets are legacy tails. Keep vias:
# the MCU vias are precisely where the new In1 routes meet the F.Cu MCU stubs.
for item in board.GetTracks():
    if isinstance(item, pcbnew.PCB_VIA):
        continue
    if item.GetLayer() == pcbnew.B_Cu and item.GetNetname() in removed_adc:
        remove.append(item)
        removed_adc[item.GetNetname()] += 1

if removed_adc[ADC_L] < 1 or removed_adc[ADC_R] < 1:
    raise RuntimeError(f"expected legacy ADC B.Cu tails on both nets, found {removed_adc}")

# Exact first-wave DRC-proven dead comparator-era supply segments.
exact_remove = [
    (GND, (91.7878, 142.2030), (91.0628, 141.4780)),
    (GND, (91.0628, 141.4780), (91.0628, 139.8280)),
    (P5,  (87.0878, 142.2030), (87.0878, 143.5522)),
    (P5,  (312.3250, 157.2800), (310.9000, 157.2800)),
    (P5,  (326.7700, 153.4250), (326.8200, 153.3750)),
]
found = {i: 0 for i in range(len(exact_remove))}
for item in board.GetTracks():
    if isinstance(item, pcbnew.PCB_VIA):
        continue
    for i, (name, a, b) in enumerate(exact_remove):
        if item.GetNetname() == name and same_ends(item, a, b):
            if item not in remove:
                remove.append(item)
            found[i] += 1

missing = [exact_remove[i] for i, count in found.items() if count != 1]
if missing:
    raise RuntimeError(f"expected exact residual segments once each; mismatches: {missing} counts={found}")

# Second DRC pass exposed the next pieces of two dead +5V branches. Match both
# the reported dangling endpoint and the KiCad-reported segment length, so a
# live neighboring branch sharing the same junction cannot be removed.
second_wave = [
    (P5, (310.9000, 157.2800), 0.7495),
    (P5, (325.2700, 153.4250), 1.5000),
]
second_found = []
for name, point, expected_len in second_wave:
    matches = [
        item for item in board.GetTracks()
        if not isinstance(item, pcbnew.PCB_VIA)
        and item.GetLayer() == pcbnew.F_Cu
        and item.GetNetname() == name
        and touches(item, point)
        and abs(length_mm(item) - expected_len) <= 0.01
        and item not in remove
    ]
    if len(matches) != 1:
        candidates = [
            (endpoints(item), round(length_mm(item), 4))
            for item in board.GetTracks()
            if not isinstance(item, pcbnew.PCB_VIA)
            and item.GetLayer() == pcbnew.F_Cu
            and item.GetNetname() == name
            and touches(item, point)
            and item not in remove
        ]
        raise RuntimeError(
            f"expected one second-wave dead segment at {name} {point} len {expected_len}; "
            f"found {len(matches)}; candidates={candidates}"
        )
    remove.append(matches[0])
    second_found.append((name, point, endpoints(matches[0]), round(length_mm(matches[0]), 4)))

for item in remove:
    board.Remove(item)

# Do not reconnect the former left comparator GND trunk. The second DRC pass
# proved the attempted 140.653 -> 139.828 link itself was a dead-end warning,
# while the board already had zero unconnected items. Leaving it absent is the
# correct cleanup result.

# U701 pads 11 and 12 are adjacent GND pins; comparator cleanup exposed the
# absence of their local bridge. Add the shortest possible same-net F.Cu link.
fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
u701 = fps.get("U701")
if u701 is None:
    raise RuntimeError("U701 missing")
pads = {str(p.GetNumber()): p for p in u701.Pads()}
for pn in ("11", "12"):
    if pn not in pads or pads[pn].GetNetname() != GND:
        raise RuntimeError(f"U701 pad {pn} is not present on GND")
p11 = mm(pads["11"].GetPosition())
p12 = mm(pads["12"].GetPosition())
if not near(p11, (191.4775, 160.4550)) or not near(p12, (191.4775, 161.1050)):
    raise RuntimeError(f"U701 GND pad coordinates changed: p11={p11} p12={p12}")
add_track(p11, p12, GND)

board.BuildConnectivity()
pcbnew.SaveBoard(str(PATH), board)
print("HALL_V4C_CLEANUP_OK", PATH)
print("REMOVED_ADC_BCU", removed_adc)
print("REMOVED_EXACT_SUPPLY_SEGMENTS", len(exact_remove))
print("REMOVED_SECOND_WAVE_SEGMENTS", second_found)
print("ADDED_U701_GND_LINK", p11, p12)
