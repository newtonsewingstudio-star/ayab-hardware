#!/usr/bin/env python3
"""Apply the Rev A passive Hall stage with MCU-scoped interface checks.

The first implementation correctly transformed the in-memory schematics but its
final check searched the entire top-level design for EOL_R_N/EOL_R_P. Those
names legitimately still exist on other machine/connector interfaces. This
wrapper scopes the check to the ESP32 child-sheet interface, which is the actual
requirement.
"""

from patch_rev_a_analog_hall import TOP, MCU, IO, patch_top, patch_mcu, patch_io, find_sheet


def main() -> None:
    top = TOP.read_text(encoding="utf-8")
    mcu = MCU.read_text(encoding="utf-8")
    io = IO.read_text(encoding="utf-8")

    already = (
        '(hierarchical_label "HALL_L_ADC"' in mcu
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

    # The old comparator polarities may legitimately remain elsewhere in the
    # machine connector hierarchy during this staged change. They must not,
    # however, remain on the ESP32 sheet interface or MCU GPIO3/4.
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
    print("Applied passive 10k/10k Hall ADC stage and freed MCU GPIO3/4")


if __name__ == "__main__":
    main()
