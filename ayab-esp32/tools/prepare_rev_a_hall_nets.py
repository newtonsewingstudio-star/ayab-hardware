#!/usr/bin/env python3
"""Create the two Rev A Hall ADC nets as an isolated KiCad mutation pass.

KiCad 9's SWIG wrappers for footprint/pad objects can become stale immediately
after BOARD.Add(NETINFO_ITEM).  This script therefore does exactly one thing:
add the missing HALL_L_ADC / HALL_R_ADC net objects and serialize the board.
The migration workflow reloads that serialized board in a new Python process
before touching any pads, footprints, tracks, or vias.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import pcbnew

NETS = ("/ESP32/HALL_L_ADC", "/ESP32/HALL_R_ADC")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()

    board = pcbnew.LoadBoard(str(args.input))
    existing = board.GetNetsByName()
    added = []

    for name in NETS:
        try:
            existing[name]
            continue
        except Exception:
            pass
        board.Add(pcbnew.NETINFO_ITEM(board, name))
        added.append(name)

    pcbnew.SaveBoard(str(args.output), board)
    print("HALL_NET_PREP_OK")
    print("ADDED", ",".join(added) if added else "none")
    print("OUTPUT", args.output)


if __name__ == "__main__":
    main()
