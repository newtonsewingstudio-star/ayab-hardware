#!/usr/bin/env python3
"""Stage 1 of the Rev A analog Hall redesign.

This converts the MCU-facing analog Hall interface from four comparator-derived
logic signals to two true ADC signals while leaving the old LM393 circuitry
physically present for one validation stage.

Electrical changes:
- EOL_L raw analog -> 10k/10k divider -> HALL_L_ADC -> ESP32 GPIO1 / ADC1_CH0
- EOL_R raw analog -> 10k/10k divider -> HALL_R_ADC -> ESP32 GPIO2 / ADC1_CH1
- comparator outputs are disconnected from ESP32 GPIO1..4
- GPIO3 (strapping) is freed
- GPIO4 is freed for the later MACHINE_PWR_SENSE implementation

A 10k/10k divider scales a nominal 0..5 V signal to 0..2.5 V, provides generous
3.3 V margin, and uses an already qualified/JLC-listed 0603 part on the design.
The raw Hall nets continue to feed the legacy comparator inputs in this staged
patch; those components will be removed only after this passive path passes
KiCad ERC/DRC and review.
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
                return text[start:i + 1], i + 1
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


def rename_sheet_pin(block: str, old: str, new: str) -> str:
    token = f'(pin "{old}"'
    if token not in block:
        if f'(pin "{new}"' in block:
            return block
        raise RuntimeError(f"Sheet pin not found: {old}")
    return block.replace(token, f'(pin "{new}"', 1)


def remove_sheet_pin(block: str, name: str) -> str:
    token = f'(pin "{name}"'
    start = block.find(token)
    if start < 0:
        return block
    _, end = extract_block(block, start)
    if end < len(block) and block[end] == "\n":
        end += 1
    return block[:start] + block[end:]


def remove_wire_between(text: str, a: tuple[float, float], b: tuple[float, float], required=True) -> str:
    pos = 0
    while True:
        start = text.find("(wire ", pos)
        if start < 0:
            if required:
                raise RuntimeError(f"Wire not found between {a} and {b}")
            return text
        block, end = extract_block(text, start)
        m = re.search(
            r"\(pts\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\)",
            block, re.S,
        )
        if m:
            p1 = (float(m.group(1)), float(m.group(2)))
            p2 = (float(m.group(3)), float(m.group(4)))
            if {p1, p2} == {a, b}:
                real_start = start
                while real_start > 0 and text[real_start - 1] == " ":
                    real_start -= 1
                if real_start > 0 and text[real_start - 1] == "\n":
                    real_start -= 1
                if end < len(text) and text[end] == "\n":
                    end += 1
                return text[:real_start] + text[end:]
        pos = end


def rename_hier_label(text: str, old: str, new: str, x: str, y: str) -> str:
    token = f'(hierarchical_label "{old}" (shape input) (at {x} {y} 0)'
    if token not in text:
        if f'(hierarchical_label "{new}" (shape input) (at {x} {y} 0)' in text:
            return text
        raise RuntimeError(f"Hierarchical label not found: {old} at {x},{y}")
    return text.replace(token, f'(hierarchical_label "{new}" (shape input) (at {x} {y} 0)', 1)


def shift_at_coordinates(block: str, dx: float, dy: float) -> str:
    pattern = re.compile(r"\(at\s+([-\d.]+)\s+([-\d.]+)(\s+[-\d.]+)?\)")
    def repl(m: re.Match) -> str:
        x = round(float(m.group(1)) + dx, 4)
        y = round(float(m.group(2)) + dy, 4)
        suffix = m.group(3) or ""
        return f"(at {x:g} {y:g}{suffix})"
    return pattern.sub(repl, block)


def clone_symbol(text: str, token: str, new_x: float, new_y: float, old_ref: str, new_ref: str,
                 force_bom: bool = False) -> str:
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
    if force_bom:
        block = block.replace("(in_bom no)", "(in_bom yes)", 1)
        block = block.replace("(dnp yes)", "(dnp no)", 1)
    return block


def next_ref(text: str, prefix: str, start_at: int) -> str:
    nums = [int(x) for x in re.findall(rf'property "Reference" "{re.escape(prefix)}(\d+)"', text)]
    return f"{prefix}{max([start_at - 1] + nums) + 1}"


def insert_before_final_close(text: str, blocks: list[str]) -> str:
    pos = text.rfind("\n)")
    if pos < 0:
        raise RuntimeError("Root closing parenthesis not found")
    return text[:pos] + "\n" + "\n".join(blocks) + "\n" + text[pos:]


def wire(a: tuple[str, str], b: tuple[str, str]) -> str:
    return (
        f'  (wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]}))\n'
        '    (stroke (width 0) (type default))\n'
        f'    (uuid {uid()})\n'
        '  )\n'
    )


def hier_out(name: str, x: str, y: str) -> str:
    return (
        f'  (hierarchical_label "{name}" (shape output) (at {x} {y} 0) (fields_autoplaced)\n'
        '    (effects (font (size 1.27 1.27)) (justify left))\n'
        f'    (uuid {uid()})\n'
        '  )\n'
    )


def patch_top(text: str) -> str:
    # Rename the two wires/pins we keep and remove the other comparator outputs.
    s, e, io_sheet = find_sheet(text, "ioconditioning.kicad_sch")
    io_sheet = rename_sheet_pin(io_sheet, "EOL_L_P", "HALL_L_ADC")
    io_sheet = rename_sheet_pin(io_sheet, "EOL_L_N", "HALL_R_ADC")
    io_sheet = remove_sheet_pin(io_sheet, "EOL_R_P")
    io_sheet = remove_sheet_pin(io_sheet, "EOL_R_N")
    text = text[:s] + io_sheet + text[e:]

    s, e, mcu_sheet = find_sheet(text, "mcu.kicad_sch")
    mcu_sheet = rename_sheet_pin(mcu_sheet, "EOL_L_P", "HALL_L_ADC")
    mcu_sheet = rename_sheet_pin(mcu_sheet, "EOL_L_N", "HALL_R_ADC")
    mcu_sheet = remove_sheet_pin(mcu_sheet, "EOL_R_P")
    mcu_sheet = remove_sheet_pin(mcu_sheet, "EOL_R_N")
    text = text[:s] + mcu_sheet + text[e:]

    text = remove_wire_between(text, (140.97, 139.7), (160.02, 139.7))
    text = remove_wire_between(text, (140.97, 142.24), (160.02, 142.24))
    return text


def patch_mcu(text: str) -> str:
    text = rename_hier_label(text, "EOL_L_P", "HALL_L_ADC", "198.12", "74.93")
    text = rename_hier_label(text, "EOL_L_N", "HALL_R_ADC", "198.12", "77.47")

    for name, y in (("EOL_R_P", "80.01"), ("EOL_R_N", "82.55")):
        if f'(hierarchical_label "{name}"' in text:
            text = remove_block(text, f'(hierarchical_label "{name}"')
        text = remove_wire_between(text, (185.42, float(y)), (198.12, float(y)), required=False)

    return text


def patch_io(text: str) -> str:
    if '(hierarchical_label "HALL_L_ADC"' in text and '(hierarchical_label "HALL_R_ADC"' in text:
        return text

    # Remove all four old comparator-facing hierarchical outputs and their tails.
    old_outputs = [
        ("EOL_L_P", (34.29, 93.98), (48.26, 93.98)),
        ("EOL_L_N", (34.29, 96.52), (50.8, 96.52)),
        ("EOL_R_P", (34.29, 99.06), (53.34, 99.06)),
        ("EOL_R_N", (34.29, 101.6), (55.88, 101.6)),
    ]
    for name, a, b in old_outputs:
        if f'(hierarchical_label "{name}"' in text:
            text = remove_block(text, f'(hierarchical_label "{name}"')
        text = remove_wire_between(text, a, b, required=False)

    # Clone the already-qualified 10k 0603 part used in this sheet.
    r_source = '(symbol (lib_id "ayab-lib:R_Small_US") (at 114.3 109.22 0)'
    g_source = '(symbol (lib_id "power:GND") (at 157.48 81.28 0)'
    r0 = next_ref(text, "R", 713)
    refs = [f"R{int(r0[1:]) + i}" for i in range(4)]
    p0 = next_ref(text, "#PWR", 720)
    prefs = [f"#PWR{int(p0[4:]) + i}" for i in range(2)]

    parts = [
        clone_symbol(text, r_source, 279.4, 45.72, "R705", refs[0], force_bom=True),
        clone_symbol(text, r_source, 279.4, 50.8, "R705", refs[1], force_bom=True),
        clone_symbol(text, r_source, 279.4, 119.38, "R705", refs[2], force_bom=True),
        clone_symbol(text, r_source, 279.4, 124.46, "R705", refs[3], force_bom=True),
        clone_symbol(text, g_source, 279.4, 55.88, "#PWR0705", prefs[0]),
        clone_symbol(text, g_source, 279.4, 129.54, "#PWR0705", prefs[1]),
    ]

    # New divider wiring. Existing raw Hall nets remain connected to LM393 inputs.
    new_wires = "".join([
        wire(("266.7", "40.64"), ("279.4", "40.64")),
        wire(("279.4", "40.64"), ("279.4", "43.18")),
        wire(("279.4", "48.26"), ("289.56", "48.26")),
        wire(("279.4", "53.34"), ("279.4", "55.88")),
        wire(("266.7", "114.3"), ("279.4", "114.3")),
        wire(("279.4", "114.3"), ("279.4", "116.84")),
        wire(("279.4", "121.92"), ("289.56", "121.92")),
        wire(("279.4", "127"), ("279.4", "129.54")),
    ])
    labels = hier_out("HALL_L_ADC", "289.56", "48.26") + hier_out("HALL_R_ADC", "289.56", "121.92")

    # Insert wires/labels before ordinary labels, then component instances near EOF.
    anchor = "  (label "
    pos = text.find(anchor)
    if pos < 0:
        raise RuntimeError("I/O conditioning label anchor not found")
    text = text[:pos] + new_wires + labels + text[pos:]
    text = insert_before_final_close(text, parts)

    # Hard postconditions.
    for name in ("HALL_L_ADC", "HALL_R_ADC"):
        if f'(hierarchical_label "{name}"' not in text:
            raise RuntimeError(f"Missing new Hall output: {name}")
    for name in ("EOL_L_P", "EOL_L_N", "EOL_R_P", "EOL_R_N"):
        if f'(hierarchical_label "{name}"' in text:
            raise RuntimeError(f"Old comparator output still exported: {name}")
    for ref in refs:
        # Confirm new divider parts are populated 10k components.
        if f'"{ref}"' not in text:
            raise RuntimeError(f"Divider resistor missing: {ref}")
    return text


def main() -> None:
    top = TOP.read_text(encoding="utf-8")
    mcu = MCU.read_text(encoding="utf-8")
    io = IO.read_text(encoding="utf-8")

    already = (
        '(pin "HALL_L_ADC" output' in top
        and '(pin "HALL_R_ADC" output' in top
        and '(pin "HALL_L_ADC" input' in top
        and '(pin "HALL_R_ADC" input' in top
        and '(hierarchical_label "HALL_L_ADC"' in mcu
        and '(hierarchical_label "HALL_R_ADC"' in mcu
        and '(hierarchical_label "HALL_L_ADC"' in io
        and '(hierarchical_label "HALL_R_ADC"' in io
    )
    if already:
        print("Rev A passive Hall ADC stage already applied")
        return

    top = patch_top(top)
    mcu = patch_mcu(mcu)
    io = patch_io(io)

    # Cross-file interface checks before writing.
    for name in ("HALL_L_ADC", "HALL_R_ADC"):
        if f'(pin "{name}" output' not in top:
            raise RuntimeError(f"I/O sheet parent output missing: {name}")
        if f'(pin "{name}" input' not in top:
            raise RuntimeError(f"MCU sheet parent input missing: {name}")
        if f'(hierarchical_label "{name}"' not in mcu:
            raise RuntimeError(f"MCU label missing: {name}")
        if f'(hierarchical_label "{name}"' not in io:
            raise RuntimeError(f"I/O conditioning label missing: {name}")

    for old in ("EOL_R_P", "EOL_R_N"):
        if f'(pin "{old}"' in top or f'(hierarchical_label "{old}"' in mcu:
            raise RuntimeError(f"Old GPIO3/4 comparator interface remains: {old}")

    TOP.write_text(top, encoding="utf-8")
    MCU.write_text(mcu, encoding="utf-8")
    IO.write_text(io, encoding="utf-8")
    print("Applied passive 10k/10k Hall ADC stage and freed GPIO3/4")


if __name__ == "__main__":
    main()
