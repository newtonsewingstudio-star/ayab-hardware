#!/usr/bin/env python3
"""Compatibility wrapper for the Rev A solenoid partition stage.

KiCad 9's GetNetcodeFromNetname() raises IndexError for a missing net instead
of returning zero.  Patch only that lookup behavior before executing the v1
fail-closed geometry/routing stage unchanged.
"""
from pathlib import Path

SRC = Path(__file__).with_name("stage_rev_a_solenoid_partition.py")
text = SRC.read_text(encoding="utf-8")
old = '''if board.GetNetcodeFromNetname(SW) > 0:
    raise RuntimeError(f"{SW} already exists; refusing partial-state migration")'''
new = '''try:
    _existing_sw = board.GetNetcodeFromNetname(SW)
except (IndexError, KeyError):
    _existing_sw = 0
if _existing_sw > 0:
    raise RuntimeError(f"{SW} already exists; refusing partial-state migration")'''
if text.count(old) != 1:
    raise RuntimeError("partition v1 missing-net lookup anchor changed")
text = text.replace(old, new, 1)
exec(compile(text, str(SRC), "exec"), {"__name__": "__main__", "__file__": str(SRC)})
