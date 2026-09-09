#!/usr/bin/env python3
"""Inspect the validated Rev A solenoid/raw +12 V copper using pcbnew.

Read-only diagnostic. It deliberately relies on KiCad's own transformed pad
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
    try:
        return mm(p.GetX()), mm(p.GetY())
    except AttributeError:
        return mm(obj.GetX()), mm(obj.GetY())


def endpoints(track):
    return (
        (mm(track.GetStartX()), mm(track.GetStartY())),
        (mm(track.GetEndX()), mm(track.GetEndY())),
    )


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
        print(f"PAD {ref}.{pn} xy=({xy[0]:.4f},{xy[1]:.4f}) netcode={p.GetNetCode()} net={p.GetNetname()}")

raw_codes = set()
raw_pads = []
for fp in board.GetFootprints():
    for p in fp.Pads():
        if p.GetNetname() == "+12V":
            raw_codes.add(p.GetNetCode())
            raw_pads.append((fp.GetReference(), str(p.GetNumber()), pos_xy(p)))
if len(raw_codes) != 1:
    raise RuntimeError(f"expected exactly one +12V net code, got {raw_codes}")
raw = next(iter(raw_codes))
print("RAW_12V_NETCODE", raw)
print("RAW_12V_ALL_PADS", len(raw_pads))
for ref, pn, xy in sorted(raw_pads, key=lambda x: (x[2][1], x[2][0], x[0], x[1])):
    print(f"RAWPAD {ref}.{pn} xy=({xy[0]:.4f},{xy[1]:.4f})")

items = []
for tr in board.GetTracks():
    if tr.GetNetCode() != raw:
        continue
    a, b = endpoints(tr)
    is_via = isinstance(tr, pcbnew.PCB_VIA)
    items.append((tr, a, b, is_via))

print("RAW_12V_TRACK_COUNT", len(items))
print("RAW_12V_ALL_ITEMS")
for i, (tr, a, b, is_via) in enumerate(items):
    layer = "VIA" if is_via else board.GetLayerName(tr.GetLayer())
    width = mm(tr.GetDrillValue()) if is_via else mm(tr.GetWidth())
    print(f"RAWITEM {i} type={layer} width_or_drill={width:.4f} a=({a[0]:.4f},{a[1]:.4f}) b=({b[0]:.4f},{b[1]:.4f})")

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
        width = mm(tr.GetDrillValue()) if is_via else mm(tr.GetWidth())
        print(f"NEAR {ref}.{pn} item={i} type={layer} width_or_drill={width:.4f} a=({a[0]:.4f},{a[1]:.4f}) b=({b[0]:.4f},{b[1]:.4f})")

print("SOLENOID_BUS_INSPECT_OK")
