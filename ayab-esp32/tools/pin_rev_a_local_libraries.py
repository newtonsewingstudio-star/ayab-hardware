#!/usr/bin/env python3
"""Pin nonstandard Rev A symbols and footprints inside this repository."""

from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parents[2]
PCB = ROOT / "ayab-esp32" / "ayab-esp32.kicad_pcb"
PSU = ROOT / "ayab-esp32" / "psu.kicad_sch"
SYMBOL_LIBRARY = ROOT / "ayab-library" / "ayab-lib.kicad_sym"
FOOTPRINT_ROOT = ROOT / "ayab-library"


def expression_at(text: str, start: int) -> str:
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
                return text[start : pos + 1]
    raise RuntimeError("unbalanced KiCad expression")


def pin_custom_symbols() -> None:
    library = SYMBOL_LIBRARY.read_text(encoding="utf-8")
    # The first repair run inserted before XL1509's embedded-fonts field.  Move
    # that bounded group to the library root before adding anything else.
    misplaced = library.find('\n\t(symbol "KMB14F_Bridge"')
    closing = library.rfind("\n\t\t(embedded_fonts no)\n\t)\n)")
    if misplaced >= 0 and closing > misplaced:
        group = library[misplaced:closing]
        library = library[:misplaced] + library[closing:]
        root_close = library.rfind("\n)")
        library = library[:root_close] + group + library[root_close:]
    additions: list[str] = []
    for schematic in sorted((ROOT / "ayab-esp32").glob("*.kicad_sch")):
        source = schematic.read_text(encoding="utf-8")
        position = 0
        marker = '(symbol "ayab-lib:'
        while True:
            start = source.find(marker, position)
            if start < 0:
                break
            symbol = expression_at(source, start)
            qualified = symbol.split('"', 2)[1]
            name = qualified.split(":", 1)[1]
            if f'(symbol "{name}"' not in library and all(
                not item.startswith(f'(symbol "{name}"') for item in additions
            ):
                additions.append(symbol.replace(f'(symbol "{qualified}"', f'(symbol "{name}"', 1))
            position = start + len(symbol)
    if additions:
        insertion = library.rfind("\n)")
        if insertion < 0:
            raise RuntimeError("symbol-library insertion point is absent")
        library = library[:insertion] + "\n".join(additions) + library[insertion:]
    SYMBOL_LIBRARY.write_text(library, encoding="utf-8", newline="\n")
    print("PINNED_SYMBOLS", len(additions))


def pin_imported_footprints() -> None:
    board = pcbnew.LoadBoard(str(PCB))
    plugin = pcbnew.PCB_IO_MGR.PluginFind(pcbnew.PCB_IO_MGR.KICAD_SEXP)
    exported: set[tuple[str, str]] = set()
    for footprint in board.GetFootprints():
        fpid = footprint.GetFPID()
        nickname = str(fpid.GetLibNickname())
        name = str(fpid.GetLibItemName())
        if nickname not in {"Library", "easyeda2kicad", "Espressif"}:
            continue
        key = (nickname, name)
        if key in exported:
            continue
        destination = FOOTPRINT_ROOT / f"{nickname}.pretty"
        destination.mkdir(exist_ok=True)
        library_copy = footprint.Duplicate()
        library_copy.SetReference("REF**")
        library_copy.SetValue(name)
        plugin.FootprintSave(str(destination), library_copy)
        exported.add(key)
    if not exported:
        raise RuntimeError("no imported footprints found to pin")
    print("PINNED_FOOTPRINTS", len(exported))


def main() -> None:
    pin_custom_symbols()
    pin_imported_footprints()
    print("LOCAL_LIBRARIES_OK")


if __name__ == "__main__":
    main()
