#!/usr/bin/env python3
"""Remove exactly the two KiCad-visible legacy K/L dangling tails.

The text migration cannot see these tracks reliably, but KiCad DRC reports them
after the board is loaded/rebuilt. Match by exact anchor geometry and expected
2.0375 mm horizontal-left length, independent of transient net assignment.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
import pcbnew

if len(sys.argv) != 2:
    raise SystemExit("usage: cleanup_rev_a_kl_legacy_tails.py BOARD.kicad_pcb")

PATH = Path(sys.argv[1]).resolve()
board = pcbnew.LoadBoard(str(PATH))
if board is None:
    raise RuntimeError(f"could not load {PATH}")

ANCHORS = [
    (193.515, 158.505),
    (193.515, 159.155),
]
EXPECTED_LEN = 2.0375
TOL = 0.02


def mm(v):
    return pcbnew.ToMM(v)


def endpoints(item):
    # KiCad 9's SWIG build can expose GetStart()/GetEnd() as opaque objects;
    # the scalar accessors are stable and documented on PCB_TRACK.
    return (
        (mm(item.GetStartX()), mm(item.GetStartY())),
        (mm(item.GetEndX()), mm(item.GetEndY())),
    )


def near(a, b, tol=TOL):
    return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol


def candidate_for_anchor(anchor):
    matches = []
    nearby = []
    for item in list(board.GetTracks()):
        if isinstance(item, pcbnew.PCB_VIA):
            continue
        if item.GetLayer() != pcbnew.F_Cu:
            continue
        a, b = endpoints(item)
        if near(a, anchor):
            other = b
        elif near(b, anchor):
            other = a
        else:
            continue
        length = math.hypot(other[0] - anchor[0], other[1] - anchor[1])
        nearby.append((a, b, item.GetNetname(), length))
        if (
            abs(length - EXPECTED_LEN) <= TOL
            and abs(other[1] - anchor[1]) <= TOL
            and other[0] < anchor[0] - 1.9
        ):
            matches.append(item)
    if len(matches) != 1:
        raise RuntimeError(
            f"expected exactly one legacy tail at {anchor}; "
            f"matches={len(matches)} nearby={nearby}"
        )
    return matches[0]


removed = []
for anchor in ANCHORS:
    item = candidate_for_anchor(anchor)
    a, b = endpoints(item)
    net = item.GetNetname()
    board.Remove(item)
    removed.append((anchor, a, b, net))

if len(removed) != 2:
    raise RuntimeError(f"legacy tail removal count mismatch: {removed}")

board.BuildConnectivity()
pcbnew.SaveBoard(str(PATH), board)
print("KL_LEGACY_TAILS_REMOVED", len(removed))
for entry in removed:
    print("KL_LEGACY_TAIL", entry)
