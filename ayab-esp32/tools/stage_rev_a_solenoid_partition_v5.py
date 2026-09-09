#!/usr/bin/env python3
"""Rev A solenoid partition v5.

The first successful v4 baseline audit measured 32 raw +12 V F.Cu track
objects wholly inside the tightly bounded left solenoid-local bus region, not
31.  v5 changes only that fail-closed expected count; all layer/net/bounds
criteria and every other exact geometry assertion remain unchanged.
"""
from pathlib import Path

SRC = Path(__file__).with_name("stage_rev_a_solenoid_partition_v4.py")
text = SRC.read_text(encoding="utf-8")
old = 'if len(_local_specs) != 31:'
new = 'if len(_local_specs) != 32:'
old_msg = 'expected 31 tracks, got {len(_local_specs)}'
new_msg = 'expected 32 tracks, got {len(_local_specs)}'
if text.count(old) != 1 or text.count(old_msg) != 1:
    raise RuntimeError("v4 audited-track-count anchors changed")
text = text.replace(old, new, 1).replace(old_msg, new_msg, 1)
exec(compile(text, str(SRC), "exec"), {"__name__":"__main__", "__file__":str(SRC)})
