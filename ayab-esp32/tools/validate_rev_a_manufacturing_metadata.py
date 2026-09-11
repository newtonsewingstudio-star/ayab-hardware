#!/usr/bin/env python3
"""Validate Rev A ordering, population, and repository-pinned footprint data."""

import collections
import json
import re
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
    "D605": ("SS54", "C22452", "SS54"),
    "D606": ("SS54", "C22452", "SS54"),
}
DNP_REFS = {"R501", "R701", "R702", "R703", "R704", "R705", "R706", "R707", "R709", "R711", "R713"}
CUSTOM_LIBRARIES = {"Library", "easyeda2kicad", "Espressif"}
EXPECTED_PATHS = {
    "R213": "/a7e0db0f-e473-44d4-a2fe-681f732aacb2/a19b05df-401b-45d1-902b-04dd5c28419d",
    "R214": "/a7e0db0f-e473-44d4-a2fe-681f732aacb2/7ec7d011-3001-49c9-8999-3317dce5e123",
    "R735": "/a44519f5-2a17-4043-8636-a7b7c38f71bc/ad5b5bd5-a30d-4dfe-bc0f-2aeb7aafd75a",
    "R736": "/a44519f5-2a17-4043-8636-a7b7c38f71bc/f53fc7b5-b429-4945-9bda-7fdfd59944c3",
    "R737": "/a44519f5-2a17-4043-8636-a7b7c38f71bc/2eb13a2b-7d02-49dd-92c0-be152b720ea3",
    "R738": "/a44519f5-2a17-4043-8636-a7b7c38f71bc/3d5b2f4e-bc42-4903-a356-cc83cf32fd79",
}
MOUNTING_REFS = {"H101", "H102", "H103", "H104", "H106", "H108"}
SPECIALTY_CONNECTORS_WITHOUT_LCSC_ID = {
    "J403": ("910.950 SOLENOIDS A", "Hirose", "HNC2-2.5P-10DS(02)"),
    "J404": ("910.950 SOLENOIDS B", "Hirose", "HNC2-2.5P-8DS(02)"),
    "J405": ("910.950 ENCODERS EOL R", "Hirose", "HNC2-2.5P-10DS(02)"),
    "J406": ("930.940 SOLENOIDS A", "HR(Joint Tech Elec)", "A2506WV-10P"),
    "J408": ("910.950 EOL L", "Hirose", "HNC2-2.5P-3DS(02)"),
}


def expression_at(text: str, start: int) -> tuple[str, int]:
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
    raise RuntimeError(f"unbalanced PCB expression at {start}")


def serialized_footprint_uuids(board_text: str) -> list[str]:
    values = []
    pos = 0
    while True:
        start = board_text.find('(footprint "', pos)
        if start < 0:
            return values
        block, pos = expression_at(board_text, start)
        values.extend(re.findall(r'\(uuid "?([0-9a-f-]{36})"?\)', block))


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
    board_text = PCB.read_text(encoding="utf-8")
    board = pcbnew.LoadBoard(str(PCB))
    serialized_uuids = serialized_footprint_uuids(board_text)
    duplicate_uuids = {
        value: count
        for value, count in collections.Counter(serialized_uuids).items()
        if count > 1
    }
    if duplicate_uuids:
        excess = sum(count - 1 for count in duplicate_uuids.values())
        raise RuntimeError(
            f"duplicate serialized footprint-tree UUIDs: {len(duplicate_uuids)} groups, {excess} excess uses"
        )
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

    fitted = [
        footprint
        for footprint in physical
        if not footprint.IsDNP() and not footprint.IsExcludedFromBOM()
    ]
    missing_lcsc = {}
    for footprint in fitted:
        fields = footprint.GetFieldsText()
        if not fields.get("LCSC ID", "").strip():
            missing_lcsc[footprint.GetReference()] = (
                footprint.GetValue().strip(),
                fields.get("OEM", "").strip(),
                fields.get("OEM PN", "").strip(),
            )
        if footprint.IsExcludedFromPosFiles():
            raise RuntimeError(
                f"fitted BOM item {footprint.GetReference()} is missing from placement output"
            )
    if missing_lcsc != SPECIALTY_CONNECTORS_WITHOUT_LCSC_ID:
        raise RuntimeError(f"unexpected fitted parts without LCSC IDs: {missing_lcsc}")
    if len(fitted) != 153:
        raise RuntimeError(f"expected 153 fitted BOM references, found {len(fitted)}")
    smd_count = sum(fp.GetAttributes() == pcbnew.FP_SMD for fp in fitted)
    through_hole_count = sum(fp.GetAttributes() == pcbnew.FP_THROUGH_HOLE for fp in fitted)
    if (smd_count, through_hole_count) != (133, 20):
        raise RuntimeError(
            "unexpected fitted technology counts: "
            f"SMD={smd_count}, through-hole={through_hole_count}"
        )

    for ref, expected in EXPECTED_PATHS.items():
        actual = by_ref[ref].GetPath().AsString()
        if actual != expected:
            raise RuntimeError(f"{ref} native schematic association mismatch: {actual!r}")

    for ref in MOUNTING_REFS:
        footprint = by_ref[ref]
        if footprint.GetValue() != "M2":
            raise RuntimeError(f"{ref} must identify the inherited 2.2 mm geometry as M2")
        drills = {tuple(pad.GetDrillSize()) for pad in footprint.Pads()}
        if drills != {(2_200_000, 2_200_000)}:
            raise RuntimeError(f"{ref} mounting drill changed from controlled 2.2 mm: {drills}")

    critical_fields = {
        "D204": ("C22452", "MDD (Microdiode Semiconductor)", "SS54", "SMA"),
        "D605": ("C22452", "MDD (Microdiode Semiconductor)", "SS54", "SMA"),
        "D606": ("C22452", "MDD (Microdiode Semiconductor)", "SS54", "SMA"),
        "D205": ("C2886021", "Comchip Technology", "CDBU0130-HF", "0603/SOD-523F"),
        "D206": ("C2886021", "Comchip Technology", "CDBU0130-HF", "0603/SOD-523F"),
        "D601": ("C880909", "FUXINSEMI", "KMB14F", "MBF"),
    }
    for ref, expected in critical_fields.items():
        fields = by_ref[ref].GetFieldsText()
        actual = tuple(fields.get(name, "") for name in ("LCSC ID", "OEM", "OEM PN", "Package"))
        if actual != expected:
            raise RuntimeError(f"{ref} critical metadata mismatch: {actual}")
        if not fields.get("Datasheet", "") or not fields.get("Description", ""):
            raise RuntimeError(f"{ref} must have datasheet and description metadata")

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

    inner_thicknesses = {
        layer: float(value)
        for layer, value in re.findall(
            r'\(layer "(In[12]\.Cu)"\s+\(type "copper"\)\s+\(thickness ([0-9.]+)\)',
            board_text,
        )
    }
    if inner_thicknesses != {"In1.Cu": 0.0175, "In2.Cu": 0.0175}:
        raise RuntimeError(f"controlled 0.5 oz inner copper stackup changed: {inner_thicknesses}")

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
    revision = next(
        drawing for drawing in board.GetDrawings()
        if isinstance(drawing, pcbnew.PCB_TEXT) and drawing.GetText() == "KH910 REV A 09/2026"
    )
    if revision.GetLayer() != pcbnew.F_SilkS:
        raise RuntimeError("revision label must remain on front silkscreen")
    revision_box = revision.GetBoundingBox().GetInflated(pcbnew.FromMM(0.20))
    board_outline = pcbnew.SHAPE_POLY_SET()
    try:
        outline_ok = board.GetBoardPolygonOutlines(board_outline)
    except TypeError:
        # KiCad 10 added the explicit infer-outline argument.  Keep KiCad 9 as
        # the authoritative CI runtime while allowing the same check on 10.
        outline_ok = board.GetBoardPolygonOutlines(board_outline, False)
    if not outline_ok:
        raise RuntimeError("cannot construct the board outline for revision-label clearance")
    revision_corners = (
        pcbnew.VECTOR2I(revision_box.GetLeft(), revision_box.GetTop()),
        pcbnew.VECTOR2I(revision_box.GetRight(), revision_box.GetTop()),
        pcbnew.VECTOR2I(revision_box.GetLeft(), revision_box.GetBottom()),
        pcbnew.VECTOR2I(revision_box.GetRight(), revision_box.GetBottom()),
    )
    if not all(board_outline.Contains(corner) for corner in revision_corners):
        raise RuntimeError("revision label and clearance margin extend beyond the board outline")

    pad_hits = []
    for footprint in physical:
        for pad in footprint.Pads():
            if pad.IsOnLayer(pcbnew.F_Mask) and revision_box.Intersects(
                pad.GetBoundingBox().GetInflated(pcbnew.FromMM(0.10))
            ):
                pad_hits.append(f"{footprint.GetReference()}.{pad.GetNumber()}")
    if pad_hits:
        raise RuntimeError(f"revision label overlaps front pad/mask clearance: {sorted(pad_hits)}")

    courtyard_hits = []
    footprint_silk_hits = []
    # Artwork footprints have no component reference but still obstruct silk.
    for footprint in board.GetFootprints():
        if footprint.GetLayer() != pcbnew.F_Cu:
            continue
        courtyard = footprint.GetCourtyard(pcbnew.F_CrtYd)
        if not courtyard.IsEmpty() and revision_box.Intersects(
            courtyard.BBox().GetInflated(pcbnew.FromMM(0.10))
        ):
            courtyard_hits.append(footprint.GetReference())
        for graphic in footprint.GraphicalItems():
            if graphic.GetLayer() != pcbnew.F_SilkS:
                continue
            if hasattr(graphic, "IsVisible") and not graphic.IsVisible():
                continue
            if revision_box.Intersects(graphic.GetBoundingBox().GetInflated(pcbnew.FromMM(0.05))):
                footprint_silk_hits.append(footprint.GetReference())
    if courtyard_hits:
        raise RuntimeError(f"revision label overlaps front footprint courtyards: {sorted(courtyard_hits)}")
    if footprint_silk_hits:
        raise RuntimeError(f"revision label overlaps front footprint silkscreen: {sorted(set(footprint_silk_hits))}")

    board_silk_hits = []
    for drawing in board.GetDrawings():
        if drawing.GetLayer() != pcbnew.F_SilkS:
            continue
        if isinstance(drawing, pcbnew.PCB_TEXT) and drawing.GetText() == revision.GetText():
            continue
        if revision_box.Intersects(drawing.GetBoundingBox().GetInflated(pcbnew.FromMM(0.05))):
            board_silk_hits.append(type(drawing).__name__)
    if board_silk_hits:
        raise RuntimeError(f"revision label overlaps existing board silkscreen: {board_silk_hits}")
    if any(fp.GetReference() == "kibuzzard-65BDBF94" for fp in board.GetFootprints()):
        raise RuntimeError("obsolete v0.1 rev A 02/24 badge is still present")
    if any(fp.GetReference() == "kibuzzard-65BFE062" for fp in board.GetFootprints()):
        raise RuntimeError("obsolete C:900,965,270 gate-area legend is still present")

    model_paths = re.findall(r'\(model "\$\{KIPRJMOD\}/\.\./ayab-library/packages3D/([^\"]+)"', board_text)
    if len(model_paths) != 165:
        raise RuntimeError(f"expected 165 repository-relative 3D models, found {len(model_paths)}")
    missing_models = sorted(name for name in model_paths if not (LIBRARY_ROOT / "packages3D" / name).is_file())
    if missing_models:
        raise RuntimeError(f"unresolved repository 3D models: {missing_models}")
    exact_model_names = {path.name for path in (LIBRARY_ROOT / "packages3D").iterdir() if path.is_file()}
    wrong_case_models = sorted(name for name in model_paths if name not in exact_model_names)
    if wrong_case_models:
        raise RuntimeError(f"3D model filename case does not match the repository: {wrong_case_models}")

    plugin_factory = getattr(pcbnew.PCB_IO_MGR, "PluginFind", None)
    if plugin_factory is None:
        plugin_factory = pcbnew.PCB_IO_MGR.FindPlugin
    plugin = plugin_factory(pcbnew.PCB_IO_MGR.KICAD_SEXP)
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
    print("FITTED_BOM_REFS", len(fitted))
    print("FITTED_SMD_REFS", smd_count)
    print("FITTED_THROUGH_HOLE_REFS", through_hole_count)
    print("SPECIALTY_CONNECTORS_WITHOUT_LCSC_ID", len(missing_lcsc))
    print("FOOTPRINT_TREE_UUIDS_UNIQUE", len(serialized_uuids))
    print("REVISION_LABEL_CLEARANCE_OK")


if __name__ == "__main__":
    main()
