#!/usr/bin/env python3
"""Audit the AYAB-ESP32 MCU sheet against the KH910 Rev A pin architecture.

KiCad library-symbol coordinates use a mathematical Y axis, while schematic sheet
coordinates increase downward. The symbol-local Y coordinate therefore has to be
inverted when converting an unrotated library pin to a sheet coordinate.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMATIC = ROOT / "mcu.kicad_sch"
REPORT = ROOT / "KH910_REV_A_CURRENT_PIN_AUDIT.md"

TARGET = {
    1: "HALL_L_ADC",
    2: "HALL_R_ADC",
    3: "RESERVED_STRAP",
    4: "MACHINE_PWR_SENSE",
    5: "ENC_A",
    6: "ENC_B",
    7: "ENC_C",
    8: "I2C0_SDA",
    9: "I2C0_SCL",
    10: "DISPLAY_CS",
    11: "SPI0_CIPO",
    12: "SPI0_COPI",
    13: "SPI0_SCK",
    14: "FRONT_PANEL_AUX",
    15: "I2C1_SDA",
    16: "I2C1_SCL",
    17: "KH910_R_K",
    18: "KH910_R_L",
    19: "USB_M",
    20: "USB_P",
    21: "SOLENOID_PWR_EN",
    33: "LED_R",
    34: "LED_G",
    35: "LED_B",
    36: "USER_BUTTON",
    38: "BUZZER",
    39: "PANEL_INT",
    40: "SPARE",
    41: "SPARE",
    42: "SPARE",
    43: "UART_TX",
    44: "UART_RX",
    45: "RESERVED_STRAP",
    46: "RESERVED_STRAP",
    47: "SPARE",
    48: "SPARE",
}

ALIASES = {
    "ENC_C": {"ENC_BP", "ENC_BELTPHASE"},
    "BUZZER": {"PIEZO", "BUZZER"},
    "LED_R": {"RED"},
    "LED_G": {"GRN"},
    "LED_B": {"YEL"},
}

IGNORE_LABEL = re.compile(r"ESP\d+$")


def extract_block(text: str, start: int) -> str:
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
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    raise RuntimeError("Unbalanced KiCad block")


def pt(x: float, y: float) -> tuple[float, float]:
    return (round(x, 4), round(y, 4))


def transform(cx: float, cy: float, x: float, y: float, rot: int) -> tuple[float, float]:
    """Convert library-symbol pin coordinates to KiCad schematic coordinates."""
    # First convert the library's Y-up coordinate system to sheet Y-down.
    y = -y
    rot %= 360
    if rot == 0:
        return pt(cx + x, cy + y)
    if rot == 90:
        return pt(cx - y, cy + x)
    if rot == 180:
        return pt(cx - x, cy - y)
    if rot == 270:
        return pt(cx + y, cy - x)
    raise RuntimeError(f"Unsupported symbol rotation: {rot}")


def on_segment(p, a, b, eps=1e-4):
    px, py = p
    ax, ay = a
    bx, by = b
    cross = (px - ax) * (by - ay) - (py - ay) * (bx - ax)
    if abs(cross) > eps:
        return False
    return (
        min(ax, bx) - eps <= px <= max(ax, bx) + eps
        and min(ay, by) - eps <= py <= max(ay, by) + eps
    )


class DSU:
    def __init__(self, items):
        self.parent = {x: x for x in items}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def main() -> None:
    text = SCHEMATIC.read_text(encoding="utf-8")

    lib_start = text.find('(symbol "ayab-lib:ESP32-S3-MINI-1"')
    if lib_start < 0:
        raise RuntimeError("ESP32-S3-MINI-1 library symbol not found")
    lib = extract_block(text, lib_start)

    inst = re.search(
        r'\(symbol\s+\(lib_id\s+"ayab-lib:ESP32-S3-MINI-1"\)\s+'
        r'\(at\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\)',
        text,
        re.S,
    )
    if not inst:
        raise RuntimeError("ESP32-S3-MINI-1 instance not found")
    cx, cy = float(inst.group(1)), float(inst.group(2))
    rotation = int(float(inst.group(3)))

    gpio_pins = {}
    cursor = 0
    while True:
        m = re.search(r"\(pin\s", lib[cursor:])
        if not m:
            break
        start = cursor + m.start()
        block = extract_block(lib, start)
        cursor = start + len(block)
        at = re.search(r"\(at\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\)", block)
        name = re.search(r'\(name\s+"([^"]+)"', block)
        number = re.search(r'\(number\s+"([^"]+)"', block)
        if not (at and name and number):
            continue
        gpio = re.search(r"GPIO(\d+)", name.group(1))
        if not gpio:
            continue
        g = int(gpio.group(1))
        gpio_pins[g] = {
            "point": transform(cx, cy, float(at.group(1)), float(at.group(2)), rotation),
            "module_pin": number.group(1),
            "symbol_name": name.group(1),
        }

    # Hard sanity anchors from the ESP32-S3-MINI symbol currently instantiated on
    # this sheet. These make an axis/rotation regression fail loudly instead of
    # producing a plausible but inverted pin map.
    expected_points = {
        19: (185.42, 67.31),   # native USB D-
        20: (185.42, 64.77),   # native USB D+
        38: (185.42, 118.11),  # buzzer row in the upstream design
        45: (185.42, 120.65),  # strapping GPIO45 / VCC_SPI row
    }
    for gpio, expected in expected_points.items():
        actual = gpio_pins[gpio]["point"]
        if actual != expected:
            raise RuntimeError(
                f"coordinate sanity failure for GPIO{gpio}: expected {expected}, got {actual}"
            )

    wires = []
    for m in re.finditer(
        r"\(wire\s+\(pts\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s+"
        r"\(xy\s+([-\d.]+)\s+([-\d.]+)\)\)",
        text,
        re.S,
    ):
        wires.append((pt(float(m.group(1)), float(m.group(2))), pt(float(m.group(3)), float(m.group(4)))))

    labels = []
    for kind, pattern in (
        ("hierarchical", r'\(hierarchical_label\s+"([^"]+)".*?\(at\s+([-\d.]+)\s+([-\d.]+)\s+[-\d.]+\)'),
        ("global", r'\(global_label\s+"([^"]+)".*?\(at\s+([-\d.]+)\s+([-\d.]+)\s+[-\d.]+\)'),
        ("local", r'\(label\s+"([^"]+)"\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+[-\d.]+\)'),
    ):
        for m in re.finditer(pattern, text, re.S):
            labels.append((m.group(1), pt(float(m.group(2)), float(m.group(3))), kind))

    semantic_points = set()
    connection_points = set()
    for a, b in wires:
        semantic_points.update((a, b))
    for _, p, _ in labels:
        semantic_points.add(p)
        connection_points.add(p)
    for info in gpio_pins.values():
        semantic_points.add(info["point"])
        connection_points.add(info["point"])
    junctions = {
        pt(float(x), float(y))
        for x, y in re.findall(r"\(junction\s+\(at\s+([-\d.]+)\s+([-\d.]+)\)", text)
    }
    semantic_points.update(junctions)
    connection_points.update(junctions)

    dsu = DSU(semantic_points)
    for a, b in wires:
        # A pure geometric crossing is not a KiCad connection.  Join the wire's
        # own endpoints plus explicit semantic points (pins, labels, junctions).
        on = [p for p in ({a, b} | connection_points) if on_segment(p, a, b)]
        if on:
            for p in on[1:]:
                dsu.union(on[0], p)

    labels_by_root = {}
    for name, p, kind in labels:
        labels_by_root.setdefault(dsu.find(p), []).append((name, kind))

    rows = []
    mismatch = 0
    for gpio in sorted(gpio_pins):
        info = gpio_pins[gpio]
        attached = labels_by_root.get(dsu.find(info["point"]), [])
        names = sorted({name for name, _ in attached if not IGNORE_LABEL.fullmatch(name)})
        target = TARGET.get(gpio, "—")
        if target in {"SPARE", "RESERVED_STRAP", "—"}:
            status = "review" if names else "open"
        else:
            acceptable = {target} | ALIASES.get(target, set())
            status = "OK" if acceptable.intersection(names) else "MISMATCH"
            if status == "MISMATCH":
                mismatch += 1
        rows.append((gpio, info["module_pin"], info["symbol_name"], info["point"], names, target, status))

    usb19 = next(r for r in rows if r[0] == 19)
    usb20 = next(r for r in rows if r[0] == 20)

    out = [
        "# AYAB-ESP32 KH910 Rev A — Current MCU Pin Audit",
        "",
        "Generated automatically from `mcu.kicad_sch` by `tools/audit_esp32_pinmap.py`.",
        "",
        "This report describes the **current electrical connectivity**, not the desired Rev A design. The target column comes from `KH910_REV_A_IO_MAP.md`.",
        "",
        f"- ESP32 instance origin: `{cx}, {cy}`, rotation `{rotation}`",
        f"- GPIOs extracted: **{len(gpio_pins)}**",
        f"- Target-function mismatches: **{mismatch}**",
        f"- Native USB GPIO19 current labels: `{', '.join(usb19[4]) or '(none)'}`",
        f"- Native USB GPIO20 current labels: `{', '.join(usb20[4]) or '(none)'}`",
        "",
        "| GPIO | Sheet coordinate | Module pin | ESP32 symbol function | Current attached net/label(s) | Rev A target | Status |",
        "|---:|---|---:|---|---|---|---|",
    ]
    for gpio, module_pin, symbol_name, point, names, target, status in rows:
        current = ", ".join(f"`{x}`" for x in names) if names else "—"
        out.append(
            f"| {gpio} | `{point[0]}, {point[1]}` | {module_pin} | `{symbol_name}` | {current} | `{target}` | **{status}** |"
        )

    out.extend([
        "",
        "## Interpretation rules",
        "",
        "- **OK** means the current named net matches the Rev A target or an explicit compatibility alias.",
        "- **MISMATCH** means the GPIO is occupied by a different function or the expected function is absent.",
        "- **review** means a pin intended to be spare/reserved is currently labeled and must be examined before reuse.",
        "- **open** means a spare/reserved pin has no meaningful label on the MCU sheet.",
        "",
        "## Fabrication rule",
        "",
        "Do not fabricate while any critical target (USB, encoder, KH-910 K/L, Hall ADC, power enable, internal I2C) remains `MISMATCH`.",
        "",
    ])

    REPORT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
