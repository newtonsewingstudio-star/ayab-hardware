#!/usr/bin/env python3
"""Compatibility wrapper for the initial K/L PCB stage transformer.

The first staged revision used a regex replacement string beginning with
``\\10603`` for the R213/R214 OEM part number.  Python interprets that prefix as
an octal escape instead of capture-group 1 followed by ``0603``.  Patch only
that exact source expression at runtime and then execute the otherwise unchanged
assertion-heavy migration.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

CORE = Path(__file__).with_name("migrate_rev_a_kl_pcb_stage.py")
source = CORE.read_text(encoding="utf-8")
old = "r'\\\\10603WAF1002T5E\\\\3'"
new = "r'\\\\g<1>0603WAF1002T5E\\\\g<3>'"
count = source.count(old)
if count != 1:
    raise RuntimeError(f"expected exactly one K/L metadata patch target, found {count}")
source = source.replace(old, new)
runtime = Path("/tmp/migrate_rev_a_kl_pcb_stage_runtime.py")
runtime.write_text(source, encoding="utf-8")
spec = importlib.util.spec_from_file_location("kh910_kl_stage_runtime", runtime)
if spec is None or spec.loader is None:
    raise RuntimeError("could not create K/L runtime module")
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

if __name__ == "__main__":
    mod.main()
