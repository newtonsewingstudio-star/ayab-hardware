#!/usr/bin/env python3
"""Compatibility wrapper for solenoid partition v3.

v3 first applies the KiCad-9 snapshot patch and then replaces the old
REMOVE/RETAG list block.  Its original end anchor therefore consumed the newly
inserted TRACK_SNAPSHOT line.  v4 changes only that source-text boundary so the
snapshot survives for the later dynamic left-bus retag step.
"""
from pathlib import Path

SRC = Path(__file__).with_name("stage_rev_a_solenoid_partition_v3.py")
text = SRC.read_text(encoding="utf-8")
old = "b = text.index('\\ndef exact_tracks', a)"
new = "b = text.index('\\nTRACK_SNAPSHOT = list(board.GetTracks())', a)"
if text.count(old) != 1:
    raise RuntimeError(f"v3 list-boundary anchor changed: expected 1, got {text.count(old)}")
text = text.replace(old, new, 1)
exec(compile(text, str(SRC), "exec"), {"__name__":"__main__", "__file__":str(SRC)})
