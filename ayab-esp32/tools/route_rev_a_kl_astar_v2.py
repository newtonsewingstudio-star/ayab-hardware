#!/usr/bin/env python3
"""Route Rev A KH-910 K/L parity using existing DRC-clean vias.

Machine K/L and the R213 pull-up route on In1.Cu between existing/new vias.
R214 is locally congested on In1.Cu, so its existing launch via routes on B.Cu
directly into the already DRC-clean horizontal L corridor at y=130.71. This
avoids adding another via or disturbing the three routes already proven by CI.

KiCad DRC after zone refill remains authoritative.
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
ENDPOINT_ESCAPE_CELLS = 4
ROUTES = [
    ("/BROTHER-CONNECTORS/EOL_R_N", (239.22, 145.65), (220.97, 134.15), "machine-k", pcbnew.In1_Cu, True),
    ("/BROTHER-CONNECTORS/EOL_R_S", (238.45, 145.63), (221.67, 134.14), "machine-l", pcbnew.In1_Cu, True),
    ("/BROTHER-CONNECTORS/EOL_R_N", (207.5, 132.025), (220.97, 134.15), "pullup-k", pcbnew.In1_Cu, True),
    # The B.Cu goal is a point on the pre-existing retagged GPIO18 corridor,
    # which spans through x=207.5 at y=130.71. No extra goal via is needed.
    ("/BROTHER-CONNECTORS/EOL_R_S", (207.5, 135.325), (207.5, 130.71), "pullup-l", pcbnew.B_Cu, False),
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


def point_on_same_net_track(name, goal, layer, tol=0.02):
    code = net_code(name)
    gx, gy = goal
    for item in board.GetTracks():
        if isinstance(item, pcbnew.PCB_VIA) or item.GetNetCode() != code or item.GetLayer() != layer:
            continue
        a = item.GetStart(); b = item.GetEnd()
        ax, ay = mm(a.x), mm(a.y); bx, by = mm(b.x), mm(b.y)
        # Goal is intentionally on a horizontal/vertical existing segment.
        if abs(ay - by) <= tol and abs(gy - ay) <= tol and min(ax, bx) - tol <= gx <= max(ax, bx) + tol:
            return True
        if abs(ax - bx) <= tol and abs(gx - ax) <= tol and min(ay, by) - tol <= gy <= max(ay, by) + tol:
            return True
    return False


for name, start, goal, _label, layer, goal_is_via in ROUTES:
    require_endpoint_via(name, start)
    if goal_is_via:
        require_endpoint_via(name, goal)
    elif not point_on_same_net_track(name, goal, layer):
        raise RuntimeError(f"goal {goal} is not on existing {name} copper on layer {layer}")

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
    (1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
    (1, 1, math.sqrt(2)), (1, -1, math.sqrt(2)),
    (-1, 1, math.sqrt(2)), (-1, -1, math.sqrt(2)),
]


def astar(start_xy, goal_xy, blocked):
    start = cell(*start_xy); goal = cell(*goal_xy)
    for q in (start, goal):
        for di in range(-ENDPOINT_ESCAPE_CELLS, ENDPOINT_ESCAPE_CELLS + 1):
            for dj in range(-ENDPOINT_ESCAPE_CELLS, ENDPOINT_ESCAPE_CELLS + 1):
                blocked.discard((q[0] + di, q[1] + dj))

    def h(c): return math.hypot(c[0] - goal[0], c[1] - goal[1])

    pq = [(h(start), 0.0, start, None)]
    best = {start: 0.0}
    parent = {}
    while pq:
        _f, g, cur, incoming = heapq.heappop(pq)
        if g != best.get(cur):
            continue
        if cur == goal:
            out = [cur]
            while cur != start:
                cur = parent[cur]
                out.append(cur)
            return list(reversed(out))
        for di, dj, cost in DIRS:
            nxt = (cur[0] + di, cur[1] + dj)
            if not in_bounds(nxt) or nxt in blocked:
                continue
            if di and dj and ((cur[0] + di, cur[1]) in blocked or (cur[0], cur[1] + dj) in blocked):
                continue
            direction = (di, dj)
            ng = g + cost + (0.10 if incoming is not None and direction != incoming else 0.0)
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                parent[nxt] = cur
                heapq.heappush(pq, (ng + h(nxt), ng, nxt, direction))
    raise RuntimeError(f"no route {start_xy}->{goal_xy}")


def simplify(cells, start, goal):
    pts = [start] + [xy(c) for c in cells[1:-1]] + [goal]
    out = [pts[0]]; last = None
    for b in pts[1:]:
        a = out[-1]
        dx = round(b[0] - a[0], 6); dy = round(b[1] - a[1], 6)
        if abs(dx) < 1e-6: d = (0, 1 if dy > 0 else -1)
        elif abs(dy) < 1e-6: d = (1 if dx > 0 else -1, 0)
        elif abs(abs(dx) - abs(dy)) < 1e-6: d = (1 if dx > 0 else -1, 1 if dy > 0 else -1)
        else: d = None
        if last is not None and d == last and len(out) >= 2:
            out[-1] = b
        else:
            out.append(b); last = d
    return out


def add_track(a, b, name, layer):
    tr = pcbnew.PCB_TRACK(board)
    tr.SetStart(pt(*a)); tr.SetEnd(pt(*b)); tr.SetLayer(layer); tr.SetWidth(iu(TRACK_W))
    n = net_obj(name)
    if hasattr(tr, "SetNet"):
        tr.SetNet(n)
    else:
        tr.SetNetCode(net_code(name))
    board.Add(tr)


def layer_name(layer):
    return board.GetLayerName(layer)


report = [
    "# KH910 Rev A K/L A* route report v2", "",
    f"grid {STEP} mm; width {TRACK_W} mm; clearance raster {CLEAR} mm; endpoint escape {ENDPOINT_ESCAPE_CELLS} cells",
    "", "Machine/GPIO endpoints reuse DRC-clean vias. R214 terminates directly on the existing B.Cu L corridor.", "",
]

for name, start, goal, label, layer, _goal_is_via in ROUTES:
    raw = astar(start, goal, build_blocked(name, layer))
    points = simplify(raw, start, goal)
    for a, b in zip(points, points[1:]):
        add_track(a, b, name, layer)
    board.BuildConnectivity()
    report += [
        f"## {label}", f"- net: `{name}`", f"- layer: `{layer_name(layer)}`",
        f"- start: {start}", f"- goal: {goal}", f"- cells: {len(raw)}",
        f"- segments: {len(points)-1}",
        "- points: " + " -> ".join(f"({x:.3f},{y:.3f})" for x, y in points), "",
    ]

pcbnew.SaveBoard(str(PATH), board)
report_path = PATH.with_name("KH910_REV_A_KL_ASTAR_ROUTE.md")
report_path.write_text("\n".join(report) + "\n")
print("KL_ASTAR_ROUTE_V2_OK", PATH)
print(report_path)
