#!/usr/bin/env python3
"""Replace PSU R406 0-ohm link with LM66100 reverse-current isolation.

Existing topology around the insertion point:
  filtered U401 5V -> C15850 10uF node -> R406 0R -> PSU hierarchical 5V

Rev A topology:
  filtered U401 5V -> MACHINE_5V_RAW -> LM66100 -> existing system 5V

LM66100 DCK pinout:
  1 VIN   -> MACHINE_5V_RAW
  2 GND   -> GND
  3 CE    -> VOUT (always-on reverse-current-blocking configuration)
  4 N/C   -> no connect
  5 ST    -> GND (status unused)
  6 VOUT  -> existing system 5V
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PSU = ROOT / "psu.kicad_sch"


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
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return text[start:i + 1], i + 1
    raise RuntimeError('Unbalanced KiCad block')


def remove_block(text: str, token: str) -> tuple[str, str]:
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f'Block not found: {token}')
    block, end = extract_block(text, start)
    real_start = start
    while real_start > 0 and text[real_start - 1] == ' ':
        real_start -= 1
    if real_start > 0 and text[real_start - 1] == '\n':
        real_start -= 1
    if end < len(text) and text[end] == '\n':
        end += 1
    return text[:real_start] + text[end:], block


def remove_wire(text: str, a: tuple[float, float], b: tuple[float, float]) -> str:
    pos = 0
    while True:
        start = text.find('(wire ', pos)
        if start < 0:
            raise RuntimeError(f'Wire not found: {a} <-> {b}')
        block, end = extract_block(text, start)
        m = re.search(
            r'\(pts\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\)',
            block, re.S,
        )
        if m:
            p1 = (float(m.group(1)), float(m.group(2)))
            p2 = (float(m.group(3)), float(m.group(4)))
            if {p1, p2} == {a, b}:
                real_start = start
                while real_start > 0 and text[real_start - 1] == ' ':
                    real_start -= 1
                if real_start > 0 and text[real_start - 1] == '\n':
                    real_start -= 1
                if end < len(text) and text[end] == '\n':
                    end += 1
                return text[:real_start] + text[end:]
        pos = end


def wire(a: tuple[str, str], b: tuple[str, str]) -> str:
    return (
        f'  (wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]}))\n'
        '    (stroke (width 0) (type default))\n'
        f'    (uuid {uid()})\n'
        '  )\n'
    )


def lm66100_lib_symbol() -> str:
    return '''    (symbol "ayab-lib:LM66100" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 8.89 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "LM66100DCKR" (at 0 6.35 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" "Package_TO_SOT_SMD:SOT-363_SC-70-6" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" "https://www.ti.com/lit/ds/symlink/lm66100.pdf" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_description" "5.5-V, 1.5-A, 79-mOhm ideal diode with reverse-current blocking" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "LM66100_0_1"
        (rectangle (start -5.08 5.08) (end 5.08 -5.08)
          (stroke (width 0.254) (type default))
          (fill (type background))
        )
      )
      (symbol "LM66100_1_1"
        (pin power_in line (at -7.62 0 0) (length 2.54)
          (name "VIN" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin power_in line (at 2.54 -7.62 90) (length 2.54)
          (name "GND" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
        (pin input line (at 7.62 2.54 180) (length 2.54)
          (name "CE" (effects (font (size 1.27 1.27))))
          (number "3" (effects (font (size 1.27 1.27))))
        )
        (pin no_connect line (at 0 7.62 270) (length 2.54)
          (name "N/C" (effects (font (size 1.27 1.27))))
          (number "4" (effects (font (size 1.27 1.27))))
        )
        (pin open_collector line (at -2.54 -7.62 90) (length 2.54)
          (name "ST" (effects (font (size 1.27 1.27))))
          (number "5" (effects (font (size 1.27 1.27))))
        )
        (pin power_out line (at 7.62 0 180) (length 2.54)
          (name "VOUT" (effects (font (size 1.27 1.27))))
          (number "6" (effects (font (size 1.27 1.27))))
        )
      )
    )
'''


def add_lib_symbol(text: str) -> str:
    if '(symbol "ayab-lib:LM66100"' in text:
        return text
    anchor = '    (symbol "power:GND"'
    p = text.find(anchor)
    if p < 0:
        raise RuntimeError('lib_symbols insertion anchor not found')
    return text[:p] + lm66100_lib_symbol() + text[p:]


def next_u_ref(text: str) -> str:
    nums = [int(x) for x in re.findall(r'property "Reference" "U(\d+)"', text)]
    return f'U{max([402] + nums) + 1}'


def clone_gnd(text: str, x: float, y: float, new_ref: str) -> str:
    token = '(symbol (lib_id "power:GND")'
    start = text.find(token)
    while start >= 0:
        block, _ = extract_block(text, start)
        mpos = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', block)
        mref = re.search(r'property "Reference" "([^"]+)"', block)
        if mpos and mref:
            ox, oy = float(mpos.group(1)), float(mpos.group(2))
            old_ref = mref.group(1)
            pat = re.compile(r'\(at\s+([-\d.]+)\s+([-\d.]+)(\s+[-\d.]+)?\)')
            def repl(m: re.Match) -> str:
                xx = round(float(m.group(1)) + x - ox, 4)
                yy = round(float(m.group(2)) + y - oy, 4)
                return f"(at {xx:g} {yy:g}{m.group(3) or ''})"
            block = pat.sub(repl, block)
            block = block.replace(f'"{old_ref}"', f'"{new_ref}"')
            block = re.sub(r'\(uuid [0-9a-f-]+\)', lambda _: f'(uuid {uid()})', block)
            return block
        start = text.find(token, start + 1)
    raise RuntimeError('Concrete GND instance not found')


def lm66100_instance(instances_source: str, ref: str) -> str:
    istart = instances_source.find('(instances')
    if istart < 0:
        raise RuntimeError('R406 instances block missing')
    instances, _ = extract_block(instances_source, istart)
    instances = re.sub(r'\(reference "[^"]+"\)', f'(reference "{ref}")', instances)
    instances = re.sub(r'\(uuid [0-9a-f-]+\)', lambda _: f'(uuid {uid()})', instances)
    return f'''  (symbol (lib_id "ayab-lib:LM66100") (at 264.16 54.61 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced)
    (uuid {uid()})
    (property "Reference" "{ref}" (at 264.16 43.18 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "LM66100DCKR" (at 264.16 45.72 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "Package_TO_SOT_SMD:SOT-363_SC-70-6" (at 264.16 54.61 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "https://www.ti.com/lit/ds/symlink/lm66100.pdf" (at 264.16 54.61 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Package" "SC-70-6" (at 264.16 54.61 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "LCSC ID" "C2869734" (at 264.16 54.61 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "OEM PN" "LM66100DCKR" (at 264.16 54.61 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "OEM" "Texas Instruments" (at 264.16 54.61 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {uid()}))
    (pin "2" (uuid {uid()}))
    (pin "3" (uuid {uid()}))
    (pin "4" (uuid {uid()}))
    (pin "5" (uuid {uid()}))
    (pin "6" (uuid {uid()}))
    {instances}
  )'''


def insert_before_root_close(text: str, blocks: list[str]) -> str:
    p = text.rfind('\n)')
    if p < 0:
        raise RuntimeError('Root close not found')
    return text[:p] + '\n' + '\n'.join(blocks) + '\n' + text[p:]


def main() -> None:
    text = PSU.read_text()
    if 'LM66100DCKR' in text and 'MACHINE_5V_RAW' in text:
        print('5V isolation already present')
        return

    text = add_lib_symbol(text)

    # R406 is the existing 0R break point between filtered machine 5V and the
    # hierarchical/system 5V output.
    text, r406 = remove_block(text, '(symbol (lib_id "ayab-lib:R_Small_US") (at 264.16 54.61 90)')
    text = remove_wire(text, (257.81, 54.61), (261.62, 54.61))
    text = remove_wire(text, (266.7, 54.61), (270.51, 54.61))

    ref = next_u_ref(text)
    gref_nums = [int(x) for x in re.findall(r'property "Reference" "#PWR(\d+)"', text)]
    gref = f'#PWR{max([719] + gref_nums) + 1}'
    gnd = clone_gnd(text, 264.16, 64.77, gref)
    device = lm66100_instance(r406, ref)

    payload = ''.join([
        wire(('257.81', '54.61'), ('256.54', '54.61')),          # VIN
        wire(('271.78', '54.61'), ('270.51', '54.61')),          # VOUT -> system 5V
        wire(('271.78', '52.07'), ('271.78', '54.61')),          # CE -> VOUT
        wire(('261.62', '62.23'), ('264.16', '62.23')),          # ST -> common GND node
        wire(('266.7', '62.23'), ('264.16', '62.23')),           # GND pin -> common GND node
        wire(('264.16', '62.23'), ('264.16', '64.77')),          # common -> GND symbol
        (
            '  (junction (at 271.78 54.61) (diameter 0) (color 0 0 0 0)\n'
            f'    (uuid {uid()})\n'
            '  )\n'
        ),
        (
            '  (junction (at 264.16 62.23) (diameter 0) (color 0 0 0 0)\n'
            f'    (uuid {uid()})\n'
            '  )\n'
        ),
        (
            '  (label "MACHINE_5V_RAW" (at 257.81 54.61 0) (fields_autoplaced)\n'
            '    (effects (font (size 1.27 1.27)) (justify left bottom))\n'
            f'    (uuid {uid()})\n'
            '  )\n'
        ),
    ])
    p = text.find('  (wire ')
    if p < 0:
        raise RuntimeError('Wire insertion anchor not found')
    text = text[:p] + payload + text[p:]
    text = insert_before_root_close(text, [device, gnd])

    # Hard postconditions.
    for required in (
        'LM66100DCKR', 'C2869734', 'Package_TO_SOT_SMD:SOT-363_SC-70-6',
        'MACHINE_5V_RAW', '(name "VIN"', '(name "VOUT"', '(name "CE"',
    ):
        if required not in text:
            raise RuntimeError(f'Missing 5V-isolation postcondition: {required}')
    if '(property "Reference" "R406"' in text:
        raise RuntimeError('R406 conductive link still present')

    PSU.write_text(text)
    print(f'Replaced R406 with {ref} LM66100 reverse-current isolation')


if __name__ == '__main__':
    main()
