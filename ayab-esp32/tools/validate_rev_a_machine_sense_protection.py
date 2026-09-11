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
for voltage in (12.0, 15.0, 40.0):
    current_ma = max(0.0, voltage - 3.6) / 47000.0 * 1000.0
    print(f"R216_OPEN_LIMIT VRAW={voltage:.1f}V ICLAMP_LE_{current_ma:.3f}mA at 3.6V node")
