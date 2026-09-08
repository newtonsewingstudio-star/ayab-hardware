#!/usr/bin/env python3
"""Add Rev A machine-power sensing on ESP32-S3 GPIO4.

Electrical change:
- existing +12V machine rail -> 47k / 10k divider -> MACHINE_PWR_SENSE
- divider output -> ESP32 GPIO4 / ADC1_CH3
- GPIO4 temporary no-connect removed

47k / 10k gives approximately 2.105 V at 12 V and reaches 3.3 V at
approximately 18.81 V, providing useful headroom above the nominal machine rail.
Parts:
- 47k: UNI-ROYAL 0603WAF4702T5E, LCSC C25819
- 10k: UNI-ROYAL 0603WAF1002T5E, LCSC C25804
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT / "ayab-esp32.kicad_sch"
MCU = ROOT / "mcu.kicad_sch"


def uid() -> str:
    return str(uuid.uuid4())


def extract_block(text: str, start: int) -> tuple[str, int]:
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start:i + 1], i + 1
    raise RuntimeError("Unbalanced KiCad block")


def find_sheet(text: str, sheetfile: str) -> tuple[int, int, str]:
    pos = 0
    while True:
        start = text.find("(sheet ", pos)
        if start < 0:
            raise RuntimeError(f"Sheet not found: {sheetfile}")
        block, end = extract_block(text, start)
        if f'(property "Sheetfile" "{sheetfile}"' in block:
            return start, end, block
        pos = end


def shift_at_coordinates(block: str, dx: float, dy: float) -> str:
    pattern = re.compile(r"\(at\s+([-\d.]+)\s+([-\d.]+)(\s+[-\d.]+)?\)")
    def repl(m: re.Match) -> str:
        x = round(float(m.group(1)) + dx, 4)
        y = round(float(m.group(2)) + dy, 4)
        suffix = m.group(3) or ""
        return f"(at {x:g} {y:g}{suffix})"
    return pattern.sub(repl, block)


def clone_symbol(text: str, token: str, new_x: float, new_y: float, old_ref: str, new_ref: str) -> str:
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f"Clone source not found: {token}")
    block, _ = extract_block(text, start)
    pos_m = re.search(r"\(at\s+([-\d.]+)\s+([-\d.]+)", block)
    if not pos_m:
        raise RuntimeError("Clone source position missing")
    old_x, old_y = float(pos_m.group(1)), float(pos_m.group(2))
    block = shift_at_coordinates(block, new_x - old_x, new_y - old_y)
    block = block.replace(f'"{old_ref}"', f'"{new_ref}"')
    block = re.sub(r"\(uuid [0-9a-f-]+\)", lambda _: f"(uuid {uid()})", block)
    return block


def next_numeric_ref(text: str, prefix: str, minimum: int) -> str:
    nums = [int(x) for x in re.findall(rf'property "Reference" "{re.escape(prefix)}(\d+)"', text)]
    return f"{prefix}{max([minimum - 1] + nums) + 1}"


def update_resistor(block: str, value: str, lcsc: str, mpn: str) -> str:
    block = re.sub(r'(property "Value" ")[^"]+(" )', rf'\g<1>{value}\g<2>', block, count=1)
    block = re.sub(r'(property "LCSC ID" ")[^"]+(" )', rf'\g<1>{lcsc}\g<2>', block, count=1)
    block = re.sub(r'(property "OEM PN" ")[^"]+(" )', rf'\g<1>{mpn}\g<2>', block, count=1)
    block = re.sub(r'(property "OEM" ")[^"]+(" )', r'\g<1>UNI-ROYAL(Uniroyal Elec)\g<2>', block, count=1)
    return block


def insert_before_final_close(text: str, blocks: list[str]) -> str:
    pos = text.rfind("\n)")
    if pos < 0:
        raise RuntimeError("Root closing parenthesis not found")
    return text[:pos] + "\n" + "\n".join(blocks) + "\n" + text[pos:]


def wire(x1: str, y1: str, x2: str, y2: str) -> str:
    return (
        f'  (wire (pts (xy {x1} {y1}) (xy {x2} {y2}))\n'
        '    (stroke (width 0) (type default))\n'
        f'    (uuid {uid()})\n'
        '  )\n'
    )


def patch_top(text: str) -> str:
    if 'MACHINE_PWR_SENSE' in text:
        return text

    # Add matching hierarchical pin to MCU sheet at the old freed EOL location.
    s, e, sheet = find_sheet(text, "mcu.kicad_sch")
    anchor = "    (instances\n"
    if anchor not in sheet:
        raise RuntimeError("MCU sheet instance anchor not found")
    pin = (
        '    (pin "MACHINE_PWR_SENSE" input (at 140.97 142.24 0)\n'
        '      (effects (font (size 1.27 1.27)) (justify right))\n'
        f'      (uuid {uid()})\n'
        '    )\n'
    )
    sheet = sheet.replace(anchor, pin + anchor, 1)
    text = text[:s] + sheet + text[e:]

    # Clone existing top-level resistor and power symbols.
    r_src = '(symbol (lib_id "ayab-lib:R_Small_US") (at 68.58 81.28 90)'
    p12_src = '(symbol (lib_id "power:+12V") (at 68.58 31.75 0)'
    gnd_src = '(symbol (lib_id "power:GND")'

    r_hi_ref = next_numeric_ref(text, "R", 103)
    r_lo_ref = f"R{int(r_hi_ref[1:]) + 1}"
    pwr_ref = next_numeric_ref(text, "#PWR", 103)
    gnd_ref = f"#PWR{int(pwr_ref[4:]) + 1}"

    r_hi = clone_symbol(text, r_src, 152.4, 137.16, "R101", r_hi_ref)
    r_hi = update_resistor(r_hi, "47k", "C25819", "0603WAF4702T5E")
    r_lo = clone_symbol(text, r_src, 152.4, 144.78, "R101", r_lo_ref)
    r_lo = update_resistor(r_lo, "10k", "C25804", "0603WAF1002T5E")
    p12 = clone_symbol(text, p12_src, 152.4, 134.62, "#PWR0101", pwr_ref)

    # Find a concrete GND symbol instance and clone it.
    gstart = text.find(gnd_src)
    while gstart >= 0:
        block, _ = extract_block(text, gstart)
        if '(lib_id "power:GND")' in block and '(at ' in block and '(property "Reference" "#PWR' in block:
            mref = re.search(r'property "Reference" "([^"]+)"', block)
            mpos = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', block)
            if mref and mpos:
                old_ref = mref.group(1)
                old_x, old_y = float(mpos.group(1)), float(mpos.group(2))
                gnd = shift_at_coordinates(block, 152.4 - old_x, 147.32 - old_y)
                gnd = gnd.replace(f'"{old_ref}"', f'"{gnd_ref}"')
                gnd = re.sub(r"\(uuid [0-9a-f-]+\)", lambda _: f"(uuid {uid()})", gnd)
                break
        gstart = text.find(gnd_src, gstart + 1)
    else:
        raise RuntimeError("Concrete GND symbol instance not found")

    # Components are vertical: high-side pins 134.62/139.70; low-side pins 142.24/147.32.
    electrical = [
        wire("152.4", "139.7", "152.4", "142.24"),
        wire("152.4", "142.24", "140.97", "142.24"),
        (
            f'  (junction (at 152.4 142.24) (diameter 0) (color 0 0 0 0)\n'
            f'    (uuid {uid()})\n'
            '  )\n'
        ),
    ]

    # Insert wires before first label; components before root close.
    pos = text.find("  (label ")
    if pos < 0:
        raise RuntimeError("Top-level label anchor not found")
    text = text[:pos] + "".join(electrical) + text[pos:]
    text = insert_before_final_close(text, [r_hi, r_lo, p12, gnd])
    return text


def patch_mcu(text: str) -> str:
    if '(hierarchical_label "MACHINE_PWR_SENSE"' in text:
        return text

    nc = re.compile(r'\n\s*\(no_connect \(at 185\.42 82\.55\) \(uuid [0-9a-f-]+\)\)')
    text, n = nc.subn('', text, count=1)
    if n != 1:
        raise RuntimeError("GPIO4 no-connect marker not found")

    label = (
        '  (hierarchical_label "MACHINE_PWR_SENSE" (shape input) (at 198.12 82.55 0) (fields_autoplaced)\n'
        '    (effects (font (size 1.27 1.27)) (justify left))\n'
        f'    (uuid {uid()})\n'
        '  )\n'
    )
    w = wire("185.42", "82.55", "198.12", "82.55")
    pos = text.find("  (label ")
    if pos < 0:
        raise RuntimeError("MCU label anchor not found")
    text = text[:pos] + w + label + text[pos:]
    return text


def main() -> None:
    top = TOP.read_text()
    mcu = MCU.read_text()
    top2 = patch_top(top)
    mcu2 = patch_mcu(mcu)

    for hay, needle in ((top2, 'MACHINE_PWR_SENSE'), (mcu2, 'MACHINE_PWR_SENSE')):
        if needle not in hay:
            raise RuntimeError(f"Postcondition missing: {needle}")
    if '(no_connect (at 185.42 82.55)' in mcu2:
        raise RuntimeError("GPIO4 remains no-connected")
    if '0603WAF4702T5E' not in top2 or 'C25819' not in top2:
        raise RuntimeError("47k divider metadata missing")

    TOP.write_text(top2)
    MCU.write_text(mcu2)
    print("Applied 47k/10k machine-power divider to GPIO4")


if __name__ == "__main__":
    main()
