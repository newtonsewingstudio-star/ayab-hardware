#!/usr/bin/env python3
"""Probe KiCad 9 pcbnew edit APIs and legacy EOL copper for Rev A.

Read-only with respect to the repository: no board is saved. In addition to
confirming the native edit APIs needed by Rev A, this emits the exact existing
EOL track/via paths and ESP32/U701 pad assignments so the Hall ADC migration
can reuse known-safe copper corridors instead of creating blind long routes.
"""

from pathlib import Path
import pcbnew

ROOT = Path(__file__).resolve().parents[1]
board = pcbnew.LoadBoard(str(ROOT / "ayab-esp32.kicad_pcb"))
fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
src = fps.get("R734") or next(fp for fp in board.GetFootprints() if fp.GetReference().startswith("R"))


def mm(point):
    return pcbnew.ToMM(point.x), pcbnew.ToMM(point.y)


def layer_name(item):
    try:
        return board.GetLayerName(item.GetLayer())
    except Exception:
        return "?"


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

# Full pad inventory for the two devices that define the old MCU corridor.
for ref in ("U201", "U701"):
    fp = fps.get(ref)
    if not fp:
        continue
    print(f"PAD_INVENTORY_BEGIN {ref}")
    rows = []
    for pad in fp.Pads():
        x, y = mm(pad.GetPosition())
        rows.append((str(pad.GetNumber()), x, y, pad.GetNetname(), pad.GetNetCode()))
    for row in sorted(rows, key=lambda r: (int(r[0]) if r[0].isdigit() else 999, r[0])):
        print("PAD", ref, row[0], f"{row[1]:.3f}", f"{row[2]:.3f}", row[3], row[4])
    print(f"PAD_INVENTORY_END {ref}")

# Dump legacy EOL copper.  These are candidates to reuse or remove when the
# new HALL_L_ADC/HALL_R_ADC nets are created.
legacy_nets = (
    "/ESP32/EOL_L_P",
    "/ESP32/EOL_L_N",
    "/ESP32/EOL_R_P",
    "/ESP32/EOL_R_N",
    "/BROTHER-CONNECTORS/EOL_L",
    "/BROTHER-CONNECTORS/EOL_R",
)

for netname in legacy_nets:
    print("ROUTE_BEGIN", netname)
    items = [item for item in board.GetTracks() if item.GetNetname() == netname]
    print("ROUTE_COUNT", netname, len(items))
    for item in items:
        kind = item.__class__.__name__
        if hasattr(item, "GetStart") and hasattr(item, "GetEnd"):
            sx, sy = mm(item.GetStart())
            ex, ey = mm(item.GetEnd())
            width = pcbnew.ToMM(item.GetWidth()) if hasattr(item, "GetWidth") else 0.0
            print("ROUTE_ITEM", netname, kind, layer_name(item), f"{sx:.3f}", f"{sy:.3f}", f"{ex:.3f}", f"{ey:.3f}", f"w={width:.3f}")
        elif hasattr(item, "GetPosition"):
            x, y = mm(item.GetPosition())
            print("ROUTE_ITEM", netname, kind, layer_name(item), f"{x:.3f}", f"{y:.3f}")
    print("ROUTE_END", netname)
