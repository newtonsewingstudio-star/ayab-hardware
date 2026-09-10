#!/usr/bin/env python3
"""Remove the verified unconnected wire islands reported by KiCad ERC.

Each listed island has no symbol, label, sheet-pin, or bus entry endpoint;
removing it is therefore netlist-preserving and eliminates stale drawing data.
"""
from pathlib import Path
import re

P = Path(__file__).resolve().parents[1] / "ioconditioning.kicad_sch"
UUIDS = {
    "387da1bd-ae41-4f40-b39e-d97c89806945", "6e50f3d3-62a8-4620-9002-7346abbd777f",
    "b99dbfce-825f-4a34-b62a-66ce1c22379b", "f831809d-f2a0-4523-93ef-61abb4afd1ea",
    "26a52f0e-fbd4-4e72-a312-b80cf08c84cf", "55947ae4-3342-485b-a85e-19cb9b9c89c3",
    "9c63d7bd-1205-4cfd-9df6-44b1b95c20c6", "a9cd88ce-4c86-4cf2-8b36-11c34fc84a73",
    "7ce91994-ebe7-49a8-8247-dc5debc30fe2", "b766ea6e-75a2-4f28-8af2-5522bb9532bc",
    "f1cc78e1-a9cd-49db-8e51-252a86339758", "0ddbd14c-8b8c-47c1-a101-60cbdde5251e",
    "8d240e2f-48ff-4e33-bbea-286c215a4c35", "fafb2264-2ad0-4d37-8fd9-338ae719d776",
    "0868575f-dbf3-4bde-88eb-0c6c176f57bf", "c24f0bd4-f0fe-4a44-b3e6-77491326fb93",
    "c6871799-7882-492f-949e-f64fed08d25c", "f96c5049-74e3-4b67-be82-aa1c33d367f8",
    "0491d59c-ac6b-4491-abb2-d51298652ad4", "7f2fe1f4-647d-4848-b134-7339711edb59",
    "a4d3268c-ce4f-4b4c-9891-9f0d912c8f2e", "e31de0a8-e2b2-4164-9387-54b37b066f16",
    "347172e1-0b34-40ef-bbb3-a53053ca461a", "40d8c6df-d9f9-4918-8306-52ad5c76e5db",
    "4b3ad9cd-2319-4ee2-8857-78ce2059e813", "1284f617-536e-40a3-bb73-a875643aeaa5",
    "bb2ecb13-e264-4446-8e08-fb0d1c3c1b6e", "e8c2803c-2fe5-4c33-9d92-87806f549221",
}

text = P.read_text(encoding="utf-8")
pattern = re.compile(r"  \(wire \(pts .*?\n  \)\n", re.S)
removed = []
def keep_or_remove(match):
    block = match.group(0)
    found = re.search(r"\(uuid ([0-9a-f-]+)\)", block)
    if found and found.group(1) in UUIDS:
        removed.append(found.group(1))
        return ""
    return block

new_text = pattern.sub(keep_or_remove, text)
if set(removed) != UUIDS or len(removed) != len(UUIDS):
    raise RuntimeError(f"expected {len(UUIDS)} exact orphan wires, removed {len(removed)}")
P.write_text(new_text, encoding="utf-8")
print(f"IOC_ERC_ORPHAN_WIRES_REMOVED {len(removed)}")
