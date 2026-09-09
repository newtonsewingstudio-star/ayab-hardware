#!/usr/bin/env python3
"""Rev A KH-910 K/L staged migration using existing board vias.

The v3 electrical transformer is correct, but its first routing prototype added
new through-vias directly on the tightly-spaced K/L traces and on the equally
close ESP17/18 corridor traces. Those signal traces are already DRC-clean at
their native narrow spacing, but 0.6 mm vias at those coordinates are not a
sensible fanout strategy.

This wrapper preserves the validated v3 electrical split, resistor placement,
and topology assertions, then removes only the six unnecessary route-endpoint
vias. The two pull-up launch vias remain. The companion router connects:

  machine K: existing via 239.22,145.65 -> existing GPIO17 via 220.97,134.15
  machine L: existing via 238.45,145.63 -> existing GPIO18 via 221.67,134.14
  R213 pull-up launch 207.5,132.025     -> existing GPIO17 via 220.97,134.15
  R214 pull-up launch 207.5,135.325     -> existing GPIO18 via 221.67,134.14

No repository PCB is installed unless the workflow subsequently refills zones,
passes topology validation, and passes both project-aware DRC gates.
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

REMOVE_VIAS = {
    (194.71, 151.86, core.MACH_K),
    (194.71, 130.91, core.MACH_K),
    (207.5, 130.91, core.MACH_K),
    (194.98, 151.99, core.MACH_L),
    (194.98, 130.71, core.MACH_L),
    (205.5, 130.71, core.MACH_L),
}
KEEP_PULLUP_VIAS = {
    (207.5, 132.025, core.MACH_K),
    (207.5, 135.325, core.MACH_L),
}


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


def strip_prototype_endpoint_vias(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    children = core.k.root_children(text)
    net_names_by_id: dict[int, str] = {}
    for item in children:
        block = text[item.start:item.end]
        if item.head == "net":
            parsed = core.k.parse_net_definition(block)
            if parsed:
                net_names_by_id[parsed[0]] = parsed[1]

    edits = []
    removed = set()
    kept = set()
    for item in children:
        if item.head != "via":
            continue
        block = text[item.start:item.end]
        sig = via_signature(block, net_names_by_id)
        if sig in REMOVE_VIAS:
            edits.append((item.start, item.end, ""))
            removed.add(sig)
        if sig in KEEP_PULLUP_VIAS:
            kept.add(sig)

    if removed != REMOVE_VIAS:
        raise RuntimeError(f"endpoint-via removal mismatch: removed={removed} expected={REMOVE_VIAS}")
    if kept != KEEP_PULLUP_VIAS:
        raise RuntimeError(f"pull-up launch vias missing after stage: {kept}")

    for start, end, repl in sorted(edits, reverse=True):
        text = text[:start] + repl + text[end:]
    path.write_text(text, encoding="utf-8")
    print("KL_V4_REUSED_EXISTING_VIAS", sorted(removed))


def migrate(src: Path, dst: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="kh910-kl-v4-") as td:
        temp = Path(td) / "stage.kicad_pcb"
        core.migrate(src, temp)
        strip_prototype_endpoint_vias(temp)
        core.validate(temp)
        dst.write_text(temp.read_text(encoding="utf-8"), encoding="utf-8")
    print("KL_V4_ELECTRICAL_STAGE_OK", dst)


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
