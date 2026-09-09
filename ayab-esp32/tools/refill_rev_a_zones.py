#!/usr/bin/env python3
from pathlib import Path
import sys
import pcbnew

if len(sys.argv) != 2:
    raise SystemExit("usage: refill_rev_a_zones.py BOARD.kicad_pcb")

path = Path(sys.argv[1]).resolve()
board = pcbnew.LoadBoard(str(path))
if board is None:
    raise RuntimeError(f"could not load {path}")

board.BuildConnectivity()
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
pcbnew.SaveBoard(str(path), board)
print(f"ZONE_REFILL_OK {path}")
