#!/usr/bin/env python3
"""Rev A machine-power-sense patch with ERC-correct divider geometry.

The existing top-level resistor instance used as a clone source is rotated 90
 degrees, so its pins are horizontal (center +/- 2.54 mm on X). Earlier staged
 geometry treated those pins as vertical; ERC correctly rejected it.

This revision keeps the same electrical design (47k/10k divider to GPIO4) but
places and wires the cloned horizontal resistor symbols according to their real
pin coordinates.
"""

from __future__ import annotations

import re
from pathlib import Path
import patch_rev_a_machine_power_sense as base

ANCHOR = '''  (label "__REV_A_PATCH_ANCHOR__" (at 0 0 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid 00000000-0000-0000-0000-000000000001)
  )
'''


def extract_block(text: str, start: int) -> tuple[str, int]:
    return base.extract_block(text, start)


def replace_symbol_by_ref(text: str, ref: str, new_center: tuple[float, float]) -> str:
    marker = f'(property "Reference" "{ref}"'
    p = text.find(marker)
    if p < 0:
        raise RuntimeError(f"Reference not found: {ref}")
    start = text.rfind('(symbol ', 0, p)
    if start < 0:
        raise RuntimeError(f"Symbol start not found: {ref}")
    block, end = extract_block(text, start)
    m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', block)
    if not m:
        raise RuntimeError(f"Symbol position not found: {ref}")
    ox, oy = float(m.group(1)), float(m.group(2))
    shifted = base.shift_at_coordinates(block, new_center[0] - ox, new_center[1] - oy)
    return text[:start] + shifted + text[end:]


def remove_wire(text: str, a: tuple[float, float], b: tuple[float, float]) -> str:
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


def remove_junction(text: str, x: float, y: float) -> str:
    pat = re.compile(
        rf'\n\s*\(junction \(at {re.escape(str(x))} {re.escape(str(y))}\) '
        rf'\(diameter 0\) \(color 0 0 0 0\)\s*\(uuid [0-9a-f-]+\)\s*\)'
    )
    return pat.sub('', text, count=1)


def insert_before_first_wire(text: str, payload: str) -> str:
    p = text.find('  (wire ')
    if p < 0:
        raise RuntimeError('Top-level wire anchor not found')
    return text[:p] + payload + text[p:]


def main() -> None:
    top = base.TOP.read_text()
    mcu = base.MCU.read_text()

    if 'MACHINE_PWR_SENSE' not in top:
        p = top.find('  (wire ')
        if p < 0:
            raise RuntimeError('Top-level wire anchor not found')
        top = top[:p] + ANCHOR + top[p:]

    top2 = base.patch_top(top).replace(ANCHOR, '')
    mcu2 = base.patch_mcu(mcu)

    # The baseline branch currently yields R103/R104 and #PWR107/#PWR108.
    # Move the low-side resistor and power symbols so the real horizontal pins
    # connect cleanly without diagonal or ambiguous wire geometry.
    top2 = replace_symbol_by_ref(top2, 'R104', (157.48, 142.24))
    top2 = replace_symbol_by_ref(top2, '#PWR107', (149.86, 132.08))
    top2 = replace_symbol_by_ref(top2, '#PWR108', (160.02, 147.32))

    # Remove the incorrect vertical-resistor wiring inserted by v1/v2.
    top2 = remove_wire(top2, (152.4, 139.7), (152.4, 142.24))
    top2 = remove_wire(top2, (152.4, 142.24), (140.97, 142.24))
    top2 = remove_junction(top2, 152.4, 142.24)

    # Actual pin geometry after placement:
    # R103 center 152.40,137.16 rot90 -> pins 149.86 and 154.94 on Y=137.16
    # R104 center 157.48,142.24 rot90 -> pins 154.94 and 160.02 on Y=142.24
    # Divider midpoint is therefore x=154.94 between the two resistors.
    wiring = ''.join([
        base.wire('149.86', '132.08', '149.86', '137.16'),
        base.wire('154.94', '137.16', '154.94', '142.24'),
        base.wire('154.94', '142.24', '140.97', '142.24'),
        base.wire('160.02', '142.24', '160.02', '147.32'),
        (
            '  (junction (at 154.94 142.24) (diameter 0) (color 0 0 0 0)\n'
            f'    (uuid {base.uid()})\n'
            '  )\n'
        ),
    ])
    top2 = insert_before_first_wire(top2, wiring)

    # Hard postconditions.
    if 'MACHINE_PWR_SENSE' not in top2 or 'MACHINE_PWR_SENSE' not in mcu2:
        raise RuntimeError('Machine-power sense postcondition failed')
    if '(no_connect (at 185.42 82.55)' in mcu2:
        raise RuntimeError('GPIO4 remains no-connected')
    for required in ('0603WAF4702T5E', 'C25819', '0603WAF1002T5E', 'C25804'):
        if required not in top2:
            raise RuntimeError(f'Missing divider metadata: {required}')
    if '__REV_A_PATCH_ANCHOR__' in top2:
        raise RuntimeError('Temporary patch anchor leaked into schematic')

    base.TOP.write_text(top2)
    base.MCU.write_text(mcu2)
    print('Applied ERC-correct 47k/10k machine-power divider to GPIO4')


if __name__ == '__main__':
    main()
