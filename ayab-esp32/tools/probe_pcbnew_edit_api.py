#!/usr/bin/env python3
"""Probe KiCad 9 pcbnew edit APIs needed for Rev A PCB migration.

Read-only: no board is saved. The script tests safe in-memory footprint cloning
and inventories net-management methods so the final migration can use native
KiCad objects instead of raw PCB text serialization.
"""

from pathlib import Path
import pcbnew

ROOT = Path(__file__).resolve().parents[1]
board = pcbnew.LoadBoard(str(ROOT / "ayab-esp32.kicad_pcb"))
fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
src = fps.get("R734") or next(fp for fp in board.GetFootprints() if fp.GetReference().startswith("R"))

print("KICAD", pcbnew.GetBuildVersion())
print("SOURCE", src.GetReference(), src.GetValue(), src.GetFPID().GetLibNickname(), src.GetFPID().GetLibItemName())
print("FOOTPRINT_COPYLIKE", [n for n in dir(src) if any(k in n.lower() for k in ("clone", "duplicate", "copy"))])
print("BOARD_NETLIKE", [n for n in dir(board) if "net" in n.lower()])
print("NETINFO_CTORS", pcbnew.NETINFO_ITEM)

attempts = []
try:
    clone = pcbnew.FOOTPRINT(src)
    attempts.append(("FOOTPRINT(copy_ctor)", True, clone.GetReference(), clone.GetValue(), len(list(clone.Pads()))))
except Exception as exc:
    attempts.append(("FOOTPRINT(copy_ctor)", False, repr(exc)))

if hasattr(src, "Duplicate"):
    try:
        clone = src.Duplicate()
        attempts.append(("Duplicate()", True, clone.GetReference(), clone.GetValue(), len(list(clone.Pads()))))
    except Exception as exc:
        attempts.append(("Duplicate()", False, repr(exc)))

if hasattr(src, "Clone"):
    try:
        clone = src.Clone()
        attempts.append(("Clone()", True, clone.GetReference(), clone.GetValue(), len(list(clone.Pads()))))
    except Exception as exc:
        attempts.append(("Clone()", False, repr(exc)))

for row in attempts:
    print("CLONE_ATTEMPT", row)

# Existing net lookup semantics.
for name in ("GND", "/BROTHER-CONNECTORS/EOL_L", "/ESP32/EOL_L_P", "/ESP32/HALL_L_ADC"):
    code = board.GetNetcodeFromNetname(name) if hasattr(board, "GetNetcodeFromNetname") else None
    print("NET_LOOKUP", name, code)

# Test creating a NETINFO_ITEM in memory but do not add it to the board.
for args in ((board, "__REV_A_PROBE_NET__"), (board, "__REV_A_PROBE_NET__", -1)):
    try:
        net = pcbnew.NETINFO_ITEM(*args)
        print("NET_CTOR_OK", len(args), net.GetNetname(), net.GetNetCode())
    except Exception as exc:
        print("NET_CTOR_FAIL", len(args), repr(exc))

# Pad net setter availability.
first_pad = next(iter(src.Pads()))
print("PAD_NETLIKE", [n for n in dir(first_pad) if "net" in n.lower()])
