#!/usr/bin/env python3
"""Rev A Hall PCB migration v2.

Deterministic serialized migration built on the audited v1 parser helpers.
Key differences from v1:
- correct KiCad footprint rotation transform (Y-down board coordinates);
- preserve the local U701<->J701 legacy Hall-header branches, but remove the
  obsolete MCU corridors;
- remove orphan comparator-cluster copper after deleting U702/U703 and their
  support network;
- route the two new ADC signals on In1.Cu, away from the B.Cu solenoid field;
- rely on the project workflow to refill zones and require 0 DRC / 0 unconnected.
"""
from __future__ import annotations

import math
from pathlib import Path

import migrate_rev_a_hall_pcb_serialized_compat as compat

k = compat.migration
reference = compat.reference
value = compat.value
replace_property = compat.replace_property

RAW_L = "/BROTHER-CONNECTORS/EOL_L"
RAW_R = "/BROTHER-CONNECTORS/EOL_R"
OLD_LP = "/ESP32/EOL_L_P"
OLD_LN = "/ESP32/EOL_L_N"
ADC_L = "/ESP32/HALL_L_ADC"
ADC_R = "/ESP32/HALL_R_ADC"
GND = "GND"
P5 = "+5V"

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
AUDITED_NET_IDS = {GND: 2, OLD_LP: 26, OLD_LN: 27, RAW_L: 63, RAW_R: 64}

AUDITED_PAD_XY = {
    ("R731", "1"): (90.1378, 139.1030),
    ("R731", "2"): (91.7878, 139.1030),
    ("R733", "1"): (91.7878, 140.6530),
    ("R733", "2"): (90.1378, 140.6530),
    ("R732", "1"): (314.6700, 156.4250),
    ("R732", "2"): (314.6700, 158.0750),
    ("R734", "1"): (313.1200, 158.0750),
    ("R734", "2"): (313.1200, 156.4250),
    ("U201", "5"): (217.1250, 127.1250),
    ("U201", "6"): (217.1250, 127.9750),
    ("U701", "17"): (197.2025, 158.5050),
    ("U701", "18"): (197.2025, 157.8550),
}

LEFT_ADC_A = AUDITED_PAD_XY[("R731", "2")]
LEFT_ADC_B = AUDITED_PAD_XY[("R733", "1")]
LEFT_MID = (91.7878, 139.8780)
LEFT_START_VIA = (95.5000, 139.8780)
LEFT_END_VIA = (215.5000, 127.1250)

RIGHT_ADC_A = AUDITED_PAD_XY[("R732", "2")]
RIGHT_ADC_B = AUDITED_PAD_XY[("R734", "1")]
RIGHT_MID = (313.8950, 158.0750)
RIGHT_START_VIA = (309.5000, 158.0750)
RIGHT_END_VIA = (215.5000, 127.9750)

LEFT_ROUTE = [
    LEFT_START_VIA,
    (125.0000, 139.2000),
    (165.0000, 137.0000),
    (200.0000, 132.0000),
    LEFT_END_VIA,
]
RIGHT_ROUTE = [
    RIGHT_START_VIA,
    (282.0000, 151.0000),
    (250.0000, 144.0000),
    (225.0000, 134.0000),
    RIGHT_END_VIA,
]

LEFT_CLUSTER = (84.0, 94.0, 125.0, 144.0)
RIGHT_CLUSTER = (309.0, 328.0, 152.0, 160.5)
OBSOLETE_NET_TOKENS = (
    "Net-(U702", "Net-(U703", "Net-(R719", "Net-(R720",
    "Net-(R721", "Net-(R722", "/IO CONDITIONING/EOL_L_K",
    "/IO CONDITIONING/EOL_L_L",
)


def correct_pad_global_xy(footprint: str, pad: str) -> tuple[float, float]:
    fx, fy, deg = k.footprint_at(footprint)
    px, py = k.pad_local_at(pad)
    r = math.radians(deg)
    gx = fx + px * math.cos(r) + py * math.sin(r)
    gy = fy - px * math.sin(r) + py * math.cos(r)
    return round(gx, 6), round(gy, 6)


def in_box(p: tuple[float, float], box) -> bool:
    x0, x1, y0, y1 = box
    return x0 <= p[0] <= x1 and y0 <= p[1] <= y1


def all_points_in_box(block: str, box) -> bool:
    pts = k.item_points(block)
    return bool(pts) and all(in_box(p, box) for p in pts)


def audit_baseline(text: str):
    children = k.root_children(text)
    nets: dict[str, int] = {}
    footprints: dict[str, str] = {}
    for s in children:
        b = text[s.start:s.end]
        if s.head == "net":
            n = k.parse_net_definition(b)
            if n:
                nets[n[1]] = n[0]
        elif s.head == "footprint":
            ref = reference(b)
            if ref:
                footprints[ref] = b

    for name, expected in AUDITED_NET_IDS.items():
        if nets.get(name) != expected:
            raise RuntimeError(f"baseline net {name}: expected {expected}, found {nets.get(name)}")
    if ADC_L in nets or ADC_R in nets:
        raise RuntimeError("Hall ADC nets already exist; refusing non-idempotent migration")
    required = STRICT_REMOVE | set(REPURPOSE) | {"U201", "U701"}
    missing = required - set(footprints)
    if missing:
        raise RuntimeError(f"baseline footprints missing: {sorted(missing)}")

    expected_pad_nets = {
        ("R731", "1"): RAW_L, ("R731", "2"): GND,
        ("R733", "1"): P5,    ("R733", "2"): RAW_L,
        ("R732", "1"): RAW_R, ("R732", "2"): GND,
        ("R734", "1"): P5,    ("R734", "2"): RAW_R,
        ("U201", "5"): OLD_LP, ("U201", "6"): OLD_LN,
        ("U701", "17"): OLD_LN, ("U701", "18"): OLD_LP,
    }
    for (ref, pn), net_name in expected_pad_nets.items():
        pb = k.direct_pad_blocks(footprints[ref]).get(pn)
        if pb is None:
            raise RuntimeError(f"{ref} missing pad {pn}")
        actual = k.pad_net(pb)
        if actual is None or actual[1] != net_name:
            raise RuntimeError(f"{ref}.{pn}: expected {net_name}, found {actual}")
        xy = correct_pad_global_xy(footprints[ref], pb)
        if not k.near(xy, AUDITED_PAD_XY[(ref, pn)], 0.003):
            raise RuntimeError(f"{ref}.{pn}: expected xy {AUDITED_PAD_XY[(ref, pn)]}, found {xy}")

    totals = {OLD_LP: 0, OLD_LN: 0}
    branches = {OLD_LP: 0, OLD_LN: 0}
    for s in children:
        if s.head not in {"segment", "via", "arc"}:
            continue
        b = text[s.start:s.end]
        nid = k.item_net_id(b)
        old_name = OLD_LP if nid == nets[OLD_LP] else OLD_LN if nid == nets[OLD_LN] else None
        if not old_name:
            continue
        totals[old_name] += 1
        if s.head == "segment" and k.item_layer(b) == "F.Cu" and max(y for _x, y in k.item_points(b)) > 150.0:
            branches[old_name] += 1
    if totals != {OLD_LP: 12, OLD_LN: 14}:
        raise RuntimeError(f"legacy corridor count mismatch: {totals}")
    if branches != {OLD_LP: 4, OLD_LN: 2}:
        raise RuntimeError(f"legacy local branch mismatch: {branches}")
    return children, nets, footprints


def pad_seed_map(footprints: dict[str, str]):
    seeds: dict[tuple[float, float], int] = {}
    for ref in STRICT_REMOVE:
        fp = footprints[ref]
        for pb in k.direct_pad_blocks(fp).values():
            net = k.pad_net(pb)
            if net:
                seeds[correct_pad_global_xy(fp, pb)] = net[0]
    changed = [
        ("R731", "2"), ("R733", "1"), ("R733", "2"),
        ("R732", "2"), ("R734", "1"), ("R734", "2"),
    ]
    for ref, pn in changed:
        fp = footprints[ref]
        pb = k.direct_pad_blocks(fp)[pn]
        net = k.pad_net(pb)
        if net:
            seeds[correct_pad_global_xy(fp, pb)] = net[0]
    return seeds


def migrate(infile: Path, outfile: Path) -> None:
    text = infile.read_text(encoding="utf-8")
    children, nets, footprints = audit_baseline(text)
    max_net = max(nets.values())
    adc_ids = {ADC_L: max_net + 1, ADC_R: max_net + 2}
    old_id_to_name = {v: name for name, v in nets.items()}
    seeds = pad_seed_map(footprints)

    edits: list[tuple[int, int, str]] = []
    last_net_end = None
    deleted_corridor = {OLD_LP: 0, OLD_LN: 0}
    kept_branch = {OLD_LP: 0, OLD_LN: 0}
    removed_seed_copper = 0
    removed_cluster_copper = 0

    for s in children:
        b = text[s.start:s.end]
        if s.head == "net":
            last_net_end = s.end
            continue
        if s.head == "footprint":
            ref = reference(b)
            if ref in STRICT_REMOVE:
                edits.append((s.start, s.end, ""))
                continue
            if ref in REPURPOSE:
                new_ref, pad_map = REPURPOSE[ref]
                nb = replace_property(b, "Reference", new_ref)
                nb = replace_property(nb, "Value", "10k")
                for pn, name in pad_map.items():
                    nid = adc_ids[name] if name in adc_ids else nets[name]
                    nb = k.replace_pad_net_in_footprint(nb, pn, nid, name)
                edits.append((s.start, s.end, nb))
                continue
            if ref == "U201":
                nb = k.replace_pad_net_in_footprint(b, "5", adc_ids[ADC_L], ADC_L)
                nb = k.replace_pad_net_in_footprint(nb, "6", adc_ids[ADC_R], ADC_R)
                edits.append((s.start, s.end, nb))
                continue

        if s.head not in {"segment", "via", "arc"}:
            continue
        nid = k.item_net_id(b)
        if nid is None:
            continue
        old_name = OLD_LP if nid == nets[OLD_LP] else OLD_LN if nid == nets[OLD_LN] else None
        if old_name:
            is_branch = s.head == "segment" and k.item_layer(b) == "F.Cu" and max(y for _x, y in k.item_points(b)) > 150.0
            if is_branch:
                kept_branch[old_name] += 1
            else:
                edits.append((s.start, s.end, ""))
                deleted_corridor[old_name] += 1
            continue

        if any(nid == old_nid and k.item_touches(b, pxy) for pxy, old_nid in seeds.items()):
            edits.append((s.start, s.end, ""))
            removed_seed_copper += 1
            continue

        net_name = old_id_to_name.get(nid, "")
        in_cluster = all_points_in_box(b, LEFT_CLUSTER) or all_points_in_box(b, RIGHT_CLUSTER)
        if in_cluster and (
            net_name in {GND, P5}
            or any(tok in net_name for tok in OBSOLETE_NET_TOKENS)
        ):
            edits.append((s.start, s.end, ""))
            removed_cluster_copper += 1
            continue

    if last_net_end is None:
        raise RuntimeError("board has no net table")
    if kept_branch != {OLD_LP: 4, OLD_LN: 2}:
        raise RuntimeError(f"unexpected kept legacy branches: {kept_branch}")
    if deleted_corridor != {OLD_LP: 8, OLD_LN: 12}:
        raise RuntimeError(f"unexpected deleted legacy corridors: {deleted_corridor}")
    if removed_seed_copper < 10:
        raise RuntimeError(f"too little obsolete/changed-pad copper removed: {removed_seed_copper}")

    net_insert = (
        f'\n\t(net {adc_ids[ADC_L]} "{ADC_L}")'
        f'\n\t(net {adc_ids[ADC_R]} "{ADC_R}")'
    )
    edits.append((last_net_end, last_net_end, net_insert))

    root_pos = k.root_start(text)
    depth = 0
    in_string = False
    escaped = False
    root_end = None
    for i in range(root_pos, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                root_end = i
                break
    if root_end is None:
        raise RuntimeError("unterminated board root")

    new_items: list[str] = []
    new_items.append(k.segment(LEFT_ADC_A, LEFT_ADC_B, "F.Cu", adc_ids[ADC_L], "v2-left-divider"))
    new_items.append(k.segment(LEFT_MID, LEFT_START_VIA, "F.Cu", adc_ids[ADC_L], "v2-left-tap"))
    new_items.append(k.via(LEFT_START_VIA, adc_ids[ADC_L], "v2-left-start-via"))
    new_items.append(k.segment(RIGHT_ADC_A, RIGHT_ADC_B, "F.Cu", adc_ids[ADC_R], "v2-right-divider"))
    new_items.append(k.segment(RIGHT_MID, RIGHT_START_VIA, "F.Cu", adc_ids[ADC_R], "v2-right-tap"))
    new_items.append(k.via(RIGHT_START_VIA, adc_ids[ADC_R], "v2-right-start-via"))
    new_items += k.polyline(LEFT_ROUTE, "In1.Cu", adc_ids[ADC_L], "v2-left-in1")
    new_items += k.polyline(RIGHT_ROUTE, "In1.Cu", adc_ids[ADC_R], "v2-right-in1")
    new_items.append(k.via(LEFT_END_VIA, adc_ids[ADC_L], "v2-left-end-via"))
    new_items.append(k.via(RIGHT_END_VIA, adc_ids[ADC_R], "v2-right-end-via"))
    new_items.append(k.segment(LEFT_END_VIA, AUDITED_PAD_XY[("U201", "5")], "F.Cu", adc_ids[ADC_L], "v2-left-mcu"))
    new_items.append(k.segment(RIGHT_END_VIA, AUDITED_PAD_XY[("U201", "6")], "F.Cu", adc_ids[ADC_R], "v2-right-mcu"))
    edits.append((root_end, root_end, "\n\t" + "\n\t".join(new_items) + "\n"))

    for a, b, repl in sorted(edits, key=lambda e: (e[0], e[1]), reverse=True):
        text = text[:a] + repl + text[b:]

    validate_text(text)
    outfile.write_text(text, encoding="utf-8")
    print("HALL_V2_MIGRATION_OK")
    print("OUTPUT", outfile)
    print("ADC_NET_IDS", adc_ids)
    print("REMOVED_SEED_COPPER", removed_seed_copper)
    print("REMOVED_CLUSTER_COPPER", removed_cluster_copper)
    print("KEPT_U701_J701_BRANCH", kept_branch)
    print("DELETED_MCU_CORRIDOR", deleted_corridor)


def validate_text(text: str) -> None:
    children = k.root_children(text)
    nets: dict[str, int] = {}
    fps: dict[str, str] = {}
    copper_counts: dict[int, int] = {}
    old_counts = {OLD_LP: 0, OLD_LN: 0}
    for s in children:
        b = text[s.start:s.end]
        if s.head == "net":
            n = k.parse_net_definition(b)
            if n:
                nets[n[1]] = n[0]
        elif s.head == "footprint":
            r = reference(b)
            if r:
                fps[r] = b
        elif s.head in {"segment", "via", "arc"}:
            nid = k.item_net_id(b)
            if nid is not None:
                copper_counts[nid] = copper_counts.get(nid, 0) + 1

    for name in (ADC_L, ADC_R):
        if name not in nets:
            raise RuntimeError(f"missing {name}")
    if STRICT_REMOVE & set(fps):
        raise RuntimeError(f"obsolete footprints remain: {sorted(STRICT_REMOVE & set(fps))}")
    expected = {
        "R735": {"1": RAW_L, "2": ADC_L},
        "R736": {"1": ADC_L, "2": GND},
        "R737": {"1": RAW_R, "2": ADC_R},
        "R738": {"1": ADC_R, "2": GND},
    }
    for ref, pmap in expected.items():
        if ref not in fps or value(fps[ref]) != "10k":
            raise RuntimeError(f"bad/missing {ref}")
        pads = k.direct_pad_blocks(fps[ref])
        for pn, name in pmap.items():
            actual = k.pad_net(pads[pn])
            if not actual or actual[1] != name:
                raise RuntimeError(f"{ref}.{pn}: expected {name}, found {actual}")

    u201 = k.direct_pad_blocks(fps["U201"])
    if k.pad_net(u201["5"])[1] != ADC_L or k.pad_net(u201["6"])[1] != ADC_R:
        raise RuntimeError("U201 ADC pad migration invalid")
    u701 = k.direct_pad_blocks(fps["U701"])
    if k.pad_net(u701["17"])[1] != OLD_LN or k.pad_net(u701["18"])[1] != OLD_LP:
        raise RuntimeError("U701 legacy local branch net changed")

    for s in children:
        if s.head not in {"segment", "via", "arc"}:
            continue
        b = text[s.start:s.end]
        nid = k.item_net_id(b)
        if nid == nets.get(OLD_LP):
            old_counts[OLD_LP] += 1
        elif nid == nets.get(OLD_LN):
            old_counts[OLD_LN] += 1
    if old_counts != {OLD_LP: 4, OLD_LN: 2}:
        raise RuntimeError(f"legacy U701/J701 branch counts wrong: {old_counts}")
    if copper_counts.get(nets[ADC_L], 0) != 9:
        raise RuntimeError(f"HALL_L_ADC copper count {copper_counts.get(nets[ADC_L], 0)} != 9")
    if copper_counts.get(nets[ADC_R], 0) != 9:
        raise RuntimeError(f"HALL_R_ADC copper count {copper_counts.get(nets[ADC_R], 0)} != 9")


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path, nargs="?")
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()
    if args.validate:
        validate_text(args.input.read_text(encoding="utf-8"))
        print("HALL_V2_VALIDATION_OK", args.input)
    else:
        if args.output is None:
            ap.error("output required")
        migrate(args.input, args.output)

if __name__ == "__main__":
    main()
