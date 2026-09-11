#!/usr/bin/env python3
"""Stage independent GPIO4 clamp/filter protection on a disposable Rev A copy.

The existing divider remains:
    +12V -- R215 47k -- MACHINE_PWR_SENSE -- R216 10k -- GND

This stage adds, physically close to the GPIO4 route:
    D205 CDBU0130-HF: MACHINE_PWR_SENSE (A) -> +3V3 (K)
    D206 CDBU0130-HF: GND (A) -> MACHINE_PWR_SENSE (K)
    C206 100n:    MACHINE_PWR_SENSE -> GND

R215 limits clamp current if R216 opens or the machine rail has a positive
transient.  D206 covers negative excursions.  C206 supplies the 100 nF ADC
input filtering used by Espressif's published ADC characterization.

The script edits only the paths supplied on the command line.  CI runs it on a
disposable project copy, refills zones, and treats KiCad 9 DRC/ERC as
authoritative before anything can be promoted.
"""

from __future__ import annotations

import re
import sys
import uuid
from pathlib import Path

import pcbnew

sys.path.insert(0, str(Path(__file__).resolve().parent))
import patch_rev_a_solenoid_pcb as pcbutil


if len(sys.argv) != 3:
    raise SystemExit("usage: stage_rev_a_machine_sense_protection.py PCB MCU_SCHEMATIC")

PCB = Path(sys.argv[1])
MCU = Path(sys.argv[2])
PSU = MCU.with_name("psu.kicad_sch")

SENSE = "/ESP32/MACHINE_PWR_SENSE"
CDBU0130_DATASHEET = (
    "https://datasheet.lcsc.com/lcsc/2205091530_"
    "Comchip-Technology-CDBU0130-HF_C2886021.pdf"
)


def uid() -> str:
    return str(uuid.uuid4())


def extract_block(text: str, start: int) -> tuple[str, int]:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start:index + 1], index + 1
    raise RuntimeError("unbalanced KiCad expression")


def clone_at(text: str, token: str, x: float, y: float, old_ref: str, new_ref: str,
             rotation: float | None = None) -> str:
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f"clone source not found: {token}")
    block, _ = extract_block(text, start)
    origin = re.search(r"\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+[-\d.]+)?\)", block)
    if not origin:
        raise RuntimeError(f"clone source has no position: {token}")
    ox, oy = float(origin.group(1)), float(origin.group(2))

    def shift(match: re.Match[str]) -> str:
        nx = float(match.group(1)) + x - ox
        ny = float(match.group(2)) + y - oy
        tail = match.group(3) or ""
        return f"(at {nx:g} {ny:g}{tail})"

    block = re.sub(r"\(at\s+([-\d.]+)\s+([-\d.]+)(\s+[-\d.]+)?\)", shift, block)
    if rotation is not None:
        block = re.sub(
            r"^(\(symbol \(lib_id [^)]+\) \(at [-\d.]+ [-\d.]+)(?: [-\d.]+)?\)",
            rf"\g<1> {rotation:g})",
            block,
            count=1,
        )
    block = block.replace(f'"{old_ref}"', f'"{new_ref}"')
    block = re.sub(r"\(uuid [0-9a-f-]+\)", lambda _: f"(uuid {uid()})", block)
    return block


def set_property(block: str, name: str, value: str) -> str:
    updated, count = re.subn(
        rf'(\(property "{re.escape(name)}" ")[^"]*"',
        rf'\g<1>{value}"',
        block,
        count=1,
    )
    if count != 1:
        raise RuntimeError(f"property {name!r} missing")
    return updated


def replace_instances(block: str, sheet_path: str, symbol_ref: str) -> str:
    start = block.find("(instances")
    if start < 0:
        raise RuntimeError(f"instances missing in {symbol_ref}")
    _, end = extract_block(block, start)
    symbol_uuid = re.search(r"\(uuid ([0-9a-f-]+)\)", block)
    if not symbol_uuid:
        raise RuntimeError(f"symbol UUID missing in {symbol_ref}")
    replacement = (
        '(instances\n'
        '      (project "ayab-esp32"\n'
        f'        (path "{sheet_path}/{symbol_uuid.group(1)}"\n'
        f'          (reference "{symbol_ref}") (unit 1)\n'
        '        )\n'
        '      )\n'
        '    )'
    )
    return block[:start] + replacement + block[end:]


def wire(a: tuple[float, float], b: tuple[float, float]) -> str:
    return (
        f"  (wire (pts (xy {a[0]:g} {a[1]:g}) (xy {b[0]:g} {b[1]:g}))\n"
        "    (stroke (width 0) (type default))\n"
        f"    (uuid {uid()})\n"
        "  )\n"
    )


def junction(x: float, y: float) -> str:
    return (
        f"  (junction (at {x:g} {y:g}) (diameter 0) (color 0 0 0 0)\n"
        f"    (uuid {uid()})\n"
        "  )\n"
    )


def local_label(name: str, x: float, y: float) -> str:
    return (
        f'  (label "{name}" (at {x:g} {y:g} 0) (fields_autoplaced)\n'
        '    (effects (font (size 1.27 1.27)) (justify left bottom))\n'
        f'    (uuid {uid()})\n'
        '  )\n'
    )


def patch_schematic() -> None:
    mcu = MCU.read_text(encoding="utf-8")
    psu = PSU.read_text(encoding="utf-8")
    present = [ref for ref in ("D205", "D206", "C206") if f'(property "Reference" "{ref}"' in mcu]
    if present:
        if set(present) == {"D205", "D206", "C206"}:
            print("SENSE_PROTECTION_SCHEMATIC_ALREADY_PRESENT")
            return
        raise RuntimeError(f"partial sense-protection schematic: {present}")

    # Copy the exact project Schottky symbol definition into the MCU sheet.
    if '(symbol "ayab-lib:D_Schottky"' not in mcu:
        source = psu.find('(symbol "ayab-lib:D_Schottky"')
        if source < 0:
            raise RuntimeError("Schottky library symbol missing from PSU sheet")
        lib_block, _ = extract_block(psu, source)
        anchor = mcu.find('    (symbol "ayab-lib:')
        if anchor < 0:
            raise RuntimeError("MCU lib_symbols insertion anchor missing")
        mcu = mcu[:anchor] + "    " + lib_block + "\n" + mcu[anchor:]

    r215_start = mcu.find('(symbol (lib_id "ayab-lib:R_Small_US") (at 205.74 80.01 0)')
    if r215_start < 0:
        raise RuntimeError("R215 anchor missing")
    r215_block, _ = extract_block(mcu, r215_start)
    path_match = re.search(r'\(path "([^\"]+/)[0-9a-f-]+"', r215_block)
    if not path_match:
        raise RuntimeError("MCU sheet path missing")
    sheet_path = path_match.group(1).rstrip("/")

    diode_token = '(symbol (lib_id "ayab-lib:D_Schottky") (at 214.63 60.96 270)'
    upper = clone_at(psu, diode_token, 213.36, 78.74, "D405", "D205", 90)
    lower = clone_at(psu, diode_token, 213.36, 86.36, "D405", "D206", 90)
    for ref, block in (("D205", upper), ("D206", lower)):
        block = set_property(block, "Value", "CDBU0130-HF")
        block = set_property(block, "Footprint", "Diode_SMD:D_0603_1608Metric")
        block = set_property(block, "Datasheet", CDBU0130_DATASHEET)
        block = set_property(block, "Package", "0603/SOD-523F")
        block = set_property(block, "LCSC ID", "C2886021")
        block = set_property(block, "OEM PN", "CDBU0130-HF")
        block = set_property(block, "OEM", "Comchip Technology")
        block = replace_instances(block, sheet_path, ref)
        if ref == "D205":
            upper = block
        else:
            lower = block

    cap_token = '(symbol (lib_id "ayab-lib:C_Small") (at 154.94 41.91 0)'
    # Put pin 1 directly on the existing sense bus.  This avoids a short
    # one-grid wire stub that KiCad correctly reports as dangling when the
    # cloned symbol has not yet been normalized by eeschema.
    cap = clone_at(mcu, cap_token, 220.98, 85.09, "C204", "C206")
    cap = set_property(cap, "Value", "100n")
    cap = set_property(cap, "LCSC ID", "C14663")
    cap = set_property(cap, "Voltage rating", "50V X7R")
    cap = set_property(cap, "Package", "0603")
    cap = set_property(cap, "OEM PN", "CL10B104KB8NNNC")
    cap = set_property(cap, "OEM", "Samsung Electro-Mechanics")
    cap = replace_instances(cap, sheet_path, "C206")

    p3_token = '(symbol (lib_id "power:+3V3") (at 213.36 102.87 0)'
    p3 = clone_at(mcu, p3_token, 213.36, 74.93, "#PWR221", "#PWR224")
    p3 = replace_instances(p3, sheet_path, "#PWR224")
    gnd_token = '(symbol (lib_id "power:GND") (at 205.74 87.63 0)'
    gnd = clone_at(mcu, gnd_token, 213.36, 90.17, "#PWR223", "#PWR225")
    gnd = replace_instances(gnd, sheet_path, "#PWR225")

    wiring = "".join(
        [
            # Explicitly name the capacitor pin as well as wiring it to the
            # bus.  This makes the cloned symbol connectivity unambiguous to
            # KiCad's standalone/top-level ERC path resolution.
            local_label("MACHINE_PWR_SENSE", 220.98, 82.55),
            wire((205.74, 82.55), (220.98, 82.55)),
            wire((220.98, 87.63), (220.98, 90.17)),
            wire((213.36, 90.17), (220.98, 90.17)),
            junction(213.36, 82.55),
            junction(220.98, 82.55),
        ]
    )
    first_wire = mcu.find("  (wire ")
    if first_wire < 0:
        raise RuntimeError("schematic wire insertion anchor missing")
    mcu = mcu[:first_wire] + wiring + mcu[first_wire:]
    root_close = mcu.rfind("\n)")
    if root_close < 0:
        raise RuntimeError("schematic root close missing")
    mcu = mcu[:root_close] + "\n" + "\n".join((upper, lower, cap, p3, gnd)) + "\n" + mcu[root_close:]

    for token in ("D205", "D206", "C206", "C2886021", "C14663", CDBU0130_DATASHEET):
        if token not in mcu:
            raise RuntimeError(f"schematic postcondition missing: {token}")
    MCU.write_text(mcu, encoding="utf-8")
    print("SENSE_PROTECTION_SCHEMATIC_STAGED D205 D206 C206")


def board_sheet_prefix(board_text: str) -> str:
    _, _, r215 = pcbutil.find_fp(board_text, "R215")
    path = re.search(r'\(path "([^\"]+)"\)', r215)
    if not path:
        raise RuntimeError("R215 footprint path missing")
    return path.group(1).rsplit("/", 1)[0]


def clone_footprint(template: str, reference: str, value: str, x: float, y: float,
                    angle: float, path: str, properties: dict[str, str],
                    padmap: dict[str, tuple[int, str]]) -> str:
    block = re.sub(r"\((uuid|tstamp) [0-9a-f-]+\)", lambda m: f"({m.group(1)} {uid()})", template)
    block, count = re.subn(
        r"^(\(footprint.*?)(\(at\s+[-\d.]+\s+[-\d.]+(?:\s+[-\d.]+)?\))",
        lambda m: m.group(1) + f"(at {x:g} {y:g} {angle:g})",
        block,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise RuntimeError(f"cannot position {reference}")
    block, count = re.subn(r'\(path "[^"]+"\)', f'(path "{path}")', block, count=1)
    if count != 1:
        raise RuntimeError(f"path missing in {reference}")
    block = re.sub(r'\(property "Reference" "[^"]+"', f'(property "Reference" "{reference}"', block, count=1)
    block = re.sub(r'\(property "Value" "[^"]+"', f'(property "Value" "{value}"', block, count=1)
    for name, prop_value in properties.items():
        if f'(property "{name}"' in block:
            block = re.sub(
                rf'(\(property "{re.escape(name)}" ")[^"]*"',
                rf'\g<1>{prop_value}"',
                block,
                count=1,
            )
    for pad_number, (net_number, net_name) in padmap.items():
        block = pcbutil.replace_pad_net(block, pad_number, net_number, net_name)
    return block


def patch_board() -> None:
    board_text = PCB.read_text(encoding="utf-8")
    schematic = MCU.read_text(encoding="utf-8")
    present = [ref for ref in ("D205", "D206", "C206") if f'(property "Reference" "{ref}"' in board_text]
    if present:
        if set(present) == {"D205", "D206", "C206"}:
            print("SENSE_PROTECTION_BOARD_ALREADY_PRESENT")
            return
        raise RuntimeError(f"partial sense-protection PCB: {present}")

    nets = pcbutil.net_defs(board_text)
    by_name = {name: number for number, name in nets.items()}
    required = {"GND", "+3V3", SENSE}
    if not required <= by_name.keys():
        raise RuntimeError(f"required nets missing: {sorted(required - by_name.keys())}")
    gnd, p3, sense = (by_name["GND"], by_name["+3V3"], by_name[SENSE])
    _, _, diode_template = pcbutil.find_fp(board_text, "D602")
    _, _, cap_template = pcbutil.find_fp(board_text, "C204")
    prefix = board_sheet_prefix(board_text)
    symbol_uuid = {ref: pcbutil.symbol_uuid_by_ref(schematic, ref) for ref in ("D205", "D206", "C206")}
    path = lambda ref: f"{prefix}/{symbol_uuid[ref]}"

    diode_props = {
        "Datasheet": CDBU0130_DATASHEET,
        "LCSC ID": "C2886021",
        "OEM PN": "CDBU0130-HF",
        "OEM": "Comchip Technology",
        "Package": "0603/SOD-523F",
    }
    cap_props = {
        "LCSC ID": "C14663",
        "OEM PN": "CL10B104KB8NNNC",
        "OEM": "Samsung Electro-Mechanics",
        "Package": "0603",
        "Voltage rating": "50V X7R",
    }
    footprints = [
        clone_footprint(diode_template, "D205", "CDBU0130-HF", 234.0, 157.0, 0.0,
                        path("D205"), diode_props, {"1": (p3, "+3V3"), "2": (sense, SENSE)}),
        clone_footprint(diode_template, "D206", "CDBU0130-HF", 234.0, 160.5, 180.0,
                        path("D206"), diode_props, {"1": (sense, SENSE), "2": (gnd, "GND")}),
        clone_footprint(cap_template, "C206", "100n", 237.25, 160.5, 0.0,
                        path("C206"), cap_props, {"1": (sense, SENSE), "2": (gnd, "GND")}),
    ]
    board_text = pcbutil.insert_before_first(board_text, "  (segment ", "\n".join(footprints))
    PCB.write_text(board_text, encoding="utf-8")

    board = pcbnew.LoadBoard(str(PCB))
    if board is None:
        raise RuntimeError("KiCad could not reload staged sense-protection board")
    fps = {footprint.GetReference(): footprint for footprint in board.GetFootprints()}
    for ref in ("D205", "D206", "C206"):
        fp = fps[ref]
        fp.Flip(fp.GetPosition(), False)
    board.BuildConnectivity()
    fps = {footprint.GetReference(): footprint for footprint in board.GetFootprints()}

    def pad(ref: str, number: str):
        item = next((p for p in fps[ref].Pads() if p.GetNumber() == number), None)
        if item is None:
            raise RuntimeError(f"pad missing: {ref}.{number}")
        pos = item.GetPosition()
        return item, (pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y))

    expected = {
        ("D205", "1"): "+3V3",
        ("D205", "2"): SENSE,
        ("D206", "1"): SENSE,
        ("D206", "2"): "GND",
        ("C206", "1"): SENSE,
        ("C206", "2"): "GND",
    }
    for (ref, number), net_name in expected.items():
        actual = pad(ref, number)[0].GetNetname()
        if actual != net_name:
            raise RuntimeError(f"{ref}.{number}: expected {net_name!r}, got {actual!r}")

    def add_segment(a: tuple[float, float], b: tuple[float, float], net_code: int,
                    layer=pcbnew.B_Cu, width: float = 0.25) -> None:
        track = pcbnew.PCB_TRACK(board)
        track.SetStart(pcbnew.VECTOR2I_MM(*a))
        track.SetEnd(pcbnew.VECTOR2I_MM(*b))
        track.SetWidth(pcbnew.FromMM(width))
        track.SetLayer(layer)
        track.SetNetCode(net_code)
        board.Add(track)

    positions = {f"{ref}.{number}": pad(ref, number)[1] for ref, number in expected}
    # Join the existing divider endpoint to the positive clamp, then branch to
    # the negative clamp and ADC filter without altering the proven GPIO4 via.
    sense_anchor = (229.325, 157.0)
    d205_sense = positions["D205.2"]
    d206_sense = positions["D206.1"]
    cap_sense = positions["C206.1"]
    # Route around the opposite-net pad of each 0603 device.  The first stage
    # used straight centreline tracks, which crossed D205.1 (+3V3) and C206.2
    # (GND); KiCad rejected those shorts.
    lower_channel_y = 161.75
    add_segment(sense_anchor, d205_sense, sense)
    add_segment(d205_sense, d206_sense, sense)
    add_segment(d206_sense, (d206_sense[0], lower_channel_y), sense)
    add_segment((d206_sense[0], lower_channel_y), (cap_sense[0], lower_channel_y), sense)
    add_segment((cap_sense[0], lower_channel_y), cap_sense, sense)

    # Reuse the nearest existing +3V3 through-via, avoiding a new rail stub or
    # a second high-impedance clamp reference.
    d205_p3 = positions["D205.1"]
    p3_via = (235.51, 151.07)
    add_segment(d205_p3, (d205_p3[0], 152.0), p3)
    add_segment((d205_p3[0], 152.0), p3_via, p3)

    pcbnew.SaveBoard(str(PCB), board)
    print("SENSE_PROTECTION_BOARD_STAGED D205 D206 C206")
    for key in sorted(positions):
        print("SENSE_PROTECTION_PAD", key, *(f"{value:.4f}" for value in positions[key]))


patch_schematic()
patch_board()
print("MACHINE_SENSE_PROTECTION_STAGE_OK")
