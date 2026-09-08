#!/usr/bin/env python3
"""Rev A machine-power-sense patch using the exact known-good GPIO4 hierarchy.

The electrical divider geometry from v3 is retained.  For the sheet-to-sheet
handoff, this revision restores the exact KiCad object identities formerly used
by the working EOL_R_N path at GPIO4 and renames that path to
MACHINE_PWR_SENSE.  This avoids synthesizing new hierarchical connectivity
objects in a file format where ERC has treated otherwise identical fresh
objects as dangling.
"""

from __future__ import annotations

import re
import patch_rev_a_machine_power_sense_v3 as v3
import patch_rev_a_machine_power_sense as base

TOP_PIN_UUID = "2a03a07d-3b69-4a23-8856-706df5086495"
TOP_WIRE_UUID = "85e9aec6-db25-469d-afb9-80e1b884e33e"
MCU_LABEL_UUID = "4388bfaa-9268-40bb-80f0-3369629ba357"
MCU_WIRE_UUID = "780baf1d-3009-40ff-a531-1002d7913e8b"


def extract_block(text: str, start: int) -> tuple[str, int]:
    return base.extract_block(text, start)


def replace_uuid_in_block(text: str, token: str, new_uuid: str) -> str:
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f"Block not found: {token}")
    block, end = extract_block(text, start)
    block2, n = re.subn(r"\(uuid [0-9a-f-]+\)", f"(uuid {new_uuid})", block, count=1)
    if n != 1:
        raise RuntimeError(f"UUID missing in block: {token}")
    return text[:start] + block2 + text[end:]


def remove_wire(text: str, a: tuple[float, float], b: tuple[float, float]) -> str:
    return v3.remove_wire(text, a, b)


def insert_before_first_wire(text: str, payload: str) -> str:
    return v3.insert_before_first_wire(text, payload)


def exact_wire(a: tuple[str, str], b: tuple[str, str], uuid: str) -> str:
    return (
        f'  (wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]}))\n'
        '    (stroke (width 0) (type default))\n'
        f'    (uuid {uuid})\n'
        '  )\n'
    )


def main() -> None:
    # Run v3 logic in-memory, but intercept its writes by reproducing its steps.
    top = base.TOP.read_text()
    mcu = base.MCU.read_text()

    if 'MACHINE_PWR_SENSE' not in top:
        p = top.find('  (wire ')
        if p < 0:
            raise RuntimeError('Top-level wire anchor not found')
        top = top[:p] + v3.ANCHOR + top[p:]

    top2 = base.patch_top(top).replace(v3.ANCHOR, '')
    mcu2 = base.patch_mcu(mcu)

    top2 = v3.replace_symbol_by_ref(top2, 'R104', (157.48, 142.24))
    top2 = v3.replace_symbol_by_ref(top2, '#PWR107', (149.86, 132.08))
    top2 = v3.replace_symbol_by_ref(top2, '#PWR108', (160.02, 147.32))

    top2 = remove_wire(top2, (152.4, 139.7), (152.4, 142.24))
    top2 = remove_wire(top2, (152.4, 142.24), (140.97, 142.24))
    top2 = v3.remove_junction(top2, 152.4, 142.24)

    # Divider geometry is the same as v3, but terminate at x=160.02 and restore
    # the exact old parent wire from the sheet edge (140.97) to x=160.02.
    wiring = ''.join([
        base.wire('149.86', '132.08', '149.86', '137.16'),
        base.wire('154.94', '137.16', '154.94', '142.24'),
        base.wire('154.94', '142.24', '160.02', '142.24'),
        exact_wire(('140.97', '142.24'), ('160.02', '142.24'), TOP_WIRE_UUID),
        base.wire('160.02', '142.24', '160.02', '147.32'),
        (
            '  (junction (at 154.94 142.24) (diameter 0) (color 0 0 0 0)\n'
            f'    (uuid {base.uid()})\n'
            '  )\n'
        ),
        (
            '  (junction (at 160.02 142.24) (diameter 0) (color 0 0 0 0)\n'
            f'    (uuid {base.uid()})\n'
            '  )\n'
        ),
    ])
    top2 = insert_before_first_wire(top2, wiring)

    # Restore exact known-good identity for the former EOL_R_N parent pin.
    top2 = replace_uuid_in_block(
        top2,
        '(pin "MACHINE_PWR_SENSE" input (at 140.97 142.24 0)',
        TOP_PIN_UUID,
    )

    # Restore exact known-good child wire/label identities and wire direction.
    mcu2 = remove_wire(mcu2, (185.42, 82.55), (198.12, 82.55))
    mcu2 = insert_before_first_wire(
        mcu2,
        exact_wire(('198.12', '82.55'), ('185.42', '82.55'), MCU_WIRE_UUID),
    )
    mcu2 = replace_uuid_in_block(
        mcu2,
        '(hierarchical_label "MACHINE_PWR_SENSE" (shape input) (at 198.12 82.55 0)',
        MCU_LABEL_UUID,
    )

    # Hard postconditions.
    for required in (
        f'(uuid {TOP_PIN_UUID})',
        f'(uuid {TOP_WIRE_UUID})',
        f'(uuid {MCU_LABEL_UUID})',
        f'(uuid {MCU_WIRE_UUID})',
        '0603WAF4702T5E', 'C25819', '0603WAF1002T5E', 'C25804',
        'MACHINE_PWR_SENSE',
    ):
        if required not in top2 + mcu2:
            raise RuntimeError(f'Missing known-good hierarchy postcondition: {required}')
    if '(no_connect (at 185.42 82.55)' in mcu2:
        raise RuntimeError('GPIO4 remains no-connected')

    base.TOP.write_text(top2)
    base.MCU.write_text(mcu2)
    print('Applied machine-power divider using restored known-good GPIO4 hierarchy')


if __name__ == '__main__':
    main()
