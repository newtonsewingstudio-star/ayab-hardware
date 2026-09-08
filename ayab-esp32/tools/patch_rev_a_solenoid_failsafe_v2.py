#!/usr/bin/env python3
"""Run the Rev A solenoid fail-safe patch while suppressing zero-length wires."""

import patch_rev_a_solenoid_failsafe as base

_original_wire = base.wire


def safe_wire(x1: float, y1: float, x2: float, y2: float) -> str:
    if x1 == x2 and y1 == y2:
        return ''
    return _original_wire(x1, y1, x2, y2)


base.wire = safe_wire

if __name__ == '__main__':
    base.main()
