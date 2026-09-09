#!/usr/bin/env python3
"""Inspect a wider lower-board region for Q805/Q806 fail-safe gate placement."""
from pathlib import Path
import sys
import pcbnew

P=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/"ayab-esp32.kicad_pcb"
b=pcbnew.LoadBoard(str(P))
if b is None:
    raise SystemExit("could not load board")
MM=pcbnew.ToMM
REG=(88.0,180.0,144.0,180.0)  # xmin,xmax,ymin,ymax

def bbox_tuple(bb):
    return (MM(bb.GetX()),MM(bb.GetY()),MM(bb.GetX()+bb.GetWidth()),MM(bb.GetY()+bb.GetHeight()))
def hit(bb):
    x0,y0,x1,y1=bbox_tuple(bb); a,c,d,e=REG
    return not (x1<a or x0>c or y1<d or y0>e)
def xy(v):
    p=v.GetPosition(); return (MM(p.x),MM(p.y))
def pxy(o):
    p=o.GetPosition(); return (MM(p.x),MM(p.y))
def layer_name(i):
    try:return b.GetLayerName(i)
    except:return str(i)
def endpoint(o,which):
    p=o.GetStart() if which==0 else o.GetEnd(); return (MM(p.x),MM(p.y))

print("GATE_LEFT_PROBE",P)
print("REGION",REG)
try:
    edge_bb=b.GetBoardEdgesBoundingBox()
except Exception:
    edge_bb=b.GetBoundingBox()
EDGE=bbox_tuple(edge_bb)
print("BOARD_EDGE_BBOX",*(round(v,3) for v in EDGE))

print("FOOTPRINTS")
for fp in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
    if hit(fp.GetBoundingBox()):
        print("FP",fp.GetReference(),fp.GetValue(),"AT",*(round(v,3) for v in xy(fp)),"BBOX",*(round(v,3) for v in bbox_tuple(fp.GetBoundingBox())))

print("KEY_PADS")
for ref in ("J401","J402","J406","J407","C302","C303","C304","C603","C604","C605","U302","U303","U304"):
    fp=next((f for f in b.GetFootprints() if f.GetReference()==ref),None)
    if fp is None: continue
    for pad in fp.Pads():
        x,y=pxy(pad)
        if REG[0]-5<=x<=REG[1]+5 and REG[2]-12<=y<=REG[3]+2:
            print("PAD",ref,pad.GetNumber(),round(x,3),round(y,3),pad.GetNetname())

print("COPPER")
for t in b.GetTracks():
    if isinstance(t,pcbnew.PCB_VIA):
        x,y=pxy(t)
        if REG[0]<=x<=REG[1] and REG[2]<=y<=REG[3]:
            try: w=MM(t.GetWidth(pcbnew.F_Cu))
            except Exception: w=MM(t.GetDrillValue())*2
            print("VIA",round(x,3),round(y,3),t.GetNetname(),"size",round(w,3),"drill",round(MM(t.GetDrillValue()),3))
        continue
    a=endpoint(t,0); z=endpoint(t,1)
    if (REG[0]<=a[0]<=REG[1] and REG[2]<=a[1]<=REG[3]) or (REG[0]<=z[0]<=REG[1] and REG[2]<=z[1]<=REG[3]):
        print("TRK",layer_name(t.GetLayer()),round(MM(t.GetWidth()),3),t.GetNetname(),tuple(round(v,3) for v in a),tuple(round(v,3) for v in z))

# Placement shortlist only.  A 4x4 mm square approximates one SOT-23 plus
# practical courtyard margin.  Require the whole square to remain at least
# 1 mm inside the board-edge bounding box and not intersect any footprint bbox.
print("COARSE_FREE_CENTERS")
fps=list(b.GetFootprints())
free=[]
for y in [147.0+3.0*i for i in range(11)]:
    for x in [91.0+3.0*i for i in range(29)]:
        box=(x-2,y-2,x+2,y+2)
        if box[0] < EDGE[0]+1 or box[2] > EDGE[2]-1 or box[1] < EDGE[1]+1 or box[3] > EDGE[3]-1:
            continue
        occupied=[]
        for fp in fps:
            q=bbox_tuple(fp.GetBoundingBox())
            if not (box[2]<q[0] or box[0]>q[2] or box[3]<q[1] or box[1]>q[3]):
                occupied.append(fp.GetReference())
        if not occupied:
            free.append((x,y))
            print("FREE",x,y)
print("FREE_COUNT",len(free))
