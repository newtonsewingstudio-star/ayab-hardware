#!/usr/bin/env python3
"""Probe KiCad pcbnew Python API availability and coordinate semantics in CI."""
from pathlib import Path
import sys

try:
    import pcbnew
except Exception as exc:
    print(f"PCBNEW_IMPORT_FAILED: {exc!r}")
    print("sys.path:")
    for p in sys.path:
        print(p)
    raise

board_path = Path(__file__).resolve().parents[1] / "ayab-esp32.kicad_pcb"
board = pcbnew.LoadBoard(str(board_path))
print("PCBNEW_VERSION", pcbnew.GetBuildVersion())
print("BOARD", board_path)

wanted = {"U302", "C302", "Q502", "U201"}
for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref not in wanted:
        continue
    print("FOOTPRINT", ref, "POS_MM", pcbnew.ToMM(fp.GetPosition().x), pcbnew.ToMM(fp.GetPosition().y), "ORI_DEG", fp.GetOrientationDegrees())
    for pad in fp.Pads():
        if pad.GetNumber() in {"1", "2", "3", "9", "21", "25"}:
            pos = pad.GetPosition()
            print("PAD", ref, pad.GetNumber(), "POS_MM", pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y), "NET", pad.GetNetname())

# Confirm the coordinates that the text-level helper got wrong.
checks = {
    ("U302", "9"): (124.005, 141.800),
    ("C302", "1"): (109.625, 140.375),
    ("U201", "25"): (225.825, 136.675),
}
lookup = {}
for fp in board.GetFootprints():
    ref = fp.GetReference()
    for pad in fp.Pads():
        key = (ref, pad.GetNumber())
        if key in checks:
            p = pad.GetPosition()
            lookup[key] = (round(pcbnew.ToMM(p.x), 3), round(pcbnew.ToMM(p.y), 3))
for key, expected in checks.items():
    actual = lookup.get(key)
    print("CHECK", key, "actual", actual, "expected", expected)
    if actual != expected:
        raise SystemExit(f"coordinate mismatch for {key}: {actual} != {expected}")

# Exercise zone fill in memory without saving the board.
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
print("ZONE_FILL_OK", board.GetAreaCount())
