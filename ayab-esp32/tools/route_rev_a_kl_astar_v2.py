#!/usr/bin/env python3
"""Route Rev A KH-910 K/L parity using fail-closed candidate paths.

The electrical migration already establishes the correct K/L nets, pull-ups,
and endpoint vias. This router only chooses physical copper paths. Machine L is
routed before K so the two close signals do not let K monopolize the open In2
corridor. Each route has a small ordered set of candidate layer/stub pairs; A*
selects the first topologically available candidate. KiCad zone refill and DRC
remain authoritative, so a geometrically available candidate is never treated
as fabrication-safe until the workflow's DRC gates pass.
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
K = "/BROTHER-CONNECTORS/EOL_R_N"
L = "/BROTHER-CONNECTORS/EOL_R_S"

ROUTES = [
    {
        "label": "machine-l", "net": L,
        "actual_start": (238.45, 145.63), "actual_goal": (221.67, 134.14),
        "candidates": [
            # Run-16 DRC proved the former diagonal 223.0,132.8 -> GPIO via
            # approach clipped the GND and ESP21 vias. End directly below the
            # L GPIO via instead; the final stub is then vertical at x=221.67.
            (pcbnew.In2_Cu, (239.80,146.80), (221.67,132.60)),
            (pcbnew.In2_Cu, (237.20,146.40), (221.67,132.40)),
            (pcbnew.B_Cu,   (239.80,145.00), (221.67,132.60)),
            (pcbnew.In1_Cu, (240.00,146.80), (221.67,132.40)),
        ],
    },
    {
        "label": "machine-k", "net": K,
        "actual_start": (239.22, 145.65), "actual_goal": (220.97, 134.15),
        "candidates": [
            (pcbnew.In2_Cu, (240.20,144.40), (220.00,133.20)),
            (pcbnew.In2_Cu, (240.60,143.80), (219.60,132.80)),
            (pcbnew.B_Cu,   (240.40,144.20), (219.80,133.00)),
        ],
    },
    {
        "label": "pullup-l", "net": L,
        "actual_start": (262.00, 126.00), "actual_goal": (238.45, 145.63),
        "candidates": [
            (pcbnew.In1_Cu, (262.80,126.00), (238.45,144.60)),
            (pcbnew.In1_Cu, (263.00,127.20), (240.00,144.40)),
            (pcbnew.B_Cu,   (262.80,126.00), (239.80,144.40)),
        ],
    },
    {
        "label": "pullup-k", "net": K,
        "actual_start": (262.00, 124.00), "actual_goal": (239.22, 145.65),
        "candidates": [
            (pcbnew.In1_Cu, (262.80,124.00), (240.20,144.40)),
            (pcbnew.In1_Cu, (263.00,125.20), (241.00,143.80)),
            (pcbnew.B_Cu,   (262.80,124.00), (240.20,144.40)),
        ],
    },
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
    code = board.GetNetcodeFromNetname(name)
    if code <= 0: raise RuntimeError(f"missing net {name}")
    return code

def net_obj(name):
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetname() == name and hasattr(pad, "GetNet"): return pad.GetNet()
    for item in board.GetTracks():
        if item.GetNetname() == name and hasattr(item, "GetNet"): return item.GetNet()
    raise RuntimeError(f"cannot resolve net object {name}")

def require_endpoint_via(name, pos, tol=0.02):
    code = net_code(name); found = []
    for item in board.GetTracks():
        if not isinstance(item, pcbnew.PCB_VIA) or item.GetNetCode() != code: continue
        p = item.GetPosition(); got = (mm(p.x), mm(p.y))
        if abs(got[0]-pos[0]) <= tol and abs(got[1]-pos[1]) <= tol: found.append(got)
    if len(found) != 1: raise RuntimeError(f"expected exactly one {name} via at {pos}, got {found}")

for route in ROUTES:
    require_endpoint_via(route["net"], route["actual_start"])
    require_endpoint_via(route["net"], route["actual_goal"])

bb = board.GetBoardEdgesBoundingBox()
X0 = math.floor(mm(bb.GetX()) / STEP) * STEP; Y0 = math.floor(mm(bb.GetY()) / STEP) * STEP
X1 = math.ceil((mm(bb.GetX()) + mm(bb.GetWidth())) / STEP) * STEP
Y1 = math.ceil((mm(bb.GetY()) + mm(bb.GetHeight())) / STEP) * STEP
NX = int(round((X1-X0)/STEP)) + 1; NY = int(round((Y1-Y0)/STEP)) + 1

def cell(x, y): return int(round((x-X0)/STEP)), int(round((y-Y0)/STEP))
def xy(c): return X0 + c[0]*STEP, Y0 + c[1]*STEP
def in_bounds(c): return 0 <= c[0] < NX and 0 <= c[1] < NY

def raster_box(blocked, box, expand):
    x0,y0,x1,y1 = box; x0 -= expand; y0 -= expand; x1 += expand; y1 += expand
    i0,j0 = cell(x0,y0); i1,j1 = cell(x1,y1)
    for i in range(max(0,min(i0,i1)), min(NX-1,max(i0,i1))+1):
        for j in range(max(0,min(j0,j1)), min(NY-1,max(j0,j1))+1): blocked.add((i,j))

def build_blocked(route_net, layer):
    blocked = set(); own = net_code(route_net)
    for item in board.GetTracks():
        same = item.GetNetCode() == own
        if isinstance(item, pcbnew.PCB_VIA):
            if not same: raster_box(blocked, bbox_mm(item), CLEAR)
        elif item.GetLayer() == layer and not same: raster_box(blocked, bbox_mm(item), CLEAR)
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetCode() == own: continue
            try: on_layer = pad.IsOnLayer(layer)
            except Exception: on_layer = True
            if on_layer: raster_box(blocked, bbox_mm(pad), CLEAR)
    for drawing in board.GetDrawings():
        if drawing.GetLayer() == pcbnew.Edge_Cuts: raster_box(blocked, bbox_mm(drawing), EDGE_CLEAR)
    return blocked

DIRS = [(1,0,1.0),(-1,0,1.0),(0,1,1.0),(0,-1,1.0),(1,1,math.sqrt(2)),(1,-1,math.sqrt(2)),(-1,1,math.sqrt(2)),(-1,-1,math.sqrt(2))]

def astar(start_xy, goal_xy, blocked):
    start = cell(*start_xy); goal = cell(*goal_xy); blocked.discard(start); blocked.discard(goal)
    def h(c): return math.hypot(c[0]-goal[0], c[1]-goal[1])
    pq = [(h(start),0.0,start,None)]; best = {start:0.0}; parent = {}
    while pq:
        _f,g,cur,incoming = heapq.heappop(pq)
        if g != best.get(cur): continue
        if cur == goal:
            out = [cur]
            while cur != start: cur = parent[cur]; out.append(cur)
            return list(reversed(out))
        for di,dj,cost in DIRS:
            nxt = (cur[0]+di, cur[1]+dj)
            if not in_bounds(nxt) or nxt in blocked: continue
            if di and dj and ((cur[0]+di,cur[1]) in blocked or (cur[0],cur[1]+dj) in blocked): continue
            direction = (di,dj); ng = g + cost + (0.10 if incoming is not None and direction != incoming else 0.0)
            if ng < best.get(nxt,float("inf")):
                best[nxt] = ng; parent[nxt] = cur; heapq.heappush(pq,(ng+h(nxt),ng,nxt,direction))
    return None

def simplify(cells, start, goal):
    pts = [start] + [xy(c) for c in cells[1:-1]] + [goal]; out = [pts[0]]; last = None
    for b in pts[1:]:
        a = out[-1]; dx = round(b[0]-a[0],6); dy = round(b[1]-a[1],6)
        if abs(dx) < 1e-6: d = (0,1 if dy>0 else -1)
        elif abs(dy) < 1e-6: d = (1 if dx>0 else -1,0)
        elif abs(abs(dx)-abs(dy)) < 1e-6: d = (1 if dx>0 else -1,1 if dy>0 else -1)
        else: d = None
        if last is not None and d == last and len(out) >= 2: out[-1] = b
        else: out.append(b); last = d
    return out

def add_track(a, b, name, layer):
    tr = pcbnew.PCB_TRACK(board); tr.SetStart(pt(*a)); tr.SetEnd(pt(*b)); tr.SetLayer(layer); tr.SetWidth(iu(TRACK_W)); n = net_obj(name)
    if hasattr(tr,"SetNet"): tr.SetNet(n)
    else: tr.SetNetCode(net_code(name))
    board.Add(tr)

def choose_candidate(route):
    name = route["net"]
    for idx,(layer,start_stub,goal_stub) in enumerate(route["candidates"], start=1):
        raw = astar(start_stub, goal_stub, build_blocked(name,layer))
        if raw is not None: return idx,layer,start_stub,goal_stub,raw
        print(f"KL_ROUTE_CANDIDATE_BLOCKED {route['label']} candidate={idx} layer={board.GetLayerName(layer)}")
    raise RuntimeError(f"no candidate route for {route['label']}")

report = ["# KH910 Rev A K/L route report v13", "", f"grid {STEP} mm; width {TRACK_W} mm; clearance raster {CLEAR} mm", "", "Pull-ups sit below J801 at y=124/126 mm. Machine L approaches its GPIO via vertically to clear the adjacent GND and ESP21 vias. KiCad DRC after zone refill is authoritative.", ""]
for route in ROUTES:
    idx,layer,start_stub,goal_stub,raw = choose_candidate(route); points = simplify(raw,start_stub,goal_stub)
    add_track(route["actual_start"], start_stub, route["net"], layer)
    for a,b in zip(points,points[1:]): add_track(a,b,route["net"],layer)
    add_track(goal_stub,route["actual_goal"],route["net"],layer); board.BuildConnectivity()
    print(f"KL_ROUTE_SELECTED {route['label']} candidate={idx} layer={board.GetLayerName(layer)} cells={len(raw)}")
    report += [f"## {route['label']}", f"- net: `{route['net']}`", f"- candidate: {idx}", f"- layer: `{board.GetLayerName(layer)}`", f"- via start: {route['actual_start']}", f"- start stub: {start_stub}", f"- goal stub: {goal_stub}", f"- via goal: {route['actual_goal']}", f"- A* cells: {len(raw)}", f"- routed segments: {len(points)+1}", "- A* points: " + " -> ".join(f"({x:.3f},{y:.3f})" for x,y in points), ""]

pcbnew.SaveBoard(str(PATH), board)
report_path = PATH.with_name("KH910_REV_A_KL_ASTAR_ROUTE.md"); report_path.write_text("\n".join(report)+"\n")
print("KL_ROUTE_V13_OK", PATH); print(report_path)
