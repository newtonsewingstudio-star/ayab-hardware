#!/usr/bin/env python3
"""Source acceptance audit for the KH910 Rev A solenoid fail-safe gate.

This protects component selection and schematic identifiers.  The separate
PCB validation workflow is authoritative for physical connectivity and DRC.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SCH = (ROOT / "solenoids.kicad_sch").read_text(encoding="utf-8")

def block_after(text, start):
    depth = 0; quote = False; escape = False
    for pos in range(start, len(text)):
        ch = text[pos]
        if quote:
            if escape: escape = False
            elif ch == "\\": escape = True
            elif ch == '"': quote = False
            continue
        if ch == '"': quote = True
        elif ch == '(': depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0: return text[start:pos + 1]
    raise RuntimeError("unbalanced schematic")

def symbol(ref):
    marker = f'(property "Reference" "{ref}"'
    at = SCH.find(marker)
    if at < 0: raise RuntimeError(f"missing schematic symbol {ref}")
    start = SCH.rfind('(symbol ', 0, at)
    return block_after(SCH, start)

def prop(block, name):
    match = re.search(r'\(property "' + re.escape(name) + r'" "([^"]*)"', block)
    return match.group(1) if match else None

expected = {
    "Q805": {"Value": "LP9435LT1G", "Footprint": "Package_TO_SOT_SMD:SOT-23", "LCSC ID": "C383257"},
    "Q806": {"Value": "AO3400A", "Footprint": "Package_TO_SOT_SMD:SOT-23", "LCSC ID": "C20917"},
    "R820": {"Value": "100k", "Footprint": "Resistor_SMD:R_0603_1608Metric"},
    "R821": {"Value": "10k", "Footprint": "Resistor_SMD:R_0603_1608Metric"},
    "R822": {"Value": "100k", "Footprint": "Resistor_SMD:R_0603_1608Metric"},
    "TP703": {"Value": "SOL12_SW", "Footprint": "TestPoint:TestPoint_Pad_D1.0mm"},
}
for ref, checks in expected.items():
    b = symbol(ref)
    for key, want in checks.items():
        got = prop(b, key)
        if got != want: raise RuntimeError(f"{ref} {key}: expected {want!r}, got {got!r}")
    if ref in {"Q805", "Q806"} and prop(b, "Datasheet") in {None, "", "~"}:
        raise RuntimeError(f"{ref} needs an explicit datasheet link")

if SCH.count('"SOLENOID_12V_SW"') < 2:
    raise RuntimeError("switched-rail label is not represented at both gate/load locations")
if '"DEFAULT_OFF' in SCH:
    raise RuntimeError("unexpected production-promotion marker in source")
print("SOLENOID_GATE_SOURCE_AUDIT_OK")
print("SOURCE_REVIEW: no prototype evidence and no fabrication output")
print("PARTS: Q805 LP9435LT1G, Q806 AO3400A, 100k/10k default-off network, TP703")
