#!/usr/bin/env python3
"""Apply the first KH910 Rev A MCU-sheet correction: native ESP32-S3 USB.

Changes are deliberately narrow and assertion-heavy:
- USB D- (USB_M) moves from GPIO38 to native USB GPIO19.
- BUZZER moves from GPIO19 to GPIO38.
- USB D+ (USB_P) moves from strapping GPIO45 to native USB GPIO20.
- The obsolete MCU-side VCC_SPI attachment on GPIO20 is removed.

This script edits only mcu.kicad_sch. It is idempotent: if the target state is
already present it exits successfully without rewriting the file.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "mcu.kicad_sch"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one occurrence, found {count}")
    return text.replace(old, new, 1)


def remove_balanced_block(text: str, start_token: str, label: str) -> str:
    start = text.find(start_token)
    if start < 0:
        raise RuntimeError(f"{label}: block start not found")
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
                end = i + 1
                # Remove one trailing newline to keep formatting tidy.
                if end < len(text) and text[end] == '\n':
                    end += 1
                return text[:start] + text[end:]
    raise RuntimeError(f"{label}: unbalanced block")


def main() -> None:
    text = PATH.read_text(encoding="utf-8")

    target_markers = [
        '(hierarchical_label "USB_M" (shape bidirectional) (at 198.12 118.11 0)',
        '(label "BUZZER" (at 198.12 67.31 180)',
        '(hierarchical_label "USB_P" (shape bidirectional) (at 198.12 120.65 0)',
    ]
    obsolete_markers = [
        '(hierarchical_label "USB_M" (shape bidirectional) (at 198.12 67.31 0)',
        '(label "BUZZER" (at 198.12 118.11 180)',
        '(hierarchical_label "USB_P" (shape bidirectional) (at 198.12 64.77 0)',
        '(label "VCC_SPI" (at 198.12 120.65 180)',
    ]

    if all(x in text for x in target_markers) and not any(x in text for x in obsolete_markers):
        print("Rev A native USB patch already applied")
        return

    # Move label identities to the GPIO rows we actually want.
    text = replace_once(
        text,
        '(hierarchical_label "USB_M" (shape bidirectional) (at 198.12 67.31 0)',
        '(hierarchical_label "USB_M" (shape bidirectional) (at 198.12 118.11 0)',
        "USB_M label",
    )
    text = replace_once(
        text,
        '(label "BUZZER" (at 198.12 118.11 180)',
        '(label "BUZZER" (at 198.12 67.31 180)',
        "BUZZER label",
    )
    text = replace_once(
        text,
        '(hierarchical_label "USB_P" (shape bidirectional) (at 198.12 64.77 0)',
        '(hierarchical_label "USB_P" (shape bidirectional) (at 198.12 120.65 0)',
        "USB_P label",
    )

    # GPIO20's VCC_SPI local label is legacy MCU-side baggage. Keep the separate
    # configuration-section VCC_SPI label intact; remove only the one on GPIO20.
    text = remove_balanced_block(
        text,
        '(label "VCC_SPI" (at 198.12 120.65 180)',
        "GPIO20 VCC_SPI label",
    )

    wire_usb_m = """(wire (pts (xy 185.42 67.31) (xy 198.12 67.31))
    (stroke (width 0) (type default))
    (uuid b6d2f484-9bee-4259-90e9-0a57fede749c)
  )"""
    wire_buzzer = """(wire (pts (xy 185.42 118.11) (xy 198.12 118.11))
    (stroke (width 0) (type default))
    (uuid 6c8d4e5b-64d5-4725-8ab2-a8260da28abb)
  )"""
    wire_usb_p = """(wire (pts (xy 185.42 64.77) (xy 198.12 64.77))
    (stroke (width 0) (type default))
    (uuid 3983eb93-9526-48db-85d8-1875e8cba104)
  )"""
    wire_vcc_spi = """(wire (pts (xy 185.42 120.65) (xy 198.12 120.65))
    (stroke (width 0) (type default))
    (uuid 2db3c421-da0a-412a-bfa1-93464a1ea3c6)
  )"""

    for block, name in (
        (wire_usb_m, "USB_M wire"),
        (wire_buzzer, "BUZZER wire"),
        (wire_usb_p, "USB_P wire"),
        (wire_vcc_spi, "VCC_SPI wire"),
    ):
        if text.count(block) != 1:
            raise RuntimeError(f"{name}: expected exactly one wire block")

    # Swap USB_M and BUZZER wire rows while preserving each wire UUID.
    token_a = "__REV_A_USB_M_WIRE__"
    token_b = "__REV_A_BUZZER_WIRE__"
    text = text.replace(wire_usb_m, token_a, 1)
    text = text.replace(wire_buzzer, token_b, 1)
    text = text.replace(
        token_a,
        wire_usb_m.replace("185.42 67.31", "185.42 118.11").replace("198.12 67.31", "198.12 118.11"),
        1,
    )
    text = text.replace(
        token_b,
        wire_buzzer.replace("185.42 118.11", "185.42 67.31").replace("198.12 118.11", "198.12 67.31"),
        1,
    )

    # Remove the obsolete GPIO20 VCC_SPI wire, then move USB_P to GPIO20.
    text = text.replace(wire_vcc_spi, "", 1)
    text = text.replace(
        wire_usb_p,
        wire_usb_p.replace("185.42 64.77", "185.42 120.65").replace("198.12 64.77", "198.12 120.65"),
        1,
    )

    # Hard postconditions: do not write a half-patched schematic.
    for marker in target_markers:
        if marker not in text:
            raise RuntimeError(f"postcondition missing: {marker}")
    for marker in obsolete_markers:
        if marker in text:
            raise RuntimeError(f"postcondition still obsolete: {marker}")

    if text.count("(xy 185.42 118.11) (xy 198.12 118.11)") != 1:
        raise RuntimeError("GPIO19 wire count is not exactly one")
    if text.count("(xy 185.42 120.65) (xy 198.12 120.65)") != 1:
        raise RuntimeError("GPIO20 wire count is not exactly one")
    if text.count("(xy 185.42 67.31) (xy 198.12 67.31)") != 1:
        raise RuntimeError("GPIO38 wire count is not exactly one")
    if "(xy 185.42 64.77) (xy 198.12 64.77)" in text:
        raise RuntimeError("GPIO45 USB wire still present")

    PATH.write_text(text, encoding="utf-8")
    print("Applied Rev A native USB patch to mcu.kicad_sch")


if __name__ == "__main__":
    main()
