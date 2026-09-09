#!/usr/bin/env python3
"""Rev A Hall PCB migration v4b: DRC-safe routing correction for v4.

v4 proved the electrical/serialization migration but its first physical route
had 11 DRC violations. This wrapper intentionally leaves the v4 electrical
transformer unchanged and only corrects the geometric/power-pruning choices:

- terminate HALL_L_ADC/HALL_R_ADC on the already-existing, already-retagged MCU
  vias at (219.55,134.13) and (218.8,134.13), rather than adding new target vias;
- use the earlier conservative In1.Cu route shapes that avoid J402/J701;
- never run generic dead-leaf pruning on GND or +5V;
- remove only the four +5V vias that KiCad v4 DRC proved became orphaned after
  comparator removal.

The base v4 structural validation still runs unchanged after this wrapper.
"""
from __future__ import annotations

from pathlib import Path
import migrate_rev_a_hall_pcb_serialized_v4 as v4

k = v4.k

# Reuse the two existing MCU Hall vias. v4 has already retagged their corridors
# to the ADC nets, so no new through-via is required at the lower-board end.
v4.LEFT_TARGET = (219.55, 134.13)
v4.RIGHT_TARGET = (218.8, 134.13)

# These route shapes were chosen specifically to stay away from the J402/J701
# PTH fields that the first v4 route clipped.
v4.LEFT_START = (95.5, 139.878)
v4.RIGHT_START = (309.5, 160.5)
v4.LEFT_ROUTE = [
    v4.LEFT_START,
    (104.0, 146.0),
    (130.0, 146.0),
    (165.0, 144.0),
    (195.0, 140.0),
    v4.LEFT_TARGET,
]
v4.RIGHT_ROUTE = [
    v4.RIGHT_START,
    (300.0, 164.0),
    (282.0, 164.0),
    (260.0, 159.0),
    (240.0, 151.0),
    (225.0, 141.0),
    v4.RIGHT_TARGET,
]

# Power nets are plane/zone-connected and cannot be safely pruned by simple
# endpoint degree. Keep them intact and remove only DRC-proven orphan vias.
v4.PRUNE_NAMES = {v4.RAW_L, v4.RAW_R, v4.LK, v4.LL, v4.RN, v4.RS}

ORPHAN_5V_VIAS = {
    (87.08, 143.56),
    (309.70, 153.37),
    (320.13, 152.30),
    (93.14, 140.71),
}

_original_via = k.via
_original_prune = v4.prune_dead_leaves


def _via_without_duplicate_target(pos, net_id, seed):
    # The target vias already exist in the baseline and are retagged by v4.
    if seed in {"v4-left-target", "v4-right-target"}:
        return ""
    return _original_via(pos, net_id, seed)


def _prune_without_power(text, names):
    text, removed = _original_prune(text, names)

    # Resolve +5V net id from the current serialized board.
    nets = {}
    children = k.root_children(text)
    for s in children:
        if s.head != "net":
            continue
        n = k.parse_net_definition(text[s.start:s.end])
        if n:
            nets[n[1]] = n[0]
    p5_id = nets[v4.P5]

    edits = []
    exact_removed = 0
    for s in children:
        if s.head != "via":
            continue
        block = text[s.start:s.end]
        if k.item_net_id(block) != p5_id:
            continue
        pts = k.item_points(block)
        if not pts:
            continue
        p = pts[0]
        if any(k.near(p, q, 0.003) for q in ORPHAN_5V_VIAS):
            edits.append((s.start, s.end, ""))
            exact_removed += 1

    if exact_removed != 4:
        raise RuntimeError(f"expected four DRC-proven orphan +5V vias, found {exact_removed}")
    for a, b, replacement in sorted(edits, key=lambda e: (e[0], e[1]), reverse=True):
        text = text[:a] + replacement + text[b:]

    removed = dict(removed)
    removed["+5V orphan vias"] = exact_removed
    return text, removed


k.via = _via_without_duplicate_target
v4.prune_dead_leaves = _prune_without_power


if __name__ == "__main__":
    v4.main()
