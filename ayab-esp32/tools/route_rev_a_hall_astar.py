#!/usr/bin/env python3
"""Route Rev A Hall ADC nets on In1.Cu using the actual staged KiCad board.

This is intentionally narrow. It assumes v4c has already:
- created HALL_L_ADC and HALL_R_ADC nets;
- retagged U201 GPIO1/GPIO2 and the proven legacy MCU corridors;
- added the divider taps and safe start vias.

The router rasterizes real In1.Cu tracks, all-layer vias, PTH pads and Edge.Cuts
with conservative clearance, then A* routes from each divider start via to the
existing retagged MCU via. KiCad DRC remains the authoritative final check.
"""
from __future__ import annotations

import heapq
import math
import sys
from pathlib import Path
import pcbnew

if len(sys.argv) != 2:
    raise SystemExit("usage: route_rev_a_hall_astar.py BOARD.kicad_pcb")

PATH = Path(sys.argv[1]).resolve()
board = pcbnew.LoadBoard(str(PATH))
if board is None:
    raise RuntimeError(f"could not load {PATH}")

LAYER = pcbnew.In1_Cu
STEP = 0.25
TRACK_W = 0.25
CLEAR = 0.22
EDGE_CLEAR = 0.45

ROUTES = [
    ("/ESP32/HALL_R_ADC", (309.5, 160.5), (218.8, 134.13)),
    ("/ESP32/HALL_L_ADC", (94.0, 136.5), (219.55, 134.13)),
]


def mm(v):
    return pcbnew.ToMM(v)


def iu(v):
    return pcbnew.FromMM(v)


def pt(x, y):
    return pcbnew.VECTOR2I(iu(x), iu(y))


def bbox_mm(obj):
    r = obj.GetBoundingBox()
    # KiCad 9 EDA_RECT supports GetX/Y/Width/Height. Keep fallbacks for minor
    # API naming differences across runner builds.
    if all(hasattr(r, n) for n in ("GetX", "GetY", "GetWidth", "GetHeight")):
        x = mm(r.GetX()); y = mm(r.GetY()); w = mm(r.GetWidth()); h = mm(r.GetHeight())
        return x, y, x + w, y + h
    return mm(r.GetLeft()), mm(r.GetTop()), mm(r.GetRight()), mm(r.GetBottom())


def net_code(name):
    code = board.GetNetcodeFromNetname(name)
    if code <= 0:
        raise RuntimeError(f"missing net {name}")
    return code


def net_obj_for(name):
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetname() == name:
                if hasattr(pad, "GetNet"):
                    return pad.GetNet()
    for item in board.GetTracks():
        if item.GetNetname() == name and hasattr(item, "GetNet"):
            return item.GetNet()
    raise RuntimeError(f"cannot resolve NETINFO_ITEM for {name}")


# Work within the physical board-edge bounding box. Edge.Cuts themselves are
# rasterized as barriers, so internal slots/notches cannot be crossed.
bb = board.GetBoardEdgesBoundingBox()
X0 = math.floor(mm(bb.GetX()) / STEP) * STEP
Y0 = math.floor(mm(bb.GetY()) / STEP) * STEP
X1 = math.ceil((mm(bb.GetX()) + mm(bb.GetWidth())) / STEP) * STEP
Y1 = math.ceil((mm(bb.GetY()) + mm(bb.GetHeight())) / STEP) * STEP
NX = int(round((X1 - X0) / STEP)) + 1
NY = int(round((Y1 - Y0) / STEP)) + 1


def cell(x, y):
    return (int(round((x - X0) / STEP)), int(round((y - Y0) / STEP)))


def xy(c):
    return (X0 + c[0] * STEP, Y0 + c[1] * STEP)


def in_bounds(c):
    return 0 <= c[0] < NX and 0 <= c[1] < NY


def raster_box(blocked, box, expand):
    x0, y0, x1, y1 = box
    x0 -= expand; y0 -= expand; x1 += expand; y1 += expand
    i0, j0 = cell(x0, y0); i1, j1 = cell(x1, y1)
    for i in range(max(0, min(i0, i1)), min(NX - 1, max(i0, i1)) + 1):
        for j in range(max(0, min(j0, j1)), min(NY - 1, max(j0, j1)) + 1):
            blocked.add((i, j))


def build_blocked(route_net):
    blocked = set()
    own_code = net_code(route_net)

    # Existing copper on In1 plus every via, excluding the route's own retagged
    # start/MCU-via copper so A* can terminate on it.
    for item in board.GetTracks():
        same = item.GetNetCode() == own_code
        is_via = isinstance(item, pcbnew.PCB_VIA)
        if is_via:
            if not same:
                raster_box(blocked, bbox_mm(item), CLEAR)
        elif item.GetLayer() == LAYER and not same:
            raster_box(blocked, bbox_mm(item), CLEAR)

    # Through-hole / multilayer pads occupy In1 even when their visible routing
    # is on another layer. SMD pads not flashed on In1 are ignored.
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetCode() == own_code:
                continue
            try:
                on_layer = pad.IsOnLayer(LAYER)
            except Exception:
                on_layer = True
            if on_layer:
                raster_box(blocked, bbox_mm(pad), CLEAR)

    # Treat Edge.Cuts geometry as a thick barrier. A route starts inside the
    # board, therefore blocking the boundary also prevents excursions outside.
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
    # The endpoints are pre-existing same-net vias; allow the exact cells and a
    # one-cell throat around them so raster quantization does not seal them off.
    for q in (start, goal):
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                blocked.discard((q[0] + di, q[1] + dj))

    def h(c):
        return math.hypot(c[0] - goal[0], c[1] - goal[1])

    pq = [(h(start), 0.0, start, None)]
    best = {start: 0.0}
    parent = {}
    pdir = {}
    while pq:
        _f, g, cur, incoming = heapq.heappop(pq)
        if g != best.get(cur):
            continue
        if cur == goal:
            out = [cur]
            while cur != start:
                cur = parent[cur]
                out.append(cur)
            out.reverse()
            return out
        for di, dj, cost in DIRS:
            nxt = (cur[0] + di, cur[1] + dj)
            if not in_bounds(nxt) or nxt in blocked:
                continue
            # Do not cut diagonally through the corner of two blocked cells.
            if di and dj and ((cur[0] + di, cur[1]) in blocked or (cur[0], cur[1] + dj) in blocked):
                continue
            direction = (di, dj)
            turn_penalty = 0.10 if incoming is not None and direction != incoming else 0.0
            ng = g + cost + turn_penalty
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                parent[nxt] = cur
                pdir[nxt] = direction
                heapq.heappush(pq, (ng + h(nxt), ng, nxt, direction))
    raise RuntimeError(f"no A* route from {start_xy} to {goal_xy}")


def simplify(cells, start_exact, goal_exact):
    pts = [start_exact] + [xy(c) for c in cells[1:-1]] + [goal_exact]
    out = [pts[0]]
    last_dir = None
    for idx in range(1, len(pts)):
        a = out[-1]
        b = pts[idx]
        dx = round(b[0] - a[0], 6); dy = round(b[1] - a[1], 6)
        # Normalize only exact grid-grid portions; endpoint stubs may be arbitrary.
        if abs(dx) < 1e-6:
            d = (0, 1 if dy > 0 else -1)
        elif abs(dy) < 1e-6:
            d = (1 if dx > 0 else -1, 0)
        elif abs(abs(dx) - abs(dy)) < 1e-6:
            d = (1 if dx > 0 else -1, 1 if dy > 0 else -1)
        else:
            d = None
        if last_dir is not None and d == last_dir and len(out) >= 2:
            out[-1] = b
        else:
            out.append(b)
            last_dir = d
    return out


def add_track(a, b, name):
    tr = pcbnew.PCB_TRACK(board)
    tr.SetStart(pt(*a)); tr.SetEnd(pt(*b)); tr.SetLayer(LAYER); tr.SetWidth(iu(TRACK_W))
    net = net_obj_for(name)
    if hasattr(tr, "SetNet"):
        tr.SetNet(net)
    elif hasattr(tr, "SetNetCode"):
        tr.SetNetCode(net_code(name))
    else:
        raise RuntimeError("PCB_TRACK has no net setter")
    board.Add(tr)


report = ["# Hall ADC A* route report", "", f"grid: {STEP} mm; track: {TRACK_W} mm; obstacle expansion: {CLEAR} mm", ""]
for name, start, goal in ROUTES:
    blocked = build_blocked(name)
    raw = astar(start, goal, blocked)
    points = simplify(raw, start, goal)
    if len(points) < 2:
        raise RuntimeError(f"empty route for {name}")
    for a, b in zip(points, points[1:]):
        add_track(a, b, name)
    board.BuildConnectivity()
    report.append(f"## {name}")
    report.append(f"- start: {start}")
    report.append(f"- goal: {goal}")
    report.append(f"- A* cells: {len(raw)}")
    report.append(f"- simplified segments: {len(points)-1}")
    report.append("- points: " + " -> ".join(f"({x:.3f},{y:.3f})" for x, y in points))
    report.append("")

pcbnew.SaveBoard(str(PATH), board)
REPORT = PATH.with_name("KH910_REV_A_HALL_ASTAR_ROUTE.md")
REPORT.write_text("\n".join(report) + "\n")
print("HALL_ASTAR_ROUTE_OK", PATH)
print(REPORT)
