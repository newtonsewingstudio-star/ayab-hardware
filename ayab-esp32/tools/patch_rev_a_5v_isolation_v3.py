#!/usr/bin/env python3
"""Apply the Rev A LM66100 isolation with ERC-correct power modeling.

Corrections over v2:
- move the existing 5V PWR_FLAG from SYS_5V to MACHINE_5V_RAW so LM66100 VIN is
  recognized as driven;
- let LM66100 VOUT be the sole power-output driver of the system 5V rail;
- model ST as passive while hard-tying it to GND, an allowed unused-ST wiring;
- rebuild VOUT directly to the PSU hierarchical 5V output instead of retaining
  the former R406/PWR_FLAG junction chain.
"""

from __future__ import annotations

import re
import patch_rev_a_5v_isolation as base


def extract_block(text: str, start: int) -> tuple[str, int]:
    return base.extract_block(text, start)


def shift_symbol_instance(text: str, token: str, new_x: float, new_y: float) -> str:
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f'Symbol instance not found: {token}')
    block, end = extract_block(text, start)
    m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', block)
    if not m:
        raise RuntimeError('Symbol origin missing')
    ox, oy = float(m.group(1)), float(m.group(2))
    dx, dy = new_x - ox, new_y - oy
    pat = re.compile(r'\(at\s+([-\d.]+)\s+([-\d.]+)(\s+[-\d.]+)?\)')

    def repl(mm: re.Match) -> str:
        x = round(float(mm.group(1)) + dx, 4)
        y = round(float(mm.group(2)) + dy, 4)
        return f"(at {x:g} {y:g}{mm.group(3) or ''})"

    block = pat.sub(repl, block)
    return text[:start] + block + text[end:]


def remove_wire_if_present(text: str, a: tuple[float, float], b: tuple[float, float]) -> str:
    pos = 0
    while True:
        start = text.find('(wire ', pos)
        if start < 0:
            return text
        block, end = extract_block(text, start)
        m = re.search(
            r'\(pts\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\)',
            block, re.S,
        )
        if m:
            p1 = (float(m.group(1)), float(m.group(2)))
            p2 = (float(m.group(3)), float(m.group(4)))
            if {p1, p2} == {a, b}:
                real_start = start
                while real_start > 0 and text[real_start - 1] == ' ':
                    real_start -= 1
                if real_start > 0 and text[real_start - 1] == '\n':
                    real_start -= 1
                if end < len(text) and text[end] == '\n':
                    end += 1
                return text[:real_start] + text[end:]
        pos = end


def remove_junction_if_present(text: str, x: float, y: float) -> str:
    pos = 0
    target = (x, y)
    while True:
        start = text.find('(junction ', pos)
        if start < 0:
            return text
        block, end = extract_block(text, start)
        m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)\)', block)
        if m and (float(m.group(1)), float(m.group(2))) == target:
            real_start = start
            while real_start > 0 and text[real_start - 1] == ' ':
                real_start -= 1
            if real_start > 0 and text[real_start - 1] == '\n':
                real_start -= 1
            if end < len(text) and text[end] == '\n':
                end += 1
            return text[:real_start] + text[end:]
        pos = end


def main() -> None:
    text = base.PSU.read_text()
    if 'LM66100DCKR' in text and 'MACHINE_5V_RAW' in text:
        print('5V isolation already present')
        return

    text = base.add_lib_symbol(text)

    # ST is deliberately hard-grounded when unused. Model it as passive so ERC
    # does not interpret an allowed open-drain-to-GND connection as output clash
    # with the global GND PWR_FLAG.
    old_st = '(pin open_collector line (at -2.54 -7.62 90)'
    new_st = '(pin passive line (at -2.54 -7.62 90)'
    if old_st not in text:
        raise RuntimeError('LM66100 ST library pin definition not found')
    text = text.replace(old_st, new_st, 1)

    target_token = '(symbol (lib_id "ayab-lib:R_Small_US") (at 264.16 54.61 90)'
    text, r406_5v = base.remove_block(text, target_token)
    text = remove_wire_if_present(text, (257.81, 54.61), (261.62, 54.61))
    text = remove_wire_if_present(text, (266.7, 54.61), (270.51, 54.61))

    # Remove the old system-side PWR_FLAG connection and direct output wire.
    # The same PWR_FLAG instance is then moved to MACHINE_5V_RAW.
    text = remove_wire_if_present(text, (270.51, 52.07), (270.51, 54.61))
    text = remove_wire_if_present(text, (270.51, 54.61), (273.05, 54.61))
    text = remove_junction_if_present(text, 270.51, 54.61)
    text = shift_symbol_instance(
        text,
        '(symbol (lib_id "power:PWR_FLAG") (at 270.51 52.07 0)',
        257.81,
        52.07,
    )

    ref = base.next_u_ref(text)
    gref_nums = [int(x) for x in re.findall(r'property "Reference" "#PWR(\d+)"', text)]
    gref = f'#PWR{max([719] + gref_nums) + 1}'
    gnd = base.clone_gnd(text, 264.16, 64.77, gref)
    device = base.lm66100_instance(r406_5v, ref)

    payload = ''.join([
        # Raw filtered 5V -> VIN and raw-side ERC power source marker.
        base.wire(('257.81', '54.61'), ('256.54', '54.61')),
        base.wire(('257.81', '52.07'), ('257.81', '54.61')),
        # VOUT directly drives the PSU hierarchical system-5V output.
        base.wire(('271.78', '54.61'), ('273.05', '54.61')),
        # CE tied to VOUT for TI's always-on reverse-current-blocking mode.
        base.wire(('271.78', '52.07'), ('271.78', '54.61')),
        # ST and GND hard tied to GND.
        base.wire(('261.62', '62.23'), ('264.16', '62.23')),
        base.wire(('266.7', '62.23'), ('264.16', '62.23')),
        base.wire(('264.16', '62.23'), ('264.16', '64.77')),
        (
            '  (junction (at 257.81 54.61) (diameter 0) (color 0 0 0 0)\n'
            f'    (uuid {base.uid()})\n'
            '  )\n'
        ),
        (
            '  (junction (at 271.78 54.61) (diameter 0) (color 0 0 0 0)\n'
            f'    (uuid {base.uid()})\n'
            '  )\n'
        ),
        (
            '  (junction (at 264.16 62.23) (diameter 0) (color 0 0 0 0)\n'
            f'    (uuid {base.uid()})\n'
            '  )\n'
        ),
        (
            '  (label "MACHINE_5V_RAW" (at 257.81 54.61 0) (fields_autoplaced)\n'
            '    (effects (font (size 1.27 1.27)) (justify left bottom))\n'
            f'    (uuid {base.uid()})\n'
            '  )\n'
        ),
    ])

    p = text.find('  (wire ')
    if p < 0:
        raise RuntimeError('Wire insertion anchor not found')
    text = text[:p] + payload + text[p:]
    text = base.insert_before_root_close(text, [device, gnd])

    for required in (
        'LM66100DCKR', 'C2869734',
        'Package_TO_SOT_SMD:SOT-363_SC-70-6',
        'MACHINE_5V_RAW', '(name "VIN"', '(name "VOUT"', '(name "CE"',
        '(symbol (lib_id "power:PWR_FLAG") (at 257.81 52.07 0)',
    ):
        if required not in text:
            raise RuntimeError(f'Missing isolation postcondition: {required}')

    if target_token in text:
        raise RuntimeError('5V R406 jumper still present at 264.16,54.61')
    if '(symbol (lib_id "power:PWR_FLAG") (at 270.51 52.07 0)' in text:
        raise RuntimeError('System-side 5V PWR_FLAG remains')

    base.PSU.write_text(text)
    print(f'Replaced 5V R406 with ERC-modeled {ref} LM66100 isolation')


if __name__ == '__main__':
    main()
