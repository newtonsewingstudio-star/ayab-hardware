#!/usr/bin/env python3
"""Probe KiCad 9 pcbnew edit APIs needed for Rev A PCB migration.

Read-only with respect to the repository: no board is saved. The script tests
safe in-memory footprint cloning, net creation/addition, and pad/track net
setters so final Rev A migrations can use native KiCad objects instead of raw
PCB text serialization.
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

for row in attempts:
    print("CLONE_ATTEMPT", row)

# Existing/missing net lookup semantics.
for name in ("GND", "/BROTHER-CONNECTORS/EOL_L", "/ESP32/EOL_L_P", "/ESP32/HALL_L_ADC"):
    try:
        code = board.GetNetcodeFromNetname(name)
        print("NET_LOOKUP", name, code)
    except Exception as exc:
        print("NET_LOOKUP_MISSING", name, type(exc).__name__, str(exc))

# Test creating and adding a NETINFO_ITEM in memory only. The board object is
# discarded at process exit and never saved.
created = None
for args in ((board, "__REV_A_PROBE_NET__"), (board, "__REV_A_PROBE_NET_2__", -1)):
    try:
        net = pcbnew.NETINFO_ITEM(*args)
        print("NET_CTOR_OK", len(args), net.GetNetname(), net.GetNetCode())
        if created is None:
            board.Add(net)
            created = net
            print("NET_ADD_OK", net.GetNetname(), net.GetNetCode(), board.GetNetcodeFromNetname(net.GetNetname()))
    except Exception as exc:
        print("NET_CTOR_OR_ADD_FAIL", len(args), repr(exc))

# Pad and routed-item setter availability.
first_pad = next(iter(src.Pads()))
print("PAD_NETLIKE", [n for n in dir(first_pad) if "net" in n.lower()])
first_track = next(iter(board.GetTracks()))
print("TRACK_NETLIKE", [n for n in dir(first_track) if "net" in n.lower()])

if created is not None:
    try:
        first_pad.SetNet(created)
        print("PAD_SETNET_OK", first_pad.GetNetname(), first_pad.GetNetCode())
    except Exception as exc:
        print("PAD_SETNET_FAIL", repr(exc))
    try:
        first_track.SetNet(created)
        print("TRACK_SETNET_OK", first_track.GetNetname(), first_track.GetNetCode())
    except Exception as exc:
        print("TRACK_SETNET_FAIL", repr(exc))
