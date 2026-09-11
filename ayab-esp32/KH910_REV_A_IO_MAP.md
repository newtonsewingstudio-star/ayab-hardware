# AYAB-ESP32 KH910 Rev A — I/O and Pin Architecture

Status: Rev A interface contract and design-intent map. The native KiCad schematic and PCB at the reviewed commit are authoritative for actual electrical connectivity and layout. `KH910_REV_A_CURRENT_PIN_AUDIT.md` is the generated reconciliation of this contract against the schematic. If these sources disagree, release is blocked until the KiCad source or this contract is corrected; this prose file never overrides the netlist.

Rows described as candidate, spare, or proposed reserve future interfaces and are not claims that the feature is populated. Implemented safety-critical assignments must be marked `OK` by the generated current-pin audit before prototype release.

## Why this document exists

The current AYAB-ESP32 hardware and the experimental ESP32 firmware must be reconciled explicitly before Rev A is fabricated. The firmware `board.h` intends encoder GPIO5/6/7, internal I2C GPIO8/9, display SPI GPIO10-13, external I2C GPIO15/16, UART GPIO43/44, piezo GPIO38, LEDs GPIO33-35 and user button GPIO36.

The current schematic also normalizes Hall/end-of-line signals through an LM393 network, while the KH-910 already provides distinct open-collector right-side K/L outputs. Upstream issue #43 documents that the board comparators can actively prevent the KH-910 outputs from being read correctly.

Rev A therefore freezes intent first, then changes KiCad to match.

## MCU audit finding and correction

A first automated audit incorrectly treated KiCad library-symbol Y coordinates as sheet coordinates and therefore reported the MCU pin map vertically inverted. KiCad's library symbols use a mathematical Y-up axis while schematic sheet coordinates increase downward. ERC exposed the error immediately: a test patch based on the inverted audit disconnected native USB D+.

That test patch was reverted. The corrected auditor now includes hard coordinate sanity anchors for GPIO19, GPIO20, GPIO38 and GPIO45 so the same transform error cannot silently recur.

The original AYAB-ESP32 schematic already routes native ESP32-S3 USB correctly:

- GPIO19 = USB D- / `USB_M`;
- GPIO20 = USB D+ / `USB_P`;
- GPIO38 = buzzer;
- GPIO45 = the existing `VCC_SPI` strapping-related net.

USB pin assignment is therefore **not** a Rev A schematic defect. USB power-path/backfeed behavior remains a separate Rev A defect to solve.

## Rev A ESP32-S3 allocation contract

| Function | Rev A GPIO | Electrical type | Notes |
|---|---:|---|---|
| Left analog Hall / EOL | GPIO1 | ADC1 input | 5 V tolerant only through passive divider/protection; no comparator normalization |
| Right analog Hall / EOL (non-KH910 machines) | GPIO2 | ADC1 input | Passive 5 V-to-3.3 V scaling; unused on KH-910 |
| Reserved / avoid external strap loading | GPIO3 | reserved | ESP32-S3 strapping pin; do not use for KH-910 pull-up input |
| Machine-power sense / spare ADC | GPIO4 | ADC1 input | Preferred for 12 V-present sensing through divider, subject to final power schematic |
| Encoder A | GPIO5 | digital input | Retain firmware intent |
| Encoder B | GPIO6 | digital input | Retain firmware intent |
| Encoder belt phase / C | GPIO7 | digital input | Retain firmware intent |
| Internal I2C SDA | GPIO8 | I2C | MCP23017 solenoid expander |
| Internal I2C SCL | GPIO9 | I2C | MCP23017 solenoid expander |
| Display SPI CS | GPIO10 | output | Retain firmware intent |
| Display SPI CIPO/MISO | GPIO11 | input | Retain firmware intent; may be unused by display |
| Display SPI COPI/MOSI | GPIO12 | output | Retain firmware intent |
| Display SPI SCK | GPIO13 | output | Retain firmware intent |
| Front-panel/display auxiliary | GPIO14 | digital I/O | Candidate D/C, reset, or panel interrupt; final assignment after display selection |
| External/front-panel I2C SDA | GPIO15 | I2C | Retain external I2C intent |
| External/front-panel I2C SCL | GPIO16 | I2C | Retain external I2C intent |
| KH-910 right K | GPIO17 | digital input | Dedicated open-collector input, external 10 kOhm pull-up to 3.3 V |
| KH-910 right L | GPIO18 | digital input | Dedicated open-collector input, external 10 kOhm pull-up to 3.3 V |
| USB D- | GPIO19 | USB | Native ESP32-S3 USB; already correct in baseline schematic |
| USB D+ | GPIO20 | USB | Native ESP32-S3 USB; already correct in baseline schematic |
| Solenoid power enable | GPIO21 | output | Proposed hard machine/solenoid-domain enable; default hardware OFF |
| RGB/status LED R | GPIO33 | output | Available on ESP32-S3-MINI-1-N4R2; retain firmware intent |
| RGB/status LED G | GPIO34 | output | Available on ESP32-S3-MINI-1-N4R2; retain firmware intent |
| RGB/status LED B | GPIO35 | output | Available on ESP32-S3-MINI-1-N4R2; retain firmware intent |
| User/service button | GPIO36 | input | Available on ESP32-S3-MINI-1-N4R2; retain firmware intent |
| Piezo/buzzer | GPIO38 | output | Retain firmware intent; already correct in baseline schematic |
| Front-panel interrupt / spare | GPIO39 | input | Candidate keypad-expander interrupt; JTAG overlap must be documented |
| Spare | GPIO40 | I/O | JTAG overlap; available after JTAG policy is defined |
| Spare | GPIO41 | I/O | JTAG overlap; available after JTAG policy is defined |
| Spare | GPIO42 | I/O | JTAG overlap; available after JTAG policy is defined |
| UART TX | GPIO43 | output | Retain firmware intent |
| UART RX | GPIO44 | input | Retain firmware intent |
| Reserved / avoid | GPIO45 | reserved | ESP32-S3 strapping pin; existing VCC_SPI strap behavior must be preserved/reviewed |
| Reserved / avoid | GPIO46 | reserved | ESP32-S3 strapping pin |
| Spare | GPIO47 | I/O | General-purpose if needed |
| Spare | GPIO48 | I/O | General-purpose if needed |

For the exact ESP32-S3-MINI-1-N4R2 configuration, GPIO33-37 remain available. GPIO26 is unavailable because it is used by the embedded PSRAM and must not be allocated by Rev A.

## KH-910 carriage / Hall architecture

### Right side — KH-910

The KH-910 exposes two separate digital open-collector outputs from its own comparator circuitry. They carry distinct carriage information and must remain separate.

Rev A requirements:

- `KH910_R_K` -> dedicated GPIO17.
- `KH910_R_L` -> dedicated GPIO18.
- Each input gets an external 10 kOhm pull-up to 3.3 V.
- No LM393 output may share either net.
- Preserve the native machine polarity; firmware interprets machine-specific meaning.
- Add labeled test points for K and L.
- Add modest input protection/series resistance if it does not distort edge timing.

Do not OR K and L together.

### Analog Hall machines

For machines that provide analog Hall/EOL outputs, use ADC-capable GPIOs through passive scaling rather than converting them to synthetic digital polarities with LM393 comparators.

Proposed:

- left analog Hall -> GPIO1 / ADC1;
- right analog Hall -> GPIO2 / ADC1;
- passive resistor divider sized for a 5 V source and adequate ADC margin;
- optional small RC filtering and clamp/ESD protection after source-impedance review;
- firmware applies thresholds/hysteresis appropriate to machine type.

This lets one board support KH-910 digital K/L and analog-Hall Brother models without electrically mixing the two schemes.

## Encoder inputs

Retain the existing firmware intent:

- encoder A -> GPIO5;
- encoder B -> GPIO6;
- belt phase / encoder C -> GPIO7.

Rev A must verify source voltage, polarity, edge rate, pull-ups and protection from the Brother connector through to the ESP32 pins. Add test points A/B/C.

## Solenoid control

Retain MCP23017 + ULN2003A as the baseline architecture unless the detailed fail-safe review finds a reason to change it.

Requirements:

- all solenoid outputs OFF during ESP32 reset/boot;
- all solenoid outputs OFF if MCP23017 is unconfigured/reset;
- all solenoid outputs OFF if firmware crashes before enabling machine power;
- separate hardware `SOLENOID_PWR_EN` is proposed on GPIO21 so logic can boot from USB without energizing the machine power domain;
- individual solenoid test mode is required in bring-up firmware.

## Front panel / replacement console

Rev A should support reuse of the original KH-910 rubber keypad and replacement of the original display, following the successful architectural precedent demonstrated by eKnitter but with our own implementation.

Preferred electrical architecture:

- display on the already-reserved SPI bus GPIO10-13, or I2C if the selected module makes that clearly superior;
- original keypad contacts reproduced on a front-panel PCB;
- keypad read through an I2C GPIO expander/keypad controller rather than consuming a large number of ESP32 pins;
- front-panel bus on GPIO15/16;
- optional panel interrupt on GPIO39;
- original Brother button legends may be reassigned in firmware;
- exact display D/C, reset and backlight pins remain unfrozen until a physical display is selected.

Mechanical geometry is intentionally not guessed here. Existing documentation will be exhausted before requesting measurements from the prototype machine.

## USB

Rev A requirement is native ESP32-S3 USB-C:

- USB D- -> GPIO19 (already correct in baseline schematic);
- USB D+ -> GPIO20 (already correct in baseline schematic);
- appropriate USB-C CC resistors and ESD protection;
- controlled differential routing and minimal stubs;
- review/add series-resistor footprints according to Espressif hardware guidance if not already present;
- USB VBUS used only as a logic-power source/sense according to the power-domain document;
- USB must never partially energize the 12 V machine/solenoid domain.

## Firmware naming cleanup

Firmware and schematic must use one naming scheme. Proposed logical names:

- `HALL_L_ADC`
- `HALL_R_ADC`
- `KH910_R_K`
- `KH910_R_L`
- `ENC_A`
- `ENC_B`
- `ENC_C`
- `SOLENOID_PWR_EN`
- `MACHINE_PWR_SENSE`

Legacy `EOL_*_P`, `EOL_*_N`, `EOL_R_S` names should not survive merely because they exist in older prototypes. Compatibility aliases may exist in firmware temporarily, but KiCad should describe the actual electrical signals.

## Freeze gate

This map is not frozen until:

1. Brother connector pins are traced to each logical signal;
2. the corrected pin auditor agrees with the KiCad MCU sheet;
3. native USB GPIO19/20 is verified by ERC after every MCU-sheet change;
4. every MCU net in the schematic is mechanically compared against this table;
5. front-panel display interface is selected;
6. ERC passes with documented exceptions only.

Sources / design evidence:

- Upstream AYAB hardware issue #43 — KH-910 digital right Hall signals vs board comparators.
- Upstream experimental ESP32 firmware `src/ayab/board.h` — intended GPIO allocation.
- Espressif ESP32-S3 and ESP32-S3-MINI-1 documentation — native USB D-/D+ on GPIO19/GPIO20, strapping/JTAG restrictions, and N4R2 PSRAM pin use.
