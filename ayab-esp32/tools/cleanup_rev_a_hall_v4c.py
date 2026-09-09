#!/usr/bin/env python3
"""Clean only residual copper identified by the v4c KiCad DRC reports.

Input is the staged v4c board after the board-aware A* Hall routes are added.
This script deliberately does not alter either A* route, divider footprint, MCU
pad assignment, or any unrelated net.

KiCad DRC is the final authority; every surgical removal is assertion checked.
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


def mm(p): return (pcbnew.ToMM(p.x), pcbnew.ToMM(p.y))
def near(a,b,tol=TOL): return math.hypot(a[0]-b[0],a[1]-b[1]) <= tol
def endpoints(item): return mm(item.GetStart()), mm(item.GetEnd())
def same_ends(item,a,b):
    p,q=endpoints(item); return (near(p,a) and near(q,b)) or (near(p,b) and near(q,a))
def touches(item,point):
    p,q=endpoints(item); return near(p,point) or near(q,point)
def length_mm(item):
    p,q=endpoints(item); return math.hypot(p[0]-q[0],p[1]-q[1])

def net_obj(name):
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetname()==name and hasattr(pad,"GetNet"): return pad.GetNet()
    for item in board.GetTracks():
        if item.GetNetname()==name and hasattr(item,"GetNet"): return item.GetNet()
    raise RuntimeError(f"cannot resolve net object for {name}")

def add_track(a,b,net_name,layer=pcbnew.F_Cu,width_mm=0.25):
    tr=pcbnew.PCB_TRACK(board)
    tr.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(a[0]),pcbnew.FromMM(a[1])))
    tr.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(b[0]),pcbnew.FromMM(b[1])))
    tr.SetLayer(layer); tr.SetWidth(pcbnew.FromMM(width_mm)); tr.SetNet(net_obj(net_name)); board.Add(tr)

def unique_track(name,point,expected_len,layer=pcbnew.F_Cu,excluded=()):
    matches=[item for item in board.GetTracks()
             if not isinstance(item,pcbnew.PCB_VIA) and item.GetLayer()==layer
             and item.GetNetname()==name and touches(item,point)
             and abs(length_mm(item)-expected_len)<=0.01 and item not in excluded]
    if len(matches)!=1:
        candidates=[(endpoints(item),round(length_mm(item),4)) for item in board.GetTracks()
                    if not isinstance(item,pcbnew.PCB_VIA) and item.GetLayer()==layer
                    and item.GetNetname()==name and touches(item,point) and item not in excluded]
        raise RuntimeError(f"expected one track at {name} {point} len {expected_len}; found {len(matches)}; candidates={candidates}")
    return matches[0]

def unique_via(name,point,excluded=()):
    matches=[item for item in board.GetTracks()
             if isinstance(item,pcbnew.PCB_VIA) and item.GetNetname()==name
             and near(mm(item.GetPosition()),point) and item not in excluded]
    if len(matches)!=1:
        candidates=[mm(item.GetPosition()) for item in board.GetTracks()
                    if isinstance(item,pcbnew.PCB_VIA) and item.GetNetname()==name
                    and near(mm(item.GetPosition()),point,0.05) and item not in excluded]
        raise RuntimeError(f"expected one via at {name} {point}; found {len(matches)}; candidates={candidates}")
    return matches[0]

removed_adc={ADC_L:0,ADC_R:0}; remove=[]
for item in board.GetTracks():
    if isinstance(item,pcbnew.PCB_VIA): continue
    if item.GetLayer()==pcbnew.B_Cu and item.GetNetname() in removed_adc:
        remove.append(item); removed_adc[item.GetNetname()]+=1
if removed_adc[ADC_L]<1 or removed_adc[ADC_R]<1:
    raise RuntimeError(f"expected legacy ADC B.Cu tails on both nets, found {removed_adc}")

# First DRC wave: exact dead comparator-era supply segments.
exact_remove=[
    (GND,(91.7878,142.2030),(91.0628,141.4780)),
    (GND,(91.0628,141.4780),(91.0628,139.8280)),
    (P5,(87.0878,142.2030),(87.0878,143.5522)),
    (P5,(312.3250,157.2800),(310.9000,157.2800)),
    (P5,(326.7700,153.4250),(326.8200,153.3750)),
]
found={i:0 for i in range(len(exact_remove))}
for item in board.GetTracks():
    if isinstance(item,pcbnew.PCB_VIA): continue
    for i,(name,a,b) in enumerate(exact_remove):
        if item.GetNetname()==name and same_ends(item,a,b):
            if item not in remove: remove.append(item)
            found[i]+=1
missing=[exact_remove[i] for i,count in found.items() if count!=1]
if missing: raise RuntimeError(f"expected exact residual segments once each; mismatches: {missing} counts={found}")

# Later DRC waves expose the next dead segment after the previous leaf is
# removed. Endpoint + KiCad-reported length uniquely identifies each branch.
wave_specs=[
    (P5,(310.9000,157.2800),0.7495),
    (P5,(325.2700,153.4250),1.5000),
    (GND,(90.1378,140.6530),0.9250),
    (P5,(310.3700,156.7500),2.1750),
    (P5,(324.4950,152.6500),1.0960),
    (P5,(310.3700,154.5750),1.6971),
    (P5,(322.5150,152.6500),1.9800),
    (P5,(311.5650,153.3700),0.0071),
    (P5,(321.6700,153.4950),1.1950),
    (P5,(320.5950,153.4950),1.0750),
    (P5,(309.7000,153.3700),1.8650),
    (P5,(320.1300,153.0300),0.6576),
]
wave_found=[]
for name,point,expected_len in wave_specs:
    item=unique_track(name,point,expected_len,excluded=remove)
    remove.append(item); wave_found.append((name,point,endpoints(item),round(length_mm(item),4)))

# Final DRC pass exposed the now-isolated via at the root of the removed left
# +5V comparator branch. Remove only that exact via.
dead_via=unique_via(P5,(309.7000,153.3700),excluded=remove)
remove.append(dead_via)

for item in remove: board.Remove(item)

# U701 pads 11/12 are adjacent GND pins; preserve the shortest local bridge.
fps={fp.GetReference():fp for fp in board.GetFootprints()}; u701=fps.get("U701")
if u701 is None: raise RuntimeError("U701 missing")
pads={str(p.GetNumber()):p for p in u701.Pads()}
for pn in ("11","12"):
    if pn not in pads or pads[pn].GetNetname()!=GND: raise RuntimeError(f"U701 pad {pn} is not present on GND")
p11=mm(pads["11"].GetPosition()); p12=mm(pads["12"].GetPosition())
if not near(p11,(191.4775,160.4550)) or not near(p12,(191.4775,161.1050)):
    raise RuntimeError(f"U701 GND pad coordinates changed: p11={p11} p12={p12}")
add_track(p11,p12,GND)

board.BuildConnectivity(); pcbnew.SaveBoard(str(PATH),board)
print("HALL_V4C_CLEANUP_OK",PATH)
print("REMOVED_ADC_BCU",removed_adc)
print("REMOVED_EXACT_SUPPLY_SEGMENTS",len(exact_remove))
print("REMOVED_DRC_WAVE_SEGMENTS",wave_found)
print("REMOVED_FINAL_DEAD_VIA",P5,(309.7000,153.3700))
print("ADDED_U701_GND_LINK",p11,p12)
