# AYAB ESP32-S3 KH910 Rev A firmware

This firmware work targets the fabricated AYAB KH910 Rev A hardware design at commit `ae8f7eb` (not an upstream generic board). The working development snapshot is Stage 5, containing USB/AYAB API v6 protocol groundwork, safe command rejection, host-side knitting session simulation, schematic-derived GPIO maps, input and I2C scaffolds, and tests.

**Safety:** This is experimental code. Machine-facing outputs are intentionally disabled. ESP32-S3 target compilation, complete cross-sheet circuit mapping, and physical bench validation are not yet verified. Do not connect to a powered knitting machine or enable solenoids based solely on this snapshot.

Firmware development is isolated on branch `firmware-esp32-kh910-reva-stage5` to preserve the fabrication revision.
