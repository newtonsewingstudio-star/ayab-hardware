#!/usr/bin/env python3
"""Apply the bounded native-source corrections from the 647998e audit.

This intentionally edits only known references, UUID paths, net aliases and
serialized copper objects.  It refuses partial or unexpected source states.
KiCad 9 DRC/ERC and native schematic parity are the postconditions.
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "ayab-esp32.kicad_pcb"
MCU = ROOT / "mcu.kicad_sch"
PSU = ROOT / "psu.kicad_sch"
AUX = ROOT / "aux-connectors.kicad_sch"

PROJECT_UUID = "ad16b75f-afc8-4717-a7c6-8dd7b69a18e2"
MCU_SHEET_UUID = "a7e0db0f-e473-44d4-a2fe-681f732aacb2"
AUX_SHEET_UUID = "b41a48c7-b009-4c26-92ce-a01689c1d02b"


def read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def write(path: Path, text: str) -> None:
    path.write_bytes(text.encode("utf-8"))


def block_at(text: str, start: int) -> tuple[str, int]:
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
    raise RuntimeError(f"unbalanced expression at {start}")


def expressions(text: str, token: str):
    pos = 0
    while True:
        start = text.find(token, pos)
        if start < 0:
            return
        block, end = block_at(text, start)
        yield start, end, block
        pos = end


def replace_expression(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one exact expression, found {count}: {old[:80]!r}")
    return text.replace(old, new, 1)


def footprint_block(text: str, ref: str) -> tuple[int, int, str]:
    for start, end, block in expressions(text, '(footprint "'):
        if re.search(rf'\(property "Reference" "{re.escape(ref)}"', block):
            return start, end, block
    raise RuntimeError(f"missing PCB footprint {ref}")


def symbol_block(text: str, ref: str) -> tuple[int, int, str]:
    for start, end, block in expressions(text, "(symbol "):
        if re.search(rf'\(property "Reference" "{re.escape(ref)}"', block):
            return start, end, block
    raise RuntimeError(f"missing schematic symbol {ref}")


def set_property(block: str, name: str, value: str) -> str:
    out, count = re.subn(
        rf'(\(property "{re.escape(name)}" ")[^"]*(")',
        lambda match: match.group(1) + value + match.group(2),
        block,
        count=1,
    )
    if count != 1:
        raise RuntimeError(f"missing property {name}")
    return out


def edit_footprint(text: str, ref: str, edit) -> str:
    start, end, block = footprint_block(text, ref)
    new = edit(block)
    if new == block:
        raise RuntimeError(f"edit made no change to {ref}")
    return text[:start] + new + text[end:]


def fix_instance_paths(text: str) -> str:
    for symbol_uuid in (
        "aaa14c5f-6969-439e-bdef-bb5fc66f917d",  # D205
        "175ec455-5c18-4495-952f-cdd672f0311a",  # D206
        "86d7191f-1078-449e-8193-ca35bc117e8d",  # C206
    ):
        old = f'/{PROJECT_UUID}/{symbol_uuid}'
        new = f'/{PROJECT_UUID}/{MCU_SHEET_UUID}'
        if text.count(old) != 1:
            raise RuntimeError(f"unexpected instance path count for {symbol_uuid}")
        text = text.replace(old, new, 1)
    return text


def repair_pcb(text: str, r209_uuid: str, r210_uuid: str) -> str:
    metadata = {
        "R820": {"LCSC ID": "C25803", "OEM PN": "0603WAF1003T5E"},
        "R821": {"LCSC ID": "C25804", "OEM PN": "0603WAF1002T5E"},
        "R822": {"LCSC ID": "C25803", "OEM PN": "0603WAF1003T5E"},
        "R735": {"LCSC ID": "C25804", "OEM PN": "0603WAF1002T5E"},
        "R736": {"LCSC ID": "C25804", "OEM PN": "0603WAF1002T5E"},
        "R737": {"LCSC ID": "C25804", "OEM PN": "0603WAF1002T5E"},
        "R738": {"LCSC ID": "C25804", "OEM PN": "0603WAF1002T5E"},
        "D204": {"LCSC ID": "C22452"},
        "TP401": {"Value": "5V"},
        "TP402": {"Value": "12V"},
        "TP701": {"Value": "HALL-L-RAW"},
        "TP702": {"Value": "HALL-R-RAW"},
        "U403": {"Package": "SC-70-6"},
    }
    for ref, fields in metadata.items():
        def update(block: str, fields=fields) -> str:
            for name, value in fields.items():
                block = set_property(block, name, value)
            return block
        text = edit_footprint(text, ref, update)

    dnp_refs = {"R501", *(f"R70{i}" for i in range(1, 8)), "R709", "R711", "R713"}
    for ref in sorted(dnp_refs):
        def mark_dnp(block: str) -> str:
            out, count = re.subn(
                r'\(attr ([^\r\n)]*exclude_from_bom[^\r\n)]*)\)',
                lambda match: "(attr " + match.group(1) + " dnp)",
                block,
                count=1,
            )
            if count != 1 or out.count(" dnp)") != 1:
                raise RuntimeError(f"could not mark {ref} DNP")
            return out
        text = edit_footprint(text, ref, mark_dnp)

    for ref, symbol_uuid in (("R209", r209_uuid), ("R210", r210_uuid)):
        def add_path(block: str, symbol_uuid=symbol_uuid) -> str:
            out = block.replace('(sheetname "ESP32")', '(sheetname "AUX-CONNECTORS")', 1)
            out = out.replace('(sheetfile "mcu.kicad_sch")', '(sheetfile "aux-connectors.kicad_sch")', 1)
            out, count = re.subn(
                r'(\r?\n\s*)(\(attr )',
                rf'\1(path "/{AUX_SHEET_UUID}/{symbol_uuid}")\1\2',
                out,
                count=1,
            )
            if count != 1:
                raise RuntimeError(f"could not add path on {ref}")
            return out
        text = edit_footprint(text, ref, add_path)

    def disconnect_gpio3(block: str) -> str:
        match = re.search(r'\(pad "7" ', block)
        if not match:
            raise RuntimeError("U201 pad 7 missing")
        pad, pad_end = block_at(block, match.start())
        new_pad, count = re.subn(
            r'\r?\n\s*\(net 29 "/ESP32/EOL_R_P"\)', "", pad, count=1
        )
        if count != 1:
            raise RuntimeError("U201.7 did not have the expected stale net")
        return block[: match.start()] + new_pad + block[pad_end:]
    text = edit_footprint(text, "U201", disconnect_gpio3)

    retained = {
        ((209.32, 128.97), (216.98, 128.97)),  # removed below, listed for readability
    }
    keep_segments = {
        ((197.2025, 159.155), (197.4025, 158.955)),
        ((197.4025, 158.955), (213.769898, 158.955)),
        ((213.769898, 158.955), (215.127498, 157.5974)),
    }
    edits: list[tuple[int, int, str]] = []
    removed = 0
    for token in ("(segment", "(via"):
        for start, end, block in expressions(text, token):
            if not re.search(r'\(net 29\)', block):
                continue
            coords = re.findall(r'\((?:start|end|at) ([0-9.]+) ([0-9.]+)', block)
            pair = tuple((float(x), float(y)) for x, y in coords[:2])
            if token == "(segment" and pair in keep_segments:
                continue
            edits.append((start, end, ""))
            removed += 1
    if removed != 14:
        raise RuntimeError(f"expected to remove 14 stale GPIO3 branch objects, got {removed}")
    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]

    aliases = {
        "/ESP32/EOL_L_P": "Net-(J701-Pin_4)",
        "/ESP32/EOL_L_N": "Net-(J701-Pin_5)",
        "/ESP32/EOL_R_P": "Net-(J701-Pin_6)",
        "/ESP32/EOL_R_N": "Net-(J701-Pin_7)",
    }
    for old, new in aliases.items():
        if old not in text:
            raise RuntimeError(f"missing retained legacy alias {old}")
        text = text.replace(f'"{old}"', f'"{new}"')

    def freshen_d205(block: str) -> str:
        return re.sub(
            r'\(uuid "[0-9a-f-]{36}"\)',
            lambda _match: f'(uuid "{uuid.uuid4()}")',
            block,
        )
    text = edit_footprint(text, "D205", freshen_d205)
    return text


def shift_ats(block: str, dx: float, dy: float) -> str:
    def shift(match: re.Match[str]) -> str:
        x = float(match.group(1)) + dx
        y = float(match.group(2)) + dy
        suffix = match.group(3) or ""
        return f"(at {x:g} {y:g}{suffix})"
    return re.sub(r'\(at (-?[0-9.]+) (-?[0-9.]+)( [^)]*)?\)', shift, block)


def make_aux_pullup(template: str, ref: str, x: float, y: float) -> tuple[str, str]:
    original_uuid = re.search(r'\(uuid ([0-9a-f-]{36})\)', template)
    if not original_uuid:
        raise RuntimeError("template symbol UUID missing")
    symbol_uuid = str(uuid.uuid4())
    block = shift_ats(template, x - 193.04, y - 59.69)
    block = set_property(block, "Reference", ref)
    block = block.replace('(property "Value" "5k1"', '(property "Value" "5k1"', 1)
    block = re.sub(r'\(uuid [0-9a-f-]{36}\)', lambda _m: f'(uuid {uuid.uuid4()})', block)
    # The first UUID is the symbol identity used by the PCB association.
    block = re.sub(r'(\(symbol .*?\(uuid )[0-9a-f-]{36}(\))', rf'\g<1>{symbol_uuid}\2', block, count=1, flags=re.S)
    block = re.sub(r'\(reference "R812"\)', f'(reference "{ref}")', block)
    return block, symbol_uuid


def add_aux_pullups(text: str) -> tuple[str, str, str]:
    _, _, template = symbol_block(text, "R812")
    r209, u209 = make_aux_pullup(template, "R209", 147.32, 88.9)
    r210, u210 = make_aux_pullup(template, "R210", 160.02, 88.9)

    def power(ref: str, x: float) -> str:
        symbol_uuid = uuid.uuid4()
        pin_uuid = uuid.uuid4()
        return f'''  (symbol (lib_id "power:+3V3") (at {x:g} 86.36 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid {symbol_uuid})
    (property "Reference" "{ref}" (at {x:g} 90.17 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "+3V3" (at {x:g} 82.55 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at {x:g} 86.36 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {x:g} 86.36 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {pin_uuid}))
    (instances
      (project "ayab-esp32"
        (path "/{PROJECT_UUID}/{AUX_SHEET_UUID}"
          (reference "{ref}") (unit 1)
        )
      )
    )
  )'''

    labels = f'''  (label "AYAB_SCL" (at 147.32 91.44 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuid.uuid4()})
  )
  (label "AYAB_SDA" (at 160.02 91.44 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuid.uuid4()})
  )'''
    insertion = "\n\n".join((labels, power("#PWR0820", 147.32), power("#PWR0821", 160.02), r209, r210))
    final = text.rfind("\n)")
    if final < 0:
        raise RuntimeError("aux final delimiter missing")
    text = text[:final] + "\n" + insertion + text[final:]
    return text, u209, u210


def remove_wire(text: str, a: tuple[float, float], b: tuple[float, float]) -> str:
    target_sets = {a, b}
    matches = []
    for start, end, block in expressions(text, "(wire "):
        points = {(float(x), float(y)) for x, y in re.findall(r'\(xy ([0-9.]+) ([0-9.]+)\)', block)}
        if points == target_sets:
            matches.append((start, end, block))
    if len(matches) != 1:
        raise RuntimeError(f"expected one wire {a}->{b}, got {len(matches)}")
    start, end, _ = matches[0]
    return text[:start] + text[end:]


def repair_psu(text: str) -> str:
    text = remove_wire(text, (26.67, 119.38), (38.1, 119.38))
    text = remove_wire(text, (58.42, 119.38), (68.58, 119.38))
    labels = f'''  (global_label "SOLENOID_12V_SW" (shape input) (at 48.26 119.38 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left))
    (uuid {uuid.uuid4()})
  )
  (global_label "+12V" (shape input) (at 68.58 119.38 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left))
    (uuid {uuid.uuid4()})
  )'''
    final = text.rfind("\n)")
    if final < 0:
        raise RuntimeError("PSU final delimiter missing")
    text = text[:final] + "\n" + labels + text[final:]
    text = text.replace('lib_id "Device:D_Bridge_+-AA"', 'lib_id "ayab-lib:KMB14F_Bridge"', 1)
    text = text.replace('(symbol "Device:D_Bridge_+-AA"', '(symbol "ayab-lib:KMB14F_Bridge"', 1)
    text = text.replace('(symbol "D_Bridge_+-AA_', '(symbol "KMB14F_Bridge_', 3)
    return text


def main() -> None:
    mcu = fix_instance_paths(read(MCU))
    aux, r209_uuid, r210_uuid = add_aux_pullups(read(AUX))
    psu = repair_psu(read(PSU))
    pcb = repair_pcb(read(PCB), r209_uuid, r210_uuid)

    write(MCU, mcu)
    write(AUX, aux)
    write(PSU, psu)
    write(PCB, pcb)
    print("AUDIT_REPAIR_CORE_OK")
    print("R209_UUID", r209_uuid)
    print("R210_UUID", r210_uuid)


if __name__ == "__main__":
    main()
