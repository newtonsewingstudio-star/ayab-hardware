#!/usr/bin/env python3
"""KiCad 9 Rev A solenoid partition v3.

v3 keeps the validated K/L-clean board as the source and changes the physical
partition strategy after DRC proved that individual upward SMD lifts collide
with the legacy ground geometry.

Architecture:
- the complete existing left solenoid-local +12 V F.Cu bus becomes
  SOLENOID_12V_SW, including C302/C303/C304 and legacy local bulk capacitors
  C603/C604/C605;
- the existing J401/J406 heavy local copper becomes switched;
- the only left raw feed removed is J401 -> global raw +12 V backbone;
- the obsolete J403 raw feed branch is removed completely and J403.9/.10 are
  fed directly by the new internal switched rail;
- the four existing vias on the left local bus become switched and one is the
  A* launch point, avoiding new vias in the dense solenoid area;
- no individual capacitor/ULN lift traces are created.

KiCad DRC is authoritative and this script is fail-closed against geometry,
net, target-count, and baseline drift.
"""
from pathlib import Path

SRC = Path(__file__).with_name("stage_rev_a_solenoid_partition.py")
text = SRC.read_text(encoding="utf-8")


def once(old, new, label):
    global text
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"partition v1 {label} anchor changed: expected 1, got {n}")
    text = text.replace(old, new, 1)

# KiCad 9 compatibility patches retained from v2.
once('CLEAR = 0.75', 'CLEAR = 0.65', 'power-route clearance raster')
once(
'''if board.GetNetcodeFromNetname(SW) > 0:\n    raise RuntimeError(f"{SW} already exists; refusing partial-state migration")''',
'''try:\n    _existing_sw = board.GetNetcodeFromNetname(SW)\nexcept (IndexError, KeyError):\n    _existing_sw = 0\nif _existing_sw > 0:\n    raise RuntimeError(f"{SW} already exists; refusing partial-state migration")''',
'missing-net lookup')
once(
'''def exact_tracks(spec, require_raw=True):\n    layer, a, b = spec\n    found = []\n    for item in list(board.GetTracks()):''',
'''TRACK_SNAPSHOT = list(board.GetTracks())\n\ndef exact_tracks(spec, require_raw=True):\n    layer, a, b = spec\n    found = []\n    for item in TRACK_SNAPSHOT:''',
'immutable pre-mutation track snapshot')
once(
'''removed = []\nfor spec in REMOVE:\n    rows = exact_tracks(spec)\n    if len(rows) != 1:\n        raise RuntimeError(f"expected one raw removal {layer_name(spec[0])} {spec[1]}->{spec[2]}, got {len(rows)}")\n    item = rows[0]\n    removed.append((layer_name(item.GetLayer()), endpoints(item)))\n    board.Remove(item)\n\nretagged = []\nfor spec in RETAG:\n    rows = exact_tracks(spec)\n    if len(rows) != 1:\n        raise RuntimeError(f"expected one raw retag {layer_name(spec[0])} {spec[1]}->{spec[2]}, got {len(rows)}")\n    item = rows[0]\n    item.SetNet(sw_net)\n    retagged.append((layer_name(item.GetLayer()), endpoints(item)))''',
'''# Resolve every exact edit before the first removal. Coincident same-net\n# duplicates at one geometry are edited together.\n_remove_groups = []\nfor spec in REMOVE:\n    rows = exact_tracks(spec)\n    if not rows:\n        raise RuntimeError(f"expected raw removal {layer_name(spec[0])} {spec[1]}->{spec[2]}, got 0")\n    _remove_groups.append((spec, rows))\n\n_retag_groups = []\nfor spec in RETAG:\n    rows = exact_tracks(spec)\n    if not rows:\n        raise RuntimeError(f"expected raw retag {layer_name(spec[0])} {spec[1]}->{spec[2]}, got 0")\n    _retag_groups.append((spec, rows))\n\n_remove_items=[]; _remove_ids=set()\nfor _spec,rows in _remove_groups:\n    for item in rows:\n        if id(item) not in _remove_ids:\n            _remove_ids.add(id(item)); _remove_items.append(item)\n_retag_items=[]; _retag_ids=set()\nfor _spec,rows in _retag_groups:\n    for item in rows:\n        if id(item) not in _retag_ids:\n            _retag_ids.add(id(item)); _retag_items.append(item)\nif _remove_ids & _retag_ids:\n    raise RuntimeError("same PCB track matched both REMOVE and RETAG specifications")\n\nremoved=[]\nfor item in _remove_items:\n    removed.append((layer_name(item.GetLayer()), endpoints(item)))\n    board.Remove(item)\nretagged=[]\nfor item in _retag_items:\n    item.SetNet(sw_net)\n    retagged.append((layer_name(item.GetLayer()), endpoints(item)))''',
'pre-resolve all exact edits')
once(
'''for ref, pns in TARGETS.items():\n    for pn in pns:\n        get_pad(ref, pn).SetNet(sw_net)\n\n\ndef add_track(a, b, layer, width=LOCAL_W):''',
'''for ref, pns in TARGETS.items():\n    for pn in pns:\n        get_pad(ref, pn).SetNet(sw_net)\n\n# Save/reload after exact edits so KiCad rebuilds a fresh connectivity graph.\npcbnew.SaveBoard(str(PATH), board)\nboard = pcbnew.LoadBoard(str(PATH))\nif board is None:\n    raise RuntimeError("could not reload staged board after exact partition edits")\nboard.BuildConnectivity()\nfps = {fp.GetReference(): fp for fp in board.GetFootprints()}\nraw_code = board.GetNetcodeFromNetname(RAW)\nsw_code = board.GetNetcodeFromNetname(SW)\nif raw_code <= 0 or sw_code <= 0:\n    raise RuntimeError("raw/switched nets missing after staged-board reload")\nsw_net = get_pad("J401", "9").GetNet()\nif get_pad("J401", "9").GetNetname() != SW:\n    raise RuntimeError("J401 switched pad did not survive staged-board reload")\n\n\ndef add_track(a, b, layer, width=LOCAL_W):''',
'save/reload before routing')

# All six local decouplers follow the switched solenoid rail in v3.
once(
'''TARGETS = {\n    "J401": ("9","10"), "J403": ("9","10"), "J406": ("9","10"),\n    "U302": ("9",), "U303": ("9",), "U304": ("9",),\n    "C302": ("1",), "C303": ("1",), "C304": ("1",),\n}\nRAW_CAPS = {"C603":"1", "C604":"1", "C605":"1"}''',
'''TARGETS = {\n    "J401": ("9","10"), "J403": ("9","10"), "J406": ("9","10"),\n    "U302": ("9",), "U303": ("9",), "U304": ("9",),\n    "C302": ("1",), "C303": ("1",), "C304": ("1",),\n    "C603": ("1",), "C604": ("1",), "C605": ("1",),\n}\nRAW_CAPS = {}''',
'local decoupler target set')

# Replace the old split/lift copper plan with the v3 exact feed cuts and the
# known heavy connector copper that remains useful.
a = text.index('REMOVE = [')
b = text.index('\ndef exact_tracks', a)
new_lists = '''REMOVE = [\n    # Left cluster: cut only the connection from J401 into the global raw bus.\n    (pcbnew.B_Cu,(116.84,153.7852),(116.84,163.10)),\n    # Right J403: remove the complete legacy raw feed, including the two local\n    # approach segments.  The new internal rail lands directly on J403.9.\n    (pcbnew.B_Cu,(336.16,127.945),(336.16,139.85)),\n    (pcbnew.B_Cu,(336.16,139.85),(334.16,141.85)),\n    (pcbnew.B_Cu,(334.16,141.85),(312.45,141.85)),\n    (pcbnew.B_Cu,(312.45,141.85),(310.91,140.31)),\n    (pcbnew.B_Cu,(310.91,140.31),(310.91,138.83)),\n]\n\nRETAG = [\n    # Existing heavy J401<->J406 local F.Cu chain.\n    (pcbnew.F_Cu,(116.84,153.7852),(116.84,151.61)),\n    (pcbnew.F_Cu,(116.84,151.61),(119.24,149.21)),\n    (pcbnew.F_Cu,(119.24,149.21),(119.24,146.28)),\n    (pcbnew.F_Cu,(116.84,153.7852),(114.84,153.7852)),\n    (pcbnew.F_Cu,(116.74,146.28),(119.24,146.28)),\n    # Existing J406 -> left local-bus B.Cu path.\n    (pcbnew.B_Cu,(119.24,146.28),(119.2426,146.2774)),\n    (pcbnew.B_Cu,(119.2426,146.2774),(119.2426,140.1026)),\n    (pcbnew.B_Cu,(119.2426,140.1026),(118.47,139.33)),\n    (pcbnew.B_Cu,(118.47,139.33),(114.03,139.33)),\n    # Keep the J403 common-pad bridge; its feed now arrives on In1.Cu at J403.9.\n    (pcbnew.B_Cu,(310.91,138.83),(308.41,138.83)),\n]\n'''
text = text[:a] + new_lists + text[b:]

# Extend RETAG from the immutable baseline snapshot to the complete left local
# +12 V F.Cu distribution.  This region contains only the interleaved solenoid
# decouplers, ULN COM feeds, and their common bus on the validated board.
needle = 'TRACK_SNAPSHOT = list(board.GetTracks())\n\ndef exact_tracks'
insert = '''TRACK_SNAPSHOT = list(board.GetTracks())\n\n_local_specs=[]\nfor _item in TRACK_SNAPSHOT:\n    if isinstance(_item, pcbnew.PCB_VIA) or _item.GetLayer()!=pcbnew.F_Cu or _item.GetNetCode()!=raw_code:\n        continue\n    _a,_b=endpoints(_item)\n    if all(96.5 <= q[0] <= 124.2 and 138.2 <= q[1] <= 141.9 for q in (_a,_b)):\n        _local_specs.append((pcbnew.F_Cu,_a,_b))\nif len(_local_specs) != 31:\n    raise RuntimeError(f"left local +12V F.Cu geometry drift: expected 31 tracks, got {len(_local_specs)}")\nRETAG.extend(_local_specs)\nprint("SOL_PARTITION_LOCAL_FCU_TRACKS",len(_local_specs))\n\ndef exact_tracks'''
once(needle, insert, 'left local FCu dynamic retag')

# Retag the four existing local-bus vias before any removals.  Their exact set
# is audited and they remain useful as layer transitions on the switched rail.
needle = '# Resolve every exact edit before the first removal.'
via_code = '''# The validated baseline has exactly four raw +12 V vias on the left local bus.\n_expected_vias={(117.93,139.30),(115.60,139.32),(114.39,139.32),(116.74,139.31)}\n_via_rows=[]\nfor _item in TRACK_SNAPSHOT:\n    if not isinstance(_item,pcbnew.PCB_VIA) or _item.GetNetCode()!=raw_code:\n        continue\n    _p=xy_obj(_item)\n    if any(near(_p,_e,0.025) for _e in _expected_vias):\n        _via_rows.append(_item)\n_got_vias={(round(xy_obj(v)[0],2),round(xy_obj(v)[1],2)) for v in _via_rows}\nif len(_via_rows)!=4:\n    raise RuntimeError(f"left local +12V via geometry drift: expected 4, got {len(_via_rows)}")\nfor _v in _via_rows:\n    _v.SetNet(sw_net)\nprint("SOL_PARTITION_LOCAL_VIAS_RETAGGED",len(_via_rows))\n\n# Resolve every exact edit before the first removal.'''
once(needle, via_code, 'local via retag')

# Remove the old six individual lift traces/trunk/right via.  The existing
# left via is the route launch and J403.9 is a through-hole route endpoint.
start = text.index('# Lift the six left SMD loads away from the raw bus.')
end = text.index('\nboard.BuildConnectivity()', start)
replacement = '''# v3 needs no individual SMD lifts.  The complete legacy local bus is switched.\nLEFT = (117.93,139.30)\nRIGHT = (310.91,138.83)\n'''
text = text[:start] + replacement + text[end:]
once('START=(124.005,143.0)', 'START=LEFT', 'A* route start')

# Remove stale raw-cap postcondition/report wording. All TARGETS, including
# C603/C604/C605, are checked on SW by the existing target loop.
once(
'''# Postconditions before saving.  Raw PSU caps must remain raw and every intended\n# load must now be on the switched net.\nfor ref,pn in RAW_CAPS.items():\n    if get_pad(ref,pn).GetNetname()!=RAW:\n        raise RuntimeError(f"raw PSU cap moved unexpectedly: {ref}.{pn}")\nfor ref,pns in TARGETS.items():''',
'''# Postconditions before saving: every intended solenoid load and local\n# decoupler must now be on the switched net.\nfor ref,pns in TARGETS.items():''',
'postcondition wording')
once(
'''print("SOLENOID_PARTITION_RAW_CAPS_OK",','.join(sorted(RAW_CAPS)))''',
'''print("SOLENOID_PARTITION_LOCAL_CAPS_SWITCHED","C302,C303,C304,C603,C604,C605")''',
'report local caps')

exec(compile(text, str(SRC), "exec"), {"__name__":"__main__", "__file__":str(SRC)})
