#!/usr/bin/env python3
"""Build progressive route-prefix variants of the rejected solenoid PCB patch.

Usage:
  debug_rev_a_solenoid_route_prefix.py ORIGINAL FULL OUTDIR

The script identifies segment/via blocks present in FULL but not ORIGINAL by
`tstamp`, then writes boards containing 0..N of those new route primitives in
the exact order/positions used by FULL. This pinpoints the first primitive that
makes KiCad reject the board without changing any already-validated footprints
or net migration.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path


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
    raise RuntimeError(f'unbalanced block starting at byte {start}')


def blocks(text: str, token: str):
    p = 0
    while True:
        p = text.find(token, p)
        if p < 0:
            return
        block, end = extract_block(text, p)
        yield p, end, block
        p = end


def tstamp(block: str) -> str:
    m = re.search(r'\(tstamp ([0-9a-f-]+)\)', block)
    return m.group(1) if m else ''


def describe(kind: str, block: str) -> str:
    layer = re.search(r'\(layer "([^"]+)"\)', block)
    net = re.search(r'\(net (\d+)\)', block)
    at = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)\)', block)
    start = re.search(r'\(start\s+([-\d.]+)\s+([-\d.]+)\)', block)
    end = re.search(r'\(end\s+([-\d.]+)\s+([-\d.]+)\)', block)
    bits = [kind, f'net={net.group(1) if net else "?"}']
    if layer:
        bits.append(f'layer={layer.group(1)}')
    if at:
        bits.append(f'at={at.group(1)},{at.group(2)}')
    if start and end:
        bits.append(f'{start.group(1)},{start.group(2)}->{end.group(1)},{end.group(2)}')
    return ' '.join(bits)


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit('usage: script ORIGINAL FULL OUTDIR')
    orig_path, full_path, outdir = map(Path, sys.argv[1:])
    outdir.mkdir(parents=True, exist_ok=True)
    original = orig_path.read_text(errors='strict')
    full = full_path.read_text(errors='strict')

    old_ids: set[str] = set()
    for token in ('(segment ', '(via '):
        for _, _, block in blocks(original, token):
            ts = tstamp(block)
            if ts:
                old_ids.add(ts)

    new_routes: list[tuple[int, int, str, str]] = []
    for token, kind in (('(segment ', 'segment'), ('(via ', 'via')):
        for start, end, block in blocks(full, token):
            ts = tstamp(block)
            if ts and ts not in old_ids:
                new_routes.append((start, end, kind, block))
    new_routes.sort(key=lambda x: x[0])
    if not new_routes:
        raise RuntimeError('no newly-added route primitives found')

    manifest = [f'route_count={len(new_routes)}']
    for idx, (_, _, kind, block) in enumerate(new_routes, 1):
        manifest.append(f'{idx:03d}\t{describe(kind, block)}\t{block}')
    (outdir / 'manifest.tsv').write_text('\n'.join(manifest) + '\n')

    # For each prefix, remove only the suffix of new primitives from FULL. This
    # preserves exact byte placement/order of all primitives retained.
    for keep in range(0, len(new_routes) + 1):
        text = full
        for start, end, _, _ in reversed(new_routes[keep:]):
            text = text[:start] + text[end:]
        (outdir / f'{keep:03d}.kicad_pcb').write_text(text)

    print((outdir / 'manifest.tsv').read_text())


if __name__ == '__main__':
    main()
