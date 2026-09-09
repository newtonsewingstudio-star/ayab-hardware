#!/usr/bin/env python3
"""Robust compatibility wrapper for the Rev A KH-910 K/L PCB stage.

The core transformer is intentionally assertion-heavy. Its only known defect is
inside clone_pullup(): a replacement string beginning with ``\\10603`` can be
interpreted as an octal escape by Python's regex replacement engine and corrupt
the cloned footprint S-expression.

Do not rewrite the core source text. Import it, replace only clone_pullup() with
a functionally identical implementation that uses callback replacements, then
run the core CLI. This keeps every topology/precondition assertion in the core
active while eliminating brittle source-string patching.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import sys
import uuid

CORE = Path(__file__).with_name("migrate_rev_a_kl_pcb_stage.py")
spec = importlib.util.spec_from_file_location("kh910_kl_stage_core", CORE)
if spec is None or spec.loader is None:
    raise RuntimeError("could not create K/L core module spec")
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def fixed_clone_pullup(src: str, ref: str, pos: tuple[float, float], machine_net_id: int,
                       machine_name: str, p3v3_id: int) -> str:
    out = mod.replace_property(src, "Reference", ref)
    out = mod.replace_property(out, "Value", "10k")

    out, n = re.subn(
        r'(property "LCSC ID" ")([^"]+)(")',
        lambda m: m.group(1) + "C25804" + m.group(3),
        out,
        count=1,
    )
    if n != 1:
        raise RuntimeError("R210 clone missing LCSC ID property")

    out, n = re.subn(
        r'(property "OEM PN" ")([^"]+)(")',
        lambda m: m.group(1) + "0603WAF1002T5E" + m.group(3),
        out,
        count=1,
    )
    if n != 1:
        raise RuntimeError("R210 clone missing OEM PN property")

    out, n = re.subn(
        r'\(at 212\.75 132\.025\)',
        f'(at {pos[0]} {pos[1]} 180)',
        out,
        count=1,
    )
    if n != 1:
        raise RuntimeError("R210 clone top-level position not found exactly once")

    idx = 0

    def repl_uuid(_m):
        nonlocal idx
        idx += 1
        return f'(uuid "{uuid.uuid5(uuid.NAMESPACE_URL, f"kh910-rev-a-{ref}-{idx}")}")'

    out = re.sub(r'\(uuid "[0-9a-f-]+"\)', repl_uuid, out)
    out = mod.k.replace_pad_net_in_footprint(out, "1", p3v3_id, mod.P3V3)
    out = mod.k.replace_pad_net_in_footprint(out, "2", machine_net_id, machine_name)
    return out


mod.clone_pullup = fixed_clone_pullup

if __name__ == "__main__":
    mod.main()
