#!/usr/bin/env python3
"""Remove the obsolete Rev A LM393 Hall/EOL comparator network.

This is a deliberately narrow KiCad schematic text patch. It removes only
component instance blocks whose annotated references are in REMOVE_REFS and
renames the two retained raw Hall test points. Library symbol definitions and
unrelated wiring are left intact. Electrical correctness is validated from a
regenerated full hierarchical netlist in CI before the patched schematic is
committed.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCH = ROOT / "ioconditioning.kicad_sch"

REMOVE_REFS = {
    "U702", "U703", "C703", "C704",
    *(f"R{i}" for i in range(715, 735)),
}
TESTPOINT_VALUES = {
    "TP701": "HALL-L-RAW",
    "TP702": "HALL-R-RAW",
}


def extract_block(text: str, start: int) -> tuple[str, int]:
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return text[start:i + 1], i + 1
    raise RuntimeError(f"unbalanced KiCad block starting at byte {start}")


def symbol_blocks(text: str):
    """Yield all symbol-expression blocks; exact refs distinguish instances."""
    token = "(symbol "
    p = 0
    while True:
        p = text.find(token, p)
        if p < 0:
            return
        block, end = extract_block(text, p)
        yield p, end, block
        p = end


def ref_of(block: str) -> str | None:
    m = re.search(r'\(property "Reference" "([^"]+)"', block)
    return m.group(1) if m else None


def replace_value(block: str, new_value: str) -> str:
    out, count = re.subn(
        r'(\(property "Value" ")[^"]+(" )',
        lambda m: m.group(1) + new_value + m.group(2),
        block,
        count=1,
    )
    if count != 1:
        raise RuntimeError(f"could not replace Value in {ref_of(block)}")
    return out


def main() -> None:
    text = SCH.read_text(errors="strict")
    found_remove: set[str] = set()
    found_tp: set[str] = set()
    edits: list[tuple[int, int, str]] = []

    for start, end, block in symbol_blocks(text):
        ref = ref_of(block)
        if ref in REMOVE_REFS:
            found_remove.add(ref)
            edits.append((start, end, ""))
        elif ref in TESTPOINT_VALUES:
            found_tp.add(ref)
            new_block = replace_value(block, TESTPOINT_VALUES[ref])
            if new_block != block:
                edits.append((start, end, new_block))

    missing_remove = sorted(REMOVE_REFS - found_remove)
    missing_tp = sorted(set(TESTPOINT_VALUES) - found_tp)

    # Idempotency: if all removal refs are already absent, allow the patch to
    # pass as long as both retained test points still exist.
    already_removed = not found_remove and not missing_tp
    if found_remove and missing_remove:
        raise RuntimeError(
            "partial comparator cleanup detected; missing expected refs: " + ", ".join(missing_remove)
        )
    if missing_tp:
        raise RuntimeError("missing retained test points: " + ", ".join(missing_tp))

    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]

    # Structural guard: no target instance reference may remain, and retained
    # Rev A divider/test references must still be present.
    for ref in REMOVE_REFS:
        if re.search(rf'\(property "Reference" "{re.escape(ref)}"', text):
            raise RuntimeError(f"obsolete instance still present: {ref}")
    for ref in ("R735", "R736", "R737", "R738", "TP701", "TP702", "U701"):
        if not re.search(rf'\(property "Reference" "{re.escape(ref)}"', text):
            raise RuntimeError(f"retained Rev A instance disappeared: {ref}")

    SCH.write_text(text)
    if already_removed and not edits:
        print("Comparator network already removed; no schematic changes required")
    else:
        print("Removed comparator-only refs:", ", ".join(sorted(found_remove)))
        print("Retained raw Hall test points renamed:", ", ".join(sorted(found_tp)))


if __name__ == "__main__":
    main()
