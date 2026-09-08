#!/usr/bin/env python3
"""Run the Rev A solenoid fail-safe patch with corrected P-MOS gate geometry.

KiCad library-symbol Y coordinates are inverted relative to schematic-sheet Y.
The v1 custom LP9435 symbol placed its Gate pin at library +7.62, which rendered
at sheet y-7.62. The gate network is intentionally below the P-MOS symbol, so
place Gate at library -7.62 to render at sheet y+7.62.
"""

import patch_rev_a_solenoid_failsafe as base

_original_wire = base.wire
_original_pmos_lib = base.pmos_lib


def safe_wire(x1: float, y1: float, x2: float, y2: float) -> str:
    if x1 == x2 and y1 == y2:
        return ''
    return _original_wire(x1, y1, x2, y2)


def corrected_pmos_lib() -> str:
    text = _original_pmos_lib()
    old = '(pin input line (at 0 7.62 270) (length 3.81)'
    new = '(pin input line (at 0 -7.62 90) (length 3.81)'
    if old not in text:
        raise RuntimeError('LP9435 gate-pin template changed unexpectedly')
    return text.replace(old, new, 1)


base.wire = safe_wire
base.pmos_lib = corrected_pmos_lib

if __name__ == '__main__':
    base.main()
