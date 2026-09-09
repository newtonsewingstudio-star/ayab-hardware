#!/usr/bin/env python3
"""Rev A solenoid partition v5.

Apply the two audited v4 corrections directly to the v3 architecture wrapper:
1. preserve TRACK_SNAPSHOT when replacing the old REMOVE/RETAG source block;
2. require the measured 32 raw +12 V F.Cu objects in the tightly bounded left
   solenoid-local bus region.

No electrical geometry, net selection, or clearance criterion is relaxed.
"""
from pathlib import Path

SRC = Path(__file__).with_name("stage_rev_a_solenoid_partition_v3.py")
text = SRC.read_text(encoding="utf-8")

patches = [
    (
        "b = text.index('\\ndef exact_tracks', a)",
        "b = text.index('\\nTRACK_SNAPSHOT = list(board.GetTracks())', a)",
        "snapshot boundary",
    ),
    (
        'if len(_local_specs) != 31:',
        'if len(_local_specs) != 32:',
        "audited local track count",
    ),
    (
        'expected 31 tracks, got {len(_local_specs)}',
        'expected 32 tracks, got {len(_local_specs)}',
        "audited local track-count message",
    ),
]
for old,new,label in patches:
    n=text.count(old)
    if n != 1:
        raise RuntimeError(f"v3 {label} anchor changed: expected 1, got {n}")
    text=text.replace(old,new,1)

exec(compile(text, str(SRC), "exec"), {"__name__":"__main__", "__file__":str(SRC)})
