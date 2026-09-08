#!/usr/bin/env python3
"""Implement Rev A machine-power sensing locally on the MCU sheet.

This avoids an unnecessary hierarchical handoff that KiCad 9 ERC continued to
flag as dangling despite matching the former EOL_R_N geometry.

Electrical design is unchanged:
    +12V -> 47k -> MACHINE_PWR_SENSE -> 10k -> GND
                                      |
                                   GPIO4/ADC1_CH3

At 12 V the ADC sees ~2.105 V.  3.3 V corresponds to ~18.81 V input.
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCU = ROOT / "mcu.kicad_sch"
TOP = ROOT / "ayab-esp32.kicad_sch"


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
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return text[start:i + 1], i + 1
    raise RuntimeError('Unbalanced KiCad block')


def shift_at_coordinates(block: str, dx: float, dy: float) -> str:
    pat = re.compile(r"\(at\s+([-\d.]+)\s+([-\d.]+)(\s+[-\d.]+)?\)")
    def repl(m: re.Match) -> str:
        x = round(float(m.group(1)) + dx, 4)
        y = round(float(m.group(2)) + dy, 4)
        suffix = m.group(3) or ''
        return f"(at {x:g} {y:g}{suffix})"
    return pat.sub(repl, block)


def clone_concrete(text: str, token: str, new_x: float, new_y: float, old_ref: str, new_ref: str) -> str:
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f'Clone source not found: {token}')
    block, _ = extract_block(text, start)
    m = re.search(r"\(at\s+([-\d.]+)\s+([-\d.]+)", block)
    if not m:
        raise RuntimeError('Clone source position missing')
    ox, oy = float(m.group(1)), float(m.group(2))
    block = shift_at_coordinates(block, new_x - ox, new_y - oy)
    block = block.replace(f'"{old_ref}"', f'"{new_ref}"')
    block = re.sub(r'\(uuid [0-9a-f-]+\)', lambda _: f'(uuid {uid()})', block)
    return block


def next_ref(text: str, prefix: str, minimum: int) -> str:
    nums = [int(x) for x in re.findall(rf'property "Reference" "{re.escape(prefix)}(\d+)"', text)]
    return f'{prefix}{max([minimum - 1] + nums) + 1}'


def ensure_12v_lib_symbol(mcu: str, top: str) -> str:
    if '(symbol "power:+12V"' in mcu:
        return mcu
    start = top.find('(symbol "power:+12V"')
    if start < 0:
        raise RuntimeError('Top-level +12V library symbol definition missing')
    block, _ = extract_block(top, start)
    anchor = '    (symbol "power:GND"'
    pos = mcu.find(anchor)
    if pos < 0:
        raise RuntimeError('MCU lib_symbols GND anchor missing')
    return mcu[:pos] + '    ' + block + '\n' + mcu[pos:]


def wire(a: tuple[str, str], b: tuple[str, str]) -> str:
    return (
        f'  (wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]}))\n'
        '    (stroke (width 0) (type default))\n'
        f'    (uuid {uid()})\n'
        '  )\n'
    )


def insert_before_first_wire(text: str, payload: str) -> str:
    p = text.find('  (wire ')
    if p < 0:
        raise RuntimeError('Wire insertion anchor missing')
    return text[:p] + payload + text[p:]


def insert_before_root_close(text: str, blocks: list[str]) -> str:
    p = text.rfind('\n)')
    if p < 0:
        raise RuntimeError('Root close missing')
    return text[:p] + '\n' + '\n'.join(blocks) + '\n' + text[p:]


def main() -> None:
    mcu = MCU.read_text()
    top = TOP.read_text()

    if '(label "MACHINE_PWR_SENSE"' in mcu:
        print('Machine-power sensing already present')
        return

    mcu = ensure_12v_lib_symbol(mcu, top)

    # Remove the intentional temporary no-connect from GPIO4.
    mcu, n = re.subn(
        r'\n\s*\(no_connect \(at 185\.42 82\.55\) \(uuid [0-9a-f-]+\)\)',
        '', mcu, count=1,
    )
    if n != 1:
        raise RuntimeError('GPIO4 no-connect marker not found')

    r_src = '(symbol (lib_id "ayab-lib:R_Small_US") (at 205.74 105.41 0)'
    g_src = '(symbol (lib_id "power:GND") (at 33.02 135.89 0)'

    r_hi_ref = next_ref(mcu, 'R', 215)
    r_lo_ref = f'R{int(r_hi_ref[1:]) + 1}'
    pwr_ref = next_ref(mcu, '#PWR', 215)
    gnd_ref = f'#PWR{int(pwr_ref[4:]) + 1}'

    r_hi = clone_concrete(mcu, r_src, 205.74, 80.01, 'R213', r_hi_ref)
    r_hi = re.sub(r'(property "Value" ")[^"]+', r'\g<1>47k', r_hi, count=1)
    r_hi = re.sub(r'(property "LCSC ID" ")[^"]+', r'\g<1>C25819', r_hi, count=1)
    r_hi = re.sub(r'(property "OEM PN" ")[^"]+', r'\g<1>0603WAF4702T5E', r_hi, count=1)

    r_lo = clone_concrete(mcu, r_src, 205.74, 85.09, 'R213', r_lo_ref)

    # Clone an MCU-sheet GND instance twice so the hierarchical instance path
    # remains correct. Transform one clone into +12V after shifting it.
    gnd = clone_concrete(mcu, g_src, 205.74, 87.63, '#PWR0201', gnd_ref)
    p12 = clone_concrete(mcu, g_src, 205.74, 77.47, '#PWR0201', pwr_ref)
    p12 = p12.replace('(lib_id "power:GND")', '(lib_id "power:+12V")', 1)
    p12 = p12.replace('(property "Value" "GND"', '(property "Value" "+12V"', 1)

    label = (
        '  (label "MACHINE_PWR_SENSE" (at 198.12 82.55 0) (fields_autoplaced)\n'
        '    (effects (font (size 1.27 1.27)) (justify left bottom))\n'
        f'    (uuid {uid()})\n'
        '  )\n'
    )
    wiring = ''.join([
        wire(('185.42', '82.55'), ('205.74', '82.55')),
        (
            '  (junction (at 205.74 82.55) (diameter 0) (color 0 0 0 0)\n'
            f'    (uuid {uid()})\n'
            '  )\n'
        ),
        label,
    ])
    mcu = insert_before_first_wire(mcu, wiring)
    mcu = insert_before_root_close(mcu, [r_hi, r_lo, p12, gnd])

    for required in (
        'MACHINE_PWR_SENSE', '47k', 'C25819', '0603WAF4702T5E',
        '10k', 'C25804', '(lib_id "power:+12V")',
    ):
        if required not in mcu:
            raise RuntimeError(f'Missing postcondition: {required}')
    if '(no_connect (at 185.42 82.55)' in mcu:
        raise RuntimeError('GPIO4 still marked no-connect')
    if '(hierarchical_label "MACHINE_PWR_SENSE"' in mcu:
        raise RuntimeError('Hierarchy dependency unexpectedly remains')

    MCU.write_text(mcu)
    print('Applied local 47k/10k +12V machine-power divider to GPIO4')


if __name__ == '__main__':
    main()
