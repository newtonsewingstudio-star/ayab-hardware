#!/usr/bin/env python3
"""Migrate the AYAB-ESP32 PCB Hall section to the KH910 Rev A architecture.

This script uses KiCad's native pcbnew object model. It removes the obsolete
LM393-only footprints, repurposes four existing 0603 locations as the two
10k/10k Hall ADC dividers, detaches the old U701 comparator routes, and reuses
the MCU-side copper corridors for HALL_L_ADC and HALL_R_ADC.

The caller must run KiCad DRC on the output before replacing the repository
board. Structural assertions are intentionally strict and fail closed.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import pcbnew

RAW_L = "/BROTHER-CONNECTORS/EOL_L"
RAW_R = "/BROTHER-CONNECTORS/EOL_R"
OLD_LP = "/ESP32/EOL_L_P"
OLD_LN = "/ESP32/EOL_L_N"
ADC_L = "/ESP32/HALL_L_ADC"
ADC_R = "/ESP32/HALL_R_ADC"
GND = "GND"

STRICT_REMOVE = {
    "C703", "C704", "U702", "U703",
    *(f"R{n}" for n in range(715, 731)),
}

REPURPOSE = {
    "R731": ("R735", {"1": RAW_L, "2": ADC_L}),
    "R733": ("R736", {"1": ADC_L, "2": GND}),
    "R732": ("R737", {"1": RAW_R, "2": ADC_R}),
    "R734": ("R738", {"1": ADC_R, "2": GND}),
}

CORRIDORS = {OLD_LP: ADC_L, OLD_LN: ADC_R}
LEFT_JOIN = (215.127, 155.057)
RIGHT_JOIN = (212.587, 157.597)
LEFT_ADC_VIA = (91.788, 139.878)
RIGHT_ADC_VIA = (313.895, 158.075)

LEFT_ROUTE = [
    LEFT_ADC_VIA,
    (105.000, 145.000),
    (155.000, 149.000),
    (200.000, 153.500),
    LEFT_JOIN,
]
RIGHT_ROUTE = [
    RIGHT_ADC_VIA,
    (285.000, 158.400),
    (250.000, 158.400),
    (220.000, 158.000),
    RIGHT_JOIN,
]

LEFT_GND_PAD = (90.138, 140.653)
LEFT_GND_VIA = (91.050, 141.565)
RIGHT_GND_PAD = (313.120, 156.425)
RIGHT_GND_VIA = (312.200, 157.345)


def pt(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


def xy(p: pcbnew.VECTOR2I) -> tuple[float, float]:
    return (round(pcbnew.ToMM(p.x), 3), round(pcbnew.ToMM(p.y), 3))


def same_xy(a: pcbnew.VECTOR2I, b: tuple[float, float], tol: float = 0.002) -> bool:
    ax, ay = xy(a)
    return abs(ax - b[0]) <= tol and abs(ay - b[1]) <= tol


def footprints(board: pcbnew.BOARD) -> dict[str, pcbnew.FOOTPRINT]:
    return {fp.GetReference(): fp for fp in board.GetFootprints()}


def get_pad(fp: pcbnew.FOOTPRINT, number: str) -> pcbnew.PAD:
    pads = fp.Pads()
    for pad in pads:
        if str(pad.GetNumber()) == number:
            return pad
    raise RuntimeError(f"{fp.GetReference()} missing pad {number}")


def get_or_add_net(board: pcbnew.BOARD, name: str) -> pcbnew.NETINFO_ITEM:
    try:
        return board.GetNetsByName()[name]
    except Exception:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        return net


def track_endpoints(item) -> tuple[tuple[float, float], tuple[float, float]]:
    return xy(item.GetStart()), xy(item.GetEnd())


def item_touches(item, coord: tuple[float, float]) -> bool:
    return hasattr(item, "GetStart") and (
        same_xy(item.GetStart(), coord) or same_xy(item.GetEnd(), coord)
    )


def add_track(board, net, start, end, layer, width_mm=0.20):
    tr = pcbnew.PCB_TRACK(board)
    tr.SetStart(pt(*start))
    tr.SetEnd(pt(*end))
    tr.SetWidth(pcbnew.FromMM(width_mm))
    tr.SetLayer(layer)
    tr.SetNet(net)
    board.Add(tr)
    return tr


def add_polyline(board, net, points, layer, width_mm=0.20):
    for a, b in zip(points, points[1:]):
        add_track(board, net, a, b, layer, width_mm)


def add_via(board, net, coord, diameter_mm=0.60, drill_mm=0.30):
    via = pcbnew.PCB_VIA(board)
    via.SetPosition(pt(*coord))
    via.SetWidth(pcbnew.FromMM(diameter_mm))
    via.SetDrill(pcbnew.FromMM(drill_mm))
    via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    via.SetNet(net)
    board.Add(via)
    return via


def remove_changed_pad_copper(board, fp, pad_number, new_net_name):
    pad = get_pad(fp, pad_number)
    old_net = pad.GetNetname()
    if old_net == new_net_name:
        return 0
    pos = xy(pad.GetPosition())
    removed = 0
    for item in list(board.GetTracks()):
        if item.GetNetname() == old_net and item_touches(item, pos):
            board.Remove(item)
            removed += 1
    return removed


def remove_orphan_net_copper(board):
    pad_counts: dict[str, int] = {}
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            name = pad.GetNetname()
            if name:
                pad_counts[name] = pad_counts.get(name, 0) + 1
    removed = 0
    for item in list(board.GetTracks()):
        name = item.GetNetname()
        if name and pad_counts.get(name, 0) == 0:
            board.Remove(item)
            removed += 1
    return removed


def migrate(infile: Path, outfile: Path) -> None:
    board = pcbnew.LoadBoard(str(infile))
    fps = footprints(board)

    missing = sorted((STRICT_REMOVE | set(REPURPOSE)) - set(fps))
    if missing:
        raise RuntimeError(f"baseline mismatch; expected footprints missing: {', '.join(missing)}")
    if any(ref in fps for ref in ("R735", "R736", "R737", "R738")):
        raise RuntimeError("board already contains R735-R738; refusing non-idempotent migration")

    if "U201" not in fps or "U701" not in fps:
        raise RuntimeError("expected U201/U701 missing")
    if get_pad(fps["U201"], "5").GetNetname() != OLD_LP or get_pad(fps["U201"], "6").GetNetname() != OLD_LN:
        raise RuntimeError("U201 pad5/pad6 baseline does not match audited legacy nets")

    # Adding NETINFO_ITEM objects can invalidate SWIG wrappers captured before
    # the board mutation. Create/retrieve the nets first, then reacquire every
    # footprint handle used below.
    for name in (RAW_L, RAW_R, GND, ADC_L, ADC_R):
        get_or_add_net(board, name)
    fps = footprints(board)
    u201 = fps["U201"]
    u701 = fps["U701"]
    nets = {name: board.GetNetsByName()[name] for name in (RAW_L, RAW_R, GND, ADC_L, ADC_R)}

    changed_copper_removed = 0
    for old_ref, (_new_ref, pad_map) in REPURPOSE.items():
        fp = fps[old_ref]
        for pad_num, new_net in pad_map.items():
            changed_copper_removed += remove_changed_pad_copper(board, fp, pad_num, new_net)

    # Reacquire after track removals as well; this avoids retaining wrappers
    # across native board container mutations.
    fps = footprints(board)
    for ref in sorted(STRICT_REMOVE):
        board.Remove(fps[ref])

    fps = footprints(board)
    for old_ref, (new_ref, pad_map) in REPURPOSE.items():
        fp = fps[old_ref]
        fp.SetReference(new_ref)
        fp.SetValue("10k")
        for pad_num, new_net_name in pad_map.items():
            get_pad(fp, pad_num).SetNet(nets[new_net_name])

    # Reacquire MCU handles after footprint removals/renames.
    fps = footprints(board)
    u201 = fps["U201"]
    u701 = fps["U701"]

    corridor_counts: dict[str, int] = {}
    removed_u701_branches = 0
    for old_name, new_name in CORRIDORS.items():
        new_net = nets[new_name]
        kept = 0
        for item in list(board.GetTracks()):
            if item.GetNetname() != old_name:
                continue
            if item.GetLayer() == pcbnew.F_Cu and hasattr(item, "GetStart"):
                s, e = track_endpoints(item)
                if max(s[1], e[1]) > 150.0:
                    board.Remove(item)
                    removed_u701_branches += 1
                    continue
            item.SetNet(new_net)
            kept += 1
        corridor_counts[new_name] = kept

    # Reacquire after route mutations before touching pads again.
    fps = footprints(board)
    u201 = fps["U201"]
    u701 = fps["U701"]
    get_pad(u201, "5").SetNet(nets[ADC_L])
    get_pad(u201, "6").SetNet(nets[ADC_R])

    add_track(board, nets[ADC_L], (91.788, 139.103), (91.788, 140.653), pcbnew.F_Cu, 0.20)
    add_via(board, nets[ADC_L], LEFT_ADC_VIA)
    add_track(board, nets[ADC_R], (314.670, 158.075), (313.120, 158.075), pcbnew.F_Cu, 0.20)
    add_via(board, nets[ADC_R], RIGHT_ADC_VIA)
    add_polyline(board, nets[ADC_L], LEFT_ROUTE, pcbnew.B_Cu, 0.20)
    add_polyline(board, nets[ADC_R], RIGHT_ROUTE, pcbnew.B_Cu, 0.20)

    add_track(board, nets[GND], LEFT_GND_PAD, LEFT_GND_VIA, pcbnew.F_Cu, 0.25)
    add_via(board, nets[GND], LEFT_GND_VIA, 0.60, 0.30)
    add_track(board, nets[GND], RIGHT_GND_PAD, RIGHT_GND_VIA, pcbnew.F_Cu, 0.25)
    add_via(board, nets[GND], RIGHT_GND_VIA, 0.60, 0.30)

    orphan_removed = remove_orphan_net_copper(board)
    board.RemoveUnusedNets()

    fps = footprints(board)
    if STRICT_REMOVE & set(fps):
        raise RuntimeError(f"obsolete footprints remain: {sorted(STRICT_REMOVE & set(fps))}")
    for ref in ("R735", "R736", "R737", "R738"):
        if ref not in fps or fps[ref].GetValue() != "10k":
            raise RuntimeError(f"divider footprint invalid: {ref}")

    expected = {
        "R735": {"1": RAW_L, "2": ADC_L},
        "R736": {"1": ADC_L, "2": GND},
        "R737": {"1": RAW_R, "2": ADC_R},
        "R738": {"1": ADC_R, "2": GND},
    }
    for ref, pad_map in expected.items():
        for pad_num, netname in pad_map.items():
            actual = get_pad(fps[ref], pad_num).GetNetname()
            if actual != netname:
                raise RuntimeError(f"{ref}.{pad_num}: expected {netname}, found {actual}")

    u201 = fps["U201"]
    u701 = fps["U701"]
    if get_pad(u201, "5").GetNetname() != ADC_L or get_pad(u201, "6").GetNetname() != ADC_R:
        raise RuntimeError("U201 Hall ADC pad migration failed")
    if any(get_pad(u701, p).GetNetname() in (ADC_L, ADC_R) for p in ("17", "18")):
        raise RuntimeError("U701 remains electrically attached to Hall ADC nets")
    if corridor_counts.get(ADC_L, 0) < 5 or corridor_counts.get(ADC_R, 0) < 5:
        raise RuntimeError(f"unexpectedly short retained corridors: {corridor_counts}")

    try:
        pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    except Exception as exc:
        print(f"ZONE_FILL_WARNING {exc!r}")

    pcbnew.SaveBoard(str(outfile), board)
    print("MIGRATION_OK")
    print("OUTPUT", outfile)
    print("CHANGED_PAD_COPPER_REMOVED", changed_copper_removed)
    print("U701_BRANCH_ITEMS_REMOVED", removed_u701_branches)
    print("ORPHAN_NET_ITEMS_REMOVED", orphan_removed)
    print("CORRIDOR_COUNTS", corridor_counts)
    print("FOOTPRINTS", len(list(board.GetFootprints())))
    print("NETS", board.GetNetCount())


def validate(boardfile: Path) -> None:
    board = pcbnew.LoadBoard(str(boardfile))
    fps = footprints(board)
    for ref in ("R735", "R736", "R737", "R738"):
        if ref not in fps:
            raise RuntimeError(f"missing {ref}")
    if STRICT_REMOVE & set(fps):
        raise RuntimeError(f"obsolete footprints remain: {sorted(STRICT_REMOVE & set(fps))}")
    u201 = fps["U201"]
    if get_pad(u201, "5").GetNetname() != ADC_L:
        raise RuntimeError("U201.5 is not HALL_L_ADC")
    if get_pad(u201, "6").GetNetname() != ADC_R:
        raise RuntimeError("U201.6 is not HALL_R_ADC")
    for name in (ADC_L, ADC_R):
        items = [i for i in board.GetTracks() if i.GetNetname() == name]
        if len(items) < 8:
            raise RuntimeError(f"{name} has too little routed copper: {len(items)} items")
    print("VALIDATION_OK", boardfile)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path, nargs="?")
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()
    if args.validate:
        validate(args.input)
    else:
        if args.output is None:
            ap.error("output is required unless --validate is used")
        migrate(args.input, args.output)


if __name__ == "__main__":
    main()
