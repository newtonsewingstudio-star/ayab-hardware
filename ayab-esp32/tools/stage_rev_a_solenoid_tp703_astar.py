#!/usr/bin/env python3
"""Place and obstacle-route TP703 on the validated solenoid switched rail."""
from __future__ import annotations
from pathlib import Path
import heapq, math, re, sys
import pcbnew

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import patch_rev_a_solenoid_pcb as u

if len(sys.argv)!=2:
    raise SystemExit("usage: stage_rev_a_solenoid_tp703_astar.py BOARD.kicad_pcb")
P=Path(sys.argv[1]).resolve()
SCH=HERE.parent/"solenoids.kicad_sch"
pcb=P.read_text(encoding="utf-8"); sch=SCH.read_text(encoding="utf-8")
REF="TP703"; NET="SOLENOID_12V_SW"; POS=(145.0,159.0)
if f'fp_text reference "{REF}"' in pcb or f'property "Reference" "{REF}"' in pcb:
    raise RuntimeError("TP703 already present")
defs=u.net_defs(pcb); NC=next((n for n,s in defs.items() if s==NET),0)
if NC<=0: raise RuntimeError(f"missing {NET}")
_,_,tpl=u.find_fp(pcb,"TP701")
prefix=u.sheet_prefix_from_existing(pcb); su=u.symbol_uuid_by_ref(sch,REF); path=prefix+'/'+su

# KiCad-9 tolerant single-pad testpoint clone.
out=re.sub(r'\((uuid|tstamp) [0-9a-f-]+\)',lambda m:f'({m.group(1)} {u.uid()})',tpl)
out,n=re.subn(r'^(\(footprint.*?)(\(at\s+[-\d.]+\s+[-\d.]+(?:\s+[-\d.]+)?\))',lambda m:m.group(1)+f'(at {POS[0]:g} {POS[1]:g} 0)',out,count=1,flags=re.S)
if n!=1: raise RuntimeError("could not relocate TP703 clone")
out,n=re.subn(r'\(path "[^"]+"\)',f'(path "{path}")',out,count=1)
if n!=1: raise RuntimeError("TP703 path anchor missing")
if re.search(r'\(fp_text reference "[^"]+"',out): out=re.sub(r'\(fp_text reference "[^"]+"',f'(fp_text reference "{REF}"',out,count=1)
else:
    out,n=re.subn(r'\(property "Reference" "[^"]+"',f'(property "Reference" "{REF}"',out,count=1)
    if n!=1: raise RuntimeError("TP703 reference field missing")
if re.search(r'\(fp_text value "[^"]+"',out): out=re.sub(r'\(fp_text value "[^"]+"','(fp_text value "SOL12_SW"',out,count=1)
else:
    out,n=re.subn(r'\(property "Value" "[^"]+"','(property "Value" "SOL12_SW"',out,count=1)
    if n!=1: raise RuntimeError("TP703 value field missing")
if '(property "LCSC ID"' in out: out=re.sub(r'\(property "LCSC ID" "[^"]*"\)','(property "LCSC ID" "")',out,count=1)
out=u.replace_pad_net(out,"1",NC,NET)
pcb=u.insert_before_first(pcb,'  (segment ',out)
P.write_text(pcb,encoding="utf-8")

b=pcbnew.LoadBoard(str(P))
if b is None: raise RuntimeError("KiCad could not reload TP703 board")
b.BuildConnectivity(); mm=pcbnew.ToMM; iu=pcbnew.FromMM
def pt(x,y): return pcbnew.VECTOR2I(iu(x),iu(y))
def pad(ref,pn):
    f=next((x for x in b.GetFootprints() if x.GetReference()==ref),None)
    if f is None: raise RuntimeError(f"missing {ref}")
    p=next((x for x in f.Pads() if x.GetNumber()==str(pn)),None)
    if p is None: raise RuntimeError(f"missing {ref}.{pn}")
    q=p.GetPosition(); return p,(mm(q.x),mm(q.y))
tp,START=pad("TP703","1"); jp,GOAL=pad("J401","9")
if tp.GetNetname()!=NET or jp.GetNetname()!=NET: raise RuntimeError("TP703/J401.9 switched-net mismatch")

STEP=.20; CLEAR=.22; EDGE_CLEAR=.45; WIDTH=.35
def bbox(obj):
    r=obj.GetBoundingBox()
    if all(hasattr(r,n) for n in ("GetX","GetY","GetWidth","GetHeight")):
        x=mm(r.GetX()); y=mm(r.GetY()); w=mm(r.GetWidth()); h=mm(r.GetHeight()); return x,y,x+w,y+h
    return mm(r.GetLeft()),mm(r.GetTop()),mm(r.GetRight()),mm(r.GetBottom())
bb=b.GetBoardEdgesBoundingBox(); X0=math.floor(mm(bb.GetX())/STEP)*STEP; Y0=math.floor(mm(bb.GetY())/STEP)*STEP
X1=math.ceil((mm(bb.GetX())+mm(bb.GetWidth()))/STEP)*STEP; Y1=math.ceil((mm(bb.GetY())+mm(bb.GetHeight()))/STEP)*STEP
NX=int(round((X1-X0)/STEP))+1; NY=int(round((Y1-Y0)/STEP))+1
def cell(x,y): return int(round((x-X0)/STEP)),int(round((y-Y0)/STEP))
def xy(c): return X0+c[0]*STEP,Y0+c[1]*STEP
def inside(c): return 0<=c[0]<NX and 0<=c[1]<NY
def raster(s,box,e):
    x0,y0,x1,y1=box; a=cell(x0-e,y0-e); z=cell(x1+e,y1+e)
    for i in range(max(0,min(a[0],z[0])),min(NX-1,max(a[0],z[0]))+1):
        for j in range(max(0,min(a[1],z[1])),min(NY-1,max(a[1],z[1]))+1): s.add((i,j))
def blocked(layer):
    s=set()
    for t in b.GetTracks():
        same=t.GetNetCode()==NC
        if isinstance(t,pcbnew.PCB_VIA):
            if not same: raster(s,bbox(t),CLEAR)
        elif t.GetLayer()==layer and not same: raster(s,bbox(t),CLEAR)
    for f in b.GetFootprints():
        for p in f.Pads():
            if p.GetNetCode()==NC: continue
            try: on=p.IsOnLayer(layer)
            except Exception: on=True
            if on: raster(s,bbox(p),CLEAR)
    for d in b.GetDrawings():
        if d.GetLayer()==pcbnew.Edge_Cuts: raster(s,bbox(d),EDGE_CLEAR)
    return s
DIRS=[(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(1,1,math.sqrt(2)),(1,-1,math.sqrt(2)),(-1,1,math.sqrt(2)),(-1,-1,math.sqrt(2))]
def astar(layer):
    s=cell(*START); g=cell(*GOAL); blk=blocked(layer); blk.discard(s); blk.discard(g)
    def h(c): return math.hypot(c[0]-g[0],c[1]-g[1])
    pq=[(h(s),0,s,None)]; best={s:0}; parent={}
    while pq:
        _,cost,cur,inc=heapq.heappop(pq)
        if cost!=best.get(cur): continue
        if cur==g:
            out=[cur]
            while cur!=s: cur=parent[cur]; out.append(cur)
            return list(reversed(out))
        for di,dj,w in DIRS:
            nxt=(cur[0]+di,cur[1]+dj)
            if not inside(nxt) or nxt in blk: continue
            if di and dj and ((cur[0]+di,cur[1]) in blk or (cur[0],cur[1]+dj) in blk): continue
            dr=(di,dj); nc=cost+w+(.1 if inc is not None and inc!=dr else 0)
            if nc<best.get(nxt,float('inf')): best[nxt]=nc; parent[nxt]=cur; heapq.heappush(pq,(nc+h(nxt),nc,nxt,dr))
    return None
def simplify(cells):
    pts=[START]+[xy(c) for c in cells[1:-1]]+[GOAL]; out=[pts[0]]; last=None
    for q in pts[1:]:
        a=out[-1]; dx=round(q[0]-a[0],6); dy=round(q[1]-a[1],6)
        if abs(dx)<1e-6:d=(0,1 if dy>0 else -1)
        elif abs(dy)<1e-6:d=(1 if dx>0 else -1,0)
        elif abs(abs(dx)-abs(dy))<1e-6:d=(1 if dx>0 else -1,1 if dy>0 else -1)
        else:d=None
        if last is not None and d==last and len(out)>=2: out[-1]=q
        else: out.append(q); last=d
    return out
layers=(pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu)
sel=None
for layer in layers:
    pth=astar(layer)
    if pth is not None: sel=(layer,pth); break
    print("TP703_LAYER_BLOCKED",b.GetLayerName(layer))
if sel is None: raise RuntimeError("no TP703 switched-rail route found")
layer,pth=sel; pts=simplify(pth); no=tp.GetNet()
# TP703 is a front-copper pad.  The selected escape is on an inner layer, so
# put a through-via inside the test-point annulus to make that layer change
# explicit; a track endpoint alone does not connect across layers.
if layer != pcbnew.F_Cu:
    v=pcbnew.PCB_VIA(b)
    v.SetPosition(pt(*START)); v.SetWidth(iu(.60)); v.SetDrill(iu(.30))
    v.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu); v.SetNet(no); b.Add(v)
for a,z in zip(pts,pts[1:]):
    t=pcbnew.PCB_TRACK(b); t.SetStart(pt(*a)); t.SetEnd(pt(*z)); t.SetLayer(layer); t.SetWidth(iu(WIDTH)); t.SetNet(no); b.Add(t)
b.BuildConnectivity(); pcbnew.SaveBoard(str(P),b)
print("TP703_STAGE_OK",f"layer={b.GetLayerName(layer)}",f"cells={len(pth)}",f"pad={tuple(round(v,3) for v in START)}")
print("TP703_ROUTE"," -> ".join(f"({x:.3f},{y:.3f})" for x,y in pts))
