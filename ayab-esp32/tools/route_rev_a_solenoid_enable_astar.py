#!/usr/bin/env python3
"""Route SOLENOID_PWR_EN from existing GPIO21 copper to staged R821.1.

The existing GPIO21 net is already routed on the promoted board. This script
branches from existing same-net copper and obstacle-routes to R821.1.

Unlike the earlier version, every proposed F.Cu<->B.Cu goal via is checked
against copper on *all* board layers before it is accepted. A through-via
cannot avoid an inner-layer trace merely by attaching its route on another
layer; its barrel passes through the full stackup.

KiCad DRC after zone refill remains authoritative.
"""
from __future__ import annotations
import heapq, math, sys
from pathlib import Path
import pcbnew

if len(sys.argv) != 2:
    raise SystemExit("usage: route_rev_a_solenoid_enable_astar.py BOARD.kicad_pcb")
PATH = Path(sys.argv[1]).resolve()
b = pcbnew.LoadBoard(str(PATH))
if b is None:
    raise RuntimeError(f"could not load {PATH}")
b.BuildConnectivity()

NET = "SOLENOID_PWR_EN"
TRACK_W = 0.25
STEP = 0.20
CLEAR = 0.22
EDGE_CLEAR = 0.45
VIA_SIZE = 0.70
VIA_DRILL = 0.35
VIA_RADIUS = VIA_SIZE / 2.0
VIA_CLEAR = 0.12
COPPER = (pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.B_Cu)

mm = pcbnew.ToMM
iu = pcbnew.FromMM

def pt(x, y):
    return pcbnew.VECTOR2I(iu(x), iu(y))

NC = b.GetNetcodeFromNetname(NET)
if NC <= 0:
    raise RuntimeError(f"missing net {NET}")


def netobj():
    for f in b.GetFootprints():
        for p in f.Pads():
            if p.GetNetname() == NET and hasattr(p, "GetNet"):
                return p.GetNet()
    for t in b.GetTracks():
        if t.GetNetname() == NET and hasattr(t, "GetNet"):
            return t.GetNet()
    raise RuntimeError("cannot resolve enable net object")

NO = netobj()


def xypos(o):
    p = o.GetPosition()
    return mm(p.x), mm(p.y)


def endpoint(t, k):
    p = t.GetStart() if k == 0 else t.GetEnd()
    return mm(p.x), mm(p.y)


def near(a, z, tol=0.03):
    return abs(a[0] - z[0]) <= tol and abs(a[1] - z[1]) <= tol


r821 = next((f for f in b.GetFootprints() if f.GetReference() == "R821"), None)
if r821 is None:
    raise RuntimeError("R821 missing; run local gate stage first")
pad1 = next((p for p in r821.Pads() if p.GetNumber() == "1"), None)
if pad1 is None or pad1.GetNetname() != NET:
    raise RuntimeError(f"R821.1 is not on {NET}")
GOAL_PAD = xypos(pad1)

# Existing same-net track endpoints are valid branch anchors. Deduplicate exact
# endpoint/layer pairs and try the geometrically nearer ones first.
anchors = {}
for t in b.GetTracks():
    if isinstance(t, pcbnew.PCB_VIA) or t.GetNetCode() != NC:
        continue
    layer = t.GetLayer()
    for k in (0, 1):
        q = endpoint(t, k)
        key = (layer, round(q[0], 3), round(q[1], 3))
        anchors[key] = (layer, q)
if not anchors:
    raise RuntimeError(f"no existing routed copper found on {NET}")
ordered = sorted(
    anchors.values(),
    key=lambda z: math.hypot(z[1][0] - GOAL_PAD[0], z[1][1] - GOAL_PAD[1]),
)
print("SOL_ENABLE_ANCHOR_COUNT", len(ordered))
for layer, q in ordered[:12]:
    print("SOL_ENABLE_NEAR_ANCHOR", b.GetLayerName(layer), *(round(v, 3) for v in q))


def bbox(obj):
    r = obj.GetBoundingBox()
    if all(hasattr(r, n) for n in ("GetX", "GetY", "GetWidth", "GetHeight")):
        x = mm(r.GetX())
        y = mm(r.GetY())
        w = mm(r.GetWidth())
        h = mm(r.GetHeight())
        return x, y, x + w, y + h
    return mm(r.GetLeft()), mm(r.GetTop()), mm(r.GetRight()), mm(r.GetBottom())


bb = b.GetBoardEdgesBoundingBox()
BOARD_X0 = mm(bb.GetX())
BOARD_Y0 = mm(bb.GetY())
BOARD_X1 = BOARD_X0 + mm(bb.GetWidth())
BOARD_Y1 = BOARD_Y0 + mm(bb.GetHeight())
X0 = math.floor(BOARD_X0 / STEP) * STEP
Y0 = math.floor(BOARD_Y0 / STEP) * STEP
X1 = math.ceil(BOARD_X1 / STEP) * STEP
Y1 = math.ceil(BOARD_Y1 / STEP) * STEP
NX = int(round((X1 - X0) / STEP)) + 1
NY = int(round((Y1 - Y0) / STEP)) + 1


def cell(x, y):
    return int(round((x - X0) / STEP)), int(round((y - Y0) / STEP))


def xy(c):
    return X0 + c[0] * STEP, Y0 + c[1] * STEP


def inside(c):
    return 0 <= c[0] < NX and 0 <= c[1] < NY


def raster(blocked, box, expand):
    x0, y0, x1, y1 = box
    x0 -= expand
    y0 -= expand
    x1 += expand
    y1 += expand
    a = cell(x0, y0)
    z = cell(x1, y1)
    for i in range(max(0, min(a[0], z[0])), min(NX - 1, max(a[0], z[0])) + 1):
        for j in range(max(0, min(a[1], z[1])), min(NY - 1, max(a[1], z[1])) + 1):
            blocked.add((i, j))


def blocked_for(layer):
    out = set()
    for t in b.GetTracks():
        same = t.GetNetCode() == NC
        if isinstance(t, pcbnew.PCB_VIA):
            if not same:
                raster(out, bbox(t), CLEAR)
        elif t.GetLayer() == layer and not same:
            raster(out, bbox(t), CLEAR)
    for f in b.GetFootprints():
        for p in f.Pads():
            if p.GetNetCode() == NC:
                continue
            try:
                on = p.IsOnLayer(layer)
            except Exception:
                on = True
            if on:
                raster(out, bbox(p), CLEAR)
    for d in b.GetDrawings():
        if d.GetLayer() == pcbnew.Edge_Cuts:
            raster(out, bbox(d), EDGE_CLEAR)
    return out


DIRS = [
    (1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1),
    (1, 1, math.sqrt(2)), (1, -1, math.sqrt(2)),
    (-1, 1, math.sqrt(2)), (-1, -1, math.sqrt(2)),
]


def astar(sxy, gxy, blocked):
    s = cell(*sxy)
    g = cell(*gxy)
    blocked.discard(s)
    blocked.discard(g)

    def h(c):
        return math.hypot(c[0] - g[0], c[1] - g[1])

    pq = [(h(s), 0.0, s, None)]
    best = {s: 0.0}
    parent = {}
    while pq:
        _, cost, cur, incoming = heapq.heappop(pq)
        if cost != best.get(cur):
            continue
        if cur == g:
            out = [cur]
            while cur != s:
                cur = parent[cur]
                out.append(cur)
            return list(reversed(out))
        for di, dj, w in DIRS:
            nxt = (cur[0] + di, cur[1] + dj)
            if not inside(nxt) or nxt in blocked:
                continue
            if di and dj and ((cur[0] + di, cur[1]) in blocked or (cur[0], cur[1] + dj) in blocked):
                continue
            direction = (di, dj)
            nc = cost + w + (0.10 if incoming is not None and incoming != direction else 0)
            if nc < best.get(nxt, float("inf")):
                best[nxt] = nc
                parent[nxt] = cur
                heapq.heappush(pq, (nc + h(nxt), nc, nxt, direction))
    return None


def simplify(cells, start, goal):
    pts = [start] + [xy(c) for c in cells[1:-1]] + [goal]
    out = [pts[0]]
    last = None
    for q in pts[1:]:
        a = out[-1]
        dx = round(q[0] - a[0], 6)
        dy = round(q[1] - a[1], 6)
        if abs(dx) < 1e-6:
            d = (0, 1 if dy > 0 else -1)
        elif abs(dy) < 1e-6:
            d = (1 if dx > 0 else -1, 0)
        elif abs(abs(dx) - abs(dy)) < 1e-6:
            d = (1 if dx > 0 else -1, 1 if dy > 0 else -1)
        else:
            d = None
        if last is not None and d == last and len(out) >= 2:
            out[-1] = q
        else:
            out.append(q)
            last = d
    return out


def point_segment_distance(q, a, z):
    qx, qy = q
    ax, ay = a
    zx, zy = z
    vx, vy = zx - ax, zy - ay
    wx, wy = qx - ax, qy - ay
    vv = vx * vx + vy * vy
    if vv <= 1e-18:
        return math.hypot(qx - ax, qy - ay)
    t = max(0.0, min(1.0, (wx * vx + wy * vy) / vv))
    px, py = ax + t * vx, ay + t * vy
    return math.hypot(qx - px, qy - py)


def point_rect_distance(q, r):
    x, y = q
    x0, y0, x1, y1 = r
    dx = max(x0 - x, 0.0, x - x1)
    dy = max(y0 - y, 0.0, y - y1)
    return math.hypot(dx, dy)


def via_clear(q):
    # Keep enough room from the actual board outline even before DRC.
    if not (
        BOARD_X0 + VIA_RADIUS + EDGE_CLEAR <= q[0] <= BOARD_X1 - VIA_RADIUS - EDGE_CLEAR
        and BOARD_Y0 + VIA_RADIUS + EDGE_CLEAR <= q[1] <= BOARD_Y1 - VIA_RADIUS - EDGE_CLEAR
    ):
        return False, "edge"

    # A through-via barrel exists on every copper layer. Check every existing
    # non-enable track/via regardless of its routing layer.
    for t in b.GetTracks():
        if t.GetNetCode() == NC:
            continue
        if isinstance(t, pcbnew.PCB_VIA):
            d = math.hypot(q[0] - xypos(t)[0], q[1] - xypos(t)[1])
            need = VIA_RADIUS + mm(t.GetWidth()) / 2.0 + VIA_CLEAR
            if d < need:
                return False, f"via:{t.GetNetname()}"
        elif t.GetLayer() in COPPER:
            d = point_segment_distance(q, endpoint(t, 0), endpoint(t, 1))
            need = VIA_RADIUS + mm(t.GetWidth()) / 2.0 + VIA_CLEAR
            if d < need:
                return False, f"track:{t.GetNetname()}:{b.GetLayerName(t.GetLayer())}"

    for f in b.GetFootprints():
        for p in f.Pads():
            if p.GetNetCode() == NC:
                continue
            try:
                on_copper = any(p.IsOnLayer(layer) for layer in COPPER)
            except Exception:
                on_copper = True
            if not on_copper:
                continue
            if point_rect_distance(q, bbox(p)) < VIA_RADIUS + VIA_CLEAR:
                return False, f"pad:{f.GetReference()}.{p.GetNumber()}:{p.GetNetname()}"
    return True, "clear"


def cells_for_segment(a, z):
    # Sample at finer than the A* grid and map back to blocked cells.
    dist = math.hypot(z[0] - a[0], z[1] - a[1])
    n = max(1, int(math.ceil(dist / (STEP / 2.0))))
    out = []
    for i in range(n + 1):
        t = i / n
        q = (a[0] + (z[0] - a[0]) * t, a[1] + (z[1] - a[1]) * t)
        c = cell(*q)
        if c not in out:
            out.append(c)
    return out


def local_stub(goal, blocked):
    # Keep the short top-layer connection orthogonal. Try both Manhattan bends.
    bends = [(goal[0], GOAL_PAD[1]), (GOAL_PAD[0], goal[1])]
    for bend in bends:
        seq = [goal]
        if not near(goal, bend, 1e-6) and not near(bend, GOAL_PAD, 1e-6):
            seq.append(bend)
        seq.append(GOAL_PAD)
        used = []
        ok = True
        for a, z in zip(seq, seq[1:]):
            cs = cells_for_segment(a, z)
            # The same-net destination pad itself is intentionally allowed.
            for c in cs[:-1]:
                if c in blocked:
                    ok = False
                    break
            if not ok:
                break
            used.extend(cs)
        if ok:
            return seq
    return None


def addseg(a, z, layer):
    t = pcbnew.PCB_TRACK(b)
    t.SetStart(pt(*a))
    t.SetEnd(pt(*z))
    t.SetLayer(layer)
    t.SetWidth(iu(TRACK_W))
    t.SetNet(NO)
    b.Add(t)


def addvia(q):
    v = pcbnew.PCB_VIA(b)
    v.SetPosition(pt(*q))
    v.SetWidth(iu(VIA_SIZE))
    v.SetDrill(iu(VIA_DRILL))
    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    v.SetNet(NO)
    b.Add(v)


# Search a real 2-D window above/around R821 rather than repeatedly nudging one
# X coordinate. Keep the via outside the SMD pad itself and rank nearer sites
# first. 0.2 mm grid matches the route lattice.
candidate_vias = []
for xi in range(-18, 19):
    for yi in range(-17, 2):
        q = (round(GOAL_PAD[0] + xi * STEP, 3), round(GOAL_PAD[1] + yi * STEP, 3))
        d = math.hypot(q[0] - GOAL_PAD[0], q[1] - GOAL_PAD[1])
        if d < 0.90 or d > 4.20:
            continue
        clear, reason = via_clear(q)
        if clear:
            stub = local_stub(q, blocked_for(pcbnew.F_Cu))
            if stub is not None:
                candidate_vias.append((d, q, stub))

candidate_vias.sort(key=lambda x: x[0])
print("SOL_ENABLE_SAFE_GOAL_COUNT", len(candidate_vias))
for d, q, stub in candidate_vias[:12]:
    print("SOL_ENABLE_SAFE_GOAL", *(round(v, 3) for v in q), f"distance={d:.3f}", "stub=" + "->".join(f"({x:.3f},{y:.3f})" for x, y in stub))
if not candidate_vias:
    raise RuntimeError("no all-layer-clear through-via site found near R821.1")

selected = None
for rank, (layer, start) in enumerate(ordered[:24], 1):
    # F.Cu can route directly to the pad with no layer-change via.
    if layer == pcbnew.F_Cu:
        path = astar(start, GOAL_PAD, blocked_for(layer))
        if path is not None:
            selected = (rank, 0, layer, start, GOAL_PAD, path, None)
            break
    else:
        for gi, (_, goal, stub) in enumerate(candidate_vias[:40], 1):
            path = astar(start, goal, blocked_for(layer))
            if path is not None:
                selected = (rank, gi, layer, start, goal, path, stub)
                break
        if selected:
            break
    print("SOL_ENABLE_ANCHOR_BLOCKED", rank, b.GetLayerName(layer), tuple(round(v, 3) for v in start))

if selected is None:
    raise RuntimeError("no obstacle-aware SOLENOID_PWR_EN route found from existing copper to an all-layer-clear goal")

rank, gi, layer, start, goal, path, stub = selected
pts = simplify(path, start, goal)
for a, z in zip(pts, pts[1:]):
    addseg(a, z, layer)
if layer != pcbnew.F_Cu:
    addvia(goal)
    for a, z in zip(stub, stub[1:]):
        addseg(a, z, pcbnew.F_Cu)

b.BuildConnectivity()
pcbnew.SaveBoard(str(PATH), b)
print("SOL_ENABLE_ROUTE_OK", f"anchor_rank={rank}", f"goal_candidate={gi}", f"layer={b.GetLayerName(layer)}", f"cells={len(path)}")
print("SOL_ENABLE_START", tuple(round(v, 4) for v in start), "GOAL", tuple(round(v, 4) for v in goal), "R821_1", tuple(round(v, 4) for v in GOAL_PAD))
print("SOL_ENABLE_POINTS", " -> ".join(f"({x:.3f},{y:.3f})" for x, y in pts))
if stub is not None:
    print("SOL_ENABLE_FINAL_STUB", " -> ".join(f"({x:.3f},{y:.3f})" for x, y in stub))
