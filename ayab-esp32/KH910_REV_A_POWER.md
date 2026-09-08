# AYAB-ESP32 KH910 Rev A — Power-Domain Architecture

Status: architecture draft. This document defines required power behavior before schematic rerouting. Do not fabricate until the implemented schematic satisfies these states and the USB backfeed path is removed.

## Goals

Rev A must support safe logic bring-up over USB without energizing the knitting machine power domain, while retaining compatibility with the Brother KH-910 installation and allowing a future external 12 V source if desired.

The design must be predictable in every connection order:

- machine power only;
- USB only;
- machine power + USB;
- hot-plug USB into an already powered machine;
- remove USB while machine remains powered;
- apply/remove machine power while USB remains attached;
- MCU reset, brownout, bootloader and firmware crash.

## Existing architecture observations

The current PSU sheet generates 12 V, 5 V and 3.3 V rails and now has corrected metadata for the 3.3 V XL1509 regulator. Upstream bring-up has also documented USB-only backfeed that raises the nominal machine/12 V domain to several volts. That behavior is unacceptable for Rev A.

The current USB sheet includes active power-path components, but Rev A will treat the existing circuit as a prototype to be revalidated rather than presumed correct.

## Required power domains

### Domain A — USB / service logic power

Purpose:

- ESP32-S3 programming and diagnostics;
- USB serial/native USB;
- optionally low-power front-panel/display diagnostics;
- no solenoid or machine-load energization.

Nominal source: USB-C VBUS 5 V.

Allowed loads under USB-only:

- ESP32-S3;
- essential 3.3 V logic;
- USB interface/protection;
- front-panel interface if current budget permits;
- diagnostic LEDs at conservative current.

Forbidden under USB-only:

- 12 V machine rail energization;
- solenoid supply energization;
- any meaningful phantom voltage on Brother machine-power connector pins;
- any half-powered peripheral whose inputs could source the machine through protection diodes.

### Domain B — Machine logic power

Purpose:

- normal standalone controller operation when the knitting machine/external supply is powered;
- 5 V and 3.3 V rails derived from the machine supply as appropriate.

Source candidates:

1. original Brother KH-910 supply input;
2. optional external regulated 12 V DC input.

Rev A may support both, but they must not be hard-paralleled without explicit ORing/protection.

### Domain C — Solenoid / high-current machine power

Purpose:

- knitting-machine solenoid drive only.

Source: machine/external 12 V domain after protection.

Requirements:

- physically/electrically absent when only USB is present;
- hardware-disabled until explicitly enabled;
- defaults OFF through reset/boot/crash;
- cannot be enabled by an unpowered or undefined GPIO state.

## Proposed architecture

### 1. Separate logic-source ORing from machine-power switching

Use a proper power mux / ideal-diode ORing arrangement for the low-voltage logic rail so the controller can run from either:

- USB 5 V; or
- machine-derived 5 V.

The exact component remains to be selected after current estimates and JLC availability review.

Requirements:

- no reverse current from USB logic supply into machine-derived 5 V;
- no reverse current from machine-derived 5 V into the USB host VBUS;
- no dependence on a buck regulator's internal/protection diode for isolation;
- graceful source handover where possible.

### 2. Machine 12 V must never be derived from USB

There must be no conductive path capable of lifting the machine 12 V net when USB is the only source.

This includes indirect paths through:

- regulator catch/protection diodes;
- MOSFET body diodes;
- ESD clamps;
- GPIO protection structures;
- powered logic driving unpowered machine-side circuits;
- pull-ups to a powered logic rail on a machine-side signal that can backfeed another IC.

USB-only acceptance target: machine/solenoid power node should measure effectively 0 V except leakage-level values defined by the final circuit.

### 3. Add a hard solenoid-power gate

Rev A should add a high-side machine-power gate or equivalent hardware enable in the solenoid power path.

Proposed logical control: `SOLENOID_PWR_EN` from GPIO21.

Hardware requirements:

- default OFF with GPIO floating;
- OFF during reset and bootloader;
- OFF if ESP32 is unpowered;
- OFF if only USB is present;
- cannot turn on until valid machine power is sensed;
- appropriate gate/source pull resistor establishes the safe state independent of firmware.

A load-switch/high-side MOSFET solution is preferred over relying solely on ULN2003 input states.

### 4. Machine-power sense

Add a divided/protected machine-power sense signal to an ADC-capable input (proposed GPIO4).

Firmware uses this for:

- reporting whether 12 V machine power is present;
- refusing to enable solenoids if absent;
- diagnostics for undervoltage/brownout;
- distinguishing USB-service mode from machine-operating mode.

The hardware solenoid gate must still fail safe without firmware.

### 5. Optional external 12 V input

A future-proof Rev A may include an external 12 V DC input as an alternative to the original Brother supply.

If included:

- polarity must be clearly marked;
- reverse-polarity protection required;
- input transient protection required;
- connector current rating must exceed worst-case solenoid load;
- original-machine and external-source paths require explicit ORing or a mutually exclusive selection method;
- user must never be able to accidentally backfeed the original Brother supply from the external adapter.

If the final mechanical design makes a barrel jack undesirable, provide pads/header or a short board-mounted cable connector rather than forcing the connector into an inaccessible enclosure location.

## Protection requirements

### Machine/external 12 V input

Evaluate and implement as appropriate:

- fuse or resettable fuse sized from measured load;
- reverse-polarity protection;
- TVS clamp for machine-side transients;
- bulk capacitance near solenoid drivers;
- local ceramic decoupling;
- controlled return-current paths so solenoid pulses do not disturb ESP32 ground/reference.

### Logic rails

- verify 5 V regulator absolute maximum and thermal margin;
- verify corrected 3.3 V regulator and inductor/diode ratings;
- provide test points for 12 V, 5 V, 3.3 V, USB VBUS and GND;
- document expected voltage tolerance at each test point.

### External machine signals

All machine-facing inputs must be checked for backfeed when the controller is powered but machine electronics are not. Series resistors/dividers should prevent powered ESP32 pull-ups from sourcing unintended machine circuits.

This is especially important for KH-910 K/L open-collector inputs: the 3.3 V pull-ups must be verified against the exact machine comparator output topology under machine-off/USB-on conditions.

## Required power-state table

| State | USB | Machine 12 V | ESP32/logic | Display/panel | Solenoid rail | Solenoid enable allowed |
|---|---|---|---|---|---|---|
| Fully off | No | No | Off | Off | 0 V | No |
| USB service | Yes | No | On | Optional/on | 0 V | No |
| Machine only | No | Yes | On | On | 12 V available behind gate | Yes, after valid boot |
| USB + machine | Yes | Yes | On | On | 12 V available behind gate | Yes, after valid boot |
| ESP32 reset with machine power | either | Yes | resetting | undefined/limited | gate OFF | No |
| Firmware crash/watchdog | either | Yes | fault/reset | undefined | gate must return OFF | No |
| Brownout | either | marginal | protected/reset | may blank | gate OFF | No |

## Boot and fail-safe sequence

Required intended behavior:

1. Power source appears.
2. Logic rails stabilize.
3. Solenoid power gate remains OFF by passive hardware default.
4. ESP32 boots.
5. MCP23017 is initialized to all-safe outputs.
6. Encoder/Hall/K/L inputs are validated.
7. Machine-power ADC confirms valid 12 V range.
8. Firmware enters READY state.
9. Only then may firmware assert `SOLENOID_PWR_EN`.
10. Any reset/watchdog/brownout returns the gate to OFF.

## USB data and VBUS

Native ESP32-S3 USB data must use GPIO19 D- and GPIO20 D+.

USB VBUS may power the logic domain but must not be tied directly into machine-derived 5 V or any regulator output that permits reverse conduction.

CC configuration, ESD protection and USB differential routing remain required.

## Front-panel power

The replacement display/front panel should normally use the logic domain, not the solenoid/machine domain.

Design targets:

- front panel can show service diagnostics during USB-only operation;
- backlight current, if using a TFT/LCD, must fit within conservative USB current budget or be disabled/dimmed in USB-only mode;
- OLED is attractive partly because it avoids a separate high-current backlight path;
- keypad scanning must not energize machine electronics when machine power is absent.

## Verification measurements before fabrication release

Schematic/design review must be able to predict these measurements, and prototype bring-up must verify them:

### USB only

- USB VBUS: nominal 5 V;
- 3.3 V logic: nominal;
- machine 12 V node: approximately 0 V;
- gated solenoid node: approximately 0 V;
- no solenoid movement/noise;
- no unexpected voltage on machine power connector.

### Machine only

- 12 V rail: within expected machine range;
- 5 V and 3.3 V regulators stable;
- no voltage presented to disconnected USB VBUS;
- solenoid gate OFF until firmware deliberately enables it.

### USB + machine

- no source fighting;
- no abnormal current into USB host;
- stable logic during connect/disconnect of USB;
- machine rail unaffected by USB removal.

### Fault tests

- hold ESP32 in reset while machine powered -> solenoid gate remains OFF;
- force watchdog/reset -> gate turns OFF;
- unplug machine power while USB remains -> solenoid rail collapses, ESP32 remains alive in service mode;
- plug machine power back in -> no automatic solenoid activation before software revalidation.

## Fabrication blockers

Power design is not ready for fabrication until:

1. USB-only backfeed path is identified and eliminated;
2. logic-source ORing/power mux is implemented;
3. high-current solenoid gate is implemented with passive OFF default;
4. machine-power sense is implemented;
5. reverse-current behavior is reviewed for every machine-facing signal;
6. protection component ratings and JLC availability are checked;
7. the full state table above is satisfied by schematic inspection;
8. ERC/DRC is clean or exceptions are explicitly justified.
