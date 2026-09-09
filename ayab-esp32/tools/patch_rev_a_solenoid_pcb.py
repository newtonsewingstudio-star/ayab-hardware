#!/usr/bin/env python3
"""Migrate the KH910 Rev A solenoid fail-safe from schematic to PCB.

This patch is intentionally conservative:
- raw +12V remains the controller/PSU rail;
- only known solenoid common/clamp loads move to SOLENOID_12V_SW;
- Q805/Q806/R820-R822/TP703 are added from repository-native footprints;
- a dedicated In1.Cu switched rail is added rather than relabeling the raw bus;
- old raw +12V tracks that terminate directly on migrated pads are removed;
- GPIO21 PCB net 148 is renamed SOLENOID_PWR_EN and routed to R821.

The workflow that calls this script must run KiCad DRC before committing the PCB.
"""

from __future__ import annotations

import math
import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "ayab-esp32.kicad_pcb"
SOL = ROOT / "solenoids.kicad_sch"


def uid() -> str:
    return str(uuid.uuid4())


def extract_block(text: str, start: int) -> tuple[str, int]:
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(text)):
        c = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == '"':
                in_string = False
            continue
        if c == '"':
            in_string = True
        elif c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return text[start:i + 1], i + 1
    raise RuntimeError("Unbalanced KiCad block")


def blocks(text: str, token: str):
    p = 0
    while True:
        p = text.find(token, p)
        if p < 0:
            return
        block, end = extract_block(text, p)
        yield p, end, block
        p = end


def fp_ref(block: str) -> str:
    m = re.search(r'\(fp_text reference "([^"]+)"', block)
    if m:
        return m.group(1)
    m = re.search(r'\(property "Reference" "([^"]+)"', block)
    return m.group(1) if m else ''


def fp_value(block: str) -> str:
    m = re.search(r'\(fp_text value "([^"]+)"', block)
    return m.group(1) if m else ''


def find_fp(text: str, ref: str) -> tuple[int, int, str]:
    for start, end, block in blocks(text, '(footprint '):
        if fp_ref(block) == ref:
            return start, end, block
    raise RuntimeError(f"PCB footprint not found: {ref}")


def top_at(block: str) -> tuple[float, float, float]:
    m = re.search(r'^\(footprint.*?\n\s*\(tstamp [^)]+\)\n\s*\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', block, re.S)
    if not m:
        m = re.search(r'^\(footprint.*?\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', block, re.S)
    if not m:
        raise RuntimeError('Footprint top-level at not found')
    return float(m.group(1)), float(m.group(2)), float(m.group(3) or 0)


def pad_num(pblock: str) -> str:
    m = re.match(r'\(pad\s+"?([^"\s)]*)"?', pblock)
    return m.group(1) if m else ''


def pad_local_at(pblock: str) -> tuple[float, float]:
    m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', pblock)
    return (float(m.group(1)), float(m.group(2))) if m else (0.0, 0.0)


def pad_global(block: str, number: str) -> tuple[float, float]:
    x0, y0, angle = top_at(block)
    th = math.radians(angle)
    ca, sa = math.cos(th), math.sin(th)
    for _, _, pb in blocks(block, '(pad '):
        if pad_num(pb) != str(number):
            continue
        lx, ly = pad_local_at(pb)
        return x0 + lx * ca - ly * sa, y0 + lx * sa + ly * ca
    raise RuntimeError(f"pad {number} missing in {fp_ref(block)}")


def net_defs(text: str) -> dict[int, str]:
    return {int(n): name for n, name in re.findall(r'^\s*\(net\s+(\d+)\s+"([^"]+)"\)', text, re.M)}


def symbol_uuid_by_ref(sch: str, ref: str) -> str:
    for _, _, block in blocks(sch, '(symbol (lib_id '):
        if re.search(rf'property "Reference" "{re.escape(ref)}"', block):
            m = re.search(r'\(uuid ([0-9a-f-]+)\)', block)
            if not m:
                raise RuntimeError(f"symbol UUID missing: {ref}")
            return m.group(1)
    raise RuntimeError(f"schematic symbol missing: {ref}")


def sheet_prefix_from_existing(text: str) -> str:
    _, _, u304 = find_fp(text, 'U304')
    m = re.search(r'\(path "([^"]+)"\)', u304)
    if not m:
        raise RuntimeError('U304 path missing')
    return m.group(1).rsplit('/', 1)[0]


def replace_pad_net(block: str, number: str, netnum: int, netname: str) -> str:
    pieces = []
    last = 0
    found = 0
    for start, end, pb in blocks(block, '(pad '):
        if pad_num(pb) != str(number):
            continue
        found += 1
        if re.search(r'\(net\s+\d+\s+"[^"]+"\)', pb):
            npb = re.sub(r'\(net\s+\d+\s+"[^"]+"\)', f'(net {netnum} "{netname}")', pb, count=1)
        else:
            close = pb.rfind(')')
            npb = pb[:close] + f'\n    (net {netnum} "{netname}")' + pb[close:]
        pieces.append((start, end, npb))
    if found == 0:
        raise RuntimeError(f"pad {number} not found in {fp_ref(block)}")
    out = block
    for start, end, npb in reversed(pieces):
        out = out[:start] + npb + out[end:]
    return out


def replace_fp(text: str, ref: str, block: str) -> str:
    start, end, _ = find_fp(text, ref)
    return text[:start] + block + text[end:]


def retimestamp(block: str) -> str:
    return re.sub(r'\(tstamp [0-9a-f-]+\)', lambda _: f'(tstamp {uid()})', block)


def clone_fp(template: str, new_ref: str, value: str, x: float, y: float, angle: float,
             path: str, lcsc: str, padmap: dict[str, tuple[int, str]]) -> str:
    out = retimestamp(template)
    out, n = re.subn(
        r'(^\(footprint.*?\n\s*\(tstamp [^)]+\)\n\s*)\(at\s+[-\d.]+\s+[-\d.]+(?:\s+[-\d.]+)?\)',
        lambda m: m.group(1) + f'(at {x:g} {y:g} {angle:g})', out, count=1, flags=re.S,
    )
    if n != 1:
        raise RuntimeError(f"could not relocate cloned footprint {new_ref}")
    out = re.sub(r'\(path "[^"]+"\)', f'(path "{path}")', out, count=1)
    out = re.sub(r'\(fp_text reference "[^"]+"', f'(fp_text reference "{new_ref}"', out, count=1)
    out = re.sub(r'\(fp_text value "[^"]+"', f'(fp_text value "{value}"', out, count=1)
    if '(property "LCSC ID"' in out:
        out = re.sub(r'\(property "LCSC ID" "[^"]*"\)', f'(property "LCSC ID" "{lcsc}")', out, count=1)
    else:
        anchor = re.search(r'\n\s*\(path "[^"]+"\)', out)
        if not anchor:
            raise RuntimeError(f"path anchor missing in {new_ref}")
        out = out[:anchor.start()] + f'\n  (property "LCSC ID" "{lcsc}")' + out[anchor.start():]
    for pn, (ni, nn) in padmap.items():
        out = replace_pad_net(out, pn, ni, nn)
    return out


def segment(x1: float, y1: float, x2: float, y2: float, width: float, layer: str, net: int) -> str:
    return (
        f'  (segment (start {x1:g} {y1:g}) (end {x2:g} {y2:g}) (width {width:g}) '
        f'(layer "{layer}") (net {net}) (tstamp {uid()}))'
    )


def via(x: float, y: float, net: int, size: float = 0.8, drill: float = 0.4) -> str:
    return (
        f'  (via (at {x:g} {y:g}) (size {size:g}) (drill {drill:g}) '
        f'(layers "F.Cu" "B.Cu") (net {net}) (tstamp {uid()}))'
    )


def seg_points(sblock: str) -> tuple[tuple[float, float], tuple[float, float], int] | None:
    a = re.search(r'\(start\s+([-\d.]+)\s+([-\d.]+)\)', sblock)
    b = re.search(r'\(end\s+([-\d.]+)\s+([-\d.]+)\)', sblock)
    n = re.search(r'\(net\s+(\d+)\)', sblock)
    if not a or not b or not n:
        return None
    return ((float(a.group(1)), float(a.group(2))), (float(b.group(1)), float(b.group(2))), int(n.group(1)))


def close(a: tuple[float, float], b: tuple[float, float], tol: float = 0.015) -> bool:
    return abs(a[0]-b[0]) <= tol and abs(a[1]-b[1]) <= tol


def remove_raw_tracks_touching(text: str, points: list[tuple[float, float]]) -> tuple[str, int]:
    removals = []
    for start, end, sb in blocks(text, '(segment '):
        d = seg_points(sb)
        if not d or d[2] != 4:
            continue
        if any(close(d[0], p) or close(d[1], p) for p in points):
            removals.append((start, end))
    for start, end, vb in blocks(text, '(via '):
        n = re.search(r'\(net\s+(\d+)\)', vb)
        a = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)\)', vb)
        if not n or int(n.group(1)) != 4 or not a:
            continue
        p = (float(a.group(1)), float(a.group(2)))
        if any(close(p, q) for q in points):
            removals.append((start, end))
    for start, end in sorted(removals, reverse=True):
        text = text[:start] + text[end:]
    return text, len(removals)


def insert_before_first(text: str, token: str, payload: str) -> str:
    # Match the requested KiCad item only at root indentation. A plain
    # substring search can match nested items (notably footprint keepout zones),
    # which makes subsequently inserted route primitives invalid PCB syntax.
    m = re.search(rf'(?m)^{re.escape(token)}', text)
    p = m.start() if m else text.rfind('\n)')
    if p < 0:
        raise RuntimeError(f"insert anchor missing: {token}")
    return text[:p] + payload + '\n' + text[p:]


def main() -> None:
    pcb = PCB.read_text(errors='strict')
    sch = SOL.read_text(errors='strict')

    present = [r for r in ('Q805','Q806','R820','R821','R822','TP703') if re.search(rf'\(fp_text reference "{r}"', pcb)]
    if present:
        if len(present) == 6 and 'SOLENOID_12V_SW' in pcb:
            print('Solenoid fail-safe PCB already present')
            return
        raise RuntimeError('Partial fail-safe PCB state present: ' + ', '.join(present))

    defs = net_defs(pcb)
    if defs.get(148) != '/ESP32/ESP21':
        raise RuntimeError(f"Expected GPIO21 PCB net 148 /ESP32/ESP21, found {defs.get(148)!r}")
    maxnet = max(defs)
    sw_net, pg_net, ng_net = maxnet + 1, maxnet + 2, maxnet + 3
    sw_name = 'SOLENOID_12V_SW'
    pg_name = 'Net-(Q805-G)'
    ng_name = 'Net-(Q806-G)'
    en_net, en_name = 148, 'SOLENOID_PWR_EN'

    pcb = pcb.replace('/ESP32/ESP21', en_name)
    new_net_text = (
        f'  (net {sw_net} "{sw_name}")\n'
        f'  (net {pg_net} "{pg_name}")\n'
        f'  (net {ng_net} "{ng_name}")\n'
    )
    pcb = insert_before_first(pcb, '  (footprint ', new_net_text.rstrip())

    targets: dict[str, tuple[str, ...]] = {
        'J401': ('9','10'), 'J403': ('9','10'), 'J406': ('9','10'),
        'U302': ('9',), 'U303': ('9',), 'U304': ('9',),
        'C302': ('1',), 'C303': ('1',), 'C304': ('1',),
    }
    target_points: list[tuple[float, float]] = []
    for ref, pads in targets.items():
        _, _, fb = find_fp(pcb, ref)
        for pn in pads:
            target_points.append(pad_global(fb, pn))

    pcb, removed = remove_raw_tracks_touching(pcb, target_points)
    print(f'Removed {removed} raw +12V segment/via blocks touching migrated solenoid pads')

    for ref, pads in targets.items():
        _, _, fb = find_fp(pcb, ref)
        for pn in pads:
            fb = replace_pad_net(fb, pn, sw_net, sw_name)
        pcb = replace_fp(pcb, ref, fb)

    _, _, q502 = find_fp(pcb, 'Q502')
    _, _, q201 = find_fp(pcb, 'Q201')
    _, _, r809 = find_fp(pcb, 'R809')
    _, _, tp701 = find_fp(pcb, 'TP701')
    prefix = sheet_prefix_from_existing(pcb)
    su = {r: symbol_uuid_by_ref(sch, r) for r in ('Q805','Q806','R820','R821','R822','TP703')}
    path = lambda r: prefix + '/' + su[r]

    newfps = [
        clone_fp(q502, 'Q805', 'LP9435LT1G', 301.0, 150.0, -90, path('Q805'), 'C383257',
                 {'1': (pg_net,pg_name), '2': (4,'+12V'), '3': (sw_net,sw_name)}),
        clone_fp(q201, 'Q806', 'AO3400A', 297.5, 151.0, 0, path('Q806'), 'C20917',
                 {'1': (ng_net,ng_name), '2': (2,'GND'), '3': (pg_net,pg_name)}),
        clone_fp(r809, 'R820', '100k', 301.0, 150.9375, 180, path('R820'), 'C25803',
                 {'1': (4,'+12V'), '2': (pg_net,pg_name)}),
        clone_fp(r809, 'R821', '10k', 294.6, 150.05, 0, path('R821'), 'C25804',
                 {'1': (en_net,en_name), '2': (ng_net,ng_name)}),
        clone_fp(r809, 'R822', '100k', 292.0, 153.0, 0, path('R822'), 'C25803',
                 {'1': (2,'GND'), '2': (ng_net,ng_name)}),
        clone_fp(tp701, 'TP703', 'SOL12_SW', 299.2, 146.8, 0, path('TP703'), '',
                 {'1': (sw_net,sw_name)}),
    ]
    pcb = insert_before_first(pcb, '  (segment ', '\n'.join(newfps))

    q805_gate = (300.05, 150.9375)
    q805_source = (301.95, 150.9375)
    q805_drain = (301.0, 149.0625)
    q806_gate = (296.5625, 150.05)
    q806_source = (296.5625, 151.95)
    q806_drain = (298.4375, 151.0)
    r820_raw = (301.825, 150.9375)
    r820_pg = (300.175, 150.9375)
    r821_en = (293.775, 150.05)
    r821_ng = (295.425, 150.05)
    r822_gnd = (291.175, 153.0)
    r822_ng = (292.825, 153.0)

    routing: list[str] = []
    routing += [
        segment(*q805_source, 303.43, 152.42, 1.0, 'F.Cu', 4),
        segment(303.43, 152.42, 303.43, 153.36, 1.0, 'F.Cu', 4),
        segment(*q805_source, *r820_raw, 0.5, 'F.Cu', 4),
    ]
    routing += [
        segment(*q805_gate, *r820_pg, 0.25, 'F.Cu', pg_net),
        segment(*q805_gate, *q806_drain, 0.25, 'F.Cu', pg_net),
    ]
    routing += [
        segment(*r821_ng, *q806_gate, 0.25, 'F.Cu', ng_net),
        segment(*r821_ng, 294.3, 151.2, 0.25, 'F.Cu', ng_net),
        segment(294.3, 151.2, 294.3, 153.0, 0.25, 'F.Cu', ng_net),
        segment(294.3, 153.0, *r822_ng, 0.25, 'F.Cu', ng_net),
    ]
    gvia = (290.8, 154.5)
    routing += [
        segment(*q806_source, 296.5625, 154.0, 0.35, 'F.Cu', 2),
        segment(296.5625, 154.0, 291.175, 154.0, 0.35, 'F.Cu', 2),
        segment(*r822_gnd, 291.175, 154.0, 0.35, 'F.Cu', 2),
        segment(291.175, 154.0, *gvia, 0.35, 'F.Cu', 2),
        via(*gvia, 2),
    ]
    en_via_mcu = (227.2, 138.1)
    en_via_gate = (292.0, 147.5)
    routing += [
        segment(225.825, 136.675, *en_via_mcu, 0.25, 'F.Cu', en_net),
        via(*en_via_mcu, en_net, 0.6, 0.3),
        segment(*en_via_mcu, 285.0, 138.1, 0.25, 'In1.Cu', en_net),
        segment(285.0, 138.1, 292.0, 145.1, 0.25, 'In1.Cu', en_net),
        segment(292.0, 145.1, *en_via_gate, 0.25, 'In1.Cu', en_net),
        via(*en_via_gate, en_net, 0.6, 0.3),
        segment(*en_via_gate, *r821_en, 0.25, 'F.Cu', en_net),
    ]

    sw_via = (301.0, 146.8)
    bus_y = 162.5
    routing += [
        segment(*q805_drain, *sw_via, 0.9, 'F.Cu', sw_net),
        via(*sw_via, sw_net, 1.0, 0.5),
        segment(299.2, 146.8, *sw_via, 0.5, 'F.Cu', sw_net),
        segment(*sw_via, 301.0, bus_y, 1.27, 'In1.Cu', sw_net),
        segment(95.65, bus_y, 310.91, bus_y, 1.27, 'In1.Cu', sw_net),
    ]

    for x, y in ((116.84,153.7852),(114.84,153.7852),(119.24,146.28),(116.74,146.28),
                 (310.91,138.83),(308.41,138.83)):
        routing.append(segment(x, y, x, bus_y, 1.0, 'In1.Cu', sw_net))

    smd_vias = [
        ((132.895,136.85),(134.295,136.85)),
        ((120.345,136.85),(121.745,136.85)),
        ((107.795,136.85),(109.195,136.85)),
        ((109.625,142.275),(111.025,142.275)),
        ((122.175,142.275),(123.575,142.275)),
        ((97.05,142.275),(95.65,142.275)),
    ]
    for pad, vv in smd_vias:
        routing.append(segment(*pad, *vv, 0.5, 'F.Cu', sw_net))
        routing.append(via(*vv, sw_net, 0.8, 0.4))
        routing.append(segment(*vv, vv[0], bus_y, 0.8, 'In1.Cu', sw_net))

    pcb = insert_before_first(pcb, '  (zone ', '\n'.join(routing))

    for ref in ('Q805','Q806','R820','R821','R822','TP703'):
        if not re.search(rf'\(fp_text reference "{ref}"', pcb):
            raise RuntimeError(f"new PCB footprint missing: {ref}")
    if f'(net {sw_net} "{sw_name}")' not in pcb:
        raise RuntimeError('switched net definition missing')
    if '/ESP32/ESP21' in pcb:
        raise RuntimeError('legacy GPIO21 PCB net name remains')
    for ref, pads in targets.items():
        _, _, fb = find_fp(pcb, ref)
        for pn in pads:
            matched = False
            for _, _, pb in blocks(fb, '(pad '):
                if pad_num(pb) == pn:
                    matched = f'(net {sw_net} "{sw_name}")' in pb
                    break
            if not matched:
                raise RuntimeError(f'{ref} pad {pn} did not migrate to switched rail')

    PCB.write_text(pcb)
    print(f'Staged solenoid fail-safe PCB: switched net {sw_net}, P-gate {pg_net}, N-gate {ng_net}')


if __name__ == '__main__':
    main()
