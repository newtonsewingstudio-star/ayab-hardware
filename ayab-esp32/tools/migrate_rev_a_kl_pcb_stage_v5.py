#!/usr/bin/env python3
"""Wrapper for the Rev A K/L text migration.

KiCad exposes two legacy 2.0375 mm local K/L dangling tails only after the board
has been loaded/rebuilt by pcbnew. The v4 text serializer therefore cannot
reliably see or remove them. This wrapper disables only that impossible
text-level assertion and applies the final measured pull-up placement below
J801; all electrical, via, and copper assertions in v4 remain fail-closed.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys

V4 = Path(__file__).with_name("migrate_rev_a_kl_pcb_stage_v4.py")
spec = importlib.util.spec_from_file_location("kh910_kl_stage_v4", V4)
if spec is None or spec.loader is None:
    raise RuntimeError("could not import K/L v4 migration")
v4 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = v4
spec.loader.exec_module(v4)

# These tracks are absent from v4's serialized input representation. They are
# removed later from the pcbnew-loaded board by cleanup_rev_a_kl_legacy_tails.py.
v4.REMOVE_ANY_SEGMENTS = set()

# Run-22 DRC established the true rotated J801 envelope: its pad field reaches
# x=259.67 and its courtyard reaches approximately x=261.45 while ending near
# y=122.05. There is no usable horizontal 0603 corridor between J801 and C609.
# Place both pull-ups below J801 instead, still left of C609.
v4.R213_NEW = (260.0, 124.0)
v4.R214_NEW = (260.0, 126.0)
v4.R213_P1 = (259.175, 124.0)
v4.R213_P2 = (260.825, 124.0)
v4.R214_P1 = (259.175, 126.0)
v4.R214_P2 = (260.825, 126.0)
v4.K_LAUNCH = (262.0, 124.0)
v4.L_LAUNCH = (262.0, 126.0)
# Existing +3V3 feed and local via are already below J801 and remain suitable.
v4.P3V3_FEED = (257.13, 122.26)
v4.P3V3_LOCAL_VIA = (258.0, 124.0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path, nargs="?")
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()

    if args.validate:
        v4.core.validate(args.input)
        print("KL_V5_WRAPPER_TOPOLOGY_OK", args.input)
        return

    if args.output is None:
        ap.error("output is required")
    v4.migrate(args.input, args.output)
    print("KL_V5_WRAPPER_MIGRATION_OK", args.output)
    print("KL_V5_FINAL_PULLUPS", v4.R213_NEW, v4.R214_NEW)
    print("KL_V5_FINAL_LAUNCH_VIAS", v4.K_LAUNCH, v4.L_LAUNCH)


if __name__ == "__main__":
    main()
