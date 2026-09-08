#!/usr/bin/env python3
"""Complete Rev A solenoid fail-safe schematic with a switched-rail test point.

The fail-safe gate itself is already present. This patch adds an explicit
SOLENOID_12V_SW test point to the solenoid sheet so board bring-up can verify
that coil power is truly absent until SOLENOID_PWR_EN is asserted.
"""

from __future__ import annotations

import re

import patch_rev_a_solenoid_failsafe_v3 as v3

base = v3.base
SOL = base.SOL


def relocate_testpoint(block: str, x: float, y: float, new_ref: str) -> str:
    m = re.search(r'\(symbol \(lib_id "ayab-lib:TestPoint"\) \(at\s+([-\d.]+)\s+([-\d.]+)', block)
    if not m:
        raise RuntimeError('TestPoint coordinate not found')
    ox, oy = float(m.group(1)), float(m.group(2))
    dx, dy = x - ox, y - oy

    def move_at(match: re.Match) -> str:
        xx = float(match.group(1)) + dx
        yy = float(match.group(2)) + dy
        rot = match.group(3) or ''
        return f'(at {xx:g} {yy:g}{rot})'

    out = re.sub(r'\(at\s+([-\d.]+)\s+([-\d.]+)(\s+[-\d.]+)?\)', move_at, block)
    out = out.replace('"TP301"', f'"{new_ref}"')
    out = out.replace('"MCP_INTA"', '"SOL12_SW"')
    out = re.sub(r'\(uuid [0-9a-f-]+\)', lambda _: f'(uuid {base.uid()})', out)
    return out


def main() -> None:
    text = SOL.read_text()
    if '"SOL12_SW"' in text:
        print('SOLENOID_12V_SW test point already present')
        return
    if 'SOLENOID_12V_SW' not in text or 'LP9435LT1G' not in text:
        raise RuntimeError('Solenoid fail-safe gate must exist before adding its test point')

    template = base.get_block(text, '(symbol (lib_id "ayab-lib:TestPoint") (at 68.58 87.63 90)')
    ref = base.next_ref('TP')
    tp_x, tp_y = 248.92, 172.72
    tp = relocate_testpoint(template, tp_x, tp_y, ref)

    # The P-MOS drain is already wired to (248.92, 167.64) and carries the
    # switched rail. Extend that node vertically to the test-point pin.
    test_wire = base.wire(248.92, 167.64, tp_x, tp_y)
    p = text.find('  (wire ')
    if p < 0:
        raise RuntimeError('Solenoid wire anchor missing')
    text = text[:p] + test_wire + '\n' + text[p:]
    text = base.insert_before_root_close(text, [tp])

    if f'"{ref}"' not in text or '"SOL12_SW"' not in text:
        raise RuntimeError('Test-point postcondition failed')
    if '(wire (pts (xy 248.92 167.64) (xy 248.92 172.72))' not in text:
        raise RuntimeError('Switched-rail test-point wire missing')

    SOL.write_text(text)
    print(f'Added {ref} SOL12_SW test point on SOLENOID_12V_SW')


if __name__ == '__main__':
    main()
