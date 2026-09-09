#!/usr/bin/env python3
"""Run the validated K/L router with pull-up K forced off pull-up L's layer.

Run 24 reached one DRC violation with zero unconnected pads: pull-up L selected
In1.Cu and pull-up K also selected In1.Cu, causing their final routes to cross.
The B.Cu K candidate is already part of the validated candidate set and was
successfully routable in earlier runs.  This wrapper changes only the ordered
candidate preference for pull-up K so B.Cu is tried first; KiCad DRC remains the
authoritative gate.
"""
from __future__ import annotations

from pathlib import Path

base = Path(__file__).with_name("route_rev_a_kl_astar_v2.py")
src = base.read_text(encoding="utf-8")
old = '''        "candidates": [
            (pcbnew.In1_Cu, (262.80,124.00), (240.20,144.40)),
            (pcbnew.In1_Cu, (263.00,125.20), (241.00,143.80)),
            (pcbnew.B_Cu,   (262.80,124.00), (240.20,144.40)),
        ],
'''
new = '''        "candidates": [
            # Run-24 DRC: K and L crossed when both chose In1.Cu. Keep L on
            # In1.Cu and force K to the already-routable B.Cu candidate first.
            (pcbnew.B_Cu,   (262.80,124.00), (240.20,144.40)),
            (pcbnew.In1_Cu, (262.80,124.00), (240.20,144.40)),
            (pcbnew.In1_Cu, (263.00,125.20), (241.00,143.80)),
        ],
'''
if src.count(old) != 1:
    raise RuntimeError("expected exactly one pullup-k candidate block")
src = src.replace(old, new, 1)
src = src.replace("# KH910 Rev A K/L route report v13", "# KH910 Rev A K/L route report v14", 1)
src = src.replace("KL_ROUTE_V13_OK", "KL_ROUTE_V14_OK", 1)
exec(compile(src, str(base), "exec"), {"__name__": "__main__", "__file__": str(base)})
