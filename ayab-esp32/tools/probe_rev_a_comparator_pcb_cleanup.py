#!/usr/bin/env python3
"""Stage removal of obsolete comparator footprints with KiCad pcbnew.

This probe does NOT modify the repository board. It loads a source PCB, records
all obsolete footprint pad positions/nets and copper endpoints attached to those
pads, removes the obsolete footprints in memory, refills zones, and saves a
staged board to an explicit output path for DRC inspection.

Usage:
  probe_rev_a_comparator_pcb_cleanup.py SOURCE_PCB OUTPUT_PCB REPORT_MD
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import pcbnew

REMOVE_REFS = {
    "U702", "U703", "C703", "C704",
    *(f"R{i}" for i in range(715, 735)),
}
RETAIN_REFS = {"U701", "R735", "R736", "R737", "R738", "TP701", "TP702"}


def mm(v: int) -> float:
    return round(pcbnew.ToMM(v), 4)


def point_key(p) -> tuple[int, int]:
    return (int(p.x), int(p.y))


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: probe_rev_a_comparator_pcb_cleanup.py SOURCE_PCB OUTPUT_PCB REPORT_MD")
    src, out, report = map(Path, sys.argv[1:])
    board = pcbnew.LoadBoard(str(src))
    fps = {fp.GetReference(): fp for fp in board.GetFootprints()}

    missing_remove = sorted(REMOVE_REFS - set(fps))
    if missing_remove:
        raise SystemExit("obsolete footprints missing before staged cleanup: " + ", ".join(missing_remove))
    missing_retain = sorted(RETAIN_REFS - set(fps))
    if missing_retain:
        raise SystemExit("retained footprints missing: " + ", ".join(missing_retain))

    # Index existing route endpoints before footprint deletion.
    endpoints = defaultdict(list)
    for item in board.GetTracks():
        if isinstance(item, pcbnew.PCB_TRACK):
            endpoints[point_key(item.GetStart())].append(
                f"track {item.GetNetname()} {mm(item.GetStart().x)},{mm(item.GetStart().y)} -> {mm(item.GetEnd().x)},{mm(item.GetEnd().y)} layer={board.GetLayerName(item.GetLayer())}"
            )
            endpoints[point_key(item.GetEnd())].append(
                f"track {item.GetNetname()} {mm(item.GetStart().x)},{mm(item.GetStart().y)} -> {mm(item.GetEnd().x)},{mm(item.GetEnd().y)} layer={board.GetLayerName(item.GetLayer())}"
            )
        elif isinstance(item, pcbnew.PCB_VIA):
            endpoints[point_key(item.GetPosition())].append(
                f"via {item.GetNetname()} at {mm(item.GetPosition().x)},{mm(item.GetPosition().y)}"
            )

    rows = []
    touched_nets = set()
    for ref in sorted(REMOVE_REFS):
        fp = fps[ref]
        for pad in fp.Pads():
            p = pad.GetPosition()
            net = pad.GetNetname()
            touched_nets.add(net)
            rows.append({
                "ref": ref,
                "pad": pad.GetNumber(),
                "net": net,
                "x": mm(p.x),
                "y": mm(p.y),
                "copper": list(endpoints.get(point_key(p), [])),
            })

    for ref in sorted(REMOVE_REFS):
        board.Remove(fps[ref])

    remaining = {fp.GetReference() for fp in board.GetFootprints()}
    still = sorted(REMOVE_REFS & remaining)
    if still:
        raise SystemExit("failed to remove footprints: " + ", ".join(still))
    missing_after = sorted(RETAIN_REFS - remaining)
    if missing_after:
        raise SystemExit("retained footprints disappeared: " + ", ".join(missing_after))

    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(out), board)

    lines = [
        "# KH910 Rev A — Comparator PCB Cleanup Probe",
        "",
        "Generated from the current board using KiCad's native `pcbnew` API. The staged board is diagnostic only and is not the repository PCB.",
        "",
        f"- obsolete footprints staged for removal: **{len(REMOVE_REFS)}**",
        f"- retained guard footprints: **{len(RETAIN_REFS)}**",
        f"- unique nets touched by removed pads: **{len(touched_nets)}**",
        "",
        "## Removed footprint pads and attached routed copper",
        "",
        "| Ref | Pad | Net | X mm | Y mm | Routed copper ending exactly at pad |",
        "|---|---:|---|---:|---:|---|",
    ]
    for r in rows:
        copper = "<br>".join(r["copper"]) if r["copper"] else "—"
        lines.append(f"| {r['ref']} | {r['pad']} | `{r['net']}` | {r['x']:.4f} | {r['y']:.4f} | {copper} |")
    lines += ["", "## Nets touched by obsolete footprints", ""]
    lines += [f"- `{n or '<no net>'}`" for n in sorted(touched_nets)]
    lines += [
        "",
        "## Next step",
        "",
        "Run DRC on the staged board and identify track-dangling/unconnected findings created by footprint deletion. Prune only copper branches attributable to the removed footprints; preserve retained Hall divider, encoder, power, and ground routing.",
    ]
    report.write_text("\n".join(lines) + "\n")
    print(report)
    print(out)


if __name__ == "__main__":
    main()
