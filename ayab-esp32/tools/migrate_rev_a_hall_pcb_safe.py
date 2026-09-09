#!/usr/bin/env python3
"""KiCad 9 safe entrypoint for the Rev A Hall PCB migration.

The Ubuntu KiCad 9 SWIG binding can expose FOOTPRINT.Pads() as an opaque
SwigPyObject after native board-container mutations.  KiCad itself provides
FOOTPRINT.FindPadByNumber(), so this entrypoint replaces collection iteration
with direct numbered-pad lookup and uses BOARD.GetPads() for the one board-wide
pad scan needed by orphan-copper cleanup.
"""

from __future__ import annotations

import migrate_rev_a_hall_pcb as migration


def direct_get_pad(fp, number: str):
    pad = fp.FindPadByNumber(str(number))
    if pad is None:
        raise RuntimeError(f"{fp.GetReference()} missing pad {number}")
    return pad


def board_pad_orphan_cleanup(board):
    pad_counts: dict[str, int] = {}
    for pad in board.GetPads():
        name = pad.GetNetname()
        if name:
            pad_counts[name] = pad_counts.get(name, 0) + 1

    removed = 0
    for item in list(board.GetTracks()):
        name = item.GetNetname()
        if name and pad_counts.get(name, 0) == 0:
            board.Remove(item)
            removed += 1
    return removed


migration.get_pad = direct_get_pad
migration.remove_orphan_net_copper = board_pad_orphan_cleanup

if __name__ == "__main__":
    migration.main()
