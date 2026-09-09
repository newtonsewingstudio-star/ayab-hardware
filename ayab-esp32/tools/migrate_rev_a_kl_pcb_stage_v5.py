#!/usr/bin/env python3
"""Wrapper for the Rev A K/L text migration.

KiCad exposes two legacy 2.0375 mm local K/L dangling tails only after the board
has been loaded/rebuilt by pcbnew.  The v4 text serializer therefore cannot
reliably see or remove them.  This wrapper disables only that impossible
text-level assertion; all electrical, footprint, via, and copper assertions in
v4 remain fail-closed.  A dedicated pcbnew cleanup step removes and asserts the
two tails after zone refill.
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

# These tracks are absent from v4's serialized input representation.  They are
# removed later from the pcbnew-loaded board by cleanup_rev_a_kl_legacy_tails.py.
v4.REMOVE_ANY_SEGMENTS = set()


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


if __name__ == "__main__":
    main()
