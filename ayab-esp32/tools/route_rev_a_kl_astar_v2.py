#!/usr/bin/env python3
"""Route Rev A KH-910 K/L parity with controlled endpoint approaches.

Machine K uses the open In2.Cu region below the ESP32. Machine L uses In1.Cu,
where its retagged legacy GPIO18 corridor already exists and same-net copper is
not an obstacle. The two pull-ups also use sparse In1.Cu to reach the existing
machine-side vias without crossing the In2 +3V3 trunk.

Close K/L via pairs use fixed outward-facing stubs; A* only routes between safe
interior stub points. KiCad DRC after zone refill remains authoritative.
"""
from __future__ import annotations

import heapq
import math
import sys
from pathlib import Path
import pcbnew

if len(sys.argv) != 2:
    raise SystemExit("usage: route_rev_a_kl_astar_v2.py BOARD.kicad_pcb")
PATH = Path(sys.argv[1]).resolve()
board = pcbnew.LoadBoard(str(PATH))
if board is None:
    raise RuntimeError(f"could not load {PATH}")

STEP = 0.20
TRACK_W = 0.25
CLEAR = 0.22
EDGE_CLEAR = 0.45

# name, actual start via, safe start stub, safe goal stub, actual goal via,
# label, layer. K and L machine runs are intentionally on different layers.
ROUTES = [
    ("/BROTHER-CONNECTORS/EOL_R_N", (239.22,145.65), (240.20,144.40), (220.00,133.20), (220.97,134.15), "machine-k", pcbnew.In2_Cu),
    ("/BROTHER-CONNECTORS/EOL_R_S", (238.45,145.63), (237.20,146.40), (222.60,133.20), (221.67,134.14), "machine-l", pcbnew.In1_Cu),
    ("/BROTHER-CONNECTORS/EOL_R_N", (241.60,118.00), (243.00,118.00), (240.20,144.40), (239.22,145.65), "pullup-k", pcbnew.In1_Cu),
    ("/BROTHER-CONNECTORS/EOL_R_S", (241.60,120.00), (244.00,120.00), (237.20,146.40), (238.45,145.63), "pullup-l", pcbnew.In1_Cu),
]


def mm(v): return pcbnew.ToMM(v)
def iu(v): return pcbnew.FromMM(v)
def pt(x, y): return pcbnew.VECTOR2I(iu(x), iu(y))


def bbox_mm(obj):
    r = obj.GetBoundingBox()
    if all(hasattr(r, n) for n in ("GetX", "GetY", "GetWidth", "GetHeight")):
        x = mm(r.GetX()); y = mm(r.GetY()); w = mm(r.GetWidth()); h = mm(r.GetHeight())
        return x, y, x + w, y + h
    return mm(r.GetLeft()), mm(r.GetTop()), mm(r.GetRight()), mm(r.GetBottom())


def net_code(name):
    c = board.GetNetcodeFromNetname(name)
    if c <= 0:
        raise RuntimeError(f"missing net {name}")
    return c


def net_obj(name):
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetname() == name and hasattr(pad, "GetNet"):
                return pad.GetNet()
    for item in board.GetTracks():
        if item.GetNetname() == name and hasattr(item, "GetNet"):
            return item.GetNet()
    raise RuntimeError(f"cannot resolve net object {name}")


def require_endpoint_via(name, xy, tol=0.02):
    code = net_code(name)
    matches = []
    for item in board.GetTracks():
        if not isinstance(item, pcbnew.PCB_VIA) or item.GetNetCode() != code:
            continue
        pos = item.GetPosition()
        got = (mm(pos.x), mm(pos.y))
        if abs(got[0] - xy[0]) <= tol and abs(got[1] - xy[1]) <= tol:
            matches.append(got)
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one {name} via at {xy}, got {matches}")


for name, actual_start, _stub_start, _stub_goal, actual_goal, _label, _layer in ROUTES:
    require_endpoint_via(name, actual_start)
    require_endpoint_via(name, actual_goal)

bb = board.GetBoardEdgesBoundingBox()
X0 = math.floor(mm(bb.GetX()) / STEP) * STEP
Y0 = math.floor(mm(bb.GetY()) / STEP) * STEP
X1 = math.ceil((mm(bb.GetX()) + mm(bb.GetWidth())) / STEP) * STEP
Y1 = math.ceil((mm(bb.GetY()) + mm(bb.GetHeight())) / STEP) * STEP
NX = int(round((X1 - X0) / STEP)) + 1
NY = int(round((Y1 - Y0) / STEP)) + 1


def cell(x, y): return int(round((x - X0) / STEP)), int(round((y - Y0) / STEP))
def xy(c): return X0 + c[0] * STEP, Y0 + c[1] * STEP
def in_bounds(c): return 0 <= c[0] < NX and 0 <= c[1] < NY


def raster_box(blocked, box, expand):
    x0, y0, x1, y1 = box
    x0 -= expand; y0 -= expand; x1 += expand; y1 += expand
    i0, j0 = cell(x0, y0); i1, j1 = cell(x1, y1)
    for i in range(max(0, min(i0, i1)), min(NX - 1, max(i0, i1)) + 1):
        for j in range(max(0, min(j0, j1)), min(NY - 1, max(j0, j1)) + 1):
            blocked.add((i, j))


def build_blocked(route_net, layer):
    blocked = set(); own = net_code(route_net)
    for item in board.GetTracks():
        same = item.GetNetCode() == own
        is_via = isinstance(item, pcbnew.PCB_VIA)
        if is_via:
            if not same:
                raster_box(blocked, bbox_mm(item), CLEAR)
        elif item.GetLayer() == layer and not same:
            raster_box(blocked, bbox_mm(item), CLEAR)
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetCode() == own:
                continue
            try:
                on_layer = pad.IsOnLayer(layer)
            except Exception:
                on_layer = True
            if on_layer:
                raster_box(blocked, bbox_mm(pad), CLEAR)
    for drawing in board.GetDrawings():
        if drawing.GetLayer() == pcbnew.Edge_Cuts:
            raster_box(blocked, bbox_mm(drawing), EDGE_CLEAR)
    return blocked


DIRS = [
    (1,0,1.0), (-1,0,1.0), (0,1,1.0), (0,-1,1.0),
    (1,1,math.sqrt(2)), (1,-1,math.sqrt(2)),
    (-1,1,math.sqrt(2)), (-1,-1,math.sqrt(2)),
]


def astar(start_xy, goal_xy, blocked):
    start = cell(*start_xy); goal = cell(*goal_xy)
    blocked.discard(start)
    blocked.discard(goal)

    def h(c): return math.hypot(c[0]-goal[0], c[1]-goal[1])
    pq=[(h(start),0.0,start,None)]; best={start:0.0}; parent={}
    while pq:
        _f,g,cur,incoming=heapq.heappop(pq)
        if g != best.get(cur): continue
        if cur == goal:
            out=[cur]
            while cur != start:
                cur=parent[cur]; out.append(cur)
            return list(reversed(out))
        for di,dj,cost in DIRS:
            nxt=(cur[0]+di,cur[1]+dj)
            if not in_bounds(nxt) or nxt in blocked: continue
            if di and dj and ((cur[0]+di,cur[1]) in blocked or (cur[0],cur[1]+dj) in blocked):
                continue
            direction=(di,dj)
            ng=g+cost+(0.10 if incoming is not None and direction != incoming else 0.0)
            if ng < best.get(nxt,float("inf")):
                best[nxt]=ng; parent[nxt]=cur
                heapq.heappush(pq,(ng+h(nxt),ng,nxt,direction))
    raise RuntimeError(f"no route {start_xy}->{goal_xy}")


def simplify(cells, start, goal):
    pts=[start]+[xy(c) for c in cells[1:-1]]+[goal]
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


def add_track(a,b,name,layer):
    tr=pcbnew.PCB_TRACK(board)
    tr.SetStart(pt(*a)); tr.SetEnd(pt(*b)); tr.SetLayer(layer); tr.SetWidth(iu(TRACK_W))
    n=net_obj(name)
    if hasattr(tr,"SetNet"): tr.SetNet(n)
    else: tr.SetNetCode(net_code(name))
    board.Add(tr)


def layer_name(layer): return board.GetLayerName(layer)


report=[
    "# KH910 Rev A K/L route report v6", "",
    f"grid {STEP} mm; width {TRACK_W} mm; clearance raster {CLEAR} mm", "",
    "Machine K uses In2.Cu; machine L and pull-ups use In1.Cu with controlled endpoint stubs.", "",
]

for name, actual_start, stub_start, stub_goal, actual_goal, label, layer in ROUTES:
    add_track(actual_start, stub_start, name, layer)
    board.BuildConnectivity()
    raw=astar(stub_start,stub_goal,build_blocked(name,layer))
    points=simplify(raw,stub_start,stub_goal)
    for a,b in zip(points,points[1:]): add_track(a,b,name,layer)
    add_track(stub_goal,actual_goal,name,layer)
    board.BuildConnectivity()
    report += [
        f"## {label}", f"- net: `{name}`", f"- layer: `{layer_name(layer)}`",
        f"- via start: {actual_start}", f"- start stub: {stub_start}",
        f"- goal stub: {stub_goal}", f"- via goal: {actual_goal}",
        f"- A* cells: {len(raw)}", f"- routed segments: {len(points)+1}",
        "- A* points: " + " -> ".join(f"({x:.3f},{y:.3f})" for x,y in points), "",
    ]

pcbnew.SaveBoard(str(PATH),board)
report_path=PATH.with_name("KH910_REV_A_KL_ASTAR_ROUTE.md")
report_path.write_text("\n".join(report)+"\n")
print("KL_ROUTE_V6_OK",PATH)
print(report_path)
