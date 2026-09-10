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


TEMPLATES = {"U403": "Q501", "R215": "R206", "R216": "R206"}
VALUES = {"U403": "LM66100DCKR", "R215": "47k", "R216": "10k"}
DEFAULT_COORDINATES = {
    "U403": (300.000, 136.500),
    "R215": (230.000, 139.000),
    "R216": (232.000, 139.000),
}


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


def coordinate(value: str) -> tuple[float, float]:
    try:
        x, y = (float(item.strip()) for item in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("coordinates must be X,Y in millimetres") from exc
    return x, y


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--u403", type=coordinate, default=DEFAULT_COORDINATES["U403"])
    parser.add_argument("--r215", type=coordinate, default=DEFAULT_COORDINATES["R215"])
    parser.add_argument("--r216", type=coordinate, default=DEFAULT_COORDINATES["R216"])
    args = parser.parse_args()
    board = pcbnew.LoadBoard(str(args.input))
    if board is None:
        raise RuntimeError(f"could not load {args.input}")
    existing = {fp.GetReference() for fp in board.GetFootprints()}
    conflicts = sorted(existing & set(TEMPLATES))
    if conflicts:
        raise RuntimeError(f"baseline already contains {', '.join(conflicts)}")

    coordinates = {"U403": args.u403, "R215": args.r215, "R216": args.r216}
    for reference, template_ref in TEMPLATES.items():
        xy = coordinates[reference]
        footprint = clone_template(board, template_ref)
        footprint.SetReference(reference)
        footprint.SetValue(VALUES[reference])
        footprint.SetPosition(point(*xy))
        # This is a geometric probe only.  Templates have electrical nets from
        # their original locations; clearing them prevents those unrelated nets
        # from creating false shorts, mask bridges, and unconnected-pad counts.
        for pad in footprint.Pads():
            pad.SetNetCode(0)
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
