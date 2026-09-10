#!/usr/bin/env python3
"""Create a disposable Rev A power-integration PCB candidate.

This stages the already-approved schematic components onto the actual board,
removes the obsolete 0-ohm 5 V bypass, and moves GPIO4 to the divider net.  It
never writes the source board: a CI workflow must run KiCad DRC on its output
before any routing or promotion is considered.
"""
from __future__ import annotations

import argparse
import heapq
import math
import re
import sys
from pathlib import Path

import pcbnew

sys.path.insert(0, str(Path(__file__).resolve().parent))
import patch_rev_a_solenoid_pcb as u


ROOT = Path(__file__).resolve().parents[1]
PSU = ROOT / "psu.kicad_sch"
MCU = ROOT / "mcu.kicad_sch"
SENSE = "/ESP32/MACHINE_PWR_SENSE"
PLACEMENTS = {"U403": (300.0, 155.0), "R215": (225.0, 159.0), "R216": (228.5, 159.0)}


def clone9(template, new_ref, value, x, y, angle, path, lcsc, padmap):
    """Clone an embedded footprint with fresh KiCad identities."""
    out = re.sub(
        r'\((uuid|tstamp)\s+"?[0-9a-f-]+"?\)',
        lambda m: f'({m.group(1)} "{u.uid()}")',
        template,
    )
    out, count = re.subn(
        r"^(\(footprint.*?)(\(at\s+[-\d.]+\s+[-\d.]+(?:\s+[-\d.]+)?\))",
        lambda m: m.group(1) + f"(at {x:g} {y:g} {angle:g})",
        out, count=1, flags=re.S,
    )
    if count != 1:
        raise RuntimeError(f"could not relocate {new_ref}")
    out, count = re.subn(r'\(path "[^"]+"\)', f'(path "{path}")', out, count=1)
    if count != 1:
        raise RuntimeError(f"path anchor missing in {new_ref}")
    out, count = re.subn(r'\(property "Reference" "[^"]+"', f'(property "Reference" "{new_ref}"', out, count=1)
    if count != 1:
        raise RuntimeError(f"reference property missing in {new_ref}")
    out, count = re.subn(r'\(property "Value" "[^"]+"', f'(property "Value" "{value}"', out, count=1)
    if count != 1:
        raise RuntimeError(f"value property missing in {new_ref}")
    if '(property "LCSC ID"' in out:
        out = re.sub(r'\(property "LCSC ID" "[^"]*"\)', f'(property "LCSC ID" "{lcsc}")', out, count=1)
    for number, (net, name) in padmap.items():
        out = u.replace_pad_net(out, number, net, name)
    return out


def clear_pad_net(block: str, number: str) -> str:
    replacements = []
    for start, end, pad in u.blocks(block, "(pad "):
        if u.pad_num(pad) == str(number):
            replacements.append((start, end, re.sub(r"\s*\(net\s+\d+\s+\"[^\"]*\"\)", "", pad, count=1)))
    if len(replacements) != 1:
        raise RuntimeError(f"expected one pad {number}")
    for start, end, replacement in reversed(replacements):
        block = block[:start] + replacement + block[end:]
    return block


def sheet_prefix(text: str, reference: str) -> str:
    _, _, block = u.find_fp(text, reference)
    match = re.search(r'\(path "([^"]+)"\)', block)
    if not match:
        raise RuntimeError(f"path missing for {reference}")
    return match.group(1).rsplit("/", 1)[0]


def root_net_defs(text: str) -> dict[int, str]:
    return {int(code): name for code, name in re.findall(r'^\t\(net\s+(\d+)\s+"([^"]+)"\)', text, re.M)}


def insert_before_root_item(text: str, item: str, payload: str) -> str:
    match = re.search(rf"(?m)^\t\({re.escape(item)}\b", text)
    if not match:
        raise RuntimeError(f"root {item} insertion anchor missing")
    return text[:match.start()] + payload + "\n" + text[match.start():]


def remove_footprint(text: str, reference: str) -> tuple[str, list[tuple[float, float]]]:
    start, end, block = u.find_fp(text, reference)
    pads = [u.pad_global(block, number) for number in ("1", "2")]
    return text[:start] + text[end:], pads


def remove_tracks_touching(text: str, points: list[tuple[float, float]]) -> tuple[str, int]:
    removals = []
    for start, end, block in u.blocks(text, "(segment"):
        details = u.seg_points(block)
        if details and any(u.close(details[0], point) or u.close(details[1], point) for point in points):
            removals.append((start, end))
    for start, end, block in u.blocks(text, "(via"):
        at = re.search(r"\(at\s+([-\d.]+)\s+([-\d.]+)\)", block)
        if at and any(u.close((float(at.group(1)), float(at.group(2))), point) for point in points):
            removals.append((start, end))
    for start, end in reversed(sorted(removals)):
        text = text[:start] + text[end:]
    return text, len(removals)


def migrate_legacy_gpio4_branch(text: str, sense_code: int) -> tuple[str, int]:
    """Reuse GPIO4's proven front-layer escape and retain J701-to-U701.

    The two F.Cu segments and existing via at (207.49, 131.97) already pass
    source-board DRC.  Retag those items for MACHINE_PWR_SENSE and remove the
    former B.Cu branch to J701.7.  The independent F.Cu J701.7-to-U701.15
    connection remains intact as a local B7 level-shifter channel.
    """
    reuse = {
        "8bac310c-0660-4140-ad94-917957d62621",
        "f6a7ea09-b6e6-4db1-860f-d027f6ed01d4",
        "0b0b05f3-c43f-4117-84c2-1f32771f5b48",
    }
    obsolete = {
        "1ca24a7c-e5bd-45aa-8151-57d10658606e",
        "3548e073-eda2-46da-b4f3-711a0330dd08",
        "65f9136a-8580-4e01-8edb-36f49b08d509",
        "540fd51e-0690-4bf9-81c8-524f3e1a6e64",
        "79032982-cb89-4a2e-b13f-d4d3cc63adde",
        "8d88b049-9a7b-45e7-ac0d-cec054d9a842",
        "dcaadd28-13b0-44f6-8fd7-82a0e23808fb",
    }
    replacements = []
    removals = []
    for start, end, block in u.blocks(text, "(segment"):
        if any(f'(uuid "{item}")' in block for item in reuse):
            replacements.append((start, end, re.sub(r"\(net\s+30\)", f"(net {sense_code})", block, count=1)))
        if any(f'(uuid "{item}")' in block for item in obsolete):
            removals.append((start, end))
    for start, end, block in u.blocks(text, "(via"):
        if any(f'(uuid "{item}")' in block for item in reuse):
            replacements.append((start, end, re.sub(r"\(net\s+30\)", f"(net {sense_code})", block, count=1)))
        if any(f'(uuid "{item}")' in block for item in obsolete):
            removals.append((start, end))
    if len(replacements) != len(reuse):
        raise RuntimeError(f"expected {len(reuse)} reusable GPIO4 items, found {len(replacements)}")
    if len(removals) != len(obsolete):
        raise RuntimeError(f"expected {len(obsolete)} legacy GPIO4 branch items, found {len(removals)}")
    edits = [(start, end, "") for start, end in removals] + replacements
    for start, end, replacement in reversed(sorted(edits)):
        text = text[:start] + replacement + text[end:]
    return text, len(removals)


def symbol_uuid(path: Path, reference: str) -> str:
    return u.symbol_uuid_by_ref(path.read_text(encoding="utf-8"), reference)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    text = args.input.read_text(encoding="utf-8")
    existing = {ref for ref in ("U403", "R215", "R216") if f'(property "Reference" "{ref}"' in text}
    if existing:
        raise RuntimeError("partial power PCB state already present: " + ", ".join(sorted(existing)))
    defs = root_net_defs(text)
    names = {name: next((code for code, value in defs.items() if value == name), 0) for name in ("GND", "+5V", "+12V", "/PSU/5V_SW")}
    if any(code <= 0 for code in names.values()):
        raise RuntimeError(f"required board net missing: {names}")
    sense_code = max(defs) + 1

    text, r611_pads = remove_footprint(text, "R611")
    text, removed_bypass_tracks = remove_tracks_touching(text, r611_pads)
    _, _, u201 = u.find_fp(text, "U201")
    u201 = u.replace_pad_net(u201, "8", sense_code, SENSE)
    text = u.replace_fp(text, "U201", u201)
    text, removed_gpio4_tracks = migrate_legacy_gpio4_branch(text, sense_code)

    _, _, q501 = u.find_fp(text, "Q501")
    _, _, r206 = u.find_fp(text, "R206")
    psu_prefix = sheet_prefix(text, "U601")
    mcu_prefix = sheet_prefix(text, "U201")
    path_u403 = psu_prefix + "/" + symbol_uuid(PSU, "U403")
    path_r215 = mcu_prefix + "/" + symbol_uuid(MCU, "R215")
    path_r216 = mcu_prefix + "/" + symbol_uuid(MCU, "R216")
    x, y = PLACEMENTS["U403"]
    u403 = clone9(q501, "U403", "LM66100DCKR", x, y, 0, path_u403, "C2869734", {
        "1": (names["/PSU/5V_SW"], "/PSU/5V_SW"), "2": (names["GND"], "GND"),
        "3": (names["+5V"], "+5V"), "4": (names["+5V"], "+5V"),
        "5": (names["GND"], "GND"), "6": (names["+5V"], "+5V"),
    })
    u403 = clear_pad_net(u403, "4")
    x, y = PLACEMENTS["R215"]
    r215 = clone9(r206, "R215", "47k", x, y, 0, path_r215, "C25819", {
        "1": (names["+12V"], "+12V"), "2": (sense_code, SENSE),
    })
    x, y = PLACEMENTS["R216"]
    r216 = clone9(r206, "R216", "10k", x, y, 0, path_r216, "C25804", {
        "1": (sense_code, SENSE), "2": (names["GND"], "GND"),
    })
    text = insert_before_root_item(text, "footprint", f'\t(net {sense_code} "{SENSE}")')
    text = insert_before_root_item(text, "segment", "\n".join((u403, r215, r216)))
    args.output.write_text(text, encoding="utf-8")

    board = pcbnew.LoadBoard(str(args.output))
    if board is None:
        raise RuntimeError("KiCad could not reload staged power board")
    for footprint in board.GetFootprints():
        if footprint.GetReference() in PLACEMENTS:
            footprint.Flip(footprint.GetPosition(), False)
    board.BuildConnectivity()

    footprints = {footprint.GetReference(): footprint for footprint in board.GetFootprints()}

    def pad_position(reference: str, number: str) -> tuple[float, float]:
        footprint = footprints.get(reference)
        if footprint is None:
            raise RuntimeError(f"staged footprint missing: {reference}")
        pad = next((item for item in footprint.Pads() if item.GetNumber() == number), None)
        if pad is None:
            raise RuntimeError(f"staged pad missing: {reference}.{number}")
        point = pad.GetPosition()
        return pcbnew.ToMM(point.x), pcbnew.ToMM(point.y)

    def add_segment(start: tuple[float, float], end: tuple[float, float], net_name: str) -> None:
        code = board.GetNetcodeFromNetname(net_name)
        if code <= 0:
            raise RuntimeError(f"staged net missing: {net_name}")
        track = pcbnew.PCB_TRACK(board)
        track.SetStart(pcbnew.VECTOR2I_MM(*start))
        track.SetEnd(pcbnew.VECTOR2I_MM(*end))
        track.SetWidth(pcbnew.FromMM(0.25))
        track.SetLayer(pcbnew.B_Cu)
        track.SetNetCode(code)
        board.Add(track)

    def add_front_segment(start: tuple[float, float], end: tuple[float, float], net_name: str) -> None:
        code = board.GetNetcodeFromNetname(net_name)
        if code <= 0:
            raise RuntimeError(f"staged net missing: {net_name}")
        track = pcbnew.PCB_TRACK(board)
        track.SetStart(pcbnew.VECTOR2I_MM(*start))
        track.SetEnd(pcbnew.VECTOR2I_MM(*end))
        track.SetWidth(pcbnew.FromMM(0.25))
        track.SetLayer(pcbnew.F_Cu)
        track.SetNetCode(code)
        board.Add(track)

    def add_via(position: tuple[float, float], net_name: str) -> None:
        code = board.GetNetcodeFromNetname(net_name)
        if code <= 0:
            raise RuntimeError(f"staged net missing: {net_name}")
        via = pcbnew.PCB_VIA(board)
        via.SetPosition(pcbnew.VECTOR2I_MM(*position))
        via.SetWidth(pcbnew.FromMM(0.60))
        via.SetDrill(pcbnew.FromMM(0.30))
        via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        via.SetNetCode(code)
        board.Add(via)

    def route_b_cu(start: tuple[float, float], goal: tuple[float, float], net_name: str,
                   bounds: tuple[float, float, float, float], layer=pcbnew.B_Cu) -> list[tuple[float, float]]:
        """Route one low-current net on a signal layer around native obstacles.

        This deliberately operates only on the disposable candidate.  DRC is
        still the authority; the coarse grid simply avoids blindly drawing a
        long trace through a known existing conductor.
        """
        step = 0.25
        clearance = 0.24
        x0, y0, x1, y1 = bounds
        nx = int(round((x1 - x0) / step)) + 1
        ny = int(round((y1 - y0) / step)) + 1
        own = board.GetNetcodeFromNetname(net_name)
        blocked: set[tuple[int, int]] = set()

        def xy(cell: tuple[int, int]) -> tuple[float, float]:
            return x0 + cell[0] * step, y0 + cell[1] * step

        def cell(point: tuple[float, float]) -> tuple[int, int]:
            return int(round((point[0] - x0) / step)), int(round((point[1] - y0) / step))

        def raster(item) -> None:
            box = item.GetBoundingBox()
            bx0 = pcbnew.ToMM(box.GetX()) - clearance
            by0 = pcbnew.ToMM(box.GetY()) - clearance
            bx1 = pcbnew.ToMM(box.GetX() + box.GetWidth()) + clearance
            by1 = pcbnew.ToMM(box.GetY() + box.GetHeight()) + clearance
            ix0 = max(0, int(math.floor((bx0 - x0) / step)))
            iy0 = max(0, int(math.floor((by0 - y0) / step)))
            ix1 = min(nx - 1, int(math.ceil((bx1 - x0) / step)))
            iy1 = min(ny - 1, int(math.ceil((by1 - y0) / step)))
            for ix in range(ix0, ix1 + 1):
                for iy in range(iy0, iy1 + 1):
                    blocked.add((ix, iy))

        for item in board.GetTracks():
            if item.GetNetCode() == own:
                continue
            if isinstance(item, pcbnew.PCB_VIA) or item.GetLayer() == layer:
                raster(item)
        for footprint in board.GetFootprints():
            for pad in footprint.Pads():
                if pad.GetNetCode() == own:
                    continue
                try:
                    on_bottom = pad.IsOnLayer(layer)
                except AttributeError:
                    on_bottom = True
                if on_bottom:
                    raster(pad)
        # Keep the disposable route inside the real board outline and out of
        # all rule/keepout areas.  DRC remains authoritative, but these are
        # hard geometric constraints rather than ordinary copper obstacles.
        edge_clearance = clearance
        clearance = 0.45
        for drawing in board.GetDrawings():
            if drawing.GetLayer() == pcbnew.Edge_Cuts:
                raster(drawing)
        clearance = edge_clearance
        for zone in board.Zones():
            if zone.GetIsRuleArea():
                raster(zone)

        origin = cell(start)
        target = cell(goal)
        for centre in (origin, target):
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    blocked.discard((centre[0] + dx, centre[1] + dy))

        queue = [(0.0, 0.0, origin)]
        parent: dict[tuple[int, int], tuple[int, int]] = {}
        cost = {origin: 0.0}
        while queue:
            _estimate, current_cost, current = heapq.heappop(queue)
            if current_cost != cost.get(current):
                continue
            if current == target:
                cells = [current]
                while current != origin:
                    current = parent[current]
                    cells.append(current)
                cells.reverse()
                points = [start] + [xy(point) for point in cells[1:-1]] + [goal]
                reduced = [points[0]]
                old_direction = None
                for point in points[1:]:
                    previous = reduced[-1]
                    direction = (round(point[0] - previous[0], 6), round(point[1] - previous[1], 6))
                    direction = (0 if abs(direction[0]) < 1e-6 else int(math.copysign(1, direction[0])),
                                 0 if abs(direction[1]) < 1e-6 else int(math.copysign(1, direction[1])))
                    if old_direction == direction and len(reduced) > 1:
                        reduced[-1] = point
                    else:
                        reduced.append(point)
                        old_direction = direction
                for first, second in zip(reduced, reduced[1:]):
                    code = board.GetNetcodeFromNetname(net_name)
                    track = pcbnew.PCB_TRACK(board)
                    track.SetStart(pcbnew.VECTOR2I_MM(*first))
                    track.SetEnd(pcbnew.VECTOR2I_MM(*second))
                    track.SetWidth(pcbnew.FromMM(0.25))
                    track.SetLayer(layer)
                    track.SetNetCode(code)
                    board.Add(track)
                return reduced
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nxt = current[0] + dx, current[1] + dy
                if not (0 <= nxt[0] < nx and 0 <= nxt[1] < ny) or nxt in blocked:
                    continue
                next_cost = current_cost + 1
                if next_cost < cost.get(nxt, float("inf")):
                    cost[nxt] = next_cost
                    parent[nxt] = current
                    distance = abs(nxt[0] - target[0]) + abs(nxt[1] - target[1])
                    heapq.heappush(queue, (next_cost + distance, next_cost, nxt))
        raise RuntimeError(f"no route for {net_name} from {start} to {goal} on layer {layer}")

    def route_any_signal_layer(start: tuple[float, float], goal: tuple[float, float], net_name: str,
                               bounds: tuple[float, float, float, float]) -> tuple[list[tuple[float, float]], int]:
        """Try each signal layer on the disposable board without forcing a crossing."""
        failures: list[str] = []
        for layer in (pcbnew.B_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.F_Cu):
            try:
                return route_b_cu(start, goal, net_name, bounds, layer), layer
            except RuntimeError as exc:
                failures.append(str(exc))
        raise RuntimeError("; ".join(failures))

    def route_multilayer(start: tuple[float, float], goal: tuple[float, float], net_name: str,
                         bounds: tuple[float, float, float, float]) -> list[tuple[float, float, int]]:
        """Route across signal layers, changing layers only at all-layer-clear cells."""
        step = 0.25
        x0, y0, x1, y1 = bounds
        nx = int(round((x1 - x0) / step)) + 1
        ny = int(round((y1 - y0) / step)) + 1
        layers = (pcbnew.B_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.F_Cu)
        own = board.GetNetcodeFromNetname(net_name)

        def xy(cell: tuple[int, int]) -> tuple[float, float]:
            return x0 + cell[0] * step, y0 + cell[1] * step

        def cell(point: tuple[float, float]) -> tuple[int, int]:
            return int(round((point[0] - x0) / step)), int(round((point[1] - y0) / step))

        def raster(blocked: set[tuple[int, int]], item, expand: float) -> None:
            box = item.GetBoundingBox()
            bx0 = pcbnew.ToMM(box.GetX()) - expand
            by0 = pcbnew.ToMM(box.GetY()) - expand
            bx1 = pcbnew.ToMM(box.GetX() + box.GetWidth()) + expand
            by1 = pcbnew.ToMM(box.GetY() + box.GetHeight()) + expand
            ix0 = max(0, int(math.floor((bx0 - x0) / step)))
            iy0 = max(0, int(math.floor((by0 - y0) / step)))
            ix1 = min(nx - 1, int(math.ceil((bx1 - x0) / step)))
            iy1 = min(ny - 1, int(math.ceil((by1 - y0) / step)))
            for ix in range(ix0, ix1 + 1):
                for iy in range(iy0, iy1 + 1):
                    blocked.add((ix, iy))

        blocked_by_layer = {layer: set() for layer in layers}
        for layer in layers:
            blocked = blocked_by_layer[layer]
            for item in board.GetTracks():
                if item.GetNetCode() != own and (isinstance(item, pcbnew.PCB_VIA) or item.GetLayer() == layer):
                    raster(blocked, item, 0.24)
            for footprint in board.GetFootprints():
                for pad in footprint.Pads():
                    if pad.GetNetCode() == own:
                        continue
                    try:
                        on_layer = pad.IsOnLayer(layer)
                    except AttributeError:
                        on_layer = True
                    if on_layer:
                        raster(blocked, pad, 0.24)
            for drawing in board.GetDrawings():
                if drawing.GetLayer() == pcbnew.Edge_Cuts:
                    raster(blocked, drawing, 0.45)
            for zone in board.Zones():
                if zone.GetIsRuleArea():
                    raster(blocked, zone, 0.24)

        origin = cell(start)
        target = cell(goal)
        for blocked in blocked_by_layer.values():
            for centre in (origin, target):
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        blocked.discard((centre[0] + dx, centre[1] + dy))
        via_clear = set.intersection(*(set((ix, iy) for ix in range(nx) for iy in range(ny)) - blocked
                                       for blocked in blocked_by_layer.values()))

        starts = [(index, origin[0], origin[1]) for index in range(len(layers))]
        queue = []
        cost = {}
        parent = {}
        for state in starts:
            estimate = abs(state[1] - target[0]) + abs(state[2] - target[1])
            heapq.heappush(queue, (estimate, 0.0, state))
            cost[state] = 0.0
        selected = None
        while queue:
            _estimate, current_cost, current = heapq.heappop(queue)
            if current_cost != cost.get(current):
                continue
            layer_index, ix, iy = current
            if (ix, iy) == target:
                selected = current
                break
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nxt = (layer_index, ix + dx, iy + dy)
                if not (0 <= nxt[1] < nx and 0 <= nxt[2] < ny):
                    continue
                if (nxt[1], nxt[2]) in blocked_by_layer[layers[layer_index]]:
                    continue
                next_cost = current_cost + 1.0
                if next_cost < cost.get(nxt, float("inf")):
                    cost[nxt] = next_cost
                    parent[nxt] = current
                    distance = abs(nxt[1] - target[0]) + abs(nxt[2] - target[1])
                    heapq.heappush(queue, (next_cost + distance, next_cost, nxt))
            if (ix, iy) in via_clear:
                for next_layer in range(len(layers)):
                    if next_layer == layer_index:
                        continue
                    nxt = (next_layer, ix, iy)
                    next_cost = current_cost + 40.0
                    if next_cost < cost.get(nxt, float("inf")):
                        cost[nxt] = next_cost
                        parent[nxt] = current
                        distance = abs(ix - target[0]) + abs(iy - target[1])
                        heapq.heappush(queue, (next_cost + distance, next_cost, nxt))
        if selected is None:
            raise RuntimeError(f"no multilayer route for {net_name} from {start} to {goal}")

        states = [selected]
        while states[-1] not in starts:
            states.append(parent[states[-1]])
        states.reverse()
        points = [(start[0], start[1], layers[states[0][0]])]
        for state in states[1:-1]:
            qx, qy = xy((state[1], state[2]))
            points.append((qx, qy, layers[state[0]]))
        points.append((goal[0], goal[1], layers[states[-1][0]]))

        reduced = [points[0]]
        previous_direction = None
        for point in points[1:]:
            prior = reduced[-1]
            if point[2] != prior[2]:
                reduced.append(point)
                previous_direction = None
                continue
            dx, dy = point[0] - prior[0], point[1] - prior[1]
            direction = (0 if abs(dx) < 1e-6 else int(math.copysign(1, dx)),
                         0 if abs(dy) < 1e-6 else int(math.copysign(1, dy)))
            if previous_direction == direction and len(reduced) > 1 and reduced[-2][2] == point[2]:
                reduced[-1] = point
            else:
                reduced.append(point)
                previous_direction = direction
        for first, second in zip(reduced, reduced[1:]):
            if first[2] != second[2]:
                add_via((first[0], first[1]), net_name)
                continue
            code = board.GetNetcodeFromNetname(net_name)
            track = pcbnew.PCB_TRACK(board)
            track.SetStart(pcbnew.VECTOR2I_MM(first[0], first[1]))
            track.SetEnd(pcbnew.VECTOR2I_MM(second[0], second[1]))
            track.SetWidth(pcbnew.FromMM(0.25))
            track.SetLayer(first[2])
            track.SetNetCode(code)
            board.Add(track)
        return reduced

    # These three ties are wholly inside the new low-voltage island.  The two
    # detours preserve clearance to U403's GND pads and R216's grounded end.
    # Keeping them local first lets CI distinguish their geometry from the
    # remaining long runs back to the existing 5 V, 12 V, GND and MCU copper.
    add_segment(pad_position("U403", "2"), pad_position("U403", "5"), "GND")
    u403_p3 = pad_position("U403", "3")
    u403_p6 = pad_position("U403", "6")
    add_segment(u403_p3, (301.50, 156.25), "+5V")
    add_segment((301.50, 156.25), (298.50, 156.25), "+5V")
    add_segment((298.50, 156.25), (298.50, u403_p6[1]), "+5V")
    add_segment((298.50, u403_p6[1]), u403_p6, "+5V")
    # Use already-routed landing points for the two shortest external ties:
    # the B.Cu +5 V trace beside U403 and the established GND through-via
    # below the divider.  The remaining raw-power and sense runs are kept out
    # of this narrow stage until their longer corridors are independently
    # checked.
    add_segment((298.50, u403_p6[1]), (296.50, u403_p6[1]), "+5V")
    add_segment((296.50, u403_p6[1]), (296.50, 146.63), "+5V")
    add_segment((296.50, 146.63), (299.73, 146.63), "+5V")
    # The obsolete bypass left a filtered-5-V endpoint on F.Cu.  Let the
    # candidate router find a B.Cu corridor around the existing +5-V spine,
    # then use one compliant via at the endpoint.
    u403_p1 = pad_position("U403", "1")
    raw_endpoint = (307.2346, 134.89)
    raw_path = route_b_cu(u403_p1, raw_endpoint, "/PSU/5V_SW", (280.0, 120.0, 330.0, 160.0))
    add_via(raw_endpoint, "/PSU/5V_SW")

    # Put the divider at the isolated end of GPIO4's proven legacy corridor,
    # immediately above the existing raw +12 V B.Cu bus.  This avoids all new
    # through-vias in the dense ESP32 fanout.
    r215_p2 = pad_position("R215", "2")
    r215_p1 = pad_position("R215", "1")
    r216_p1 = pad_position("R216", "1")
    r216_p2 = pad_position("R216", "2")
    routing_failures: list[str] = []
    legacy_sense_escape = (207.490, 131.970)
    add_via(r215_p2, SENSE)
    try:
        sense_route = route_multilayer(
            legacy_sense_escape, r215_p2, SENSE, (62.0, 122.50, 335.0, 164.0)
        )
        sense_path = [(x, y) for x, y, _layer in sense_route]
        sense_layer = ",".join(board.GetLayerName(layer) for _x, _y, layer in sense_route)
    except RuntimeError as exc:
        sense_path = []
        sense_layer = -1
        routing_failures.append(str(exc))
    local_sense_path = [r215_p2, (r215_p2[0], 157.00), (r216_p1[0], 157.00), r216_p1]
    for first, second in zip(local_sense_path, local_sense_path[1:]):
        add_segment(first, second, SENSE)
    plus12_endpoint = (r215_p1[0], 163.10)
    plus12_path = [r215_p1, plus12_endpoint]
    add_segment(r215_p1, plus12_endpoint, "+12V")
    plus12_layer = pcbnew.B_Cu
    plus12_bottom_path = plus12_path
    ground_bottom_path = []
    ground_path = []
    ground_layer = pcbnew.B_Cu

    board.BuildConnectivity()
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(args.output), board)
    print("POWER_STAGE_OK", args.output)
    print("REMOVED_BYPASS_TRACKS", removed_bypass_tracks)
    print("REMOVED_GPIO4_TRACKS", removed_gpio4_tracks)
    print("RAW_ROUTE_POINTS", " ".join(f"{x:.2f},{y:.2f}" for x, y in raw_path))
    print("LOCAL_SENSE_ROUTE_POINTS", " ".join(f"{x:.2f},{y:.2f}" for x, y in local_sense_path))
    print("GPIO_FRONT_ROUTE_POINTS", "reused-source-corridor")
    print("SENSE_BOTTOM_ROUTE_POINTS", "reused-source-corridor")
    print("SENSE_ROUTE_POINTS", " ".join(f"{x:.2f},{y:.2f}" for x, y in sense_path))
    print("SENSE_ROUTE_LAYER", sense_layer)
    print("PLUS12_ROUTE_POINTS", " ".join(f"{x:.2f},{y:.2f}" for x, y in plus12_path))
    print("PLUS12_ROUTE_LAYER", plus12_layer)
    print("PLUS12_BOTTOM_ROUTE_POINTS", " ".join(f"{x:.2f},{y:.2f}" for x, y in plus12_bottom_path))
    print("GROUND_ROUTE_POINTS", " ".join(f"{x:.2f},{y:.2f}" for x, y in ground_path))
    print("GROUND_ROUTE_LAYER", ground_layer)
    print("GROUND_BOTTOM_ROUTE_POINTS", " ".join(f"{x:.2f},{y:.2f}" for x, y in ground_bottom_path))
    print("ROUTE_STUDY_FAILURES", " | ".join(routing_failures))


if __name__ == "__main__":
    main()
