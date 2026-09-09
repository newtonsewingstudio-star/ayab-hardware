#!/usr/bin/env python3
"""Rev A KH-910 K/L staged migration with DRC-oriented physical cleanup.

The electrical split from v3 is retained, but the physical implementation is
post-processed before routing:

- remove the obsolete machine-to-U701 branch copper left behind by the split;
- remove the now-dangling local bridge stubs;
- remove all prototype endpoint/pull-up vias and short pull-up-bank traces;
- move R213/R214 onto the real top-right board area at x=265 mm, beyond both
  the top-edge notch and the rotated J801 footprint;
- feed both pull-ups from existing +3V3 below J801 through a new local via;
- launch the two machine sides from well-spaced new vias at (267,118/120).

The companion router then uses controlled stubs and separate internal layers for
K and L. The repository PCB remains fail-closed behind topology and two DRC
gates.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import re
import sys
import tempfile

V3 = Path(__file__).with_name("migrate_rev_a_kl_pcb_stage_v3.py")
spec = importlib.util.spec_from_file_location("kh910_kl_stage_v3", V3)
if spec is None or spec.loader is None:
    raise RuntimeError("could not import K/L v3 migration")
v3 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = v3
spec.loader.exec_module(v3)
core = v3.mod

# The board has a top-edge notch ending around x=249.71 mm. J801 is rotated 90
# degrees and its physical courtyard extends to roughly x=261.45 mm. Keep the
# pull-ups to the right of both structures with comfortable assembly clearance.
R213_NEW = (265.0, 118.0)
R214_NEW = (265.0, 120.0)
R213_P1 = (264.175, 118.0)
R213_P2 = (265.825, 118.0)
R214_P1 = (264.175, 120.0)
R214_P2 = (265.825, 120.0)
# Existing +3V3 In2 segment from J801.3 ends at this point; extend from here so
# no new copper crosses J801.4 (GND) on F.Cu.
P3V3_FEED = (257.13, 122.26)
P3V3_LOCAL_VIA = (263.0, 124.0)
K_LAUNCH = (267.0, 118.0)
L_LAUNCH = (267.0, 120.0)

REMOVE_VIAS = {
    (194.71, 151.86, core.MACH_K),
    (194.71, 130.91, core.MACH_K),
    (207.5, 130.91, core.MACH_K),
    (194.98, 151.99, core.MACH_L),
    (194.98, 130.71, core.MACH_L),
    (205.5, 130.71, core.MACH_L),
    (207.5, 132.025, core.MACH_K),
    (207.5, 135.325, core.MACH_L),
    (239.22, 149.86, core.MACH_K),
    (238.43, 150.42, core.MACH_L),
}

REMOVE_SEGMENTS = {
    core.MACH_K: {
        frozenset(((208.675, 132.025), (207.5, 132.025))),
        frozenset(((239.22, 149.86), (239.11, 149.75))),
        frozenset(((239.11, 149.75), (196.82, 149.75))),
        frozenset(((196.82, 149.75), (194.71, 151.86))),
        frozenset(((239.22, 149.86), (239.22, 145.65))),
    },
    core.MACH_L: {
        frozenset(((208.675, 135.325), (207.5, 135.325))),
        frozenset(((238.43, 150.42), (238.11, 150.10))),
        frozenset(((238.11, 150.10), (196.87, 150.10))),
        frozenset(((196.87, 150.10), (194.98, 151.99))),
        frozenset(((238.45, 150.40), (238.43, 150.42))),
        frozenset(((238.45, 145.63), (238.45, 150.40))),
    },
    core.P3V3: {
        frozenset(((210.325, 132.025), (211.925, 132.025))),
        frozenset(((210.325, 135.325), (211.925, 135.325))),
    },
    core.LOCAL_K: {
        frozenset(((194.71, 157.31), (193.515, 158.505))),
    },
    core.LOCAL_L: {
        frozenset(((194.98, 157.69), (193.515, 159.155))),
    },
}


def near(a, b, tol=0.004):
    return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol


def pair_key(points):
    if len(points) < 2:
        return None
    return frozenset(((round(points[0][0], 3), round(points[0][1], 3)),
                      (round(points[-1][0], 3), round(points[-1][1], 3))))


def root_items(text: str):
    for item in core.k.root_children(text):
        yield item, text[item.start:item.end]


def via_signature(block: str, net_names_by_id: dict[int, str]):
    if not block.lstrip().startswith("(via"):
        return None
    m = re.search(r"\(at\s+([-0-9.]+)\s+([-0-9.]+)\)", block)
    n = re.search(r"\(net\s+(\d+)\)", block)
    if not m or not n:
        return None
    x, y = float(m.group(1)), float(m.group(2))
    name = net_names_by_id.get(int(n.group(1)))
    return (round(x, 6), round(y, 6), name)


def move_footprint(block: str, ref: str) -> str:
    if ref == "R213":
        new = R213_NEW
        old = r"\(at 209\.5 132\.025 180\)"
    elif ref == "R214":
        new = R214_NEW
        old = r"\(at 209\.5 135\.325 180\)"
    else:
        return block
    out, n = re.subn(old, f"(at {new[0]} {new[1]})", block, count=1)
    if n != 1:
        raise RuntimeError(f"could not move {ref} exactly once")
    return out


def postprocess(path: Path) -> None:
    # Fail closed on both geometry mistakes encountered during development.
    if R213_NEW[0] <= 262.9 or R214_NEW[0] <= 262.9:
        raise RuntimeError("K/L pull-ups must clear both top-edge notch and J801 courtyard")

    text = path.read_text(encoding="utf-8")
    children = core.k.root_children(text)
    net_names_by_id: dict[int, str] = {}
    net_ids_by_name: dict[str, int] = {}
    for item in children:
        block = text[item.start:item.end]
        if item.head == "net":
            parsed = core.k.parse_net_definition(block)
            if parsed:
                net_names_by_id[parsed[0]] = parsed[1]
                net_ids_by_name[parsed[1]] = parsed[0]

    edits = []
    removed_vias = set()
    removed_segments: dict[str, set[frozenset]] = {k: set() for k in REMOVE_SEGMENTS}
    moved = set()

    for item in children:
        block = text[item.start:item.end]
        if item.head == "footprint":
            ref = core.reference(block)
            if ref in {"R213", "R214"}:
                edits.append((item.start, item.end, move_footprint(block, ref)))
                moved.add(ref)
            continue
        if item.head == "via":
            sig = via_signature(block, net_names_by_id)
            if sig in REMOVE_VIAS:
                edits.append((item.start, item.end, ""))
                removed_vias.add(sig)
            continue
        if item.head != "segment":
            continue
        nid = core.k.item_net_id(block)
        name = net_names_by_id.get(nid)
        if name not in REMOVE_SEGMENTS:
            continue
        key = pair_key(core.k.item_points(block))
        if key in REMOVE_SEGMENTS[name]:
            edits.append((item.start, item.end, ""))
            removed_segments[name].add(key)

    if moved != {"R213", "R214"}:
        raise RuntimeError(f"pull-up move mismatch: {moved}")
    if removed_vias != REMOVE_VIAS:
        raise RuntimeError(f"via cleanup mismatch: removed={removed_vias} expected={REMOVE_VIAS}")
    for name, expected in REMOVE_SEGMENTS.items():
        if removed_segments[name] != expected:
            raise RuntimeError(f"segment cleanup mismatch for {name}: {removed_segments[name]} != {expected}")

    for start, end, repl in sorted(edits, key=lambda e: (e[0], e[1]), reverse=True):
        text = text[:start] + repl + text[end:]

    for need in (core.P3V3, core.MACH_K, core.MACH_L):
        if need not in net_ids_by_name:
            raise RuntimeError(f"missing net id for {need}")
    n3 = net_ids_by_name[core.P3V3]
    nk = net_ids_by_name[core.MACH_K]
    nl = net_ids_by_name[core.MACH_L]

    extra = [
        # Extend existing +3V3 on In2 below J801, then rise locally to F.Cu.
        core.k.segment(P3V3_FEED, (257.13, 124.0), "In2.Cu", n3, "kl-v7-3v3-down"),
        core.k.segment((257.13, 124.0), P3V3_LOCAL_VIA, "In2.Cu", n3, "kl-v7-3v3-right"),
        core.k.via(P3V3_LOCAL_VIA, n3, "kl-v7-3v3-via"),
        core.k.segment(P3V3_LOCAL_VIA, (263.0, 120.0), "F.Cu", n3, "kl-v7-3v3-rise-a"),
        core.k.segment((263.0, 120.0), R214_P1, "F.Cu", n3, "kl-v7-r214-3v3"),
        core.k.segment((263.0, 120.0), (263.0, 118.0), "F.Cu", n3, "kl-v7-3v3-rise-b"),
        core.k.segment((263.0, 118.0), R213_P1, "F.Cu", n3, "kl-v7-r213-3v3"),
        # Short machine-side stubs to well-spaced launch vias.
        core.k.segment(R213_P2, K_LAUNCH, "F.Cu", nk, "kl-v7-r213-k"),
        core.k.segment(R214_P2, L_LAUNCH, "F.Cu", nl, "kl-v7-r214-l"),
        core.k.via(K_LAUNCH, nk, "kl-v7-k-launch"),
        core.k.via(L_LAUNCH, nl, "kl-v7-l-launch"),
    ]
    rend = core.root_end(text)
    text = text[:rend] + "\n\t" + "\n\t".join(extra) + "\n" + text[rend:]
    path.write_text(text, encoding="utf-8")
    print("KL_V7_PHYSICAL_CLEANUP_OK")
    print("KL_V7_PULLUPS", R213_NEW, R214_NEW)
    print("KL_V7_LAUNCH_VIAS", K_LAUNCH, L_LAUNCH)
    print("KL_V7_3V3_LOCAL_VIA", P3V3_LOCAL_VIA)


def migrate(src: Path, dst: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="kh910-kl-v7-") as td:
        temp = Path(td) / "stage.kicad_pcb"
        core.migrate(src, temp)
        postprocess(temp)
        core.validate(temp)
        dst.write_text(temp.read_text(encoding="utf-8"), encoding="utf-8")
    print("KL_V7_ELECTRICAL_STAGE_OK", dst)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path, nargs="?")
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()
    if args.validate:
        core.validate(args.input)
        return
    if args.output is None:
        ap.error("output is required")
    migrate(args.input, args.output)


if __name__ == "__main__":
    main()
