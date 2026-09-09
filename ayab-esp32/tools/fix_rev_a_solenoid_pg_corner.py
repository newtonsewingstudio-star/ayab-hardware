#!/usr/bin/env python3
"""Replace the final P-gate In2 diagonal with a GND-via-safe corner."""
from pathlib import Path
import sys
import pcbnew

if len(sys.argv)!=2:
    raise SystemExit("usage: fix_rev_a_solenoid_pg_corner.py BOARD.kicad_pcb")
P=Path(sys.argv[1]).resolve()
b=pcbnew.LoadBoard(str(P))
if b is None: raise RuntimeError(f"could not load {P}")
NET="Net-(Q805-G)"
NC=b.GetNetcodeFromNetname(NET)
if NC<=0: raise RuntimeError(f"missing {NET}")
MM=pcbnew.ToMM
START=(113.35,160.90)
END=(115.35,158.55)
MID=(113.35,158.55)

def ep(t,k):
    p=t.GetStart() if k==0 else t.GetEnd(); return MM(p.x),MM(p.y)
def near(a,z,tol=0.03): return abs(a[0]-z[0])<=tol and abs(a[1]-z[1])<=tol
hits=[]
for t in b.GetTracks():
    if isinstance(t,pcbnew.PCB_VIA) or t.GetNetCode()!=NC or t.GetLayer()!=pcbnew.In2_Cu: continue
    a,z=ep(t,0),ep(t,1)
    if (near(a,START) and near(z,END)) or (near(a,END) and near(z,START)): hits.append(t)
if len(hits)!=1:
    raise RuntimeError(f"expected exactly one P-gate diagonal {START}->{END}, got {len(hits)}")
b.Remove(hits[0])
netobj=None
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetNetname()==NET and hasattr(p,"GetNet"): netobj=p.GetNet(); break
    if netobj is not None: break
if netobj is None: raise RuntimeError("cannot resolve P-gate net object")
def add(a,z):
    t=pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I_MM(*a)); t.SetEnd(pcbnew.VECTOR2I_MM(*z)); t.SetLayer(pcbnew.In2_Cu); t.SetWidth(pcbnew.FromMM(0.25)); t.SetNet(netobj); b.Add(t)
add(START,MID); add(MID,END)
b.BuildConnectivity(); pcbnew.SaveBoard(str(P),b)
print("SOL_PG_CORNER_OK",START,"->",MID,"->",END)
