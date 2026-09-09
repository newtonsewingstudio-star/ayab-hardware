#!/usr/bin/env python3
"""Add TP703 to the staged KH910 Rev A solenoid fail-safe gate.

TP703 is a schematic-defined TestPoint_Pad_D1.0mm on SOLENOID_12V_SW.  Clone
repository-native TP701, bind it to the TP703 schematic symbol/path, and place
it on a short switched-rail spur beside the compact gate.  The calling
workflow must refill zones and require KiCad DRC 0/0/0.
"""
from pathlib import Path
import re, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import patch_rev_a_solenoid_pcb as u
import pcbnew

if len(sys.argv) != 2:
    raise SystemExit("usage: stage_rev_a_solenoid_tp703.py BOARD.kicad_pcb")
P = Path(sys.argv[1]).resolve()
SCH = Path(__file__).resolve().parents[1] / "solenoids.kicad_sch"
pcb = P.read_text(encoding="utf-8")
sch = SCH.read_text(encoding="utf-8")

if 'fp_text reference "TP703"' in pcb or 'property "Reference" "TP703"' in pcb:
    raise RuntimeError("refusing partial TP703 state: TP703 already on PCB")

defs = u.net_defs(pcb)
sw_net = next((n for n, s in defs.items() if s == "SOLENOID_12V_SW"), 0)
if sw_net <= 0:
    raise RuntimeError("SOLENOID_12V_SW net missing")

_, _, template = u.find_fp(pcb, "TP701")
prefix = u.sheet_prefix_from_existing(pcb)
su = u.symbol_uuid_by_ref(sch, "TP703")
path = prefix + "/" + su

# Keep enough room below Q805 and above J401.  A short vertical spur reaches
# the existing 1 mm switched-power trace at x=117.9375, y=158.0.
X, Y = 117.9375, 157.0
out = re.sub(r'\((uuid|tstamp) [0-9a-f-]+\)', lambda m: f'({m.group(1)} {u.uid()})', template)
out, n = re.subn(
    r'^(\(footprint.*?)(\(at\s+[-\d.]+\s+[-\d.]+(?:\s+[-\d.]+)?\))',
    lambda m: m.group(1) + f'(at {X:g} {Y:g} 0)', out, count=1, flags=re.S,
)
if n != 1:
    raise RuntimeError("could not relocate TP703 clone")
out, n = re.subn(r'\(path "[^"]+"\)', f'(path "{path}")', out, count=1)
if n != 1:
    raise RuntimeError("TP703 path anchor missing")
if re.search(r'\(fp_text reference "[^"]+"', out):
    out = re.sub(r'\(fp_text reference "[^"]+"', '(fp_text reference "TP703"', out, count=1)
else:
    out, n = re.subn(r'\(property "Reference" "[^"]+"', '(property "Reference" "TP703"', out, count=1)
    if n != 1:
        raise RuntimeError("TP703 reference field missing")
if re.search(r'\(fp_text value "[^"]+"', out):
    out = re.sub(r'\(fp_text value "[^"]+"', '(fp_text value "SOL12_SW"', out, count=1)
else:
    out, n = re.subn(r'\(property "Value" "[^"]+"', '(property "Value" "SOL12_SW"', out, count=1)
    if n != 1:
        raise RuntimeError("TP703 value field missing")
out = u.replace_pad_net(out, "1", sw_net, "SOLENOID_12V_SW")
pcb = u.insert_before_first(pcb, '  (segment ', out)
P.write_text(pcb, encoding="utf-8")

b = pcbnew.LoadBoard(str(P))
if b is None:
    raise RuntimeError("KiCad could not reload TP703 staged board")
b.BuildConnectivity()
tp = next((f for f in b.GetFootprints() if f.GetReference() == "TP703"), None)
if tp is None:
    raise RuntimeError("TP703 missing after clone")
pad = next((p for p in tp.Pads() if p.GetNumber() == "1"), None)
if pad is None or pad.GetNetname() != "SOLENOID_12V_SW":
    raise RuntimeError(f"TP703.1 net mismatch: {pad.GetNetname() if pad else None!r}")
q = pad.GetPosition(); pos = (pcbnew.ToMM(q.x), pcbnew.ToMM(q.y))

# Connect to the already-staged switched-power vertical at the same X.
t = pcbnew.PCB_TRACK(b)
t.SetStart(pcbnew.VECTOR2I_MM(*pos))
t.SetEnd(pcbnew.VECTOR2I_MM(117.9375, 158.0))
t.SetLayer(pcbnew.F_Cu)
t.SetWidth(pcbnew.FromMM(0.50))
t.SetNet(pad.GetNet())
b.Add(t)
b.BuildConnectivity()
pcbnew.SaveBoard(str(P), b)
print("SOL_TP703_STAGE_OK", f"pad=({pos[0]:.4f},{pos[1]:.4f})", "net=SOLENOID_12V_SW", "spur=(117.9375,158.0)")
