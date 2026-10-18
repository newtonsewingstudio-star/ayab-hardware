# AYAB ESP32-S3 KH910 Rev A - Stage 2 (USB-only)

Fabrication source: [Newton Sewing Studio hardware commit ae8f7eb](https://github.com/newtonsewingstudio-star/ayab-hardware/tree/ae8f7eb/ayab-esp32).

**NOT READY TO CONTROL A KNITTING MACHINE.** No GPIO or solenoid controls are implemented.

## Implemented

- Native USB CDC transport using Arduino ESP32-S3 (PlatformIO configuration, unbuilt in this environment).
- Bounded SLIP packet decoder and transmitter.
- Exact AYAB API v6 `reqInfo` (0x03) to 22-byte `cnfInfo` (0xC3) response layout.
- Dallas/Maxim CRC8 algorithm factored for later implementation.
- No success acknowledgments for machine initialization/start/test commands.
- Native host compilation unit test for framing, invalid escapes, overflow recovery, info packet.
- Python unit tests and a read-only USB probe from Stage 1.

## Build locally

Install VS Code + PlatformIO, open this project, build `esp32s3_usb`. Hardware not required for a build. PlatformIO package downloads are unavailable in this build environment, so a complete ESP32 build has **not** been claimed.

Native smoke test: `g++ -std=c++17 -Wall -Wextra -Werror tests/test_native.cpp -o /tmp/ayab_test && /tmp/ayab_test`
Python: `python -m pytest -q tests`

## Next gating tasks

Use KiCad 8 or later to generate netlist from the exact 7-sheet design at `ae8f7eb`, derive actual MCU GPIO/pad-to-net map and MCP23017 output mapping, then compare against soldered board with continuity measurements before enabling any machine outputs. The next full MCU build also needs to confirm the board profile's flash layout and USB CDC configuration.

## Attribution

Adapted from upstream AYAB GPL-3.0-or-later protocol definitions. Licensing preserved.

## Stage 3 changes
Read-only AYAB USB identification plus fail-closed explicit error responses for `reqInit`, `reqStart`, `reqTest`. A new native regression test verifies every rejected control command returns a non-success code; see `BENCH_TEST_PLAN.md`. **No machine I/O implemented. No ESP32 hardware build or flash demonstrated.**

## Stage 3 changes
Read-only AYAB USB identification plus fail-closed explicit error responses for `reqInit`, `reqStart`, `reqTest`. A new native regression test verifies every rejected control command returns a non-success code; see `BENCH_TEST_PLAN.md`. **No machine I/O implemented. No ESP32 hardware build or flash demonstrated.**

## Stage 4: isolated simulated knitting session

`src/bench_session.h` provides a deterministic, host-testable session model with
25-byte row buffers, monotonic line sequence checks, and simulated carriage
passes. This is **not** a port of the live AYAB knitter; it uses a deliberately
synthetic machine ID (`0x91`) and is NOT wired into the USB handler or any GPIO.
It supports validating data-flow behavior while the exact machine enum, sensor
timing, and schematic-derived GPIO map are verified. No live knitting capability
is claimed. Run `pytest -q tests` or build the C++ test with `g++`.
