# AYAB-ESP32 KH910 Rev A

Status: design review complete enough to begin schematic/layout revision. Do not fabricate upstream `main` unchanged.

## Project target

Create a modern AYAB controller for Brother KH-910 machines using the upstream AYAB-ESP32 design as the baseline. Hardware should be forward-looking even if firmware support follows later. The first intended installation is the donated KH-910; a second board may later be installed in the working KH-910.

## Baseline

- Upstream project: `AllYarnsAreBeautiful/ayab-hardware`, `ayab-esp32`
- MCU module: ESP32-S3-MINI-1-N4R2
- USB-C retained
- MCP23017 solenoid I/O expansion retained
- ULN2003A solenoid drivers retained
- Existing AYAB JLCPCB output workflow retained

## Confirmed issues to address

### 1. KH-910 right Hall / carriage inputs

The KH-910 exposes two digital open-collector comparator outputs for the right-side carriage detector. They are not electrically/semantically equivalent to the analog-right-Hall comparator network currently on AYAB-ESP32.

Do not OR the two KH-910 outputs together. Separate K/L information is required to distinguish carriage types.

Rev A direction:

- Remove/bypass the LM393-generated right-side K/L outputs from the KH-910 path.
- Give the two KH-910 right-side digital outputs dedicated ESP32 GPIO inputs.
- Provide 10 kOhm pull-ups to 3.3 V on these open-collector inputs.
- Preserve native polarity and handle interpretation in firmware.
- Keep support for analog Hall sensing used by other Brother models by routing analog Hall signals to ADC-capable ESP32 pins through appropriate 5 V to 3.3 V scaling.

Rationale: AYAB contributors measured the KH-910 uPC339 outputs as open collector and experimentally demonstrated a 10 kOhm pull-up with very large timing margin.

### 2. 3.3 V regulator BOM error

Upstream `psu.kicad_sch` still identifies U602 with `XL1509-5.0E1` metadata despite U602 being the 3.3 V rail. Rev A must use the correct 3.3 V regulator/part metadata and verify the PCB footprint/BOM mapping.

### 3. USB-only backfeed

Upstream bring-up documented the nominal machine/12 V rail sitting at approximately 4 V when only USB is connected, attributed to the XL1509 protection-diode path.

Rev A requirement:

- USB-only connection must be safe for programming/debugging.
- Solenoid/machine supply must not be unintentionally partially energized by USB power.
- Add or alter isolation/power-path circuitry if necessary after schematic review.

### 4. Connector/serviceability considerations

- Preserve KH-910 Hirose compatibility.
- Keep pin-1 markings obvious.
- Keep reference designators visible after assembly where practical.
- Add/retain useful test points for 3.3 V, 5 V, machine supply, GND, encoder A/B/C, left Hall, right K, and right L.
- Prefer factory-assembled SMD parts; minimize required manual soldering.

## Items explicitly *not* being changed without evidence

- ESP32-S3-MINI-1 module selection.
- MCU pin map solely because of the previously reported bare-ESP32-vs-module pin-number confusion.
- ULN2003A driver topology.
- MCP23017 architecture.
- USB-C interface.
- Expansion capability (I2C/Qwiic and available GPIO).

## Firmware strategy

Hardware correctness takes precedence over compatibility with the current mature AVR firmware. There is an experimental upstream `ayab-esp32` firmware branch and ESP32-S3 pin definitions already exist. Firmware will be brought forward after Rev A hardware is stable.

Firmware must eventually:

- support KH-910 digital K/L right-sensor inputs;
- preserve machine-specific polarity/logic;
- use edge-based carriage/position handling consistent with later AYAB encoder work;
- support USB first, with Wi-Fi/web operation as a later software feature.

## Manufacturing strategy

Use the existing AYAB KiCad/JLCPCB pipeline after Rev A is complete. The upstream repository already contains scripts to produce JLC-formatted BOM and CPL files and a workflow to export Gerbers/assembly outputs.

Initial target quantity: 5 assembled boards, subject to final JLCPCB component/assembly pricing.

## Fabrication gate

Do not order boards until all of the following are complete:

- schematic changes implemented;
- PCB rerouted as required;
- ERC/DRC clean or deviations documented;
- correct regulator verified in BOM;
- KH-910 K/L inputs electrically isolated from LM393 outputs;
- USB-only backfeed resolved;
- connector orientation checked;
- JLC BOM/CPL generated and component availability reviewed;
- fabrication outputs visually reviewed.

## Source branch

Working branch: `ayab-esp32-kh910-rev-a`
