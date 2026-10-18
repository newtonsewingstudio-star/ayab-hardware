# KH910 Rev A — bench verification gates (fabrication commit ae8f7eb)

## Current firmware capabilities
This is a **communications-only, output-disabled** firmware prototype. It responds to AYAB API v6 `reqInfo` (0x03) with `cnfInfo` (0xC3). It explicitly REJECTS `reqInit`, `reqStart`, and `reqTest` with nonzero errors. It must NOT be used to knit. Its presence on USB is **not** evidence that solenoids or encoders work.

## Gate A: unpowered checks
1. Inspect USB-C connector, ESP32-S3 solder joints, regulator area and orientation.
2. Check shorts between GND/3V3, GND/5V, and machine-power rails with a DMM.
3. Confirm the actual module suffix and installed components match the BOM.
4. Use the fabrication commit's netlist to resolve whether USB VBUS feeds only the USB interface or the board's regulators. **Do not assume USB-only power is supported.**

## Gate B: USB communications only
1. With machine interface DISCONNECTED, provide a current-limited power source ONLY after Gate A is passed and the correct board voltage and current limit are validated.
2. Connect USB-C to Windows; inspect enumerated COM port / USB identifiers.
3. Flash the firmware using PlatformIO only after bootloader and USB pin routing are verified.
4. Run `python tests/probe_usb.py --help` to inspect command arguments; run info-only probe against the correct serial port.
5. Verify the device returns API v6 and the `bench-no-io` diagnostic suffix.
6. Send init/start/test requests only with outputs electrically isolated; confirm **nonzero** errors and that no outputs toggle.

## Gate C: simulated machinery (NOT IMPLEMENTED)
A bench harness must provide sensor signals at verified voltage levels. Never drive ESP32 GPIO from a 5V signal. Simulate encoders/Hall/EOL only after the final KiCad netlist and conditioning network are traced. Test selected outputs with appropriate current-limited fixtures, NOT actual solenoids first.

## Gate D: KH910 machine validation (NOT STARTED)
Only after the physical signals, timing, machine-power scheme, and driver safety are proven. Keep stock control board available for restoration.
