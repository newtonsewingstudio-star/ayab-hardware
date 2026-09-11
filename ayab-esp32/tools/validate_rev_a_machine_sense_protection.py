#!/usr/bin/env python3
"""Fail-closed schematic/PCB topology check for GPIO4 machine-sense protection."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pcbnew


PCB = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "ayab-esp32.kicad_pcb"
MCU = PCB.with_name("mcu.kicad_sch")
SENSE = "/ESP32/MACHINE_PWR_SENSE"

schematic = MCU.read_text(encoding="utf-8")
pcb_text = PCB.read_text(encoding="utf-8")
for ref, value in (("R215", "47k"), ("R216", "10k"), ("D205", "CDBU0130-HF"),
                   ("D206", "CDBU0130-HF"), ("C206", "100n")):
    marker = f'(property "Reference" "{ref}"'
    start = schematic.find(marker)
    if start < 0:
        raise RuntimeError(f"schematic component missing: {ref}")
    symbol_start = schematic.rfind("(symbol (lib_id ", 0, start)
    snippet = schematic[symbol_start:start + 1400]
    if not re.search(rf'\(property "Value" "{re.escape(value)}"', snippet):
        raise RuntimeError(f"{ref} schematic value is not {value}")

for token in ("C2886021", "CDBU0130-HF", "C14663", "CL10B104KB8NNNC"):
    if token not in schematic:
        raise RuntimeError(f"schematic ordering metadata missing: {token}")


def component_snippet(text: str, ref: str, kind: str) -> str:
    marker = f'(property "Reference" "{ref}"'
    marker_at = text.find(marker)
    if marker_at < 0:
        raise RuntimeError(f"{kind} component missing: {ref}")
    if kind == "schematic":
        start = text.rfind("(symbol (lib_id ", 0, marker_at)
        return text[start:marker_at + 1400]
    start = text.rfind("(footprint ", 0, marker_at)
    next_start = text.find("\n\t(footprint ", marker_at)
    return text[start:next_start if next_start >= 0 else len(text)]


# The earlier BOM metadata named a 10 nF part on eight footprints whose design
# value is 100 nF.  Require one consistent, orderable 100 nF/50 V X7R part in
# both schematic and PCB so the value error cannot return at ordering time.
cap_refs = {"C201", "C202", "C203", "C204", "C206", "C301", "C305", "C701", "C702"}
schematic_texts = [
    path.read_text(encoding="utf-8")
    for path in MCU.parent.glob("*.kicad_sch")
]
for ref in sorted(cap_refs):
    source = next((text for text in schematic_texts if f'(property "Reference" "{ref}"' in text), None)
    if source is None:
        raise RuntimeError(f"schematic capacitor missing: {ref}")
    for kind, snippet in (
        ("schematic", component_snippet(source, ref, "schematic")),
        ("PCB", component_snippet(pcb_text, ref, "PCB")),
    ):
        for token in ('(property "Value" "100n"', "C14663", "CL10B104KB8NNNC", "50V X7R"):
            if token not in snippet:
                raise RuntimeError(f"{ref} {kind} 100 nF ordering metadata missing: {token}")

for ref in ("D205", "D206"):
    for kind, snippet in (
        ("schematic", component_snippet(schematic, ref, "schematic")),
        ("PCB", component_snippet(pcb_text, ref, "PCB")),
    ):
        for token in ('(property "Value" "CDBU0130-HF"', "C2886021", "Comchip Technology"):
            if token not in snippet:
                raise RuntimeError(f"{ref} {kind} diode ordering metadata missing: {token}")

board = pcbnew.LoadBoard(str(PCB))
if board is None:
    raise RuntimeError(f"could not load {PCB}")
board.BuildConnectivity()
fps = {footprint.GetReference(): footprint for footprint in board.GetFootprints()}


def require(ref: str, number: str, net_name: str) -> None:
    fp = fps.get(ref)
    if fp is None:
        raise RuntimeError(f"PCB footprint missing: {ref}")
    pad = next((item for item in fp.Pads() if item.GetNumber() == number), None)
    if pad is None:
        raise RuntimeError(f"PCB pad missing: {ref}.{number}")
    if pad.GetNetname() != net_name:
        raise RuntimeError(f"{ref}.{number}: expected {net_name!r}, got {pad.GetNetname()!r}")


for requirement in (
    ("U201", "8", SENSE),
    ("R215", "1", "+12V"), ("R215", "2", SENSE),
    ("R216", "1", SENSE), ("R216", "2", "GND"),
    ("D205", "1", "+3V3"), ("D205", "2", SENSE),
    ("D206", "1", SENSE), ("D206", "2", "GND"),
    ("C206", "1", SENSE), ("C206", "2", "GND"),
):
    require(*requirement)

print("MACHINE_SENSE_PROTECTION_TOPOLOGY_OK")
print("POSITIVE_CLAMP D205: MACHINE_PWR_SENSE anode, +3V3 cathode")
print("NEGATIVE_CLAMP D206: GND anode, MACHINE_PWR_SENSE cathode")
print("ADC_FILTER C206: 100n MACHINE_PWR_SENSE to GND")
# R215/C25819 is specified as 47 kohm +/-1%, +/-100 ppm/C, -55 to +155 C.
# Across that full rated element-temperature range, the largest departure from
# the 25 C nominal is 130 C.  Applying tolerance and worst-sign TCR together is
# deliberately conservative.  A node >= 0 V then gives a loose current upper
# bound that does not rely on ambient temperature or a particular clamp voltage.
r215_min_ohm_full_rated_temperature = 47000.0 * (1.0 - 0.01 - 100e-6 * 130.0)
for voltage in (12.0, 15.0, 40.0):
    conditional_ma = max(0.0, voltage - 3.6) / 47000.0 * 1000.0
    loose_upper_ma = voltage / r215_min_ohm_full_rated_temperature * 1000.0
    print(
        f"R216_OPEN_CURRENT VRAW={voltage:.1f}V "
        f"CONDITIONAL_{conditional_ma:.3f}mA_AT_3V6_NOMINAL_R215 "
        f"LOOSE_UPPER_{loose_upper_ma:.3f}mA_NODE_GE_0V_R215_MIN_FULL_RATED_ELEMENT_TEMP"
    )
print("CURRENT_BOUNDS_DO_NOT_GUARANTEE_GPIO_VOLTAGE_OR_SURGE_COMPLIANCE")
