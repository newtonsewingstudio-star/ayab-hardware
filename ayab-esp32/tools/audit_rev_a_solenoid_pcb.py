#!/usr/bin/env python3
"""Audit PCB parity for the KH910 Rev A solenoid fail-safe stage.

This deliberately does not alter the PCB. It extracts the project-level
references of the new schematic devices and compares them with the existing
board, then inventories nearby/useful footprint and net patterns for the
layout patch.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "ayab-esp32.kicad_pcb"
SOL = ROOT / "solenoids.kicad_sch"
OUT = ROOT / "KH910_REV_A_SOLENOID_PCB_AUDIT.md"


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


def top_blocks(text: str, token: str):
    p = 0
    while True:
        p = text.find(token, p)
        if p < 0:
            return
        block, end = extract_block(text, p)
        yield block
        p = end


def project_ref(symbol_block: str) -> str | None:
    # Prefer the fully annotated ayab-esp32 instance reference over the local
    # sheet reference/property.
    m = re.search(
        r'\(project "ayab-esp32".*?\(reference "([A-Z#]+\d+)"\)',
        symbol_block, re.S,
    )
    if m:
        return m.group(1)
    m = re.search(r'property "Reference" "([A-Z#]+\d+)"', symbol_block)
    return m.group(1) if m else None


def find_schematic_devices(text: str) -> list[dict]:
    out = []
    for block in top_blocks(text, '(symbol (lib_id '):
        if not any(x in block for x in ('LP9435LT1G', 'AO3400A_FAILSAFE', 'FAILSAFE_R')):
            continue
        ref = project_ref(block)
        value = re.search(r'property "Value" "([^"]+)"', block)
        lcsc = re.search(r'property "LCSC ID" "([^"]+)"', block)
        footprint = re.search(r'property "Footprint" "([^"]+)"', block)
        at = re.search(r'^\s*\(symbol .*?\(at\s+([-\d.]+)\s+([-\d.]+)', block, re.S)
        out.append({
            'ref': ref or '?',
            'value': value.group(1) if value else '?',
            'lcsc': lcsc.group(1) if lcsc else '',
            'footprint': footprint.group(1) if footprint else '',
            'sch_at': f"{at.group(1)},{at.group(2)}" if at else '',
        })
    return out


def fp_ref(block: str) -> str | None:
    patterns = [
        r'\(property "Reference" "([^"]+)"',
        r'\(fp_text reference "([^"]+)"',
    ]
    for pat in patterns:
        m = re.search(pat, block)
        if m:
            return m.group(1)
    return None


def fp_value(block: str) -> str:
    patterns = [
        r'\(property "Value" "([^"]+)"',
        r'\(fp_text value "([^"]+)"',
    ]
    for pat in patterns:
        m = re.search(pat, block)
        if m:
            return m.group(1)
    return ''


def fp_at(block: str) -> str:
    m = re.search(r'^\(footprint\s+"[^"]+".*?\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+[-\d.]+)?\)', block, re.S)
    if not m:
        m = re.search(r'^\(footprint.*?\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+[-\d.]+)?\)', block, re.S)
    return f"{m.group(1)},{m.group(2)}" if m else ''


def fp_name(block: str) -> str:
    m = re.match(r'\(footprint\s+"([^"]+)"', block)
    return m.group(1) if m else ''


def pad_rows(block: str) -> list[str]:
    rows = []
    for pblock in top_blocks(block, '(pad '):
        head = re.match(r'\(pad\s+"?([^"\s)]*)"?', pblock)
        num = head.group(1) if head else '?'
        net = re.search(r'\(net\s+(\d+)\s+"([^"]+)"\)', pblock)
        at = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', pblock)
        rows.append(
            f"pad {num}: net={net.group(2) if net else '<none>'} "
            f"(#{net.group(1) if net else '-'}) local_at={at.group(1)+','+at.group(2) if at else '?'}"
        )
    return rows


def compact_snippet(block: str, max_lines: int = 40) -> str:
    keep = []
    for line in block.splitlines():
        if any(k in line for k in (
            '(footprint ', '(property "Reference"', '(property "Value"',
            '(property "LCSC ID"', '(at ', '(pad ', '(net ', '(path ', '(tstamp ', '(uuid '
        )):
            keep.append(line.strip())
        if len(keep) >= max_lines:
            break
    return '\n'.join(keep)


def main() -> None:
    pcb = PCB.read_text(errors='replace')
    sol = SOL.read_text(errors='replace')
    devices = find_schematic_devices(sol)

    footprints = list(top_blocks(pcb, '(footprint '))
    fp_by_ref = {fp_ref(b): b for b in footprints if fp_ref(b)}

    net_defs = re.findall(r'^\s*\(net\s+(\d+)\s+"([^"]+)"\)', pcb, re.M)
    interesting_nets = [
        (n, name) for n, name in net_defs
        if any(k in name.upper() for k in ('12V', 'SOL', 'GPIO21', 'PWR_EN', 'MACHINE_PWR'))
    ]

    lines = [
        '# KH910 Rev A — Solenoid PCB Parity Audit', '',
        'Generated from the current branch schematic and PCB.', '',
        f'- PCB bytes: **{len(pcb):,}**',
        f'- PCB footprints parsed: **{len(footprints)}**',
        f'- PCB nets parsed: **{len(net_defs)}**', '',
        '## New fail-safe schematic devices', '',
        '| Project ref | Value | LCSC | Footprint | On PCB? | PCB at |',
        '|---|---|---|---|---|---|',
    ]
    for d in devices:
        b = fp_by_ref.get(d['ref'])
        lines.append(
            f"| {d['ref']} | {d['value']} | {d['lcsc']} | `{d['footprint']}` | "
            f"{'YES' if b else '**NO**'} | {fp_at(b) if b else '—'} |"
        )

    lines += ['', '## Interesting existing board nets', '']
    if interesting_nets:
        lines += [f'- net {n}: `{name}`' for n, name in interesting_nets]
    else:
        lines.append('- No net names containing 12V/SOL/GPIO21/PWR_EN/MACHINE_PWR were found.')

    lines += ['', '## Relevant footprints already on PCB', '']
    relevant = []
    for b in footprints:
        r = fp_ref(b) or ''
        v = fp_value(b)
        name = fp_name(b)
        if (
            r.startswith(('Q', 'TP')) or
            'AO3400' in v.upper() or 'SOT-23' in name.upper() or
            'ULN2003' in v.upper() or
            r.startswith(('U6', 'J6', 'J4'))
        ):
            relevant.append((r, v, name, fp_at(b), pad_rows(b)))
    relevant.sort(key=lambda x: x[0])
    for r, v, name, at, pads in relevant[:120]:
        lines.append(f'### {r or "?"} — {v or "?"}')
        lines.append(f'- footprint: `{name}`')
        lines.append(f'- at: `{at}`')
        for row in pads:
            lines.append(f'- {row}')
        lines.append('')

    # Include compact raw templates for representative footprint classes so a
    # subsequent deterministic board patch can clone repository-native syntax.
    lines += ['## Representative raw footprint templates', '']
    chosen = []
    for b in footprints:
        r = fp_ref(b) or ''
        v = fp_value(b).upper()
        name = fp_name(b).upper()
        if not any(tag == r for tag, _ in chosen):
            if 'SOT-23' in name and not any(tag == 'SOT23' for tag, _ in chosen):
                chosen.append(('SOT23', b))
            elif 'R_0603' in name and not any(tag == 'R0603' for tag, _ in chosen):
                chosen.append(('R0603', b))
            elif r.startswith('TP') and not any(tag == 'TP' for tag, _ in chosen):
                chosen.append(('TP', b))
            elif 'ULN2003' in v and not any(tag == 'ULN' for tag, _ in chosen):
                chosen.append(('ULN', b))
    for tag, b in chosen:
        lines += [f'### {tag}', '```text', compact_snippet(b), '```', '']

    missing = [d['ref'] for d in devices if d['ref'] not in fp_by_ref]
    lines += ['## Parity result', '']
    if missing:
        lines.append('**PCB update required.** Missing fail-safe schematic device footprints: ' + ', '.join(missing))
    else:
        lines.append('All new fail-safe schematic device references already exist on the PCB.')

    OUT.write_text('\n'.join(lines) + '\n')
    print(OUT)
    if missing:
        print('Missing PCB refs:', ', '.join(missing))


if __name__ == '__main__':
    main()
