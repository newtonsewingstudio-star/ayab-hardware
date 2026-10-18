# Stage 5 validation

- MCU net mapping: extracted from exact fabrication schematic commit ae8f7eb.
- Input-only and read-only I2C driver scaffolds: implemented, **not activated** in firmware main loop.
- MCP23017 writes and solenoid outputs: **not implemented**, pending full root/solenoid cross-sheet verification.
- ESP32-S3 target build: **NOT COMPILED**. This environment has neither PlatformIO nor its Espressif toolchain and cannot fetch packages. `platformio.ini` is supplied for later reproducible build.
- Native C++ tests: run locally; these do not replace firmware target build or electronics testing.

To compile on a networked development machine with PlatformIO: `pio run -e esp32s3_usb`. Do not flash to a machine-connected board until power and signals are electrically verified.