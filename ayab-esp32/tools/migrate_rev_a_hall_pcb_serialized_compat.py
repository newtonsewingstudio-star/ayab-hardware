#!/usr/bin/env python3
"""Compatibility entrypoint for the deterministic KH910 Hall PCB migration.

The branch PCB uses the older KiCad footprint serialization (`fp_text
reference/value`), while a KiCad 9 save rewrites those fields as `property
"Reference"/"Value"`.  The core transformer supports the audited electrical
migration; this wrapper makes reference/value access format-preserving across
both serializations without changing any unrelated board text.

It also applies one narrowly asserted runtime correction to the first core
revision: Python evaluates the default argument to dict.get eagerly, so the
new ADC-net lookup must use an explicit conditional rather than
`adc_ids.get(net_name, nets[net_name])`.  The exact source line is required to
occur once; otherwise this wrapper aborts instead of silently patching code.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import sys

CORE = Path(__file__).with_name("migrate_rev_a_hall_pcb_serialized.py")
source = CORE.read_text(encoding="utf-8")
old = "net_id = adc_ids.get(net_name, nets[net_name])"
new = "net_id = adc_ids[net_name] if net_name in adc_ids else nets[net_name]"
if source.count(old) != 1:
    raise RuntimeError(f"expected exactly one ADC net-selection expression, found {source.count(old)}")
source = source.replace(old, new)

runtime_core = Path("/tmp/migrate_rev_a_hall_pcb_serialized_runtime.py")
runtime_core.write_text(source, encoding="utf-8")
spec = importlib.util.spec_from_file_location("kh910_hall_serialized_runtime", runtime_core)
if spec is None or spec.loader is None:
    raise RuntimeError("could not create runtime module spec")
migration = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = migration
spec.loader.exec_module(migration)


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

    # Legacy branch serialization. Preserve whether the token was quoted or
    # bare so the edit remains minimal.
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
