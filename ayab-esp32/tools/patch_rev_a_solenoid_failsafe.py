#!/usr/bin/env python3
"""Add Rev A hardware-default-OFF solenoid power gate.

Topology:
  RAW +12V -> LP9435LT1G P-MOS -> SOLENOID_12V_SW
  P-MOS gate pulled to source by 100k (OFF default)
  AO3400A pulls P-MOS gate low when SOLENOID_PWR_EN is high
  AO3400A gate has 10k series + 100k pulldown

SOLENOID_12V_SW feeds both Brother solenoid connector common power and
ULN2003A COM/flyback rails. GPIO21 drives SOLENOID_PWR_EN.
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCU = ROOT / "mcu.kicad_sch"
SOL = ROOT / "solenoids.kicad_sch"
CONN = ROOT / "brother-connectors.kicad_sch"


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
    raise RuntimeError("Unbalanced KiCad block")


def remove_block(text: str, token: str) -> tuple[str, str]:
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f"Block not found: {token}")
    block, end = extract_block(text, start)
    real_start = start
    while real_start > 0 and text[real_start - 1] == ' ':
        real_start -= 1
    if real_start > 0 and text[real_start - 1] == '\n':
        real_start -= 1
    if end < len(text) and text[end] == '\n':
        end += 1
    return text[:real_start] + text[end:], block


def get_block(text: str, token: str) -> str:
    start = text.find(token)
    if start < 0:
        raise RuntimeError(f"Block not found: {token}")
    block, _ = extract_block(text, start)
    return block


def insert_before_root_close(text: str, blocks: list[str]) -> str:
    p = text.rfind('\n)')
    if p < 0:
        raise RuntimeError("Root close not found")
    return text[:p] + '\n' + '\n'.join(blocks) + '\n' + text[p:]


def add_lib_symbols(text: str, blocks: list[str]) -> str:
    marker = '(lib_symbols\n'
    p = text.find(marker)
    if p < 0:
        raise RuntimeError("lib_symbols anchor not found")
    p += len(marker)
    payload = ''.join('    ' + b + '\n' for b in blocks)
    return text[:p] + payload + text[p:]


def next_ref(prefix: str) -> str:
    nums: list[int] = []
    rx = re.compile(rf'(?:property "Reference"|reference) "{re.escape(prefix)}(\d+)"')
    for path in ROOT.glob('*.kicad_sch'):
        t = path.read_text()
        nums.extend(int(x) for x in rx.findall(t))
    return f"{prefix}{max(nums, default=0) + 1}"


def next_power_ref(text: str) -> str:
    nums = [int(x) for x in re.findall(r'#PWR(\d+)', text)]
    return f"#PWR{max(nums, default=0) + 1:04d}"


def template_instances(text: str) -> str:
    token = '(symbol (lib_id "ayab-lib:ULN2003A")'
    start = text.find(token)
    if start < 0:
        raise RuntimeError("ULN2003A instance template missing")
    block, _ = extract_block(text, start)
    p = block.find('(instances')
    if p < 0:
        raise RuntimeError("ULN2003A instances block missing")
    inst, _ = extract_block(block, p)
    return inst


def instances_for(template: str, ref: str) -> str:
    return re.sub(r'\(reference "[^"]+"\)', f'(reference "{ref}")', template)


def relocate_power(block: str, x: float, y: float, new_ref: str) -> str:
    m = re.search(r'\(symbol \(lib_id "power:[^"]+"\) \(at\s+([-\d.]+)\s+([-\d.]+)', block)
    if not m:
        raise RuntimeError("Power-symbol coordinate not found")
    ox, oy = float(m.group(1)), float(m.group(2))
    dx, dy = x - ox, y - oy

    def move_at(match: re.Match) -> str:
        xx = float(match.group(1)) + dx
        yy = float(match.group(2)) + dy
        rot = match.group(3) or ''
        return f'(at {xx:g} {yy:g}{rot})'

    out = re.sub(r'\(at\s+([-\d.]+)\s+([-\d.]+)(\s+[-\d.]+)?\)', move_at, block)
    old_ref = re.search(r'property "Reference" "([^"]+)"', out)
    if not old_ref:
        raise RuntimeError("Power reference missing")
    out = out.replace(f'"{old_ref.group(1)}"', f'"{new_ref}"')
    out = re.sub(r'\(uuid [0-9a-f-]+\)', lambda _: f'(uuid {uid()})', out)
    return out


def wire(x1: float, y1: float, x2: float, y2: float) -> str:
    return (
        f'  (wire (pts (xy {x1:g} {y1:g}) (xy {x2:g} {y2:g}))\n'
        '    (stroke (width 0) (type default))\n'
        f'    (uuid {uid()})\n'
        '  )'
    )


def junction(x: float, y: float) -> str:
    return (
        f'  (junction (at {x:g} {y:g}) (diameter 0) (color 0 0 0 0)\n'
        f'    (uuid {uid()})\n'
        '  )'
    )


def local_label(name: str, x: float, y: float) -> str:
    return (
        f'  (label "{name}" (at {x:g} {y:g} 0) (fields_autoplaced)\n'
        '    (effects (font (size 1.27 1.27)) (justify left bottom))\n'
        f'    (uuid {uid()})\n'
        '  )'
    )


def global_label(name: str, shape: str, x: float, y: float, angle: int = 0) -> str:
    justify = 'left' if angle == 0 else 'left'
    return (
        f'  (global_label "{name}" (shape {shape}) (at {x:g} {y:g} {angle}) (fields_autoplaced)\n'
        f'    (effects (font (size 1.27 1.27)) (justify {justify}))\n'
        f'    (uuid {uid()})\n'
        '  )'
    )


def failsafe_resistor_lib() -> str:
    return '''(symbol "ayab-lib:FAILSAFE_R" (pin_numbers hide) (pin_names (offset 0.254) hide) (in_bom yes) (on_board yes)
      (property "Reference" "R" (at 0 1.905 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "R" (at 0 -1.905 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" "~" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "FAILSAFE_R_0_1"
        (rectangle (start -1.27 0.635) (end 1.27 -0.635)
          (stroke (width 0.254) (type default))
          (fill (type none))
        )
      )
      (symbol "FAILSAFE_R_1_1"
        (pin passive line (at -3.81 0 0) (length 2.54)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 3.81 0 180) (length 2.54)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
      )
    )'''


def pmos_lib() -> str:
    return '''(symbol "ayab-lib:LP9435LT1G" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
      (property "Reference" "Q" (at 0 6.985 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "LP9435LT1G" (at 0 4.445 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" "Package_TO_SOT_SMD:SOT-23" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" "https://static.chipdip.ru/lib/569/DOC042569635.pdf" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_description" "30V 5.3A P-channel MOSFET, SOT-23; pin 1 Gate, 2 Source, 3 Drain" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "LP9435LT1G_0_1"
        (rectangle (start -5.08 3.81) (end 5.08 -3.81)
          (stroke (width 0.254) (type default))
          (fill (type background))
        )
      )
      (symbol "LP9435LT1G_1_1"
        (pin input line (at 0 7.62 270) (length 3.81)
          (name "G" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin power_in line (at -7.62 0 0) (length 2.54)
          (name "S" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
        (pin power_out line (at 7.62 0 180) (length 2.54)
          (name "D" (effects (font (size 1.27 1.27))))
          (number "3" (effects (font (size 1.27 1.27))))
        )
      )
    )'''


def nmos_lib() -> str:
    return '''(symbol "ayab-lib:AO3400A_FAILSAFE" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
      (property "Reference" "Q" (at 0 6.985 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "AO3400A" (at 0 4.445 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" "Package_TO_SOT_SMD:SOT-23" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" "https://www.aosmd.com/res/data_sheets/AO3400A.pdf" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_description" "30V 5.7A N-channel MOSFET, SOT-23; gate pull-down for solenoid power switch" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "AO3400A_FAILSAFE_0_1"
        (rectangle (start -3.81 5.08) (end 3.81 -5.08)
          (stroke (width 0.254) (type default))
          (fill (type background))
        )
      )
      (symbol "AO3400A_FAILSAFE_1_1"
        (pin input line (at -7.62 0 0) (length 3.81)
          (name "G" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 0 7.62 270) (length 2.54)
          (name "S" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 0 -7.62 90) (length 2.54)
          (name "D" (effects (font (size 1.27 1.27))))
          (number "3" (effects (font (size 1.27 1.27))))
        )
      )
    )'''


def device_instance(lib: str, ref: str, value: str, x: float, y: float,
                    footprint: str, lcsc: str, oem_pn: str, oem: str,
                    pin_count: int, instances: str) -> str:
    pins = '\n'.join(f'    (pin "{i}" (uuid {uid()}))' for i in range(1, pin_count + 1))
    return f'''  (symbol (lib_id "{lib}") (at {x:g} {y:g} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced)
    (uuid {uid()})
    (property "Reference" "{ref}" (at {x:g} {y-8.89:g} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "{value}" (at {x:g} {y-6.35:g} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "{footprint}" (at {x:g} {y:g} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (at {x:g} {y:g} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Package" "{'0603' if '0603' in footprint else 'SOT-23'}" (at {x:g} {y:g} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "LCSC ID" "{lcsc}" (at {x:g} {y:g} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "OEM PN" "{oem_pn}" (at {x:g} {y:g} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "OEM" "{oem}" (at {x:g} {y:g} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
{pins}
    {instances_for(instances, ref)}
  )'''


def resistor_instance(ref: str, value: str, x: float, y: float,
                      lcsc: str, oem_pn: str, instances: str) -> str:
    return device_instance(
        'ayab-lib:FAILSAFE_R', ref, value, x, y,
        'Resistor_SMD:R_0603_1608Metric', lcsc, oem_pn,
        'UNI-ROYAL(Uniroyal Elec)', 2, instances,
    )


def patch_mcu(text: str) -> str:
    if 'SOLENOID_PWR_EN' in text:
        return text
    if '(wire (pts (xy 185.42 115.57) (xy 203.2 115.57))' not in text:
        raise RuntimeError('GPIO21 wire anchor missing')
    payload = '\n'.join([
        local_label('SOLENOID_PWR_EN', 195.58, 115.57),
        global_label('SOLENOID_PWR_EN', 'output', 203.2, 115.57),
    ])
    p = text.find('  (wire ')
    if p < 0:
        raise RuntimeError('MCU wire anchor missing')
    return text[:p] + payload + '\n' + text[p:]


def patch_connectors(text: str) -> str:
    coords = [(55.88, 34.29), (144.78, 34.29), (234.95, 36.83)]
    labels: list[str] = []
    for x, y in coords:
        token = f'(symbol (lib_id "power:+12V") (at {x:g} {y:g} 0)'
        text, _ = remove_block(text, token)
        labels.append(global_label('SOLENOID_12V_SW', 'input', x, y))
    p = text.find('  (wire ')
    if p < 0:
        raise RuntimeError('Connector wire anchor missing')
    return text[:p] + '\n'.join(labels) + '\n' + text[p:]


def patch_solenoids(text: str) -> str:
    if 'LP9435LT1G' in text or 'SOLENOID_12V_SW' in text:
        raise RuntimeError('Partial solenoid fail-safe markers already present')

    # Save the original raw +12 V power symbol as a relocation template, then
    # replace the existing ULN COM/clamp +12 V connection with the switched net.
    raw_token = '(symbol (lib_id "power:+12V") (at 227.33 25.4 0)'
    text, raw12_template = remove_block(text, raw_token)

    inst_template = template_instances(text)

    # Add compact, explicit symbols for the fail-safe stage.
    text = add_lib_symbols(text, [failsafe_resistor_lib(), pmos_lib(), nmos_lib()])

    q_p = next_ref('Q')
    q_n = f'Q{int(q_p[1:]) + 1}'
    r1 = next_ref('R')
    r2 = f'R{int(r1[1:]) + 1}'
    r3 = f'R{int(r1[1:]) + 2}'

    # Re-create RAW +12 V only at the new gate source; the old solenoid rail
    # becomes SOLENOID_12V_SW.
    raw_pwr_ref = next_power_ref(text)
    raw12 = relocate_power(raw12_template, 228.6, 165.1, raw_pwr_ref)

    gnd_template = get_block(text, '(symbol (lib_id "power:GND") (at 184.15 152.4 0)')
    gnd_ref = next_power_ref(text + raw12)
    gnd = relocate_power(gnd_template, 220.98, 200.66, gnd_ref)

    pmos = device_instance(
        'ayab-lib:LP9435LT1G', q_p, 'LP9435LT1G', 236.22, 167.64,
        'Package_TO_SOT_SMD:SOT-23', 'C383257', 'LP9435LT1G', 'LRC', 3,
        inst_template,
    )
    nmos = device_instance(
        'ayab-lib:AO3400A_FAILSAFE', q_n, 'AO3400A', 236.22, 190.5,
        'Package_TO_SOT_SMD:SOT-23', 'C20917', 'AO3400A',
        'Alpha & Omega Semicon', 3, inst_template,
    )
    pullup = resistor_instance(r1, '100k', 224.79, 175.26, 'C25803', '0603WAF1003T5E', inst_template)
    series = resistor_instance(r2, '10k', 217.17, 190.5, 'C25804', '0603WAF1002T5E', inst_template)
    pulldown = resistor_instance(r3, '100k', 224.79, 195.58, 'C25803', '0603WAF1003T5E', inst_template)

    geometry = [
        # Original ULN COM / flyback rail is now switched.
        global_label('SOLENOID_12V_SW', 'input', 227.33, 25.4),

        # High-side P-MOS source and drain.
        wire(228.6, 165.1, 228.6, 167.64),
        wire(228.6, 167.64, 220.98, 167.64),
        wire(220.98, 167.64, 220.98, 175.26),
        wire(220.98, 175.26, 220.98, 175.26),
        wire(228.6, 175.26, 236.22, 175.26),
        wire(243.84, 167.64, 248.92, 167.64),
        global_label('SOLENOID_12V_SW', 'output', 248.92, 167.64),
        local_label('SOLENOID_12V_SW', 243.84, 167.64),
        junction(228.6, 167.64),
        junction(236.22, 175.26),

        # N-MOS pulls P-MOS gate low only when GPIO21 is asserted.
        wire(236.22, 175.26, 236.22, 182.88),
        wire(210.82, 190.5, 213.36, 190.5),
        global_label('SOLENOID_PWR_EN', 'input', 210.82, 190.5),
        wire(220.98, 190.5, 228.6, 190.5),
        wire(228.6, 190.5, 228.6, 195.58),
        wire(220.98, 195.58, 220.98, 200.66),
        wire(236.22, 198.12, 236.22, 200.66),
        wire(236.22, 200.66, 220.98, 200.66),
        junction(228.6, 190.5),
        junction(220.98, 200.66),
    ]

    p = text.find('  (wire ')
    if p < 0:
        raise RuntimeError('Solenoid wire anchor missing')
    text = text[:p] + '\n'.join(geometry) + '\n' + text[p:]
    text = insert_before_root_close(text, [raw12, gnd, pmos, nmos, pullup, series, pulldown])
    return text


def main() -> None:
    mcu = MCU.read_text()
    sol = SOL.read_text()
    conn = CONN.read_text()

    complete = (
        'SOLENOID_PWR_EN' in mcu and
        'LP9435LT1G' in sol and
        sol.count('SOLENOID_12V_SW') >= 2 and
        conn.count('SOLENOID_12V_SW') >= 3
    )
    if complete:
        print('Solenoid fail-safe already present')
        return

    mcu = patch_mcu(mcu)
    conn = patch_connectors(conn)
    sol = patch_solenoids(sol)

    # Structural postconditions before KiCad gets a chance to validate.
    required_mcu = ['SOLENOID_PWR_EN', '185.42 115.57']
    required_sol = ['LP9435LT1G', 'C383257', 'AO3400A', 'C20917',
                    'C25803', 'C25804', 'SOLENOID_12V_SW', 'SOLENOID_PWR_EN']
    for marker in required_mcu:
        if marker not in mcu:
            raise RuntimeError(f'MCU postcondition missing: {marker}')
    for marker in required_sol:
        if marker not in sol:
            raise RuntimeError(f'Solenoid postcondition missing: {marker}')
    if conn.count('SOLENOID_12V_SW') < 3:
        raise RuntimeError('Not all Brother solenoid supply groups moved to switched rail')
    if '(symbol (lib_id "power:+12V") (at 227.33 25.4 0)' in sol:
        raise RuntimeError('ULN COM rail is still directly on raw +12V')
    for x, y in [(55.88, 34.29), (144.78, 34.29), (234.95, 36.83)]:
        if f'(symbol (lib_id "power:+12V") (at {x:g} {y:g} 0)' in conn:
            raise RuntimeError(f'Brother connector solenoid supply still raw +12V at {x},{y}')

    MCU.write_text(mcu)
    SOL.write_text(sol)
    CONN.write_text(conn)
    print('Added GPIO21 hardware-default-OFF solenoid power gate')


if __name__ == '__main__':
    main()
