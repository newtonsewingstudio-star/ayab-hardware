#!/usr/bin/env python3
"""Ensure native ESP32-S3 USB is connected to the correct MCU sheet rows.

KiCad sheet coordinates increase downward, so the ESP32-S3-MINI library pin rows
are vertically inverted relative to the library symbol definition. The correct
sheet locations are:
- GPIO19 / USB D-: y=67.31
- GPIO20 / USB D+: y=64.77
- GPIO38 / buzzer: y=118.11
- GPIO45 / VCC_SPI strapping row: y=120.65

This script restores those upstream-correct connections if an earlier audit-axis
mistake moved them. It is assertion-heavy and idempotent.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "mcu.kicad_sch"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one occurrence, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    text = PATH.read_text(encoding="utf-8")

    correct_markers = [
        '(hierarchical_label "USB_M" (shape bidirectional) (at 198.12 67.31 0)',
        '(hierarchical_label "USB_P" (shape bidirectional) (at 198.12 64.77 0)',
        '(label "BUZZER" (at 198.12 118.11 180)',
        '(label "VCC_SPI" (at 198.12 120.65 180)',
    ]
    if all(marker in text for marker in correct_markers):
        print("Native USB/buzzer/VCC_SPI MCU mapping already correct")
        return

    # Undo the erroneous vertically-inverted mapping if present.
    text = replace_once(
        text,
        '(hierarchical_label "USB_M" (shape bidirectional) (at 198.12 118.11 0)',
        '(hierarchical_label "USB_M" (shape bidirectional) (at 198.12 67.31 0)',
        "USB_M label",
    )
    text = replace_once(
        text,
        '(label "BUZZER" (at 198.12 67.31 180)',
        '(label "BUZZER" (at 198.12 118.11 180)',
        "BUZZER label",
    )
    text = replace_once(
        text,
        '(hierarchical_label "USB_P" (shape bidirectional) (at 198.12 120.65 0)',
        '(hierarchical_label "USB_P" (shape bidirectional) (at 198.12 64.77 0)',
        "USB_P label",
    )

    # Restore the local GPIO45/VCC_SPI label removed by the erroneous patch.
    if '(label "VCC_SPI" (at 198.12 120.65 180)' not in text:
        anchor = '  (label "ESP14" (at 198.12 107.95 180)'
        block = '''  (label "VCC_SPI" (at 198.12 120.65 180) (fields_autoplaced)\n    (effects (font (size 1.27 1.27)) (justify right bottom))\n    (uuid f1f8d09c-bb40-4cd2-b2a8-64507c3c2397)\n  )\n'''
        pos = text.find(anchor)
        if pos < 0:
            raise RuntimeError("VCC_SPI insertion anchor not found")
        text = text[:pos] + block + text[pos:]

    # Correct the three wire rows. UUIDs identify the original logical wires.
    wrong_to_right = {
        '''(wire (pts (xy 185.42 118.11) (xy 198.12 118.11))\n    (stroke (width 0) (type default))\n    (uuid b6d2f484-9bee-4259-90e9-0a57fede749c)\n  )''':
        '''(wire (pts (xy 185.42 67.31) (xy 198.12 67.31))\n    (stroke (width 0) (type default))\n    (uuid b6d2f484-9bee-4259-90e9-0a57fede749c)\n  )''',
        '''(wire (pts (xy 185.42 67.31) (xy 198.12 67.31))\n    (stroke (width 0) (type default))\n    (uuid 6c8d4e5b-64d5-4725-8ab2-a8260da28abb)\n  )''':
        '''(wire (pts (xy 185.42 118.11) (xy 198.12 118.11))\n    (stroke (width 0) (type default))\n    (uuid 6c8d4e5b-64d5-4725-8ab2-a8260da28abb)\n  )''',
        '''(wire (pts (xy 185.42 120.65) (xy 198.12 120.65))\n    (stroke (width 0) (type default))\n    (uuid 3983eb93-9526-48db-85d8-1875e8cba104)\n  )''':
        '''(wire (pts (xy 185.42 64.77) (xy 198.12 64.77))\n    (stroke (width 0) (type default))\n    (uuid 3983eb93-9526-48db-85d8-1875e8cba104)\n  )''',
    }
    for wrong, right in wrong_to_right.items():
        text = replace_once(text, wrong, right, "MCU wire restoration")

    # Restore the original VCC_SPI wire if missing.
    vcc_wire = '''(wire (pts (xy 185.42 120.65) (xy 198.12 120.65))\n    (stroke (width 0) (type default))\n    (uuid 2db3c421-da0a-412a-bfa1-93464a1ea3c6)\n  )'''
    if vcc_wire not in text:
        anchor = '(wire (pts (xy 185.42 118.11) (xy 198.12 118.11))'
        pos = text.find(anchor)
        if pos < 0:
            raise RuntimeError("VCC_SPI wire insertion anchor not found")
        text = text[:pos] + vcc_wire + "\n  " + text[pos:]

    # Hard postconditions.
    for marker in correct_markers:
        if marker not in text:
            raise RuntimeError(f"postcondition missing: {marker}")
    expected_wires = [
        '(xy 185.42 67.31) (xy 198.12 67.31)',
        '(xy 185.42 64.77) (xy 198.12 64.77)',
        '(xy 185.42 118.11) (xy 198.12 118.11)',
        '(xy 185.42 120.65) (xy 198.12 120.65)',
    ]
    for wire in expected_wires:
        if text.count(wire) != 1:
            raise RuntimeError(f"expected exactly one MCU wire at {wire}")

    PATH.write_text(text, encoding="utf-8")
    print("Restored correct native USB/buzzer/VCC_SPI MCU mapping")


if __name__ == "__main__":
    main()
