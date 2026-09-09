#!/usr/bin/env python3
"""Inspect the validated Rev A solenoid/raw +12 V copper using pcbnew.

Read-only diagnostic.  It deliberately relies on KiCad's own transformed pad
positions instead of reproducing footprint rotation math in text scripts.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
import pcbnew

if len(sys.argv) != 2:
    raise SystemExit("usage: inspect_rev_a_solenoid_bus.py BOARD.kicad_pcb")

path = Path(sys.argv[1]).resolve()
board = pcbnew.LoadBoard(str(path))
if board is None:
    raise RuntimeError(f"could not load {path}")
board.BuildConnectivity()

TARGETS = {
    "J401": ("9", "10"),
    "J403": ("9", "10"),
    "J406": ("9", "10"),
    "U302": ("9",),
    "U303": ("9",),
    "U304": ("9",),
    "C302": ("1",),
    "C303": ("1",),
    "C304": ("1",),
    "C603": ("1",),
    "C604": ("1",),
    "C605": ("1",),
}


def mm(v):
    return pcbnew.ToMM(v)


def pos_xy(obj):
    p = obj.GetPosition()
    # KiCad's VECTOR2I supports GetX/GetY in the runner SWIG build.
    try:
        return mm(p.GetX()), mm(p.GetY())
    except AttributeError:
        return mm(obj.GetX()), mm(obj.GetY())


def endpoints(track):
    return (
        (mm(track.GetStartX()), mm(track.GetStartY())),
        (mm(track.GetEndX()), mm(track.GetEndY())),
    )


def key(p):
    return round(p[0], 4), round(p[1], 4)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
missing = sorted(set(TARGETS) - set(fps))
if missing:
    raise RuntimeError(f"missing target footprints: {missing}")

print("SOLENOID_BUS_INSPECT_BOARD", path)
print("SOLENOID_BUS_INSPECT_TARGETS")
pad_points = {}
for ref, wanted in TARGETS.items():
    fp = fps[ref]
    fpx, fpy = pos_xy(fp)
    print(f"FOOTPRINT {ref} at=({fpx:.4f},{fpy:.4f}) orient={fp.GetOrientationDegrees():.1f}")
    bynum = {str(p.GetNumber()): p for p in fp.Pads()}
    for pn in wanted:
        if pn not in bynum:
            raise RuntimeError(f"{ref}.{pn} missing")
        p = bynum[pn]
        xy = pos_xy(p)
        pad_points[(ref, pn)] = xy
        print(
            f"PAD {ref}.{pn} xy=({xy[0]:.4f},{xy[1]:.4f}) "
            f"netcode={p.GetNetCode()} net={p.GetNetname()}"
        )

raw_codes = set()
for fp in board.GetFootprints():
    for p in fp.Pads():
        if p.GetNetname() == "+12V":
            raw_codes.add(p.GetNetCode())
if len(raw_codes) != 1:
    raise RuntimeError(f"expected exactly one +12V net code, got {raw_codes}")
raw = next(iter(raw_codes))
print("RAW_12V_NETCODE", raw)

# Build a geometric endpoint graph of raw +12 V tracks and vias.  This is not
# a substitute for KiCad connectivity; it is a diagnostic map around the pads.
items = []
for tr in board.GetTracks():
    if tr.GetNetCode() != raw:
        continue
    a, b = endpoints(tr)
    is_via = isinstance(tr, pcbnew.PCB_VIA)
    items.append((tr, a, b, is_via))

print("RAW_12V_TRACK_COUNT", len(items))

# Show every raw +12 item terminating within 0.8 mm of one of the relevant pad
# centers.  This exposes the exact interleaving of the PSU and solenoid loads.
print("RAW_12V_ITEMS_NEAR_TARGETS")
seen = set()
for (ref, pn), pxy in pad_points.items():
    for i, (tr, a, b, is_via) in enumerate(items):
        if min(dist(a, pxy), dist(b, pxy)) > 0.8:
            continue
        sig = (i, ref, pn)
        if sig in seen:
            continue
        seen.add(sig)
        layer = "VIA" if is_via else board.GetLayerName(tr.GetLayer())
        width = mm(tr.GetWidth()) if not is_via else mm(tr.GetWidth())
        print(
            f"NEAR {ref}.{pn} item={i} type={layer} width={width:.4f} "
            f"a=({a[0]:.4f},{a[1]:.4f}) b=({b[0]:.4f},{b[1]:.4f})"
        )

# Dump the entire raw +12 V copper graph in the bounding region containing all
# 12 target pad centers, padded by 8 mm.  This is compact enough for CI logs and
# sufficient to identify shared trunks and split points.
xs = [p[0] for p in pad_points.values()]
ys = [p[1] for p in pad_points.values()]
box = (min(xs)-8, max(xs)+8, min(ys)-8, max(ys)+8)
print(
    "RAW_12V_TARGET_BOX",
    f"xmin={box[0]:.4f} xmax={box[1]:.4f} ymin={box[2]:.4f} ymax={box[3]:.4f}",
)
print("RAW_12V_ITEMS_IN_TARGET_BOX")
for i, (tr, a, b, is_via) in enumerate(items):
    if not (
        max(a[0], b[0]) >= box[0] and min(a[0], b[0]) <= box[1]
        and max(a[1], b[1]) >= box[2] and min(a[1], b[1]) <= box[3]
    ):
        continue
    layer = "VIA" if is_via else board.GetLayerName(tr.GetLayer())
    width = mm(tr.GetWidth())
    print(
        f"RAWITEM {i} type={layer} width={width:.4f} "
        f"a=({a[0]:.4f},{a[1]:.4f}) b=({b[0]:.4f},{b[1]:.4f})"
    )

print("SOLENOID_BUS_INSPECT_OK")
