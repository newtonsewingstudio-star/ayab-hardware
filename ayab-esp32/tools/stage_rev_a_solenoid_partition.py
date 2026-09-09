#!/usr/bin/env python3
"""Stage the KH910 Rev A raw/switched solenoid +12 V PCB partition.

This stage intentionally does NOT add the high-side MOSFET yet.  It proves the
hard physical part first:

* raw +12 V and the PSU bulk caps C603/C604/C605 remain untouched;
* only the Brother solenoid commons, ULN2003 clamp pins, and local solenoid
  decouplers move to SOLENOID_12V_SW;
* the existing heavy J401<->J406 copper is reused after isolating its raw feeds;
* J403 is isolated at its natural right-side raw branch point;
* six SMD solenoid loads launch upward to a new internal switched trunk;
* one 1.0 mm A* route joins the left and right switched clusters.

The resulting switched rail is intentionally unpowered.  The workflow must
refill zones and prove 0 DRC / 0 unconnected before the MOSFET stage is added.
"""
from __future__ import annotations

import heapq
import math
import sys
from pathlib import Path
import pcbnew

if len(sys.argv) != 2:
    raise SystemExit("usage: stage_rev_a_solenoid_partition.py BOARD.kicad_pcb")

PATH = Path(sys.argv[1]).resolve()
board = pcbnew.LoadBoard(str(PATH))
if board is None:
    raise RuntimeError(f"could not load {PATH}")
board.BuildConnectivity()

RAW = "+12V"
SW = "SOLENOID_12V_SW"
STEP = 0.40
ROUTE_W = 1.00
LOCAL_W = 0.75
VIA_D = 0.90
VIA_DRILL = 0.45
CLEAR = 0.75
EDGE_CLEAR = 0.90


def mm(v): return pcbnew.ToMM(v)
def iu(v): return pcbnew.FromMM(v)
def pt(x, y): return pcbnew.VECTOR2I(iu(x), iu(y))

def xy_obj(obj):
    p = obj.GetPosition()
    try:
        return mm(p.GetX()), mm(p.GetY())
    except AttributeError:
        return mm(p.x), mm(p.y)

def endpoints(item):
    return ((mm(item.GetStartX()), mm(item.GetStartY())),
            (mm(item.GetEndX()), mm(item.GetEndY())))

def near(a, b, tol=0.025):
    return abs(a[0]-b[0]) <= tol and abs(a[1]-b[1]) <= tol

def same_pair(a, b, c, d, tol=0.025):
    return (near(a,c,tol) and near(b,d,tol)) or (near(a,d,tol) and near(b,c,tol))

def layer_name(layer): return board.GetLayerName(layer)

def bbox_mm(obj):
    r = obj.GetBoundingBox()
    if all(hasattr(r, n) for n in ("GetX", "GetY", "GetWidth", "GetHeight")):
        x = mm(r.GetX()); y = mm(r.GetY()); w = mm(r.GetWidth()); h = mm(r.GetHeight())
        return x, y, x+w, y+h
    return mm(r.GetLeft()), mm(r.GetTop()), mm(r.GetRight()), mm(r.GetBottom())

fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
TARGETS = {
    "J401": ("9","10"), "J403": ("9","10"), "J406": ("9","10"),
    "U302": ("9",), "U303": ("9",), "U304": ("9",),
    "C302": ("1",), "C303": ("1",), "C304": ("1",),
}
RAW_CAPS = {"C603":"1", "C604":"1", "C605":"1"}
for ref in set(TARGETS) | set(RAW_CAPS):
    if ref not in fps:
        raise RuntimeError(f"missing footprint {ref}")

raw_code = board.GetNetcodeFromNetname(RAW)
if raw_code <= 0:
    raise RuntimeError("raw +12V net missing")
if board.GetNetcodeFromNetname(SW) > 0:
    raise RuntimeError(f"{SW} already exists; refusing partial-state migration")

# Fail closed on all expected starting pad assignments and the KiCad-native
# coordinates measured from the K/L-clean board.
EXPECTED = {
    ("J401","9"):(116.8400,153.7852), ("J401","10"):(114.8400,153.7852),
    ("J403","9"):(310.9100,138.8300), ("J403","10"):(308.4100,138.8300),
    ("J406","9"):(119.2400,146.2800), ("J406","10"):(116.7400,146.2800),
    ("U302","9"):(124.0050,141.8000), ("U303","9"):(111.4550,141.8000),
    ("U304","9"):(98.9050,141.8000),
    ("C302","1"):(109.6250,140.3750), ("C303","1"):(122.1750,140.3750),
    ("C304","1"):(97.0500,140.3750),
    ("C603","1"):(97.0576,138.2624), ("C604","1"):(109.6250,138.2750),
    ("C605","1"):(122.1750,138.2750),
}

def get_pad(ref, pn):
    rows = [p for p in fps[ref].Pads() if str(p.GetNumber()) == str(pn)]
    if len(rows) != 1:
        raise RuntimeError(f"expected exactly one {ref}.{pn}, got {len(rows)}")
    return rows[0]

for key, expected in EXPECTED.items():
    p = get_pad(*key)
    got = xy_obj(p)
    if not near(got, expected, 0.03):
        raise RuntimeError(f"pad coordinate drift {key}: {got} != {expected}")
    if p.GetNetname() != RAW:
        raise RuntimeError(f"expected {key} on {RAW}, got {p.GetNetname()}")

# Create the new switched net using KiCad's native net object.
sw_net = pcbnew.NETINFO_ITEM(board, SW)
board.Add(sw_net)
sw_code = sw_net.GetNetCode()
if sw_code <= 0 or board.GetNetcodeFromNetname(SW) != sw_code:
    raise RuntimeError("could not create switched solenoid net")

# Exact raw-copper changes.  We remove only the branches that tie solenoid
# loads/clusters back to raw +12 V, and retag only known heavy local copper that
# should remain as part of the switched distribution.
REMOVE = [
    # C304/C302/C303 downward raw stubs.
    (pcbnew.F_Cu,(97.05,140.375),(97.05,138.9276)),
    (pcbnew.F_Cu,(97.05,138.9276),(97.0576,138.92)),
    (pcbnew.F_Cu,(109.625,140.375),(109.625,139.485)),
    (pcbnew.F_Cu,(109.625,139.485),(109.79,139.32)),
    (pcbnew.F_Cu,(122.175,140.375),(122.175,139.335)),
    (pcbnew.F_Cu,(122.175,139.335),(122.16,139.32)),
    # ULN COM downward raw stubs.
    (pcbnew.F_Cu,(98.905,141.8),(98.905,139.535)),
    (pcbnew.F_Cu,(98.905,139.535),(99.12,139.32)),
    (pcbnew.F_Cu,(111.455,141.8),(111.455,139.375)),
    (pcbnew.F_Cu,(111.455,139.375),(111.51,139.32)),
    (pcbnew.F_Cu,(124.005,141.8),(124.005,139.455)),
    (pcbnew.F_Cu,(124.005,139.455),(123.87,139.32)),
    # J401 and J406 raw B.Cu feeds; their F.Cu local chain is retained/retagged.
    (pcbnew.B_Cu,(116.84,153.7852),(116.84,163.10)),
    (pcbnew.B_Cu,(119.2426,146.2774),(119.2426,140.1026)),
    (pcbnew.B_Cu,(119.2426,140.1026),(118.47,139.33)),
    (pcbnew.B_Cu,(118.47,139.33),(114.03,139.33)),
    (pcbnew.B_Cu,(119.24,146.28),(119.2426,146.2774)),
    # J403 natural raw branch cut.
    (pcbnew.B_Cu,(334.16,141.85),(312.45,141.85)),
]

RETAG = [
    # Existing heavy J401<->J406 local copper.
    (pcbnew.F_Cu,(116.84,153.7852),(116.84,151.61)),
    (pcbnew.F_Cu,(116.84,151.61),(119.24,149.21)),
    (pcbnew.F_Cu,(119.24,149.21),(119.24,146.28)),
    (pcbnew.F_Cu,(116.84,153.7852),(114.84,153.7852)),
    (pcbnew.F_Cu,(116.74,146.28),(119.24,146.28)),
    # Existing heavy J403 local branch after the raw cut.
    (pcbnew.B_Cu,(312.45,141.85),(310.91,140.31)),
    (pcbnew.B_Cu,(310.91,140.31),(310.91,138.83)),
    (pcbnew.B_Cu,(310.91,138.83),(308.41,138.83)),
]

def exact_tracks(spec, require_raw=True):
    layer, a, b = spec
    found = []
    for item in list(board.GetTracks()):
        if isinstance(item, pcbnew.PCB_VIA):
            continue
        if item.GetLayer() != layer:
            continue
        if require_raw and item.GetNetCode() != raw_code:
            continue
        x, y = endpoints(item)
        if same_pair(x, y, a, b):
            found.append(item)
    return found

removed = []
for spec in REMOVE:
    rows = exact_tracks(spec)
    if len(rows) != 1:
        raise RuntimeError(f"expected one raw removal {layer_name(spec[0])} {spec[1]}->{spec[2]}, got {len(rows)}")
    item = rows[0]
    removed.append((layer_name(item.GetLayer()), endpoints(item)))
    board.Remove(item)

retagged = []
for spec in RETAG:
    rows = exact_tracks(spec)
    if len(rows) != 1:
        raise RuntimeError(f"expected one raw retag {layer_name(spec[0])} {spec[1]}->{spec[2]}, got {len(rows)}")
    item = rows[0]
    item.SetNet(sw_net)
    retagged.append((layer_name(item.GetLayer()), endpoints(item)))

# Move exactly the intended pads to the switched net.
for ref, pns in TARGETS.items():
    for pn in pns:
        get_pad(ref, pn).SetNet(sw_net)


def add_track(a, b, layer, width=LOCAL_W):
    tr = pcbnew.PCB_TRACK(board)
    tr.SetStart(pt(*a)); tr.SetEnd(pt(*b)); tr.SetLayer(layer); tr.SetWidth(iu(width)); tr.SetNet(sw_net)
    board.Add(tr)
    return tr

def add_via(pos):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(pt(*pos)); v.SetWidth(iu(VIA_D)); v.SetDrill(iu(VIA_DRILL)); v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); v.SetNet(sw_net)
    board.Add(v)
    return v

# Lift the six left SMD loads away from the raw bus.  Vias are above the target
# pads, never in-pad, and align on a common y=143.0 mm internal trunk.
LIFTS = [
    ((97.050,140.375),(97.050,143.000)),
    ((98.905,141.800),(98.905,143.000)),
    ((109.625,140.375),(109.625,143.000)),
    ((111.455,141.800),(111.455,143.000)),
    ((122.175,140.375),(122.175,143.000)),
    ((124.005,141.800),(124.005,143.000)),
]
for padpos, viapos in LIFTS:
    add_track(padpos, viapos, pcbnew.F_Cu, LOCAL_W)
    add_via(viapos)

# Local switched trunk.  Sequential segments make every via an explicit node.
TRUNK_X = [97.050,98.905,109.625,111.455,122.175,124.005]
for a, b in zip(TRUNK_X, TRUNK_X[1:]):
    add_track((a,143.0),(b,143.0),pcbnew.In1_Cu,ROUTE_W)
# J406 is through-hole, so it can join the internal rail directly.
add_track((119.24,146.28),(119.24,143.0),pcbnew.In1_Cu,ROUTE_W)

# J403's retained B.Cu branch ends here.  A via converts that endpoint to the
# internal switched interconnect.  The A* route terminates on this via.
RIGHT = (312.45,141.85)
add_via(RIGHT)

board.BuildConnectivity()

# A* route from the left trunk to J403.  Try In1 first (preferred), then In2.
bb = board.GetBoardEdgesBoundingBox()
X0 = math.floor(mm(bb.GetX())/STEP)*STEP; Y0 = math.floor(mm(bb.GetY())/STEP)*STEP
X1 = math.ceil((mm(bb.GetX())+mm(bb.GetWidth()))/STEP)*STEP
Y1 = math.ceil((mm(bb.GetY())+mm(bb.GetHeight()))/STEP)*STEP
NX = int(round((X1-X0)/STEP))+1; NY = int(round((Y1-Y0)/STEP))+1

def cell(x,y): return int(round((x-X0)/STEP)), int(round((y-Y0)/STEP))
def cell_xy(c): return X0+c[0]*STEP, Y0+c[1]*STEP
def in_bounds(c): return 0 <= c[0] < NX and 0 <= c[1] < NY

def raster_box(blocked, box, expand):
    x0,y0,x1,y1=box; x0-=expand; y0-=expand; x1+=expand; y1+=expand
    i0,j0=cell(x0,y0); i1,j1=cell(x1,y1)
    for i in range(max(0,min(i0,i1)),min(NX-1,max(i0,i1))+1):
        for j in range(max(0,min(j0,j1)),min(NY-1,max(j0,j1))+1): blocked.add((i,j))

def build_blocked(layer):
    blocked=set()
    for item in board.GetTracks():
        same=item.GetNetCode()==sw_code
        if isinstance(item,pcbnew.PCB_VIA):
            if not same: raster_box(blocked,bbox_mm(item),CLEAR)
        elif item.GetLayer()==layer and not same:
            raster_box(blocked,bbox_mm(item),CLEAR)
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetCode()==sw_code: continue
            try: on_layer=pad.IsOnLayer(layer)
            except Exception: on_layer=True
            if on_layer: raster_box(blocked,bbox_mm(pad),CLEAR)
    for drawing in board.GetDrawings():
        if drawing.GetLayer()==pcbnew.Edge_Cuts:
            raster_box(blocked,bbox_mm(drawing),EDGE_CLEAR)
    return blocked

DIRS=[(1,0,1.0),(-1,0,1.0),(0,1,1.0),(0,-1,1.0),(1,1,math.sqrt(2)),(1,-1,math.sqrt(2)),(-1,1,math.sqrt(2)),(-1,-1,math.sqrt(2))]
def astar(start_xy,goal_xy,blocked):
    start=cell(*start_xy); goal=cell(*goal_xy)
    # Only the exact endpoint cells are cleared; broad endpoint clearing caused
    # false routes in earlier K/L work.
    blocked.discard(start); blocked.discard(goal)
    def h(c): return math.hypot(c[0]-goal[0],c[1]-goal[1])
    pq=[(h(start),0.0,start,None)]; best={start:0.0}; parent={}
    while pq:
        _f,g,cur,incoming=heapq.heappop(pq)
        if g != best.get(cur): continue
        if cur==goal:
            out=[cur]
            while cur!=start: cur=parent[cur]; out.append(cur)
            return list(reversed(out))
        for di,dj,cost in DIRS:
            nxt=(cur[0]+di,cur[1]+dj)
            if not in_bounds(nxt) or nxt in blocked: continue
            if di and dj and ((cur[0]+di,cur[1]) in blocked or (cur[0],cur[1]+dj) in blocked): continue
            direction=(di,dj); ng=g+cost+(0.12 if incoming is not None and direction!=incoming else 0.0)
            if ng < best.get(nxt,float("inf")):
                best[nxt]=ng; parent[nxt]=cur; heapq.heappush(pq,(ng+h(nxt),ng,nxt,direction))
    return None

def simplify(cells,start,goal):
    pts=[start]+[cell_xy(c) for c in cells[1:-1]]+[goal]
    out=[pts[0]]; last=None
    for b in pts[1:]:
        a=out[-1]; dx=round(b[0]-a[0],6); dy=round(b[1]-a[1],6)
        if abs(dx)<1e-6: d=(0,1 if dy>0 else -1)
        elif abs(dy)<1e-6: d=(1 if dx>0 else -1,0)
        elif abs(abs(dx)-abs(dy))<1e-6: d=(1 if dx>0 else -1,1 if dy>0 else -1)
        else: d=None
        if last is not None and d==last and len(out)>=2: out[-1]=b
        else: out.append(b); last=d
    return out

START=(124.005,143.0)
selected=None
for layer in (pcbnew.In1_Cu,pcbnew.In2_Cu):
    raw=astar(START,RIGHT,build_blocked(layer))
    if raw is None:
        print("SOL_PARTITION_ROUTE_BLOCKED",layer_name(layer))
        continue
    points=simplify(raw,START,RIGHT)
    for a,b in zip(points,points[1:]): add_track(a,b,layer,ROUTE_W)
    selected=(layer,raw,points)
    print("SOL_PARTITION_ROUTE_SELECTED",layer_name(layer),"cells",len(raw),"segments",len(points)-1)
    break
if selected is None:
    raise RuntimeError("no safe A* corridor for 1.0 mm switched interconnect")

board.BuildConnectivity()

# Postconditions before saving.  Raw PSU caps must remain raw and every intended
# load must now be on the switched net.
for ref,pn in RAW_CAPS.items():
    if get_pad(ref,pn).GetNetname()!=RAW:
        raise RuntimeError(f"raw PSU cap moved unexpectedly: {ref}.{pn}")
for ref,pns in TARGETS.items():
    for pn in pns:
        if get_pad(ref,pn).GetNetname()!=SW:
            raise RuntimeError(f"switched target assignment failed: {ref}.{pn}")

pcbnew.SaveBoard(str(PATH),board)
print("SOLENOID_PARTITION_STAGE_OK",PATH)
print("SOLENOID_PARTITION_REMOVED",len(removed))
print("SOLENOID_PARTITION_RETAGGED",len(retagged))
print("SOLENOID_PARTITION_SW_NET",sw_code)
print("SOLENOID_PARTITION_RAW_CAPS_OK",','.join(sorted(RAW_CAPS)))
print("SOLENOID_PARTITION_TARGET_PADS",sum(len(v) for v in TARGETS.values()))
