#!/usr/bin/env python3
"""Deterministically migrate the KH910 Rev A Hall section in a serialized KiCad PCB.

Why serialized editing?
KiCad 9's legacy pcbnew/SWIG Python wrappers intermittently expose footprint
pads as raw SwigPyObject instances after board mutations.  This tool edits only
balanced KiCad S-expression blocks that were explicitly audited on the Rev A
branch, preserves all unrelated board text verbatim, and relies on kicad-cli
DRC as the final authority before any repository board is committed.

The migration is intentionally fail-closed.  If the audited references, pad
nets, corridor counts, or coordinates differ, no output is written.
"""

from __future__ import annotations

import argparse
import math
import re
import uuid
from dataclasses import dataclass
from pathlib import Path

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

# old reference -> (new reference, pad-number -> new net name)
REPURPOSE = {
    "R731": ("R735", {"1": RAW_L, "2": ADC_L}),
    "R733": ("R736", {"1": ADC_L, "2": GND}),
    "R732": ("R737", {"1": RAW_R, "2": ADC_R}),
    "R734": ("R738", {"1": ADC_R, "2": GND}),
}

# Audited legacy net IDs on the current Rev A board.  We still resolve names
# dynamically and assert these values rather than silently relying on them.
AUDITED_NET_IDS = {
    GND: 2,
    OLD_LP: 26,
    OLD_LN: 27,
    RAW_L: 63,
    RAW_R: 64,
}

# Audited global pad coordinates (mm).  These catch rotation/placement mistakes
# before any copper is generated.
AUDITED_PAD_XY = {
    ("R731", "1"): (90.1378, 139.1030),
    ("R731", "2"): (91.7878, 139.1030),
    ("R733", "1"): (91.7878, 140.6530),
    ("R733", "2"): (90.1378, 140.6530),
    ("R732", "1"): (314.6700, 158.0750),
    ("R732", "2"): (314.6700, 156.4250),
    ("R734", "1"): (313.1200, 156.4250),
    ("R734", "2"): (313.1200, 158.0750),
    ("U201", "5"): (217.1250, 127.1250),
    ("U201", "6"): (217.1250, 127.9750),
    ("U701", "17"): (197.2025, 158.5050),
    ("U701", "18"): (197.2025, 157.8550),
}

# Divider copper.  Note the right divider is at y=156.425; the earlier SWIG
# prototype incorrectly used the y=158.075 raw/GND row.  This file encodes the
# audited, corrected pad geometry.
LEFT_ADC_A = AUDITED_PAD_XY[("R731", "2")]
LEFT_ADC_B = AUDITED_PAD_XY[("R733", "1")]
LEFT_ADC_VIA = (91.7878, 139.8780)
LEFT_GND_PAD = AUDITED_PAD_XY[("R733", "2")]
LEFT_GND_VIA = (91.0500, 141.5650)

RIGHT_ADC_A = AUDITED_PAD_XY[("R732", "2")]
RIGHT_ADC_B = AUDITED_PAD_XY[("R734", "1")]
RIGHT_ADC_VIA = (313.8950, 156.4250)
RIGHT_GND_PAD = AUDITED_PAD_XY[("R734", "2")]
RIGHT_GND_VIA = (312.2000, 158.9950)

LEFT_JOIN = (215.127498, 155.0574)
RIGHT_JOIN = (212.587498, 157.5974)

# First-pass B.Cu routes.  kicad-cli DRC is required to approve them; these are
# never committed merely because the transformer can serialize them.
LEFT_ROUTE = [
    LEFT_ADC_VIA,
    (105.0000, 145.0000),
    (155.0000, 149.0000),
    (200.0000, 153.5000),
    LEFT_JOIN,
]
RIGHT_ROUTE = [
    RIGHT_ADC_VIA,
    (285.0000, 156.7000),
    (250.0000, 157.0000),
    (220.0000, 157.3000),
    RIGHT_JOIN,
]


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    head: str


def _scan_children(text: str, outer_start: int) -> list[Span]:
    """Return direct child S-expression spans inside the expression at outer_start."""
    if text[outer_start] != "(":
        raise ValueError("outer_start must point at '('")
    depth = 0
    in_string = False
    escaped = False
    child_start = None
    out: list[Span] = []
    i = outer_start
    while i < len(text):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            i += 1
            continue
        if ch == "(":
            depth += 1
            if depth == 2:
                child_start = i
        elif ch == ")":
            if depth == 2 and child_start is not None:
                block = text[child_start:i + 1]
                m = re.match(r"\(\s*([^\s()]+)", block)
                out.append(Span(child_start, i + 1, m.group(1) if m else ""))
                child_start = None
            depth -= 1
            if depth == 0:
                return out
        i += 1
    raise RuntimeError("unterminated S-expression")


def root_start(text: str) -> int:
    p = text.find("(kicad_pcb")
    if p < 0:
        raise RuntimeError("not a kicad_pcb file")
    return p


def root_children(text: str) -> list[Span]:
    return _scan_children(text, root_start(text))


def expr_head(block: str) -> str:
    m = re.match(r"\(\s*([^\s()]+)", block)
    return m.group(1) if m else ""


def parse_net_definition(block: str):
    m = re.fullmatch(r'\(net\s+(\d+)\s+"((?:\\.|[^"\\])*)"\s*\)', block.strip(), re.S)
    return (int(m.group(1)), m.group(2)) if m else None


def reference(block: str) -> str | None:
    m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
    return m.group(1) if m else None


def value(block: str) -> str | None:
    m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', block)
    return m.group(1) if m else None


def footprint_at(block: str) -> tuple[float, float, float]:
    # (at ...) is a direct footprint child; use direct children to avoid property at's.
    for s in _scan_children(block, 0):
        if s.head != "at":
            continue
        m = re.match(r"\(at\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)(?:\s+([-+0-9.eE]+))?", block[s.start:s.end])
        if m:
            return float(m.group(1)), float(m.group(2)), float(m.group(3) or 0.0)
    raise RuntimeError(f"footprint {reference(block)} missing direct at")


def pad_number(block: str) -> str | None:
    m = re.match(r'\(pad\s+"([^"]+)"', block)
    return m.group(1) if m else None


def pad_local_at(block: str) -> tuple[float, float]:
    for s in _scan_children(block, 0):
        if s.head != "at":
            continue
        m = re.match(r"\(at\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)", block[s.start:s.end])
        if m:
            return float(m.group(1)), float(m.group(2))
    return (0.0, 0.0)


def pad_global_xy(footprint: str, pad: str) -> tuple[float, float]:
    fx, fy, deg = footprint_at(footprint)
    px, py = pad_local_at(pad)
    r = math.radians(deg)
    gx = fx + px * math.cos(r) - py * math.sin(r)
    gy = fy + px * math.sin(r) + py * math.cos(r)
    return round(gx, 6), round(gy, 6)


def pad_net(block: str) -> tuple[int, str] | None:
    m = re.search(r'\(net\s+(\d+)\s+"([^"]+)"\)', block)
    return (int(m.group(1)), m.group(2)) if m else None


def direct_pad_blocks(footprint: str) -> dict[str, str]:
    out = {}
    for s in _scan_children(footprint, 0):
        if s.head != "pad":
            continue
        b = footprint[s.start:s.end]
        n = pad_number(b)
        if n is not None:
            out[n] = b
    return out


def replace_direct_children(block: str, replacements: dict[tuple[int, int], str], removals: set[tuple[int, int]] | None = None) -> str:
    removals = removals or set()
    edits = [(a, b, "") for a, b in removals]
    edits.extend((a, b, new) for (a, b), new in replacements.items())
    for a, b, new in sorted(edits, reverse=True):
        block = block[:a] + new + block[b:]
    return block


def replace_property(block: str, prop_name: str, new_value: str) -> str:
    children = _scan_children(block, 0)
    for s in children:
        if s.head != "property":
            continue
        pb = block[s.start:s.end]
        m = re.match(r'\(property\s+"([^"]+)"\s+"([^"]*)"', pb)
        if m and m.group(1) == prop_name:
            new_pb = pb[:m.start(2)] + new_value + pb[m.end(2):]
            return block[:s.start] + new_pb + block[s.end:]
    raise RuntimeError(f"{reference(block)} missing property {prop_name}")


def replace_pad_net_in_footprint(footprint: str, number: str, net_id: int, net_name: str) -> str:
    children = _scan_children(footprint, 0)
    for s in children:
        if s.head != "pad":
            continue
        pb = footprint[s.start:s.end]
        if pad_number(pb) != number:
            continue
        old = pad_net(pb)
        if old is None:
            raise RuntimeError(f"{reference(footprint)} pad {number} has no net")
        new_pb, n = re.subn(
            r'\(net\s+\d+\s+"[^"]+"\)',
            f'(net {net_id} "{net_name}")',
            pb,
            count=1,
        )
        if n != 1:
            raise RuntimeError(f"failed net replacement on {reference(footprint)} pad {number}")
        return footprint[:s.start] + new_pb + footprint[s.end:]
    raise RuntimeError(f"{reference(footprint)} missing pad {number}")


def item_net_id(block: str) -> int | None:
    m = re.search(r"\(net\s+(\d+)\s*\)", block)
    return int(m.group(1)) if m else None


def item_layer(block: str) -> str | None:
    m = re.search(r'\(layer\s+"([^"]+)"\)', block)
    return m.group(1) if m else None


def item_points(block: str) -> list[tuple[float, float]]:
    pts = []
    for tag in ("start", "end", "at"):
        for m in re.finditer(rf"\({tag}\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)", block):
            pts.append((float(m.group(1)), float(m.group(2))))
    return pts


def near(a: tuple[float, float], b: tuple[float, float], tol: float = 0.002) -> bool:
    return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol


def item_touches(block: str, xy: tuple[float, float]) -> bool:
    return any(near(p, xy) for p in item_points(block))


def replace_item_net(block: str, net_id: int) -> str:
    new, n = re.subn(r"\(net\s+\d+\s*\)", f"(net {net_id})", block, count=1)
    if n != 1:
        raise RuntimeError("copper item has no replaceable net")
    return new


def fmt(v: float) -> str:
    s = f"{v:.6f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def new_uuid(label: str) -> str:
    # Stable IDs make reruns/diffs deterministic.
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"ayab-kh910-rev-a:{label}"))


def segment(a, b, layer: str, net_id: int, label: str, width: float = 0.20) -> str:
    return (
        "(segment\n"
        f"\t\t(start {fmt(a[0])} {fmt(a[1])})\n"
        f"\t\t(end {fmt(b[0])} {fmt(b[1])})\n"
        f"\t\t(width {fmt(width)})\n"
        f"\t\t(layer \"{layer}\")\n"
        f"\t\t(net {net_id})\n"
        f"\t\t(uuid \"{new_uuid(label)}\")\n"
        "\t)"
    )


def via(p, net_id: int, label: str, size: float = 0.60, drill: float = 0.30) -> str:
    return (
        "(via\n"
        f"\t\t(at {fmt(p[0])} {fmt(p[1])})\n"
        f"\t\t(size {fmt(size)})\n"
        f"\t\t(drill {fmt(drill)})\n"
        "\t\t(layers \"F.Cu\" \"B.Cu\")\n"
        f"\t\t(net {net_id})\n"
        f"\t\t(uuid \"{new_uuid(label)}\")\n"
        "\t)"
    )


def polyline(points, layer: str, net_id: int, prefix: str, width: float = 0.20) -> list[str]:
    return [segment(a, b, layer, net_id, f"{prefix}-{i}", width) for i, (a, b) in enumerate(zip(points, points[1:]), 1)]


def audit_baseline(text: str):
    children = root_children(text)
    nets: dict[str, int] = {}
    footprints: dict[str, str] = {}
    for s in children:
        b = text[s.start:s.end]
        if s.head == "net":
            n = parse_net_definition(b)
            if n:
                nets[n[1]] = n[0]
        elif s.head == "footprint":
            ref = reference(b)
            if ref:
                footprints[ref] = b

    for name, expected_id in AUDITED_NET_IDS.items():
        actual = nets.get(name)
        if actual != expected_id:
            raise RuntimeError(f"baseline net {name}: expected id {expected_id}, found {actual}")
    if ADC_L in nets or ADC_R in nets:
        raise RuntimeError("Hall ADC nets already exist; refusing non-idempotent migration")

    expected_refs = STRICT_REMOVE | set(REPURPOSE) | {"U201", "U701"}
    missing = expected_refs - set(footprints)
    if missing:
        raise RuntimeError(f"baseline footprints missing: {sorted(missing)}")
    if any(r in footprints for r in ("R735", "R736", "R737", "R738")):
        raise RuntimeError("R735-R738 already present")

    expected_pad_nets = {
        ("R731", "1"): RAW_L, ("R731", "2"): GND,
        ("R733", "1"): P5,    ("R733", "2"): RAW_L,
        ("R732", "1"): RAW_R, ("R732", "2"): GND,
        ("R734", "1"): P5,    ("R734", "2"): RAW_R,
        ("U201", "5"): OLD_LP, ("U201", "6"): OLD_LN,
        ("U701", "17"): OLD_LN, ("U701", "18"): OLD_LP,
    }
    for (ref, pn), net_name in expected_pad_nets.items():
        pb = direct_pad_blocks(footprints[ref]).get(pn)
        if pb is None:
            raise RuntimeError(f"{ref} missing pad {pn}")
        actual = pad_net(pb)
        if actual is None or actual[1] != net_name:
            raise RuntimeError(f"{ref}.{pn}: expected {net_name}, found {actual}")
        actual_xy = pad_global_xy(footprints[ref], pb)
        expected_xy = AUDITED_PAD_XY[(ref, pn)]
        if not near(actual_xy, expected_xy, 0.003):
            raise RuntimeError(f"{ref}.{pn}: expected xy {expected_xy}, found {actual_xy}")

    corridor_counts = {OLD_LP: 0, OLD_LN: 0}
    branch_counts = {OLD_LP: 0, OLD_LN: 0}
    for s in children:
        if s.head not in {"segment", "via", "arc"}:
            continue
        b = text[s.start:s.end]
        nid = item_net_id(b)
        if nid == nets[OLD_LP]:
            corridor_counts[OLD_LP] += 1
            if s.head == "segment" and item_layer(b) == "F.Cu" and max(y for _x, y in item_points(b)) > 150.0:
                branch_counts[OLD_LP] += 1
        elif nid == nets[OLD_LN]:
            corridor_counts[OLD_LN] += 1
            if s.head == "segment" and item_layer(b) == "F.Cu" and max(y for _x, y in item_points(b)) > 150.0:
                branch_counts[OLD_LN] += 1
    if corridor_counts != {OLD_LP: 12, OLD_LN: 14}:
        raise RuntimeError(f"legacy corridor count mismatch: {corridor_counts}")
    if branch_counts != {OLD_LP: 4, OLD_LN: 2}:
        raise RuntimeError(f"U701 branch count mismatch: {branch_counts}")

    return children, nets, footprints


def migrate(infile: Path, outfile: Path) -> None:
    text = infile.read_text(encoding="utf-8")
    children, nets, footprints = audit_baseline(text)

    max_net_id = max(nets.values())
    adc_ids = {ADC_L: max_net_id + 1, ADC_R: max_net_id + 2}

    edits: list[tuple[int, int, str]] = []
    last_net_end = None
    changed_pad_old = {
        AUDITED_PAD_XY[("R731", "2")]: nets[GND],
        AUDITED_PAD_XY[("R733", "1")]: nets[P5],
        AUDITED_PAD_XY[("R733", "2")]: nets[RAW_L],
        AUDITED_PAD_XY[("R732", "2")]: nets[GND],
        AUDITED_PAD_XY[("R734", "1")]: nets[P5],
        AUDITED_PAD_XY[("R734", "2")]: nets[RAW_R],
    }
    removed_changed_pad_copper = 0
    removed_u701_branches = {OLD_LP: 0, OLD_LN: 0}
    reassigned_corridor = {OLD_LP: 0, OLD_LN: 0}

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
                for pn, net_name in pad_map.items():
                    net_id = adc_ids.get(net_name, nets[net_name])
                    nb = replace_pad_net_in_footprint(nb, pn, net_id, net_name)
                edits.append((s.start, s.end, nb))
                continue
            if ref == "U201":
                nb = replace_pad_net_in_footprint(b, "5", adc_ids[ADC_L], ADC_L)
                nb = replace_pad_net_in_footprint(nb, "6", adc_ids[ADC_R], ADC_R)
                edits.append((s.start, s.end, nb))
                continue

        if s.head in {"segment", "via", "arc"}:
            nid = item_net_id(b)
            # Remove copper from pads whose electrical role changes.  Only an
            # item on the pad's OLD net is eligible, preventing broad deletion.
            remove_for_pad = False
            for pxy, old_nid in changed_pad_old.items():
                if nid == old_nid and item_touches(b, pxy):
                    remove_for_pad = True
                    break
            if remove_for_pad:
                edits.append((s.start, s.end, ""))
                removed_changed_pad_copper += 1
                continue

            old_name = OLD_LP if nid == nets[OLD_LP] else OLD_LN if nid == nets[OLD_LN] else None
            if old_name:
                if s.head == "segment" and item_layer(b) == "F.Cu" and max(y for _x, y in item_points(b)) > 150.0:
                    edits.append((s.start, s.end, ""))
                    removed_u701_branches[old_name] += 1
                else:
                    new_id = adc_ids[ADC_L if old_name == OLD_LP else ADC_R]
                    edits.append((s.start, s.end, replace_item_net(b, new_id)))
                    reassigned_corridor[old_name] += 1

    if last_net_end is None:
        raise RuntimeError("board has no net definitions")
    if removed_u701_branches != {OLD_LP: 4, OLD_LN: 2}:
        raise RuntimeError(f"unexpected removed U701 branches: {removed_u701_branches}")
    if reassigned_corridor != {OLD_LP: 8, OLD_LN: 12}:
        raise RuntimeError(f"unexpected retained corridor counts: {reassigned_corridor}")
    if removed_changed_pad_copper < 4:
        raise RuntimeError(f"too little changed-pad copper removed: {removed_changed_pad_copper}")

    # Insert new root net definitions immediately after the existing net table.
    net_insert = (
        f'\n\t(net {adc_ids[ADC_L]} "{ADC_L}")'
        f'\n\t(net {adc_ids[ADC_R]} "{ADC_R}")'
    )
    edits.append((last_net_end, last_net_end, net_insert))

    # Add new divider and route copper just before the root closing paren.
    root_pos = root_start(text)
    root_end = None
    depth = 0
    in_string = False
    escaped = False
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

    new_items = []
    # Divider midpoint copper and ADC vias.
    new_items += [segment(LEFT_ADC_A, LEFT_ADC_B, "F.Cu", adc_ids[ADC_L], "left-divider-adc")]
    new_items += [via(LEFT_ADC_VIA, adc_ids[ADC_L], "left-adc-via")]
    new_items += [segment(RIGHT_ADC_A, RIGHT_ADC_B, "F.Cu", adc_ids[ADC_R], "right-divider-adc")]
    new_items += [via(RIGHT_ADC_VIA, adc_ids[ADC_R], "right-adc-via")]
    # Ground the low side of each 10k/10k divider into the GND plane.
    new_items += [segment(LEFT_GND_PAD, LEFT_GND_VIA, "F.Cu", nets[GND], "left-divider-gnd", 0.25)]
    new_items += [via(LEFT_GND_VIA, nets[GND], "left-gnd-via")]
    new_items += [segment(RIGHT_GND_PAD, RIGHT_GND_VIA, "F.Cu", nets[GND], "right-divider-gnd", 0.25)]
    new_items += [via(RIGHT_GND_VIA, nets[GND], "right-gnd-via")]
    # Long ADC routes to the retained MCU-side legacy corridors.
    new_items += polyline(LEFT_ROUTE, "B.Cu", adc_ids[ADC_L], "left-adc-route")
    new_items += polyline(RIGHT_ROUTE, "B.Cu", adc_ids[ADC_R], "right-adc-route")
    edits.append((root_end, root_end, "\n\t" + "\n\t".join(new_items) + "\n"))

    # Apply from the end so original spans remain valid.
    for a, b, repl in sorted(edits, key=lambda e: (e[0], e[1]), reverse=True):
        text = text[:a] + repl + text[b:]

    validate_text(text, migrated=True)
    outfile.write_text(text, encoding="utf-8")
    print("SERIALIZED_MIGRATION_OK")
    print("OUTPUT", outfile)
    print("ADC_NET_IDS", adc_ids)
    print("REMOVED_CHANGED_PAD_COPPER", removed_changed_pad_copper)
    print("REMOVED_U701_BRANCHES", removed_u701_branches)
    print("REASSIGNED_CORRIDOR", reassigned_corridor)


def validate_text(text: str, migrated: bool = True) -> None:
    children = root_children(text)
    nets: dict[str, int] = {}
    footprints: dict[str, str] = {}
    copper_counts: dict[int, int] = {}
    for s in children:
        b = text[s.start:s.end]
        if s.head == "net":
            n = parse_net_definition(b)
            if n:
                nets[n[1]] = n[0]
        elif s.head == "footprint":
            ref = reference(b)
            if ref:
                footprints[ref] = b
        elif s.head in {"segment", "via", "arc"}:
            nid = item_net_id(b)
            if nid is not None:
                copper_counts[nid] = copper_counts.get(nid, 0) + 1

    for name in (ADC_L, ADC_R):
        if name not in nets:
            raise RuntimeError(f"missing migrated net {name}")
    if STRICT_REMOVE & set(footprints):
        raise RuntimeError(f"obsolete footprints remain: {sorted(STRICT_REMOVE & set(footprints))}")

    expected = {
        "R735": {"1": RAW_L, "2": ADC_L},
        "R736": {"1": ADC_L, "2": GND},
        "R737": {"1": RAW_R, "2": ADC_R},
        "R738": {"1": ADC_R, "2": GND},
    }
    for ref, pad_map in expected.items():
        if ref not in footprints:
            raise RuntimeError(f"missing {ref}")
        if value(footprints[ref]) != "10k":
            raise RuntimeError(f"{ref} is not 10k")
        pads = direct_pad_blocks(footprints[ref])
        for pn, name in pad_map.items():
            actual = pad_net(pads[pn])
            if actual is None or actual[1] != name:
                raise RuntimeError(f"{ref}.{pn}: expected {name}, found {actual}")

    u201 = direct_pad_blocks(footprints["U201"])
    if pad_net(u201["5"])[1] != ADC_L or pad_net(u201["6"])[1] != ADC_R:
        raise RuntimeError("U201 Hall ADC pad migration invalid")
    u701 = direct_pad_blocks(footprints["U701"])
    if pad_net(u701["17"])[1] != OLD_LN or pad_net(u701["18"])[1] != OLD_LP:
        raise RuntimeError("U701 legacy pad isolation changed unexpectedly")

    if copper_counts.get(nets[ADC_L], 0) < 15:
        raise RuntimeError(f"HALL_L_ADC has too little copper: {copper_counts.get(nets[ADC_L], 0)}")
    if copper_counts.get(nets[ADC_R], 0) < 19:
        raise RuntimeError(f"HALL_R_ADC has too little copper: {copper_counts.get(nets[ADC_R], 0)}")


def validate_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    validate_text(text, migrated=True)
    print("SERIALIZED_VALIDATION_OK", path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path, nargs="?")
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()
    if args.validate:
        validate_file(args.input)
    else:
        if args.output is None:
            ap.error("output is required unless --validate is used")
        migrate(args.input, args.output)


if __name__ == "__main__":
    main()
