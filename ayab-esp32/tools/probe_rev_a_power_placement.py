#!/usr/bin/env python3
"""Place-only DRC probe for the three missing Rev A power parts.

This intentionally adds no copper and never edits the source board.  Its only
job is to prove that the proposed physical locations are clear before a later
routing stage removes the legacy 5 V jumper and GPIO4 branch.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


PLACEMENTS = {
    "U403": ("Q501", (310.120, 136.890)),
    "R215": ("R206", (210.600, 129.400)),
    "R216": ("R206", (210.600, 131.100)),
}
VALUES = {"U403": "LM66100DCKR", "R215": "47k", "R216": "10k"}


def point(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


def clone_template(board: pcbnew.BOARD, reference: str) -> pcbnew.FOOTPRINT:
    """Copy a footprint already embedded in the validated source board.

    The CI KiCad runtime deliberately has no configured global footprint-table,
    so ``FootprintLoad`` cannot load a standard-library module by pathname.
    Q501 and R206 are the exact standard SOT-363 and 0603 land patterns used
    by this board.  The native copy constructor preserves their geometry while
    keeping this probe independent of a runner-specific library installation.
    """
    for footprint in board.GetFootprints():
        if footprint.GetReference() == reference:
            return pcbnew.FOOTPRINT(footprint)
    raise RuntimeError(f"template footprint not found: {reference}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    board = pcbnew.LoadBoard(str(args.input))
    if board is None:
        raise RuntimeError(f"could not load {args.input}")
    existing = {fp.GetReference() for fp in board.GetFootprints()}
    conflicts = sorted(existing & set(PLACEMENTS))
    if conflicts:
        raise RuntimeError(f"baseline already contains {', '.join(conflicts)}")

    for reference, (template_ref, xy) in PLACEMENTS.items():
        footprint = clone_template(board, template_ref)
        footprint.SetReference(reference)
        footprint.SetValue(VALUES[reference])
        footprint.SetPosition(point(*xy))
        board.Add(footprint)
        pads = []
        for pad in footprint.Pads():
            pos = pad.GetPosition()
            pads.append(f"{pad.GetNumber()}=({pcbnew.ToMM(pos.x):.3f},{pcbnew.ToMM(pos.y):.3f})")
        print(
            "PLACED", reference, f"template={template_ref}",
            f"at=({xy[0]:.3f},{xy[1]:.3f})", "pads=" + ",".join(pads),
        )

    pcbnew.SaveBoard(str(args.output), board)
    print("PLACEMENT_PROBE_OK", args.output)


if __name__ == "__main__":
    main()
