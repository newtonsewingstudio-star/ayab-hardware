#!/usr/bin/env python3
"""Check that prototype-critical Rev A schematic parts exist on the PCB.

KiCad DRC checks a board's geometry and connectivity, but it does not report a
schematic part that has never been placed on that board.  This focused audit
keeps the prototype power path and the hardware-default-OFF solenoid gate from
being accepted as documentation-only changes.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PCB = (ROOT / "ayab-esp32.kicad_pcb").read_text(encoding="utf-8")


def references(text: str) -> dict[str, str]:
    """Return PCB reference/value pairs without relying on display formatting."""
    out: dict[str, str] = {}
    for block in re.findall(r'\(footprint\b.*?(?=\n\s*\(footprint\b|\n\)\s*$)', text, re.S | re.M):
        ref = re.search(r'\(property "Reference" "([^"]+)"', block)
        value = re.search(r'\(property "Value" "([^"]*)"', block)
        if ref:
            out[ref.group(1)] = value.group(1) if value else ""
    return out


expected = {
    # USB/machine-source isolation and both machine-derived regulators.
    "U601": "XL1509",
    "U602": "XL1509-3.3E1",
    "U403": "LM66100DCKR",
    # Machine-presence divider on GPIO4.
    "R215": "47k",
    "R216": "10k",
    "D205": "CDBU0130-HF",
    "D206": "CDBU0130-HF",
    "C206": "100n",
    # A directly accessible 3.3 V check point.
    "TP603": "3V3",
    # Hardware-default-OFF solenoid power gate.
    "Q805": "LP9435LT1G",
    "Q806": "AO3400A",
    "R820": "100k",
    "R821": "10k",
    "R822": "100k",
    "TP703": "SOL12_SW",
}

on_pcb = references(PCB)
missing = []
wrong_value = []
for ref, value in expected.items():
    actual = on_pcb.get(ref)
    if actual is None:
        missing.append(ref)
    elif actual != value:
        wrong_value.append(f"{ref}: expected {value!r}, got {actual!r}")

print("PROTOTYPE_PCB_PARITY_AUDIT")
print("PRESENT", ", ".join(sorted(set(expected) - set(missing) - {x.split(':', 1)[0] for x in wrong_value})))
if missing:
    print("MISSING", ", ".join(missing))
if wrong_value:
    print("VALUE_MISMATCH", "; ".join(wrong_value))
if missing or wrong_value:
    raise SystemExit("Prototype-critical schematic parts are not fully integrated on the PCB")
print("PROTOTYPE_PCB_PARITY_OK")
