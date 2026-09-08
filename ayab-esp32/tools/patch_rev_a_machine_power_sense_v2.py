#!/usr/bin/env python3
"""Robust wrapper for the Rev A machine-power-sense patch.

The top-level schematic has no local `label` records, while the original patch
used the first local label only as an insertion anchor. This wrapper injects a
temporary syntactically valid label before the first wire, runs the original
patch logic, then removes the temporary label before writing the schematic.
The electrical design is unchanged.
"""

from pathlib import Path
import patch_rev_a_machine_power_sense as base

ANCHOR = '''  (label "__REV_A_PATCH_ANCHOR__" (at 0 0 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid 00000000-0000-0000-0000-000000000001)
  )
'''


def main() -> None:
    top = base.TOP.read_text()
    mcu = base.MCU.read_text()

    if 'MACHINE_PWR_SENSE' not in top:
        pos = top.find('  (wire ')
        if pos < 0:
            raise RuntimeError('Top-level wire anchor not found')
        top = top[:pos] + ANCHOR + top[pos:]

    top2 = base.patch_top(top).replace(ANCHOR, '')
    mcu2 = base.patch_mcu(mcu)

    if 'MACHINE_PWR_SENSE' not in top2 or 'MACHINE_PWR_SENSE' not in mcu2:
        raise RuntimeError('Machine-power sense postcondition failed')
    if '__REV_A_PATCH_ANCHOR__' in top2:
        raise RuntimeError('Temporary patch anchor leaked into schematic')
    if '(no_connect (at 185.42 82.55)' in mcu2:
        raise RuntimeError('GPIO4 remains no-connected')
    if '0603WAF4702T5E' not in top2 or 'C25819' not in top2:
        raise RuntimeError('47k divider metadata missing')

    base.TOP.write_text(top2)
    base.MCU.write_text(mcu2)
    print('Applied 47k/10k machine-power divider to GPIO4')


if __name__ == '__main__':
    main()
