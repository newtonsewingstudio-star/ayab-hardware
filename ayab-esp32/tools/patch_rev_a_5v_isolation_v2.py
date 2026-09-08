#!/usr/bin/env python3
"""Apply LM66100 isolation with coordinate-scoped R406 validation."""

from __future__ import annotations

import re
import patch_rev_a_5v_isolation as base


def main() -> None:
    text = base.PSU.read_text()
    if 'LM66100DCKR' in text and 'MACHINE_5V_RAW' in text:
        print('5V isolation already present')
        return

    text = base.add_lib_symbol(text)

    target_token = '(symbol (lib_id "ayab-lib:R_Small_US") (at 264.16 54.61 90)'
    text, r406_5v = base.remove_block(text, target_token)
    text = base.remove_wire(text, (257.81, 54.61), (261.62, 54.61))
    text = base.remove_wire(text, (266.7, 54.61), (270.51, 54.61))

    ref = base.next_u_ref(text)
    gref_nums = [int(x) for x in re.findall(r'property "Reference" "#PWR(\d+)"', text)]
    gref = f'#PWR{max([719] + gref_nums) + 1}'
    gnd = base.clone_gnd(text, 264.16, 64.77, gref)
    device = base.lm66100_instance(r406_5v, ref)

    payload = ''.join([
        base.wire(('257.81', '54.61'), ('256.54', '54.61')),
        base.wire(('271.78', '54.61'), ('270.51', '54.61')),
        base.wire(('271.78', '52.07'), ('271.78', '54.61')),
        base.wire(('261.62', '62.23'), ('264.16', '62.23')),
        base.wire(('266.7', '62.23'), ('264.16', '62.23')),
        base.wire(('264.16', '62.23'), ('264.16', '64.77')),
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
    ):
        if required not in text:
            raise RuntimeError(f'Missing isolation postcondition: {required}')

    # Only the 0R at the 5V isolation coordinates must disappear. Other local
    # PSU subcircuits legitimately reuse the local reference R406.
    if target_token in text:
        raise RuntimeError('5V R406 jumper still present at 264.16,54.61')

    base.PSU.write_text(text)
    print(f'Replaced 5V R406 jumper with {ref} LM66100 isolation')


if __name__ == '__main__':
    main()
