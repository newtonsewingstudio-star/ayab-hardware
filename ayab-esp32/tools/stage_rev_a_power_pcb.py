#!/usr/bin/env python3
"""Create a disposable Rev A power-integration PCB candidate.

This stages the already-approved schematic components onto the actual board,
removes the obsolete 0-ohm 5 V bypass, and moves GPIO4 to the divider net.  It
never writes the source board: a CI workflow must run KiCad DRC on its output
before any routing or promotion is considered.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pcbnew

sys.path.insert(0, str(Path(__file__).resolve().parent))
import patch_rev_a_solenoid_pcb as u


ROOT = Path(__file__).resolve().parents[1]
PSU = ROOT / "psu.kicad_sch"
MCU = ROOT / "mcu.kicad_sch"
SENSE = "/ESP32/MACHINE_PWR_SENSE"
PLACEMENTS = {"U403": (300.0, 155.0), "R215": (230.0, 142.0), "R216": (233.0, 142.0)}


def clone9(template, new_ref, value, x, y, angle, path, lcsc, padmap):
    """Clone an embedded footprint with fresh KiCad identities."""
    out = re.sub(r"\((uuid|tstamp) [0-9a-f-]+\)", lambda m: f"({m.group(1)} {u.uid()})", template)
    out, count = re.subn(
        r"^(\(footprint.*?)(\(at\s+[-\d.]+\s+[-\d.]+(?:\s+[-\d.]+)?\))",
        lambda m: m.group(1) + f"(at {x:g} {y:g} {angle:g})",
        out, count=1, flags=re.S,
    )
    if count != 1:
        raise RuntimeError(f"could not relocate {new_ref}")
    out, count = re.subn(r'\(path "[^"]+"\)', f'(path "{path}")', out, count=1)
    if count != 1:
        raise RuntimeError(f"path anchor missing in {new_ref}")
    out, count = re.subn(r'\(property "Reference" "[^"]+"', f'(property "Reference" "{new_ref}"', out, count=1)
    if count != 1:
        raise RuntimeError(f"reference property missing in {new_ref}")
    out, count = re.subn(r'\(property "Value" "[^"]+"', f'(property "Value" "{value}"', out, count=1)
    if count != 1:
        raise RuntimeError(f"value property missing in {new_ref}")
    if '(property "LCSC ID"' in out:
        out = re.sub(r'\(property "LCSC ID" "[^"]*"\)', f'(property "LCSC ID" "{lcsc}")', out, count=1)
    for number, (net, name) in padmap.items():
        out = u.replace_pad_net(out, number, net, name)
    return out


def clear_pad_net(block: str, number: str) -> str:
    replacements = []
    for start, end, pad in u.blocks(block, "(pad "):
        if u.pad_num(pad) == str(number):
            replacements.append((start, end, re.sub(r"\s*\(net\s+\d+\s+\"[^\"]*\"\)", "", pad, count=1)))
    if len(replacements) != 1:
        raise RuntimeError(f"expected one pad {number}")
    for start, end, replacement in reversed(replacements):
        block = block[:start] + replacement + block[end:]
    return block


def sheet_prefix(text: str, reference: str) -> str:
    _, _, block = u.find_fp(text, reference)
    match = re.search(r'\(path "([^"]+)"\)', block)
    if not match:
        raise RuntimeError(f"path missing for {reference}")
    return match.group(1).rsplit("/", 1)[0]


def root_net_defs(text: str) -> dict[int, str]:
    return {int(code): name for code, name in re.findall(r'^\t\(net\s+(\d+)\s+"([^"]+)"\)', text, re.M)}


def insert_before_root_item(text: str, item: str, payload: str) -> str:
    match = re.search(rf"(?m)^\t\({re.escape(item)}\b", text)
    if not match:
        raise RuntimeError(f"root {item} insertion anchor missing")
    return text[:match.start()] + payload + "\n" + text[match.start():]


def remove_footprint(text: str, reference: str) -> tuple[str, list[tuple[float, float]]]:
    start, end, block = u.find_fp(text, reference)
    pads = [u.pad_global(block, number) for number in ("1", "2")]
    return text[:start] + text[end:], pads


def remove_tracks_touching(text: str, points: list[tuple[float, float]]) -> tuple[str, int]:
    removals = []
    for start, end, block in u.blocks(text, "(segment"):
        details = u.seg_points(block)
        if details and any(u.close(details[0], point) or u.close(details[1], point) for point in points):
            removals.append((start, end))
    for start, end, block in u.blocks(text, "(via"):
        at = re.search(r"\(at\s+([-\d.]+)\s+([-\d.]+)\)", block)
        if at and any(u.close((float(at.group(1)), float(at.group(2))), point) for point in points):
            removals.append((start, end))
    for start, end in reversed(sorted(removals)):
        text = text[:start] + text[end:]
    return text, len(removals)


def remove_gpio4_branch(text: str) -> tuple[str, int]:
    target = ((209.785, 129.675), (217.125, 129.675))
    removals = []
    for start, end, block in u.blocks(text, "(segment"):
        details = u.seg_points(block)
        if not details:
            continue
        if (u.close(details[0], target[0]) and u.close(details[1], target[1])) or (u.close(details[0], target[1]) and u.close(details[1], target[0])):
            removals.append((start, end))
    if len(removals) != 1:
        raise RuntimeError(f"expected one direct GPIO4 legacy segment, found {len(removals)}")
    start, end = removals[0]
    return text[:start] + text[end:], 1


def symbol_uuid(path: Path, reference: str) -> str:
    return u.symbol_uuid_by_ref(path.read_text(encoding="utf-8"), reference)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    text = args.input.read_text(encoding="utf-8")
    existing = {ref for ref in ("U403", "R215", "R216") if f'(property "Reference" "{ref}"' in text}
    if existing:
        raise RuntimeError("partial power PCB state already present: " + ", ".join(sorted(existing)))
    defs = root_net_defs(text)
    names = {name: next((code for code, value in defs.items() if value == name), 0) for name in ("GND", "+5V", "+12V", "/PSU/5V_SW")}
    if any(code <= 0 for code in names.values()):
        raise RuntimeError(f"required board net missing: {names}")
    sense_code = max(defs) + 1

    text, r611_pads = remove_footprint(text, "R611")
    text, removed_bypass_tracks = remove_tracks_touching(text, r611_pads)
    _, _, u201 = u.find_fp(text, "U201")
    u201 = u.replace_pad_net(u201, "8", sense_code, SENSE)
    text = u.replace_fp(text, "U201", u201)
    text, removed_gpio4_tracks = remove_gpio4_branch(text)

    _, _, q501 = u.find_fp(text, "Q501")
    _, _, r206 = u.find_fp(text, "R206")
    psu_prefix = sheet_prefix(text, "U601")
    mcu_prefix = sheet_prefix(text, "U201")
    path_u403 = psu_prefix + "/" + symbol_uuid(PSU, "U403")
    path_r215 = mcu_prefix + "/" + symbol_uuid(MCU, "R215")
    path_r216 = mcu_prefix + "/" + symbol_uuid(MCU, "R216")
    x, y = PLACEMENTS["U403"]
    u403 = clone9(q501, "U403", "LM66100DCKR", x, y, 0, path_u403, "C2869734", {
        "1": (names["/PSU/5V_SW"], "/PSU/5V_SW"), "2": (names["GND"], "GND"),
        "3": (names["+5V"], "+5V"), "4": (names["+5V"], "+5V"),
        "5": (names["GND"], "GND"), "6": (names["+5V"], "+5V"),
    })
    u403 = clear_pad_net(u403, "4")
    x, y = PLACEMENTS["R215"]
    r215 = clone9(r206, "R215", "47k", x, y, 0, path_r215, "C25819", {
        "1": (names["+12V"], "+12V"), "2": (sense_code, SENSE),
    })
    x, y = PLACEMENTS["R216"]
    r216 = clone9(r206, "R216", "10k", x, y, 0, path_r216, "C25804", {
        "1": (sense_code, SENSE), "2": (names["GND"], "GND"),
    })
    text = insert_before_root_item(text, "footprint", f'\t(net {sense_code} "{SENSE}")')
    text = insert_before_root_item(text, "segment", "\n".join((u403, r215, r216)))
    args.output.write_text(text, encoding="utf-8")

    board = pcbnew.LoadBoard(str(args.output))
    if board is None:
        raise RuntimeError("KiCad could not reload staged power board")
    for footprint in board.GetFootprints():
        if footprint.GetReference() in PLACEMENTS:
            footprint.Flip(footprint.GetPosition(), False)
    board.BuildConnectivity()

    footprints = {footprint.GetReference(): footprint for footprint in board.GetFootprints()}

    def pad_position(reference: str, number: str) -> tuple[float, float]:
        footprint = footprints.get(reference)
        if footprint is None:
            raise RuntimeError(f"staged footprint missing: {reference}")
        pad = next((item for item in footprint.Pads() if item.GetNumber() == number), None)
        if pad is None:
            raise RuntimeError(f"staged pad missing: {reference}.{number}")
        point = pad.GetPosition()
        return pcbnew.ToMM(point.x), pcbnew.ToMM(point.y)

    def add_segment(start: tuple[float, float], end: tuple[float, float], net_name: str) -> None:
        code = board.GetNetcodeFromNetname(net_name)
        if code <= 0:
            raise RuntimeError(f"staged net missing: {net_name}")
        track = pcbnew.PCB_TRACK(board)
        track.SetStart(pcbnew.VECTOR2I_MM(*start))
        track.SetEnd(pcbnew.VECTOR2I_MM(*end))
        track.SetWidth(pcbnew.FromMM(0.25))
        track.SetLayer(pcbnew.B_Cu)
        track.SetNetCode(code)
        board.Add(track)

    # These three ties are wholly inside the new low-voltage island.  The two
    # detours preserve clearance to U403's GND pads and R216's grounded end.
    # Keeping them local first lets CI distinguish their geometry from the
    # remaining long runs back to the existing 5 V, 12 V, GND and MCU copper.
    add_segment(pad_position("U403", "2"), pad_position("U403", "5"), "GND")
    u403_p3 = pad_position("U403", "3")
    u403_p6 = pad_position("U403", "6")
    add_segment(u403_p3, (301.50, 156.25), "+5V")
    add_segment((301.50, 156.25), (298.50, 156.25), "+5V")
    add_segment((298.50, 156.25), (298.50, u403_p6[1]), "+5V")
    add_segment((298.50, u403_p6[1]), u403_p6, "+5V")
    r215_p2 = pad_position("R215", "2")
    r216_p1 = pad_position("R216", "1")
    add_segment(r215_p2, (r215_p2[0], 143.00), SENSE)
    add_segment((r215_p2[0], 143.00), (234.50, 143.00), SENSE)
    add_segment((234.50, 143.00), r216_p1, SENSE)

    # Use already-routed landing points for the two shortest external ties:
    # the B.Cu +5 V trace beside U403 and the established GND through-via
    # below the divider.  The remaining raw-power and sense runs are kept out
    # of this narrow stage until their longer corridors are independently
    # checked.
    add_segment((301.50, 156.25), (302.00, 156.25), "+5V")
    add_segment((302.00, 156.25), (302.00, 148.75), "+5V")
    add_segment((302.00, 148.75), (301.09, 147.99), "+5V")
    r216_p2 = pad_position("R216", "2")
    add_segment(r216_p2, (r216_p2[0], 145.30), "GND")
    add_segment((r216_p2[0], 145.30), (230.41, 145.30), "GND")

    board.BuildConnectivity()
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(args.output), board)
    print("POWER_STAGE_OK", args.output)
    print("REMOVED_BYPASS_TRACKS", removed_bypass_tracks)
    print("REMOVED_GPIO4_TRACKS", removed_gpio4_tracks)


if __name__ == "__main__":
    main()
