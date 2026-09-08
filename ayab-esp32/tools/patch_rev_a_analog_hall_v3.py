#!/usr/bin/env python3
"""Apply the Rev A passive Hall stage with MCU-scoped checks and explicit NCs.

GPIO3 is intentionally reserved and GPIO4 is intentionally freed for the next
machine-power-sense stage. KiCad ERC requires deliberate open MCU pins to carry
no-connect markers, so this stage adds temporary NCs at those two pins. The
GPIO4 NC must be removed when MACHINE_PWR_SENSE is implemented.
"""

import uuid

from patch_rev_a_analog_hall import TOP, MCU, IO, patch_top, patch_mcu, patch_io, find_sheet


def ensure_no_connect(text: str, x: str, y: str) -> str:
    marker = f"(no_connect (at {x} {y})"
    if marker in text:
        return text
    anchor = "  (no_connect "
    pos = text.find(anchor)
    if pos < 0:
        raise RuntimeError("No-connect insertion anchor not found")
    block = f"  (no_connect (at {x} {y}) (uuid {uuid.uuid4()}))\n"
    return text[:pos] + block + text[pos:]


def main() -> None:
    top = TOP.read_text(encoding="utf-8")
    mcu = MCU.read_text(encoding="utf-8")
    io = IO.read_text(encoding="utf-8")

    already = (
        '(hierarchical_label "HALL_L_ADC"' in mcu
        and '(hierarchical_label "HALL_R_ADC"' in mcu
        and '(hierarchical_label "HALL_L_ADC"' in io
        and '(hierarchical_label "HALL_R_ADC"' in io
        and '(no_connect (at 185.42 80.01)' in mcu
        and '(no_connect (at 185.42 82.55)' in mcu
    )
    if already:
        print("Rev A passive Hall ADC stage already applied")
        return

    top = patch_top(top)
    mcu = patch_mcu(mcu)
    io = patch_io(io)

    # Explicitly mark the two now-open MCU pins for this staged revision.
    mcu = ensure_no_connect(mcu, "185.42", "80.01")
    mcu = ensure_no_connect(mcu, "185.42", "82.55")

    _, _, io_sheet = find_sheet(top, "ioconditioning.kicad_sch")
    _, _, mcu_sheet = find_sheet(top, "mcu.kicad_sch")

    for name in ("HALL_L_ADC", "HALL_R_ADC"):
        if f'(pin "{name}" output' not in io_sheet:
            raise RuntimeError(f"I/O sheet parent output missing: {name}")
        if f'(pin "{name}" input' not in mcu_sheet:
            raise RuntimeError(f"MCU sheet parent input missing: {name}")
        if f'(hierarchical_label "{name}"' not in mcu:
            raise RuntimeError(f"MCU label missing: {name}")
        if f'(hierarchical_label "{name}"' not in io:
            raise RuntimeError(f"I/O conditioning label missing: {name}")

    for old in ("EOL_R_P", "EOL_R_N"):
        if f'(pin "{old}"' in mcu_sheet:
            raise RuntimeError(f"Old comparator pin remains on MCU sheet: {old}")
        if f'(hierarchical_label "{old}"' in mcu:
            raise RuntimeError(f"Old comparator label remains on MCU child: {old}")

    for old in ("EOL_L_P", "EOL_L_N", "EOL_R_P", "EOL_R_N"):
        if f'(hierarchical_label "{old}"' in io:
            raise RuntimeError(f"Old comparator output still exported by conditioning sheet: {old}")

    TOP.write_text(top, encoding="utf-8")
    MCU.write_text(mcu, encoding="utf-8")
    IO.write_text(io, encoding="utf-8")
    print("Applied passive Hall ADC stage; GPIO3/4 explicitly NC for staged ERC")


if __name__ == "__main__":
    main()
