#!/usr/bin/env python3
"""Inspect only the serialized KiCad blocks relevant to the KH910 Hall migration.

This avoids pcbnew/SWIG object wrappers entirely.  It is read-only: the script
prints net definitions, audited footprints, and copper items on the legacy Hall
corridor nets so a deterministic serialized-file migration can be written from
facts in the checked-out branch.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TARGET_NETS = {
    "GND",
    "/BROTHER-CONNECTORS/EOL_L",
    "/BROTHER-CONNECTORS/EOL_R",
    "/ESP32/EOL_L_P",
    "/ESP32/EOL_L_N",
    "/ESP32/HALL_L_ADC",
    "/ESP32/HALL_R_ADC",
}

TARGET_REFS = {
    "U201", "U701", "U702", "U703", "C703", "C704",
    *(f"R{n}" for n in range(715, 739)),
}


def child_blocks(text: str):
    """Yield direct children of the root kicad_pcb S-expression."""
    root = text.find("(kicad_pcb")
    if root < 0:
        raise RuntimeError("not a KiCad PCB file")

    depth = 0
    in_string = False
    escaped = False
    child_start = None
    i = root
    while i < len(text):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            i += 1
            continue
        if ch == "(":
            depth += 1
            if depth == 2:
                child_start = i
        elif ch == ")":
            if depth == 2 and child_start is not None:
                yield text[child_start:i + 1]
                child_start = None
            depth -= 1
            if depth == 0:
                break
        i += 1


def head(block: str) -> str:
    m = re.match(r"\(\s*([^\s()]+)", block)
    return m.group(1) if m else ""


def net_tuple(block: str):
    m = re.match(r'\(net\s+(\d+)\s+"((?:\\.|[^"\\])*)"\s*\)$', block.strip(), re.S)
    if not m:
        return None
    return int(m.group(1)), m.group(2)


def reference(block: str):
    patterns = [
        r'\(property\s+"Reference"\s+"([^"]+)"',
        r'\(fp_text\s+reference\s+"?([^"\s()]+)"?',
    ]
    for pat in patterns:
        m = re.search(pat, block)
        if m:
            return m.group(1)
    return None


def item_net_id(block: str):
    matches = re.findall(r"\(net\s+(\d+)(?:\s|\))", block)
    return int(matches[-1]) if matches else None


def compact(block: str) -> str:
    # Preserve the actual serialized syntax but strip trailing blank lines.
    return block.rstrip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("board", type=Path)
    args = ap.parse_args()
    text = args.board.read_text(encoding="utf-8")
    blocks = list(child_blocks(text))

    nets = {}
    for block in blocks:
        if head(block) != "net":
            continue
        parsed = net_tuple(block)
        if parsed:
            net_id, name = parsed
            nets[name] = net_id

    print("SERIALIZED_HALL_AUDIT")
    print("BOARD", args.board)
    print("BYTES", len(text.encode("utf-8")))
    vm = re.search(r"\(version\s+(\d+)\)", text)
    print("VERSION", vm.group(1) if vm else "UNKNOWN")

    print("\n=== TARGET NET DEFINITIONS ===")
    for name in sorted(TARGET_NETS):
        print(f"{name}: {nets.get(name, 'MISSING')}")

    print("\n=== TARGET FOOTPRINT BLOCKS ===")
    found_refs = set()
    for block in blocks:
        if head(block) != "footprint":
            continue
        ref = reference(block)
        if ref in TARGET_REFS:
            found_refs.add(ref)
            print(f"\n--- {ref} ---")
            print(compact(block))
    print("\nFOUND_REFS", ",".join(sorted(found_refs)))
    print("MISSING_REFS", ",".join(sorted(TARGET_REFS - found_refs)))

    legacy_ids = {nets[n] for n in ("/ESP32/EOL_L_P", "/ESP32/EOL_L_N") if n in nets}
    print("\n=== LEGACY HALL CORRIDOR COPPER ===")
    count = 0
    for block in blocks:
        if head(block) not in {"segment", "via", "arc"}:
            continue
        nid = item_net_id(block)
        if nid in legacy_ids:
            count += 1
            print(f"\n--- COPPER {count} net={nid} ---")
            print(compact(block))
    print("\nLEGACY_COPPER_COUNT", count)


if __name__ == "__main__":
    main()
