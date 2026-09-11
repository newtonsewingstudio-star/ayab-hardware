#!/usr/bin/env python3
"""Close the final 00b3978 preorder audit's two bounded PCB findings."""

from __future__ import annotations

import collections
import re
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "ayab-esp32.kicad_pcb"
NEW_ID_REFS = ("R820", "R821", "R822", "TP703", "Q805", "C206", "D206", "Q806")
EXPECTED_ROOT_DUPLICATES = {
    "04bae630-8fbb-4b37-987d-bc6f441de592": {"R809", "R820", "R821", "R822"},
    "142ef7ec-f59c-4a67-83ea-4f13d29254a0": {"TP701", "TP703"},
    "4febda2b-1d6f-4510-9fa3-8716fa0d528e": {"Q502", "Q805"},
    "71a20b46-214c-45fb-82e3-9fb1b0c494c5": {"C204", "C206"},
    "787d9318-5ad6-4459-91fb-ae67f161ad4b": {"D602", "D206"},
    "de24da1d-d22b-41b8-b322-6a5b98d17f15": {"Q201", "Q806"},
}
NAMESPACE = uuid.UUID("8be35d54-b70c-4ce5-b34b-46ceea72828e")
EXPECTED_DIMENSION_UUID_PAIRS = {
    "8d3eeec5-bd74-42bb-8e7a-8bd8a2f82130": 2,
    "c65b5428-2a4b-47c8-bfee-f4a6bc8e5635": 2,
    "e4248d07-abde-4bf7-a19c-ed5d8b0ae978": 2,
    "eefb47fd-4a88-4e66-b5ef-d5b4610de02c": 2,
}


def block_at(text: str, start: int) -> tuple[str, int]:
    depth = 0
    quoted = False
    escaped = False
    for pos in range(start, len(text)):
        char = text[pos]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : pos + 1], pos + 1
    raise RuntimeError(f"unbalanced expression at {start}")


def expressions(text: str, token: str):
    pos = 0
    while True:
        start = text.find(token, pos)
        if start < 0:
            return
        block, end = block_at(text, start)
        yield start, end, block
        pos = end


def footprint_blocks(text: str) -> dict[str, tuple[int, int, str]]:
    result = {}
    for start, end, block in expressions(text, '(footprint "'):
        match = re.search(r'\(property "Reference" "([^"]+)"', block)
        if match:
            result[match.group(1)] = (start, end, block)
    return result


def root_uuid(block: str) -> str:
    match = re.search(r'\(uuid "([0-9a-f-]{36})"\)', block)
    if not match:
        raise RuntimeError("footprint has no root UUID")
    return match.group(1)


def uuid_duplicates(text: str) -> dict[str, int]:
    values = re.findall(r'\(uuid "?([0-9a-f-]{36})"?\)', text)
    return {value: count for value, count in collections.Counter(values).items() if count > 1}


def main() -> None:
    text = PCB.read_bytes().decode("utf-8")
    blocks = footprint_blocks(text)
    actual_groups: dict[str, set[str]] = collections.defaultdict(set)
    for ref, (_, _, block) in blocks.items():
        actual_groups[root_uuid(block)].add(ref)
    actual_root_duplicates = {key: refs for key, refs in actual_groups.items() if len(refs) > 1}
    if actual_root_duplicates != EXPECTED_ROOT_DUPLICATES:
        raise RuntimeError(f"unexpected starting footprint UUID groups: {actual_root_duplicates}")

    before_duplicates = uuid_duplicates(text)
    if len(before_duplicates) != 137 or sum(before_duplicates.values()) - len(before_duplicates) != 183:
        raise RuntimeError("unexpected starting nested UUID duplicate inventory")

    edits = []
    for ref in NEW_ID_REFS:
        start, end, block = blocks[ref]
        index = 0

        def replace_id(match: re.Match[str]) -> str:
            nonlocal index
            index += 1
            old = match.group(1)
            new = uuid.uuid5(NAMESPACE, f"{ref}:{index}:{old}")
            return f'(uuid "{new}")'

        changed = re.sub(r'\(uuid "([0-9a-f-]{36})"\)', replace_id, block)
        if index == 0:
            raise RuntimeError(f"{ref} had no serialized UUIDs")
        edits.append((start, end, changed))

    label_matches = list(expressions(text, '(gr_text "KH910 REV A 09/2026"'))
    if len(label_matches) != 1:
        raise RuntimeError(f"expected one revision marking, found {len(label_matches)}")
    start, end, label = label_matches[0]
    moved, count = re.subn(r'\(at 174 161\.2 0\)', '(at 180 142 0)', label, count=1)
    if count != 1:
        raise RuntimeError("revision marking is not at the audited starting location")
    edits.append((start, end, moved))

    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]

    remaining = uuid_duplicates(text)
    if remaining != EXPECTED_DIMENSION_UUID_PAIRS:
        raise RuntimeError(f"unexpected UUID duplicates remain after repair: {remaining}")
    PCB.write_bytes(text.encode("utf-8"))
    print("FINAL_PREORDER_AUDIT_REPAIR_OK")
    print("FRESHENED_FOOTPRINTS", ",".join(NEW_ID_REFS))
    print("REVISION_LABEL_AT 180.0,142.0")
    print("FOOTPRINT_TREE_UUID_DUPLICATE_GROUPS 0")
    print("INTENTIONAL_DIMENSION_LABEL_UUID_PAIRS", len(EXPECTED_DIMENSION_UUID_PAIRS))


if __name__ == "__main__":
    main()
