#!/usr/bin/env python3
"""Rev A Hall PCB migration v4c: electrical migration only, route later with pcbnew.

v4's electrical transformation is retained unchanged. The only differences are:
- no hand-authored cross-board ADC polylines;
- no new target vias (the existing MCU Hall vias are already retagged by v4);
- no generic GND/+5V pruning.

A separate pcbnew A* router adds the two In1.Cu ADC routes after this stage, then
the original v4 validator and KiCad DRC are run on the completed staged board.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import migrate_rev_a_hall_pcb_serialized_v4 as v4

k = v4.k
BASE_VALIDATE = v4.validate
BASE_POLYLINE = k.polyline
BASE_VIA = k.via

# The retagged legacy corridors already terminate at these existing vias.
MCU_LEFT_VIA = (219.55, 134.13)
MCU_RIGHT_VIA = (218.8, 134.13)

# Keep power networks intact. Dead comparator power stubs are cleaned later by
# a connectivity-aware pcbnew pass, not by endpoint leaf pruning.
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
    # v4 validates final route-item counts internally. Suppress that one final
    # validation only while writing this deliberately unrouted intermediate.
    old_validate = v4.validate
    v4.validate = lambda _text: None
    try:
        v4.migrate(src, dst)
    finally:
        v4.validate = old_validate


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path, nargs="?")
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()
    if args.validate:
        BASE_VALIDATE(args.input.read_text(encoding="utf-8"))
        print("HALL_V4C_FINAL_VALIDATION_OK", args.input)
        return
    if args.output is None:
        ap.error("output required")
    migrate(args.input, args.output)
    print("HALL_V4C_ELECTRICAL_STAGE_OK", args.output)


if __name__ == "__main__":
    main()
