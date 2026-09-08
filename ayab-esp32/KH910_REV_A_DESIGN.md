# AYAB-ESP32 KH910 Rev A

Status: architecture redesign in progress. Do not fabricate from the current schematic. The authoritative I/O and power specifications are being defined before KiCad is rerouted.

## Project target

Create a production-capable modern replacement controller for Brother KH-910 machines using the upstream AYAB-ESP32 design as the baseline.

Primary validation target: Brother KH-910.

Compatibility with other electronic Brother machines should be retained where it does not compromise KH-910 correctness, safety, or serviceability.

The first intended installation is the donated KH-910; a second board may later be installed in the working KH-910. Initial manufacturing target remains approximately five assembled boards after Rev A passes fabrication review.

## Product direction

Rev A is no longer treated as a small patch set to the AYAB-ESP32 prototype. It is a complete hardware revision with controlled architecture documents.

The intended system now includes:

- ESP32-S3 controller;
- USB-C and Wi-Fi capability;
- machine/encoder/Hall inputs;
- KH-910-specific native K/L carriage inputs;
- MCP23017 + ULN2003A solenoid architecture;
- safe machine/solenoid power gating;
- service/test points;
- provision for a replacement front-panel display;
- provision to reuse the original KH-910 rubber keypad through a replacement contact PCB/front-panel interface;
- local diagnostics and eventual standalone operation in addition to AYAB host control.

The successful eKnitter architecture demonstrates that replacing the original KH-910 electronics while retaining the original physical controls and screen location is mechanically practical. Rev A will use that as architectural evidence, not as a design to copy.

## Controlled design documents

The following documents govern schematic work:

- `KH910_REV_A_IO_MAP.md` — authoritative signal and ESP32 pin architecture;
- `KH910_REV_A_POWER.md` — required power domains, source isolation, solenoid fail-safe behavior and state table;
- this document — project-level requirements and fabrication gate.

A later mechanical/front-panel document will define keypad contact geometry, display aperture and mounting only after existing documentation has been exhausted. Physical measurements from the prototype machine will be requested only for unresolved dimensions.

## Baseline retained from AYAB-ESP32

- MCU module: ESP32-S3-MINI-1-N4R2, subject to final module-pin restriction audit;
- USB-C form/function, but native USB routing must be corrected/audited;
- MCP23017 solenoid I/O expansion;
- ULN2003A solenoid drivers;
- Brother connector architecture/Hirose compatibility;
- existing KiCad/JLCPCB manufacturing pipeline;
- factory-assembled SMD preference.

## Confirmed issues and redesign requirements

### 1. KH-910 right Hall / carriage inputs

The KH-910 exposes two digital open-collector comparator outputs for the right-side carriage detector. They are not electrically or semantically equivalent to the analog-right-Hall comparator network currently on AYAB-ESP32.

Do not OR the two KH-910 outputs together. Separate K/L information is required to distinguish carriage behavior.

Rev A direction:

- remove the LM393-derived signals from the KH-910 K/L path;
- give the two KH-910 right-side digital outputs dedicated ESP32 GPIO inputs;
- provide external 10 kOhm pull-ups to 3.3 V;
- preserve native polarity and interpret it in firmware;
- route analog Hall signals used by other Brother models directly to ADC-capable ESP32 inputs through passive scaling rather than active comparator normalization;
- add labeled K/L and analog Hall test points.

### 2. MCU pin-map drift / native USB audit

The current KiCad MCU sheet and experimental ESP32 firmware do not form a reliable single source of truth.

Rev A must reconcile every MCU signal against `KH910_REV_A_IO_MAP.md`.

Native ESP32-S3 USB must use GPIO19 for D- and GPIO20 for D+. Any existing schematic assignment that conflicts with this is a fabrication blocker.

### 3. 3.3 V regulator metadata

The 3.3 V rail metadata has now been corrected to `XL1509-3.3E1`, LCSC C74193 in the working branch.

This correction remains subject to final BOM/footprint/rating verification.

### 4. USB-only backfeed

Upstream bring-up documented the nominal machine/12 V rail sitting at several volts when only USB is connected, caused by an unintended reverse/backfeed path.

Rev A requirements are defined in `KH910_REV_A_POWER.md`:

- USB-only service/programming must leave machine/solenoid power effectively at 0 V;
- USB and machine-derived logic sources must not backfeed each other;
- a hardware-default-OFF solenoid power gate is required;
- machine-power presence should be sensed by the MCU;
- reset, bootloader, watchdog and brownout must all force the solenoid domain OFF.

### 5. Front-panel replacement console

Rev A should support a finished KH-910 replacement-console architecture rather than remaining a headless internal adapter.

Preferred direction:

- reuse the original KH-910 rubber keypad and external button legends;
- reproduce switch contact geometry on a replacement front-panel PCB;
- connect the keypad through an I2C expander/controller rather than consuming many ESP32 GPIOs;
- use the already planned display bus for a modern graphic display;
- support local status, row count, carriage diagnostics, sensor diagnostics, network information, errors and service/test modes;
- keep physical display choice and geometry unfrozen until the existing KH-910/eKnitter documentation has been fully mined.

### 6. Connector/serviceability/manufacturing

- preserve KH-910 Hirose compatibility;
- keep pin-1 markings obvious;
- keep reference designators visible where practical;
- add/retain test points for 12 V, 5 V, 3.3 V, USB VBUS, GND, encoder A/B/C, analog Hall inputs, KH-910 K/L and solenoid power;
- prefer factory-assembled SMD parts;
- avoid unnecessary manual soldering;
- account for known enclosure/USB-placement problems on other Brother models rather than assuming the upstream board outline/USB connector is universally correct.

## Fail-safe requirements

The following are mandatory before fabrication:

- all solenoids OFF during ESP32 reset/boot;
- all solenoids OFF while MCP23017 is uninitialized/reset;
- all solenoids OFF after watchdog or firmware crash;
- machine/solenoid power gate has a passive hardware OFF state;
- machine-facing inputs cannot materially backfeed an unpowered machine;
- connector transients/ESD are reviewed;
- logic and high-current return paths are reviewed so solenoid pulses do not destabilize the MCU.

## Items not being changed without evidence

- ESP32-S3 family/module concept;
- MCP23017 architecture;
- ULN2003A topology;
- USB-C as the service/data connector;
- ability to use I2C/SPI expansion;
- core AYAB compatibility.

A touchscreen, SD card, different MCU family or other feature expansion should not be added unless it solves a demonstrated requirement.

## Firmware strategy

Hardware correctness takes precedence over compatibility with the current mature AVR firmware.

The experimental upstream ESP32 branch remains useful as evidence of intended GPIO assignments and architecture, but it is not authoritative where it conflicts with the hardware or ESP32-S3 requirements.

Bring-up firmware should begin before full AYAB feature work and provide:

- USB communications;
- MCP23017 enumeration;
- safe all-solenoids-off initialization;
- individual solenoid test with hardware gate control;
- encoder A/B/C live diagnostics;
- KH-910 K/L live diagnostics;
- analog Hall ADC display;
- machine-power sense;
- front-panel key and display test once hardware exists.

Full knitting state-machine compatibility follows hardware bring-up.

## Manufacturing strategy

Use the AYAB KiCad/JLCPCB pipeline after Rev A schematic/layout work is complete.

The standard design-check workflow must be run explicitly on the Rev A branch or changed so branch pushes invoke it; current workflow triggers are not sufficient evidence by themselves.

Before ordering:

- export Gerbers;
- export BOM/CPL;
- verify JLC/LCSC availability and substitutions;
- inspect all generated layers visually;
- verify connector orientation and mechanical clearances;
- archive a reproducible manufacturing package.

## Fabrication gate

Do not order boards until all of the following are complete:

- I/O map frozen and reconciled to KiCad;
- complete MCU pin audit finished;
- native USB routed correctly to GPIO19/20;
- KH-910 K/L inputs electrically separated from LM393 circuitry;
- analog Hall paths implemented as ADC inputs with passive scaling;
- power architecture/state table implemented;
- USB-only backfeed eliminated;
- hardware-default-OFF solenoid gate implemented;
- machine-power sense implemented;
- reset/boot/fault solenoid behavior reviewed;
- front-panel electrical interface reserved/implemented as appropriate for Rev A;
- connector orientation checked;
- all required test points present;
- ERC/DRC clean or deviations documented;
- BOM/CPL generated and reviewed;
- fabrication outputs visually reviewed;
- prototype bring-up checklist prepared.

## Source branch

Working branch: `ayab-esp32-kh910-rev-a`
