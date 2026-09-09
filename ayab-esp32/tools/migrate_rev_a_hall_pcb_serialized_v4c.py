#!/usr/bin/env python3
"""Rev A Hall PCB migration v4c: electrical migration plus topology validation.

v4's electrical transformation is retained unchanged. The only migration-stage
differences are:
- no hand-authored cross-board ADC polylines;
- no new target vias (the existing MCU Hall vias are already retagged by v4);
- no generic GND/+5V pruning.

A separate pcbnew A* router adds the two In1.Cu ADC routes and a narrow cleanup
removes obsolete legacy tails. Final validation checks topology rather than an
arbitrary minimum copper-item count, then KiCad DRC is authoritative.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import migrate_rev_a_hall_pcb_serialized_v4 as v4

k = v4.k
BASE_POLYLINE = k.polyline
BASE_VIA = k.via

MCU_LEFT_VIA = (219.55, 134.13)
MCU_RIGHT_VIA = (218.8, 134.13)

# Keep power networks intact. Dead comparator power stubs are cleaned later by
# a narrowly scoped pcbnew pass, not by endpoint leaf pruning.
v4.PRUNE_NAMES = {v4.RAW_L, v4.RAW_R, v4.LK, v4.LL, v4.RN, v4.RS}


def no_guessed_adc_polyline(points, layer, net_id, seed):
    if seed in {"v4-left-in1", "v4-right-in1"}:
        return []
    return BASE_POLYLINE(points, layer, net_id, seed)


def no_new_target_via(pos, net_id, seed):
    if seed in {"v4-left-target", "v4-right-target"}:
        return ""
    return BASE_VIA(pos, net_id, seed)


k.polyline = no_guessed_adc_polyline
k.via = no_new_target_via


def migrate(src: Path, dst: Path) -> None:
    # v4's final validator expects its original long-route copper counts.  This
    # stage is intentionally unrouted, so suppress only that final call while
    # retaining all of v4's migration-time electrical assertions.
    old_validate = v4.validate
    v4.validate = lambda _text: None
    try:
        v4.migrate(src, dst)
    finally:
        v4.validate = old_validate


def final_validate(text: str) -> None:
    children = k.root_children(text)
    nets = {}
    fps = {}
    oldc = {v4.OLD_LP: 0, v4.OLD_LN: 0}
    in1 = {v4.ADC_L: 0, v4.ADC_R: 0}
    adc_bcu = {v4.ADC_L: 0, v4.ADC_R: 0}
    via_hits = {v4.ADC_L: 0, v4.ADC_R: 0}

    for s in children:
        block = text[s.start:s.end]
        if s.head == "net":
            n = k.parse_net_definition(block)
            if n:
                nets[n[1]] = n[0]
        elif s.head == "footprint":
            ref = v4.reference(block)
            if ref:
                fps[ref] = block

    for name in (v4.ADC_L, v4.ADC_R):
        if name not in nets:
            raise RuntimeError(f"missing {name}")
    if v4.STRICT_REMOVE & set(fps):
        raise RuntimeError(f"obsolete refs remain: {sorted(v4.STRICT_REMOVE & set(fps))}")

    expected = {
        "R735": {"1": v4.RAW_L, "2": v4.ADC_L},
        "R736": {"1": v4.ADC_L, "2": v4.GND},
        "R737": {"1": v4.RAW_R, "2": v4.ADC_R},
        "R738": {"1": v4.ADC_R, "2": v4.GND},
    }
    for ref, padmap in expected.items():
        if ref not in fps or v4.value(fps[ref]) != "10k":
            raise RuntimeError(f"bad or missing {ref}")
        pads = k.direct_pad_blocks(fps[ref])
        for pn, netname in padmap.items():
            got = k.pad_net(pads[pn])
            if not got or got[1] != netname:
                raise RuntimeError(f"{ref}.{pn} {got} != {netname}")

    u201 = k.direct_pad_blocks(fps["U201"])
    if k.pad_net(u201["5"])[1] != v4.ADC_L or k.pad_net(u201["6"])[1] != v4.ADC_R:
        raise RuntimeError("U201 Hall ADC pad assignment mismatch")

    for s in children:
        if s.head not in {"segment", "via", "arc"}:
            continue
        block = text[s.start:s.end]
        nid = k.item_net_id(block)
        if nid == nets.get(v4.OLD_LP):
            oldc[v4.OLD_LP] += 1
        elif nid == nets.get(v4.OLD_LN):
            oldc[v4.OLD_LN] += 1

        for name, target in ((v4.ADC_L, MCU_LEFT_VIA), (v4.ADC_R, MCU_RIGHT_VIA)):
            if nid != nets[name]:
                continue
            layer = k.item_layer(block)
            if s.head == "segment" and layer == "In1.Cu":
                in1[name] += 1
            if s.head == "segment" and layer == "B.Cu":
                adc_bcu[name] += 1
            if s.head == "via" and any(k.near(p, target, 0.003) for p in k.item_points(block)):
                via_hits[name] += 1

    if oldc != {v4.OLD_LP: 4, v4.OLD_LN: 2}:
        raise RuntimeError(f"retained local old-net copper mismatch: {oldc}")
    for name in (v4.ADC_L, v4.ADC_R):
        if in1[name] < 1:
            raise RuntimeError(f"no In1.Cu A* route on {name}")
        if via_hits[name] != 1:
            raise RuntimeError(f"expected exactly one MCU target via on {name}, found {via_hits[name]}")
        if adc_bcu[name] != 0:
            raise RuntimeError(f"obsolete B.Cu tail remains on {name}: {adc_bcu[name]} segments")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path, nargs="?")
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()
    if args.validate:
        final_validate(args.input.read_text(encoding="utf-8"))
        print("HALL_V4C_FINAL_VALIDATION_OK", args.input)
        return
    if args.output is None:
        ap.error("output required")
    migrate(args.input, args.output)
    print("HALL_V4C_ELECTRICAL_STAGE_OK", args.output)


if __name__ == "__main__":
    main()
