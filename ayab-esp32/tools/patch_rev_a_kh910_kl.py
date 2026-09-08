#!/usr/bin/env python3
"""Implement the KH-910 right-side K/L Rev A schematic architecture.

This is deliberately a staged change:

* The KH-910's two digital open-collector outputs are disconnected from the
  LM393 conditioning sheet, so the board comparators cannot sink or alter them.
* Those two machine outputs are routed separately to ESP32 GPIO17 and GPIO18.
* Each GPIO gets an external 10 kOhm pull-up to 3.3 V.
* Existing analog Hall/comparator paths are left intact for the next staged
  change, so this patch does not yet remove the LM393 hardware altogether.

Files modified:
  ayab-esp32.kicad_sch
  mcu.kicad_sch
  ioconditioning.kicad_sch

The script is assertion-heavy and idempotent. KiCad ERC/DRC is the final gate.
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT / "ayab-esp32.kicad_sch"
MCU = ROOT / "mcu.kicad_sch"
IO = ROOT / "ioconditioning.kicad_sch"


def uid() -> str:
    return str(uuid.uuid4())


def extract_block(text: str, start: int) -> tuple[str, int]:
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start : i + 1], i + 1
    raise RuntimeError("Unbalanced KiCad block")


def remove_block(text: str, token: str, required: bool = True) -> str:
    start = text.find(token)
    if start < 0:
        if required:
            raise RuntimeError(f"Block not found: {token}")
        return text
    _, end = extract_block(text, start)
    if end < len(text) and text[end] == "\n":
        end += 1
    return text[:start] + text[end:]


def find_sheet(text: str, sheetfile: str) -> tuple[int, int, str]:
    pos = 0
    while True:
        start = text.find("(sheet ", pos)
        if start < 0:
            raise RuntimeError(f"Sheet not found: {sheetfile}")
        block, end = extract_block(text, start)
        if f'(property "Sheetfile" "{sheetfile}"' in block:
            return start, end, block
        pos = end


def remove_pin_from_sheet(block: str, pin_name: str) -> str:
    token = f'(pin "{pin_name}"'
    start = block.find(token)
    if start < 0:
        raise RuntimeError(f"Sheet pin not found: {pin_name}")
    _, end = extract_block(block, start)
    if end < len(block) and block[end] == "\n":
        end += 1
    return block[:start] + block[end:]


def add_pin_to_sheet(block: str, name: str, y: str) -> str:
    if f'(pin "{name}"' in block:
        return block
    marker = "    (instances"
    pos = block.find(marker)
    if pos < 0:
        raise RuntimeError("Sheet instances anchor not found")
    pin = (
        f'    (pin "{name}" input (at 140.97 {y} 0)\n'
        '      (effects (font (size 1.27 1.27)) (justify right))\n'
        f'      (uuid {uid()})\n'
        '    )\n'
    )
    return block[:pos] + pin + block[pos:]


def wire_block(a: tuple[str, str], b: tuple[str, str]) -> str:
    return (
        f'  (wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]}))\n'
        '    (stroke (width 0) (type default))\n'
        f'    (uuid {uid()})\n'
        '  )\n'
    )


def remove_wire_between(text: str, a: tuple[float, float], b: tuple[float, float]) -> str:
    pos = 0
    while True:
        start = text.find("(wire ", pos)
        if start < 0:
            raise RuntimeError(f"Wire not found between {a} and {b}")
        block, end = extract_block(text, start)
        m = re.search(
            r"\(pts\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\)",
            block,
            re.S,
        )
        if m:
            p1 = (float(m.group(1)), float(m.group(2)))
            p2 = (float(m.group(3)), float(m.group(4)))
            if {p1, p2} == {a, b}:
                # Remove indentation/newline belonging to this root item as well.
                real_start = start
                while real_start > 0 and text[real_start - 1] == " ":
                    real_start -= 1
                if real_start > 0 and text[real_start - 1] == "\n":
                    real_start -= 1
                if end < len(text) and text[end] == "\n":
                    end += 1
                return text[:real_start] + text[end:]
        pos = end


def replace_local_label_with_hier(text: str, old: str, new: str, x: str, y: str) -> str:
    if f'(hierarchical_label "{new}"' in text:
        return text
    token = f'(label "{old}" (at {x} {y} 180)'
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f"Local MCU label not found: {old}")
    _, end = extract_block(text, start)
    if end < len(text) and text[end] == "\n":
        end += 1
    text = text[:start] + text[end:]

    marker = "  (hierarchical_label "
    pos = text.find(marker)
    if pos < 0:
        raise RuntimeError("MCU hierarchical-label anchor not found")
    block = (
        f'  (hierarchical_label "{new}" (shape input) (at {x} {y} 0) (fields_autoplaced)\n'
        '    (effects (font (size 1.27 1.27)) (justify left))\n'
        f'    (uuid {uid()})\n'
        '  )\n'
    )
    return text[:pos] + block + text[pos:]


def shift_at_coordinates(block: str, dx: float, dy: float) -> str:
    pattern = re.compile(r"\(at\s+([-\d.]+)\s+([-\d.]+)(\s+[-\d.]+)?\)")

    def repl(m: re.Match) -> str:
        x = round(float(m.group(1)) + dx, 4)
        y = round(float(m.group(2)) + dy, 4)
        suffix = m.group(3) or ""
        return f"(at {x:g} {y:g}{suffix})"

    return pattern.sub(repl, block)


def clone_symbol(text: str, token: str, new_x: float, new_y: float, old_ref: str, new_ref: str) -> str:
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f"Clone source not found: {token}")
    block, _ = extract_block(text, start)
    pos_m = re.search(r"\(at\s+([-\d.]+)\s+([-\d.]+)", block)
    if not pos_m:
        raise RuntimeError("Clone source position missing")
    old_x, old_y = float(pos_m.group(1)), float(pos_m.group(2))
    block = shift_at_coordinates(block, new_x - old_x, new_y - old_y)
    block = block.replace(f'"{old_ref}"', f'"{new_ref}"')
    block = re.sub(r"\(uuid [0-9a-f-]+\)", lambda _: f"(uuid {uid()})", block)
    return block


def next_ref(text: str, prefix: str, start_at: int) -> str:
    nums = [int(x) for x in re.findall(rf'property "Reference" "{re.escape(prefix)}(\d+)"', text)]
    n = max([start_at - 1] + nums) + 1
    return f"{prefix}{n}"


def insert_before_final_close(text: str, blocks: list[str]) -> str:
    pos = text.rfind("\n)")
    if pos < 0:
        raise RuntimeError("Root closing parenthesis not found")
    payload = "\n" + "\n".join(blocks) + "\n"
    return text[:pos] + payload + text[pos:]


def patch_mcu(text: str) -> str:
    if '(hierarchical_label "KH910_R_K"' in text and '(hierarchical_label "KH910_R_L"' in text:
        return text

    text = replace_local_label_with_hier(text, "ESP17", "KH910_R_K", "198.12", "110.49")
    text = replace_local_label_with_hier(text, "ESP18", "KH910_R_L", "198.12", "113.03")

    r1 = next_ref(text, "R", 209)
    # Reserve the first number before computing the second.
    r2 = f"R{int(r1[1:]) + 1}"
    p1 = next_ref(text, "#PWR", 220)
    p2 = f"#PWR{int(p1[4:]) + 1}"

    if r1 in text or r2 in text or p1 in text or p2 in text:
        raise RuntimeError("Unexpected reference collision while adding K/L pull-ups")

    # Clone known-good 10k resistor R205 and a +3V3 power symbol.
    r_source = '(symbol (lib_id "ayab-lib:R_Small_US") (at 87.63 41.91 0)'
    p_source = '(symbol (lib_id "power:+3V3") (at 247.65 33.02 0)'
    r_k = clone_symbol(text, r_source, 205.74, 105.41, "R205", r1)
    r_l = clone_symbol(text, r_source, 213.36, 107.95, "R205", r2)
    p_k = clone_symbol(text, p_source, 205.74, 100.33, "#PWR0211", p1)
    p_l = clone_symbol(text, p_source, 213.36, 102.87, "#PWR0211", p2)

    # Add pull-up wiring before the label section.
    marker = "  (label "
    pos = text.find(marker)
    if pos < 0:
        raise RuntimeError("MCU wire insertion anchor not found")
    wires = "".join([
        wire_block(("198.12", "110.49"), ("205.74", "110.49")),
        wire_block(("205.74", "110.49"), ("205.74", "107.95")),
        wire_block(("205.74", "102.87"), ("205.74", "100.33")),
        wire_block(("198.12", "113.03"), ("213.36", "113.03")),
        wire_block(("213.36", "113.03"), ("213.36", "110.49")),
        wire_block(("213.36", "105.41"), ("213.36", "102.87")),
    ])
    text = text[:pos] + wires + text[pos:]
    text = insert_before_final_close(text, [r_k, r_l, p_k, p_l])

    # Confirm cloned resistor values remained 10k.
    if text.count('(property "Value" "10k"') < 2:
        raise RuntimeError("10k pull-up resistor values not present")
    return text


def patch_io(text: str) -> str:
    # Remove only the KH910 digital input labels and their short attachments to
    # the comparator network. The analog comparator circuit remains for now.
    if '(hierarchical_label "EOL_R_K"' in text:
        text = remove_block(text, '(hierarchical_label "EOL_R_K"')
        text = remove_wire_between(text, (182.88, 120.65), (181.61, 120.65))
    if '(hierarchical_label "EOL_R_L"' in text:
        text = remove_block(text, '(hierarchical_label "EOL_R_L"')
        text = remove_wire_between(text, (182.88, 144.78), (179.07, 144.78))
    return text


def patch_top(text: str) -> str:
    if '(pin "KH910_R_K" input' in text and '(pin "KH910_R_L" input' in text:
        return text

    # Remove K/L pins from IO CONDITIONING sheet.
    s, e, io_sheet = find_sheet(text, "ioconditioning.kicad_sch")
    io_sheet = remove_pin_from_sheet(io_sheet, "EOL_R_K")
    io_sheet = remove_pin_from_sheet(io_sheet, "EOL_R_L")
    text = text[:s] + io_sheet + text[e:]

    # Add dedicated inputs to MCU sheet.
    s, e, mcu_sheet = find_sheet(text, "mcu.kicad_sch")
    mcu_sheet = add_pin_to_sheet(mcu_sheet, "KH910_R_K", "149.86")
    mcu_sheet = add_pin_to_sheet(mcu_sheet, "KH910_R_L", "152.4")
    text = text[:s] + mcu_sheet + text[e:]

    # Disconnect raw Brother digital outputs from the comparator sheet.
    text = remove_wire_between(text, (200.66, 144.78), (219.71, 144.78))
    text = remove_wire_between(text, (200.66, 147.32), (219.71, 147.32))

    # Route each raw signal around/below the IO-conditioning sheet to the new
    # MCU sheet pins. Separate geometry prevents accidental K/L junctions.
    routes = [
        (("219.71", "144.78"), ("215.9", "144.78")),
        (("215.9", "144.78"), ("215.9", "160.02")),
        (("215.9", "160.02"), ("146.05", "160.02")),
        (("146.05", "160.02"), ("146.05", "149.86")),
        (("146.05", "149.86"), ("140.97", "149.86")),
        (("219.71", "147.32"), ("218.44", "147.32")),
        (("218.44", "147.32"), ("218.44", "162.56")),
        (("218.44", "162.56"), ("148.59", "162.56")),
        (("148.59", "162.56"), ("148.59", "152.4")),
        (("148.59", "152.4"), ("140.97", "152.4")),
    ]
    payload = "".join(wire_block(a, b) for a, b in routes)
    marker = "  (sheet "
    pos = text.find(marker)
    if pos < 0:
        raise RuntimeError("Top-level wire insertion anchor not found")
    text = text[:pos] + payload + text[pos:]
    return text


def main() -> None:
    top = TOP.read_text(encoding="utf-8")
    mcu = MCU.read_text(encoding="utf-8")
    io = IO.read_text(encoding="utf-8")

    already = (
        '(pin "KH910_R_K" input' in top
        and '(pin "KH910_R_L" input' in top
        and '(hierarchical_label "KH910_R_K"' in mcu
        and '(hierarchical_label "KH910_R_L"' in mcu
        and '(hierarchical_label "EOL_R_K"' not in io
        and '(hierarchical_label "EOL_R_L"' not in io
    )
    if already:
        print("KH910 K/L Rev A schematic patch already applied")
        return

    top = patch_top(top)
    mcu = patch_mcu(mcu)
    io = patch_io(io)

    # Cross-file postconditions.
    for name in ("KH910_R_K", "KH910_R_L"):
        if f'(pin "{name}" input' not in top:
            raise RuntimeError(f"Top-level MCU sheet pin missing: {name}")
        if f'(hierarchical_label "{name}"' not in mcu:
            raise RuntimeError(f"MCU hierarchical label missing: {name}")
    if '(hierarchical_label "EOL_R_K"' in io or '(hierarchical_label "EOL_R_L"' in io:
        raise RuntimeError("KH910 digital inputs are still attached to IO conditioning")
    if '(pin "EOL_R_K" input' in top or '(pin "EOL_R_L" input' in top:
        raise RuntimeError("Top-level IO-conditioning K/L pins still exist")

    TOP.write_text(top, encoding="utf-8")
    MCU.write_text(mcu, encoding="utf-8")
    IO.write_text(io, encoding="utf-8")
    print("Applied KH910 K/L comparator bypass and 3.3V pull-ups")


if __name__ == "__main__":
    main()
