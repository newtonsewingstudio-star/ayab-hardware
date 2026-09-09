#!/usr/bin/env python3
"""KiCad 9 compatibility wrapper for the Rev A solenoid partition stage.

The v1 stage is intentionally fail-closed and remains the source of electrical
and geometry intent.  This wrapper patches two KiCad 9 Python binding quirks:

1. GetNetcodeFromNetname() raises IndexError when a net is absent.
2. GetTracks() can become non-iterable after an in-memory board.Remove().

To avoid the second issue, resolve one immutable track snapshot before any
mutation, mark removed tracks as dead, and use the filtered snapshot for both
exact cut/retag lookup and A* obstacle rasterization.  Newly-added items are all
on SOLENOID_12V_SW, so omitting them from the obstacle snapshot is intentional.
"""
from pathlib import Path

SRC = Path(__file__).with_name("stage_rev_a_solenoid_partition.py")
text = SRC.read_text(encoding="utf-8")

patches = [
    (
        '''if board.GetNetcodeFromNetname(SW) > 0:\n    raise RuntimeError(f"{SW} already exists; refusing partial-state migration")''',
        '''try:\n    _existing_sw = board.GetNetcodeFromNetname(SW)\nexcept (IndexError, KeyError):\n    _existing_sw = 0\nif _existing_sw > 0:\n    raise RuntimeError(f"{SW} already exists; refusing partial-state migration")''',
        "missing-net lookup",
    ),
    (
        '''def exact_tracks(spec, require_raw=True):\n    layer, a, b = spec\n    found = []\n    for item in list(board.GetTracks()):''',
        '''TRACK_SNAPSHOT = list(board.GetTracks())\nREMOVED_TRACK_IDS = set()\n\ndef exact_tracks(spec, require_raw=True):\n    layer, a, b = spec\n    found = []\n    for item in TRACK_SNAPSHOT:\n        if id(item) in REMOVED_TRACK_IDS:\n            continue''',
        "immutable track snapshot",
    ),
    (
        '''    removed.append((layer_name(item.GetLayer()), endpoints(item)))\n    board.Remove(item)''',
        '''    removed.append((layer_name(item.GetLayer()), endpoints(item)))\n    REMOVED_TRACK_IDS.add(id(item))\n    board.Remove(item)''',
        "removed-track bookkeeping",
    ),
    (
        '''def build_blocked(layer):\n    blocked=set()\n    for item in board.GetTracks():''',
        '''def build_blocked(layer):\n    blocked=set()\n    for item in TRACK_SNAPSHOT:\n        if id(item) in REMOVED_TRACK_IDS:\n            continue''',
        "A* obstacle snapshot",
    ),
]

for old, new, label in patches:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"partition v1 {label} anchor changed: expected 1, got {count}")
    text = text.replace(old, new, 1)

exec(compile(text, str(SRC), "exec"), {"__name__": "__main__", "__file__": str(SRC)})
