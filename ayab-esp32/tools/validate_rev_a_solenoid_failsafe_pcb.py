#!/usr/bin/env python3
"""Fail-closed electrical topology audit for the KH910 Rev A solenoid fail-safe.

Run only after the physical gate is staged/promoted. KiCad DRC remains the
physical-clearance/connectivity authority; this script freezes the intended
net assignment and default-OFF fail-safe topology so a geometrically clean but
electrically wrong board cannot be accepted.
"""
from pathlib import Path
import sys
import pcbnew

P=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/"ayab-esp32.kicad_pcb"
b=pcbnew.LoadBoard(str(P))
if b is None: raise RuntimeError("could not load PCB")
b.BuildConnectivity()
fps={f.GetReference():f for f in b.GetFootprints()}

RAW="+12V"
SW="SOLENOID_12V_SW"
EN="SOLENOID_PWR_EN"
PG="Net-(Q805-G)"
NG="Net-(Q806-G)"
GND="GND"


def pad(ref,pn):
    f=fps.get(ref)
    if f is None: raise RuntimeError(f"missing footprint {ref}")
    p=next((q for q in f.Pads() if q.GetNumber()==str(pn)),None)
    if p is None: raise RuntimeError(f"missing pad {ref}.{pn}")
    return p

def require(ref,pn,net):
    got=pad(ref,pn).GetNetname()
    if got!=net: raise RuntimeError(f"{ref}.{pn}: expected {net!r}, got {got!r}")

# Gate topology.  Static defaults are deliberate:
# R820 pulls P-MOS gate to its +12 V source => Q805 OFF without control.
# R822 pulls Q806 gate to ground => Q806 OFF if MCU/GPIO21 is absent.
for ref,pn,net in (
    ("Q805","1",PG),("Q805","2",RAW),("Q805","3",SW),
    ("Q806","1",NG),("Q806","2",GND),("Q806","3",PG),
    ("R820","1",RAW),("R820","2",PG),
    ("R821","1",EN),("R821","2",NG),
    ("R822","1",GND),("R822","2",NG),
    ("TP703","1",SW),
): require(ref,pn,net)

# All left solenoid common/flyback loads must remain behind the switched rail.
for ref,pn in (
    ("J401","9"),("J401","10"),("J406","9"),("J406","10"),
    ("U302","9"),("U303","9"),("U304","9"),
    ("C302","1"),("C303","1"),("C304","1"),
    ("C603","1"),("C604","1"),("C605","1"),
): require(ref,pn,SW)

# The right machine power/common branch was separately partitioned and must
# not regress to raw +12 V.
for ref,pn in (("J403","9"),("J403","10")):
    require(ref,pn,SW)

# Sanity: no legacy GPIO21 functional name may survive after gate migration.
legacy=[]
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetNetname()=="/ESP32/ESP21": legacy.append(f"{f.GetReference()}.{p.GetNumber()}")
for t in b.GetTracks():
    if t.GetNetname()=="/ESP32/ESP21": legacy.append("track")
if legacy: raise RuntimeError("legacy /ESP32/ESP21 net remains: "+", ".join(legacy[:12]))

print("SOLENOID_FAILSAFE_TOPOLOGY_OK")
print("DEFAULT_OFF Q805 gate pulled to +12V by R820; Q806 gate pulled to GND by R822")
print("ENABLE",EN,"through R821")
print("SWITCHED_RAIL",SW,"validated on left and right machine power branches")
