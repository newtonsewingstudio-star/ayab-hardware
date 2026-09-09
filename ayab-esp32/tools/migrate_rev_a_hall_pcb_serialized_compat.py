#!/usr/bin/env python3
"""Compatibility entrypoint for the deterministic KH910 Hall PCB migration.

The branch PCB uses the older KiCad footprint serialization (`fp_text
reference/value`), while a KiCad 9 save rewrites those fields as `property
"Reference"/"Value"`.  The core transformer supports the audited electrical
migration; this wrapper makes reference/value access format-preserving across
both serializations without changing any unrelated board text.
"""

from __future__ import annotations

import re
import migrate_rev_a_hall_pcb_serialized as migration


def reference(block: str) -> str | None:
    m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
    if m:
        return m.group(1)
    m = re.search(r'\(fp_text\s+reference\s+(?:"([^"]+)"|([^\s()]+))', block)
    return (m.group(1) or m.group(2)) if m else None


def value(block: str) -> str | None:
    m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', block)
    if m:
        return m.group(1)
    m = re.search(r'\(fp_text\s+value\s+(?:"([^"]+)"|([^\s()]+))', block)
    return (m.group(1) or m.group(2)) if m else None


def replace_property(block: str, prop_name: str, new_value: str) -> str:
    children = migration._scan_children(block, 0)

    # New KiCad serialization.
    for s in children:
        if s.head != "property":
            continue
        pb = block[s.start:s.end]
        m = re.match(r'\(property\s+"([^"]+)"\s+"([^"]*)"', pb)
        if m and m.group(1) == prop_name:
            new_pb = pb[:m.start(2)] + new_value + pb[m.end(2):]
            return block[:s.start] + new_pb + block[s.end:]

    # Legacy branch serialization.  Preserve whether the original token was
    # quoted or bare so the edit is as small as possible.
    kind = "reference" if prop_name == "Reference" else "value" if prop_name == "Value" else None
    if kind is not None:
        for s in children:
            if s.head != "fp_text":
                continue
            pb = block[s.start:s.end]
            m = re.match(rf'(\(fp_text\s+{kind}\s+)("([^"]*)"|([^\s()]+))', pb)
            if not m:
                continue
            replacement = f'"{new_value}"' if m.group(3) is not None else new_value
            new_pb = pb[:m.start(2)] + replacement + pb[m.end(2):]
            return block[:s.start] + new_pb + block[s.end:]

    raise RuntimeError(f"{reference(block)} missing {prop_name} field")


migration.reference = reference
migration.value = value
migration.replace_property = replace_property

if __name__ == "__main__":
    migration.main()
