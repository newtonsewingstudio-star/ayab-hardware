#!/usr/bin/env python3
"""Validate Rev A ordering, population, and repository-pinned footprint data."""

import json
from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parents[2]
PCB = ROOT / "ayab-esp32" / "ayab-esp32.kicad_pcb"
PROJECT = ROOT / "ayab-esp32" / "ayab-esp32.kicad_pro"
LIBRARY_ROOT = ROOT / "ayab-library"

ORDERING = {
    "R820": ("100k", "C25803", "0603WAF1003T5E"),
    "R821": ("10k", "C25804", "0603WAF1002T5E"),
    "R822": ("100k", "C25803", "0603WAF1003T5E"),
    "R735": ("10k", "C25804", "0603WAF1002T5E"),
    "R736": ("10k", "C25804", "0603WAF1002T5E"),
    "R737": ("10k", "C25804", "0603WAF1002T5E"),
    "R738": ("10k", "C25804", "0603WAF1002T5E"),
}
DNP_REFS = {"R501", "R701", "R702", "R703", "R704", "R705", "R706", "R707", "R709", "R711", "R713"}
CUSTOM_LIBRARIES = {"Library", "easyeda2kicad", "Espressif"}


def pad_signature(footprint) -> dict[str, tuple]:
    result = {}
    for pad in footprint.Pads():
        result[str(pad.GetNumber())] = (
            tuple(pad.GetFPRelativePosition()),
            tuple(pad.GetSize()),
            tuple(pad.GetDrillSize()),
            int(pad.GetShape()),
            int(pad.GetAttribute()),
        )
    return result


def main() -> None:
    board = pcbnew.LoadBoard(str(PCB))
    physical = [fp for fp in board.GetFootprints() if fp.GetReference() != "G***"]
    by_ref = {fp.GetReference(): fp for fp in physical}
    if len(by_ref) != len(physical):
        raise RuntimeError("duplicate PCB references")

    for ref, (value, lcsc, part_number) in ORDERING.items():
        footprint = by_ref[ref]
        fields = footprint.GetFieldsText()
        actual = (footprint.GetValue(), fields.get("LCSC ID", ""), fields.get("OEM PN", ""))
        if actual != (value, lcsc, part_number):
            raise RuntimeError(f"{ref} ordering mismatch: {actual}")

    for ref in DNP_REFS:
        if not by_ref[ref].IsDNP():
            raise RuntimeError(f"{ref} must be marked DNP on the PCB")

    expected_values = {
        "R209": "5k1", "R210": "5k1", "TP701": "HALL-L-RAW",
        "TP702": "HALL-R-RAW", "D204": "SS54",
    }
    for ref, value in expected_values.items():
        if by_ref[ref].GetValue() != value:
            raise RuntimeError(f"{ref} expected {value}, got {by_ref[ref].GetValue()}")

    bridge = by_ref["D601"]
    bridge_id = bridge.GetFPID()
    if (str(bridge_id.GetLibNickname()), str(bridge_id.GetLibItemName())) != (
        "easyeda2kicad", "MBF-SMD_L4.8-W3.8-P2.54-LS6.8-TL"
    ):
        raise RuntimeError("D601 custom bridge footprint identity changed")
    bridge_nets = {pad.GetNumber(): pad.GetNetname() for pad in bridge.Pads()}
    if bridge_nets != {"1": "/PSU/INP_1", "2": "/PSU/INP_2", "3": "+12V", "4": "GND"}:
        raise RuntimeError(f"D601 customized pin mapping changed: {bridge_nets}")

    project_rules = json.loads(PROJECT.read_text(encoding="utf-8"))["board"]["design_settings"]["rules"]
    required_rules = {
        "min_clearance": 0.1,
        "min_track_width": 0.1,
        "min_copper_edge_clearance": 0.25,
        "min_through_hole_diameter": 0.2,
        "min_via_annular_width": 0.05,
    }
    for name, minimum in required_rules.items():
        if float(project_rules.get(name, 0)) < minimum:
            raise RuntimeError(f"manufacturing rule {name} is below {minimum} mm")

    required_labels = {
        "KH910 REV A 09/2026", "SOLENOID GATE", "TP703 SW",
        "D205 K=3V3", "D206 A=GND",
    }
    actual_labels = {
        drawing.GetText()
        for drawing in board.GetDrawings()
        if isinstance(drawing, pcbnew.PCB_TEXT)
    }
    missing_labels = required_labels - actual_labels
    if missing_labels:
        raise RuntimeError(f"missing controlled assembly labels: {sorted(missing_labels)}")
    if any(fp.GetReference() == "kibuzzard-65BDBF94" for fp in board.GetFootprints()):
        raise RuntimeError("obsolete v0.1 rev A 02/24 badge is still present")
    if any(fp.GetReference() == "kibuzzard-65BFE062" for fp in board.GetFootprints()):
        raise RuntimeError("obsolete C:900,965,270 gate-area legend is still present")

    plugin = pcbnew.PCB_IO_MGR.PluginFind(pcbnew.PCB_IO_MGR.KICAD_SEXP)
    checked_ids = set()
    checked_instances = 0
    for footprint in board.GetFootprints():
        fpid = footprint.GetFPID()
        nickname = str(fpid.GetLibNickname())
        name = str(fpid.GetLibItemName())
        if nickname not in CUSTOM_LIBRARIES:
            continue
        library_path = LIBRARY_ROOT / f"{nickname}.pretty"
        module_path = library_path / f"{name}.kicad_mod"
        if not module_path.is_file():
            raise RuntimeError(f"missing pinned footprint {nickname}:{name}")
        library_footprint = plugin.FootprintLoad(str(library_path), name)
        if library_footprint is None:
            raise RuntimeError(f"cannot load pinned footprint {nickname}:{name}")
        if pad_signature(footprint) != pad_signature(library_footprint):
            raise RuntimeError(f"pad geometry differs from pinned library: {footprint.GetReference()}")
        checked_ids.add(f"{nickname}:{name}")
        checked_instances += 1

    print("MANUFACTURING_METADATA_OK")
    print("ORDERING_REFS", len(ORDERING))
    print("DNP_REFS", len(DNP_REFS))
    print("PINNED_FOOTPRINT_IDS", len(checked_ids))
    print("PINNED_FOOTPRINT_INSTANCES", checked_instances)
    print("CONTROLLED_BOARD_RULES", len(required_rules))
    print("CONTROLLED_ASSEMBLY_LABELS", len(required_labels))


if __name__ == "__main__":
    main()
