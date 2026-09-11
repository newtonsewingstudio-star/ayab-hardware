#!/usr/bin/env python3
"""Remove independently identified obsolete ERC remnants from Rev A sheets."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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
    raise RuntimeError("unbalanced expression")


def remove_matching(text: str, token: str, predicate) -> tuple[str, int]:
    removals: list[tuple[int, int]] = []
    position = 0
    while True:
        start = text.find(token, position)
        if start < 0:
            break
        block, end = block_at(text, start)
        if predicate(block):
            removals.append((start, end))
        position = end
    for start, end in reversed(removals):
        text = text[:start] + text[end:]
    return text, len(removals)


def remove_label(path: Path, name: str, coordinate: tuple[float, float]) -> None:
    text = path.read_text(encoding="utf-8")
    x, y = coordinate
    coordinate_text = f"(at {x:g} {y:g} "
    text, count = remove_matching(
        text,
        f'(label "{name}"',
        lambda block: coordinate_text in block,
    )
    if count not in (0, 1):
        raise RuntimeError(f"expected at most one {name} label at {coordinate}, found {count}")
    path.write_text(text, encoding="utf-8", newline="\n")


def remove_comparator_wires() -> None:
    path = ROOT / "ioconditioning.kicad_sch"
    text = path.read_text(encoding="utf-8")
    independently_reported_wires = {
        frozenset({(194.31, 33.02), (190.50, 33.02)}),
        frozenset({(179.07, 58.42), (179.07, 43.18)}),
        frozenset({(179.07, 43.18), (194.31, 43.18)}),
        frozenset({(179.07, 58.42), (190.50, 58.42)}),
        frozenset({(181.61, 60.96), (190.50, 60.96)}),
        frozenset({(204.47, 33.02), (199.39, 33.02)}),
        frozenset({(204.47, 33.02), (204.47, 35.56)}),
        frozenset({(204.47, 30.48), (204.47, 33.02)}),
        frozenset({(181.61, 74.93), (194.31, 74.93)}),
        frozenset({(204.47, 50.80), (204.47, 53.34)}),
        frozenset({(209.55, 40.64), (213.36, 40.64)}),
        frozenset({(194.31, 106.68), (190.50, 106.68)}),
        frozenset({(209.55, 77.47), (250.19, 77.47)}),
        frozenset({(204.47, 106.68), (199.39, 106.68)}),
        frozenset({(181.61, 116.84), (194.31, 116.84)}),
        frozenset({(181.61, 132.08), (190.50, 132.08)}),
        frozenset({(204.47, 106.68), (204.47, 109.22)}),
        frozenset({(204.47, 104.14), (204.47, 106.68)}),
        frozenset({(179.07, 134.62), (190.50, 134.62)}),
        frozenset({(209.55, 114.30), (213.36, 114.30)}),
        frozenset({(233.68, 45.72), (233.68, 48.26)}),
        frozenset({(233.68, 48.26), (233.68, 50.80)}),
        frozenset({(204.47, 124.46), (204.47, 127.00)}),
        frozenset({(233.68, 68.58), (233.68, 71.12)}),
        frozenset({(194.31, 149.86), (179.07, 149.86)}),
        frozenset({(243.84, 48.26), (243.84, 50.80)}),
        frozenset({(243.84, 68.58), (243.84, 71.12)}),
        frozenset({(209.55, 152.40), (250.19, 152.40)}),
        frozenset({(256.54, 40.64), (256.54, 44.45)}),
        frozenset({(256.54, 49.53), (256.54, 52.07)}),
        frozenset({(261.62, 30.48), (261.62, 33.02)}),
        frozenset({(261.62, 38.10), (261.62, 40.64)}),
        frozenset({(233.68, 121.92), (233.68, 124.46)}),
        frozenset({(233.68, 119.38), (233.68, 121.92)}),
        frozenset({(233.68, 142.24), (233.68, 144.78)}),
        frozenset({(243.84, 121.92), (243.84, 124.46)}),
        frozenset({(243.84, 142.24), (243.84, 144.78)}),
        frozenset({(256.54, 114.30), (256.54, 118.11)}),
        frozenset({(261.62, 104.14), (261.62, 106.68)}),
        frozenset({(261.62, 111.76), (261.62, 114.30)}),
        frozenset({(256.54, 123.19), (256.54, 125.73)}),
    }

    def obsolete(block: str) -> bool:
        points = {
            (float(x), float(y))
            for x, y in re.findall(r"\(xy ([0-9.]+) ([0-9.]+)\)", block)
        }
        return frozenset(points) in independently_reported_wires

    text, count = remove_matching(text, "(wire ", obsolete)
    if count not in (0, 41):
        raise RuntimeError(f"expected 0 or 41 independently mapped obsolete wires, found {count}")
    path.write_text(text, encoding="utf-8", newline="\n")
    print("REMOVED_COMPARATOR_WIRES", count)


def remove_exposed_comparator_stubs() -> None:
    path = ROOT / "ioconditioning.kicad_sch"
    text = path.read_text(encoding="utf-8")
    exposed = {
        frozenset({(181.61, 74.93), (181.61, 60.96)}),
        frozenset({(190.50, 33.02), (190.50, 35.56)}),
        frozenset({(190.50, 106.68), (190.50, 109.22)}),
        frozenset({(181.61, 120.65), (181.61, 132.08)}),
        frozenset({(179.07, 149.86), (179.07, 144.78)}),
        frozenset({(233.68, 71.12), (243.84, 71.12)}),
        frozenset({(233.68, 48.26), (243.84, 48.26)}),
        frozenset({(250.19, 77.47), (250.19, 40.64)}),
        frozenset({(233.68, 121.92), (243.84, 121.92)}),
        frozenset({(233.68, 144.78), (243.84, 144.78)}),
        frozenset({(250.19, 152.40), (250.19, 114.30)}),
    }

    def is_exposed(block: str) -> bool:
        points = frozenset(
            (float(x), float(y))
            for x, y in re.findall(r"\(xy ([0-9.]+) ([0-9.]+)\)", block)
        )
        return points in exposed

    text, wire_count = remove_matching(text, "(wire ", is_exposed)
    if wire_count not in (0, 11):
        raise RuntimeError(f"expected 0 or 11 exposed stubs, found {wire_count}")

    orphan_power_refs = {
        "#PWR0706", "#PWR0707", "#PWR0708", "#PWR0709", "#PWR0710", "#PWR0711", "#PWR0712",
        "#PWR0713", "#PWR0716", "#PWR0717", "#PWR0718", "#PWR0719",
    }
    text, symbol_count = remove_matching(
        text,
        "(symbol ",
        lambda block: any(f'(property "Reference" "{ref}"' in block for ref in orphan_power_refs),
    )
    if symbol_count not in (0, 2, 12):
        raise RuntimeError(f"unexpected orphan power-symbol count: {symbol_count}")
    path.write_text(text, encoding="utf-8", newline="\n")
    remove_label(path, "EOL_L_K", (184.15, 43.18))
    remove_label(path, "EOL_L_L", (184.15, 74.93))
    print("REMOVED_EXPOSED_STUBS", wire_count, symbol_count)


def main() -> None:
    remove_comparator_wires()
    remove_exposed_comparator_stubs()
    remove_label(ROOT / "mcu.kicad_sch", "ESP21", (198.12, 115.57))
    remove_label(ROOT / "mcu.kicad_sch", "SOLENOID_PWR_EN", (195.58, 115.57))
    remove_label(ROOT / "mcu.kicad_sch", "ESP14", (198.12, 107.95))
    remove_label(ROOT / "mcu.kicad_sch", "ESP39", (82.5122, 69.85))
    remove_label(ROOT / "solenoids.kicad_sch", "SOLENOID_12V_SW", (243.84, 167.64))
    remove_label(ROOT / "psu.kicad_sch", "BRIDGE_P", (71.12, 36.83))
    remove_label(ROOT / "psu.kicad_sch", "MACHINE_5V_RAW", (257.81, 54.61))
    for name in (
        "ioconditioning.kicad_sch", "mcu.kicad_sch", "psu.kicad_sch",
        "solenoids.kicad_sch",
    ):
        path = ROOT / name
        lines = path.read_text(encoding="utf-8").splitlines()
        path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8", newline="\n")
    print("ERC_SOURCE_CLEANUP_OK")


if __name__ == "__main__":
    main()
