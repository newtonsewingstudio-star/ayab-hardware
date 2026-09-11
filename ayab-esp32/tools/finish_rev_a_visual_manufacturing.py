#!/usr/bin/env python3
"""Apply the final Rev A assembly-marking cleanup with KiCad 9 pcbnew."""

from pathlib import Path
import subprocess
import tempfile

import pcbnew


ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "ayab-esp32.kicad_pcb"


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def point(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(mm(x), mm(y))


board = pcbnew.LoadBoard(str(PCB))

# Two zone-only GND stitching vias sat just inside the antenna-recess edge.
# Shift them 0.30 mm inward so the controlled 0.25 mm copper-edge rule passes.
edge_vias = {(244.71, 122.26): (244.71, 122.56), (237.82, 122.28): (237.82, 122.58)}
for track in board.GetTracks():
    if isinstance(track, pcbnew.PCB_VIA):
        position = track.GetPosition()
        here = (round(pcbnew.ToMM(position.x), 2), round(pcbnew.ToMM(position.y), 2))
        if track.GetNetname() == "GND" and here in edge_vias:
            track.SetPosition(point(*edge_vias[here]))

# Remove the obsolete C-family marketing legend. It obscured both the new gate
# area and the nearby connector when moved; the J401/J406 references remain the
# unambiguous assembly identifiers.
obsolete_revision = None
obsolete_c_legend = None
restore_refs = {"kibuzzard-65BFD905", "kibuzzard-65A1DFCB"}
present_refs = set()
for footprint in board.GetFootprints():
    if footprint.GetReference() == "kibuzzard-65BFE062":
        obsolete_c_legend = footprint
    if footprint.GetReference() == "kibuzzard-65BDBF94":
        obsolete_revision = footprint
    if footprint.GetReference() in restore_refs:
        present_refs.add(footprint.GetReference())

# An earlier version of this repair script misidentified this unrelated legacy
# label. Restore it exactly from the audited parent commit when needed.
missing_refs = restore_refs - present_refs
if missing_refs:
    source = subprocess.check_output(
        ["git", "show", "HEAD:ayab-esp32/ayab-esp32.kicad_pcb"], cwd=ROOT.parent
    )
    temporary = tempfile.NamedTemporaryFile(suffix=".kicad_pcb", delete=False)
    try:
        temporary.write(source)
        temporary.close()
        parent_board = pcbnew.LoadBoard(temporary.name)
        parent_labels = {
            fp.GetReference(): fp for fp in parent_board.GetFootprints()
            if fp.GetReference() in missing_refs
        }
        for reference in sorted(missing_refs):
            board.Add(parent_labels[reference].Duplicate())
    finally:
        Path(temporary.name).unlink(missing_ok=True)

# This legacy KiBuzzard badge contains the obsolete "v0.1 rev A 02/24" text.
if obsolete_revision is not None:
    board.Remove(obsolete_revision)
if obsolete_c_legend is not None:
    board.Remove(obsolete_c_legend)

labels = {
    "KH910 REV A 09/2026": (174.0, 161.2, "F.SilkS", 0.80),
    "SOLENOID GATE": (106.5, 156.8, "F.SilkS", 0.80),
    "TP703 SW": (145.0, 162.4, "F.SilkS", 0.80),
    "D205 K=3V3": (235.5, 153.5, "B.SilkS", 0.80),
    "D206 A=GND": (235.5, 154.8, "B.SilkS", 0.80),
}

# Idempotence: replace only labels owned by this script.
for drawing in list(board.GetDrawings()):
    if isinstance(drawing, pcbnew.PCB_TEXT) and drawing.GetText() in labels:
        board.Remove(drawing)

for value, (x, y, layer_name, size) in labels.items():
    text = pcbnew.PCB_TEXT(board)
    text.SetText(value)
    text.SetPosition(point(x, y))
    text.SetLayer(board.GetLayerID(layer_name))
    text.SetTextSize(point(size, size))
    text.SetTextThickness(mm(0.13))
    text.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
    text.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
    if layer_name == "B.SilkS":
        text.SetMirrored(True)
    board.Add(text)

pcbnew.SaveBoard(str(PCB), board)
print("REV_A_VISUAL_MARKINGS_OK")
