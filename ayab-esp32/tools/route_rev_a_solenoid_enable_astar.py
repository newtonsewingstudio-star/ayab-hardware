#!/usr/bin/env python3
"""Route SOLENOID_PWR_EN from existing GPIO21 copper to staged R821.1.

The existing GPIO21 net is already fully routed on the promoted board.  This
script does not assume one historical coordinate: it inventories endpoints of
that same-net copper, tries the nearest useful anchors first, and A* routes a
new branch to R821.1. KiCad DRC after zone refill remains authoritative.
"""
from __future__ import annotations
import heapq, math, sys
from pathlib import Path
import pcbnew

if len(sys.argv)!=2:
    raise SystemExit("usage: route_rev_a_solenoid_enable_astar.py BOARD.kicad_pcb")
PATH=Path(sys.argv[1]).resolve()
b=pcbnew.LoadBoard(str(PATH))
if b is None: raise RuntimeError(f"could not load {PATH}")
b.BuildConnectivity()

NET="SOLENOID_PWR_EN"
TRACK_W=0.25
STEP=0.20
CLEAR=0.22
EDGE_CLEAR=0.45
mm=pcbnew.ToMM
iu=pcbnew.FromMM
def pt(x,y): return pcbnew.VECTOR2I(iu(x),iu(y))
NC=b.GetNetcodeFromNetname(NET)
if NC<=0: raise RuntimeError(f"missing net {NET}")

def netobj():
    for f in b.GetFootprints():
        for p in f.Pads():
            if p.GetNetname()==NET and hasattr(p,"GetNet"): return p.GetNet()
    for t in b.GetTracks():
        if t.GetNetname()==NET and hasattr(t,"GetNet"): return t.GetNet()
    raise RuntimeError("cannot resolve enable net object")
NO=netobj()

def xypos(o):
    p=o.GetPosition(); return mm(p.x),mm(p.y)
def endpoint(t,k):
    p=t.GetStart() if k==0 else t.GetEnd(); return mm(p.x),mm(p.y)

r821=next((f for f in b.GetFootprints() if f.GetReference()=="R821"),None)
if r821 is None: raise RuntimeError("R821 missing; run local gate stage first")
pad1=next((p for p in r821.Pads() if p.GetNumber()=="1"),None)
if pad1 is None or pad1.GetNetname()!=NET: raise RuntimeError(f"R821.1 is not on {NET}")
GOAL_PAD=xypos(pad1)

# Use endpoints of existing same-net tracks as branch anchors. They are already
# electrically part of GPIO21, regardless of which track KiCad happens to cite
# in an unconnected-items report. Deduplicate coincident endpoint/layer pairs.
anchors={}
for t in b.GetTracks():
    if isinstance(t,pcbnew.PCB_VIA) or t.GetNetCode()!=NC: continue
    layer=t.GetLayer()
    for k in (0,1):
        q=endpoint(t,k)
        key=(layer,round(q[0],3),round(q[1],3))
        anchors[key]=(layer,q)
if not anchors: raise RuntimeError(f"no existing routed copper found on {NET}")
ordered=sorted(anchors.values(),key=lambda z:math.hypot(z[1][0]-GOAL_PAD[0],z[1][1]-GOAL_PAD[1]))
print("SOL_ENABLE_ANCHOR_COUNT",len(ordered))
for layer,q in ordered[:12]: print("SOL_ENABLE_NEAR_ANCHOR",b.GetLayerName(layer),*(round(v,3) for v in q))

def bbox(obj):
    r=obj.GetBoundingBox()
    if all(hasattr(r,n) for n in ("GetX","GetY","GetWidth","GetHeight")):
        x=mm(r.GetX()); y=mm(r.GetY()); w=mm(r.GetWidth()); h=mm(r.GetHeight()); return x,y,x+w,y+h
    return mm(r.GetLeft()),mm(r.GetTop()),mm(r.GetRight()),mm(r.GetBottom())

bb=b.GetBoardEdgesBoundingBox()
X0=math.floor(mm(bb.GetX())/STEP)*STEP; Y0=math.floor(mm(bb.GetY())/STEP)*STEP
X1=math.ceil((mm(bb.GetX())+mm(bb.GetWidth()))/STEP)*STEP
Y1=math.ceil((mm(bb.GetY())+mm(bb.GetHeight()))/STEP)*STEP
NX=int(round((X1-X0)/STEP))+1; NY=int(round((Y1-Y0)/STEP))+1
def cell(x,y): return int(round((x-X0)/STEP)),int(round((y-Y0)/STEP))
def xy(c): return X0+c[0]*STEP,Y0+c[1]*STEP
def inside(c): return 0<=c[0]<NX and 0<=c[1]<NY

def raster(blocked,box,expand):
    x0,y0,x1,y1=box; x0-=expand; y0-=expand; x1+=expand; y1+=expand
    a=cell(x0,y0); z=cell(x1,y1)
    for i in range(max(0,min(a[0],z[0])),min(NX-1,max(a[0],z[0]))+1):
        for j in range(max(0,min(a[1],z[1])),min(NY-1,max(a[1],z[1]))+1): blocked.add((i,j))

def blocked_for(layer):
    out=set()
    for t in b.GetTracks():
        same=t.GetNetCode()==NC
        if isinstance(t,pcbnew.PCB_VIA):
            if not same: raster(out,bbox(t),CLEAR)
        elif t.GetLayer()==layer and not same:
            raster(out,bbox(t),CLEAR)
    for f in b.GetFootprints():
        for p in f.Pads():
            if p.GetNetCode()==NC: continue
            try: on=p.IsOnLayer(layer)
            except Exception: on=True
            if on: raster(out,bbox(p),CLEAR)
    for d in b.GetDrawings():
        if d.GetLayer()==pcbnew.Edge_Cuts: raster(out,bbox(d),EDGE_CLEAR)
    return out

DIRS=[(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(1,1,math.sqrt(2)),(1,-1,math.sqrt(2)),(-1,1,math.sqrt(2)),(-1,-1,math.sqrt(2))]
def astar(sxy,gxy,blocked):
    s=cell(*sxy); g=cell(*gxy); blocked.discard(s); blocked.discard(g)
    def h(c): return math.hypot(c[0]-g[0],c[1]-g[1])
    pq=[(h(s),0.0,s,None)]; best={s:0.0}; parent={}
    while pq:
        _,cost,cur,incoming=heapq.heappop(pq)
        if cost!=best.get(cur): continue
        if cur==g:
            out=[cur]
            while cur!=s: cur=parent[cur]; out.append(cur)
            return list(reversed(out))
        for di,dj,w in DIRS:
            nxt=(cur[0]+di,cur[1]+dj)
            if not inside(nxt) or nxt in blocked: continue
            if di and dj and ((cur[0]+di,cur[1]) in blocked or (cur[0],cur[1]+dj) in blocked): continue
            direction=(di,dj); nc=cost+w+(0.10 if incoming is not None and incoming!=direction else 0)
            if nc<best.get(nxt,float("inf")):
                best[nxt]=nc; parent[nxt]=cur; heapq.heappush(pq,(nc+h(nxt),nc,nxt,direction))
    return None

def simplify(cells,start,goal):
    pts=[start]+[xy(c) for c in cells[1:-1]]+[goal]; out=[pts[0]]; last=None
    for q in pts[1:]:
        a=out[-1]; dx=round(q[0]-a[0],6); dy=round(q[1]-a[1],6)
        if abs(dx)<1e-6: d=(0,1 if dy>0 else -1)
        elif abs(dy)<1e-6: d=(1 if dx>0 else -1,0)
        elif abs(abs(dx)-abs(dy))<1e-6: d=(1 if dx>0 else -1,1 if dy>0 else -1)
        else: d=None
        if last is not None and d==last and len(out)>=2: out[-1]=q
        else: out.append(q); last=d
    return out

def addseg(a,z,layer):
    t=pcbnew.PCB_TRACK(b); t.SetStart(pt(*a)); t.SetEnd(pt(*z)); t.SetLayer(layer); t.SetWidth(iu(TRACK_W)); t.SetNet(NO); b.Add(t)
def addvia(q,size=0.7,drill=0.35):
    v=pcbnew.PCB_VIA(b); v.SetPosition(pt(*q)); v.SetWidth(iu(size)); v.SetDrill(iu(drill)); v.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu); v.SetNet(NO); b.Add(v)

# For a non-F.Cu branch, land at a via just above R821.1 and make the final
# short vertical-ish F.Cu connection. F.Cu candidates may terminate on the pad.
goal_vias=[(124.175,157.20),(123.40,157.00),(125.00,157.00)]
selected=None
for rank,(layer,start) in enumerate(ordered[:24],1):
    goals=[GOAL_PAD] if layer==pcbnew.F_Cu else goal_vias
    for gi,goal in enumerate(goals,1):
        path=astar(start,goal,blocked_for(layer))
        if path is not None:
            selected=(rank,gi,layer,start,goal,path); break
    if selected: break
    print("SOL_ENABLE_ANCHOR_BLOCKED",rank,b.GetLayerName(layer),tuple(round(v,3) for v in start))
if selected is None: raise RuntimeError("no obstacle-aware SOLENOID_PWR_EN route found from nearest existing copper anchors")
rank,gi,layer,start,goal,path=selected
pts=simplify(path,start,goal)
for a,z in zip(pts,pts[1:]): addseg(a,z,layer)
if layer!=pcbnew.F_Cu:
    addvia(goal)
    addseg(goal,GOAL_PAD,pcbnew.F_Cu)
b.BuildConnectivity(); pcbnew.SaveBoard(str(PATH),b)
print("SOL_ENABLE_ROUTE_OK",f"anchor_rank={rank}",f"goal_candidate={gi}",f"layer={b.GetLayerName(layer)}",f"cells={len(path)}")
print("SOL_ENABLE_START",tuple(round(v,4) for v in start),"GOAL",tuple(round(v,4) for v in goal),"R821_1",tuple(round(v,4) for v in GOAL_PAD))
print("SOL_ENABLE_POINTS"," -> ".join(f"({x:.3f},{y:.3f})" for x,y in pts))
