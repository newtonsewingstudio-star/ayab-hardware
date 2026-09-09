#!/usr/bin/env python3
"""KiCad 9 compatibility wrapper for the Rev A solenoid partition stage.

The v1 stage remains the source of electrical and geometry intent. This wrapper
only adapts that fail-closed migration to KiCad 9's SWIG behavior:

1. GetNetcodeFromNetname() raises IndexError when a net is absent.
2. GetTracks() may become non-iterable after board.Remove().
3. Wrappers for removed tracks may be recycled, so an old track snapshot must
   not be queried after mutation.

All exact REMOVE/RETAG objects are therefore resolved and uniqueness-checked
before the first mutation. After those edits and pad retagging, the staged board
is saved and reloaded before any new routing so A* sees a fresh KiCad object
container and connectivity graph.
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
        '''TRACK_SNAPSHOT = list(board.GetTracks())\n\ndef exact_tracks(spec, require_raw=True):\n    layer, a, b = spec\n    found = []\n    for item in TRACK_SNAPSHOT:''',
        "immutable pre-mutation track snapshot",
    ),
    (
        '''removed = []\nfor spec in REMOVE:\n    rows = exact_tracks(spec)\n    if len(rows) != 1:\n        raise RuntimeError(f"expected one raw removal {layer_name(spec[0])} {spec[1]}->{spec[2]}, got {len(rows)}")\n    item = rows[0]\n    removed.append((layer_name(item.GetLayer()), endpoints(item)))\n    board.Remove(item)\n\nretagged = []\nfor spec in RETAG:\n    rows = exact_tracks(spec)\n    if len(rows) != 1:\n        raise RuntimeError(f"expected one raw retag {layer_name(spec[0])} {spec[1]}->{spec[2]}, got {len(rows)}")\n    item = rows[0]\n    item.SetNet(sw_net)\n    retagged.append((layer_name(item.GetLayer()), endpoints(item)))''',
        '''# Resolve and validate every exact edit against one immutable board state\n# before the first mutation. KiCad 9 may recycle SWIG wrappers after Remove().\n_remove_items = []\nfor spec in REMOVE:\n    rows = exact_tracks(spec)\n    if len(rows) != 1:\n        raise RuntimeError(f"expected one raw removal {layer_name(spec[0])} {spec[1]}->{spec[2]}, got {len(rows)}")\n    _remove_items.append(rows[0])\n\n_retag_items = []\nfor spec in RETAG:\n    rows = exact_tracks(spec)\n    if len(rows) != 1:\n        raise RuntimeError(f"expected one raw retag {layer_name(spec[0])} {spec[1]}->{spec[2]}, got {len(rows)}")\n    _retag_items.append(rows[0])\n\nif len({id(x) for x in _remove_items + _retag_items}) != len(_remove_items) + len(_retag_items):\n    raise RuntimeError("same PCB track matched more than one REMOVE/RETAG specification")\n\nremoved = []\nfor item in _remove_items:\n    removed.append((layer_name(item.GetLayer()), endpoints(item)))\n    board.Remove(item)\n\nretagged = []\nfor item in _retag_items:\n    item.SetNet(sw_net)\n    retagged.append((layer_name(item.GetLayer()), endpoints(item)))''',
        "pre-resolve all exact edits",
    ),
    (
        '''for ref, pns in TARGETS.items():\n    for pn in pns:\n        get_pad(ref, pn).SetNet(sw_net)\n\n\ndef add_track(a, b, layer, width=LOCAL_W):''',
        '''for ref, pns in TARGETS.items():\n    for pn in pns:\n        get_pad(ref, pn).SetNet(sw_net)\n\n# Drop all mutated SWIG wrappers before routing. A fresh KiCad load gives A*\n# a valid track iterator and an authoritative post-partition connectivity graph.\npcbnew.SaveBoard(str(PATH), board)\nboard = pcbnew.LoadBoard(str(PATH))\nif board is None:\n    raise RuntimeError("could not reload staged board after exact partition edits")\nboard.BuildConnectivity()\nfps = {fp.GetReference(): fp for fp in board.GetFootprints()}\nraw_code = board.GetNetcodeFromNetname(RAW)\nsw_code = board.GetNetcodeFromNetname(SW)\nif raw_code <= 0 or sw_code <= 0:\n    raise RuntimeError("raw/switched nets missing after staged-board reload")\nsw_net = get_pad("J401", "9").GetNet()\nif get_pad("J401", "9").GetNetname() != SW:\n    raise RuntimeError("J401 switched pad did not survive staged-board reload")\n\n\ndef add_track(a, b, layer, width=LOCAL_W):''',
        "save/reload before routing",
    ),
]

for old, new, label in patches:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"partition v1 {label} anchor changed: expected 1, got {count}")
    text = text.replace(old, new, 1)

exec(compile(text, str(SRC), "exec"), {"__name__": "__main__", "__file__": str(SRC)})
