#!/usr/bin/env python3
"""Move the final SOLENOID_PWR_EN layer-change via into the clear inner-layer window."""
from pathlib import Path
import sys
import pcbnew

if len(sys.argv)!=2:
    raise SystemExit("usage: fix_rev_a_solenoid_enable_goal_via.py BOARD.kicad_pcb")
P=Path(sys.argv[1]).resolve(); b=pcbnew.LoadBoard(str(P))
if b is None: raise RuntimeError(f"could not load {P}")
b.BuildConnectivity(); MM=pcbnew.ToMM; NET="SOLENOID_PWR_EN"; NC=b.GetNetcodeFromNetname(NET)
if NC<=0: raise RuntimeError(f"missing {NET}")
OLD=(124.175,157.20); NEW=(124.175,157.60)

def pos(o):
    p=o.GetPosition(); return MM(p.x),MM(p.y)
def ep(t,k):
    p=t.GetStart() if k==0 else t.GetEnd(); return MM(p.x),MM(p.y)
def near(a,z,tol=.03): return abs(a[0]-z[0])<=tol and abs(a[1]-z[1])<=tol
r821=next((f for f in b.GetFootprints() if f.GetReference()=="R821"),None)
if r821 is None: raise RuntimeError("R821 missing")
pad=next((p for p in r821.Pads() if p.GetNumber()=="1"),None)
if pad is None or pad.GetNetname()!=NET: raise RuntimeError("R821.1 enable pad missing")
PAD=pos(pad)

vias=[v for v in b.GetTracks() if isinstance(v,pcbnew.PCB_VIA) and v.GetNetCode()==NC and near(pos(v),OLD)]
if len(vias)!=1: raise RuntimeError(f"expected one enable via at {OLD}, got {len(vias)}")
stubs=[]
for t in b.GetTracks():
    if isinstance(t,pcbnew.PCB_VIA) or t.GetNetCode()!=NC or t.GetLayer()!=pcbnew.F_Cu: continue
    a,z=ep(t,0),ep(t,1)
    if (near(a,OLD) and near(z,PAD)) or (near(a,PAD) and near(z,OLD)): stubs.append(t)
if len(stubs)!=1: raise RuntimeError(f"expected one old enable F.Cu stub, got {len(stubs)}")
b.Remove(vias[0]); b.Remove(stubs[0])
no=pad.GetNet()
def addseg(a,z,layer):
    t=pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I_MM(*a)); t.SetEnd(pcbnew.VECTOR2I_MM(*z)); t.SetLayer(layer); t.SetWidth(pcbnew.FromMM(.25)); t.SetNet(no); b.Add(t)
def addvia(q):
    v=pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I_MM(*q)); v.SetWidth(pcbnew.FromMM(.7)); v.SetDrill(pcbnew.FromMM(.35)); v.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu); v.SetNet(no); b.Add(v)
addseg(OLD,NEW,pcbnew.B_Cu); addvia(NEW); addseg(NEW,PAD,pcbnew.F_Cu)
b.BuildConnectivity(); pcbnew.SaveBoard(str(P),b)
print("SOL_ENABLE_GOAL_VIA_MOVED",OLD,"->",NEW,"R821.1",PAD)
