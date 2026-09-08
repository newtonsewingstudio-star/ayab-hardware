# AYAB-ESP32 KH910 Rev A — Solenoid Fail-Safe Power Gate

Status: implementation architecture for Rev A. Do not fabricate until the KiCad implementation passes ERC/DRC and the prototype power-state tests in this document.

## Objective

The ESP32-S3 and controller logic must be allowed to boot from USB or machine power without making solenoid energization possible until firmware deliberately enables the machine output stage.

The existing MCP23017 + ULN2003A architecture remains the baseline. Rev A adds a separate high-side hardware gate in the solenoid +12 V feed.

## Selected topology

```
RAW +12V
   |
   | source
 LP9435LT1G P-MOSFET
   | drain
   +---- SOLENOID_12V_SW ---- Brother solenoid connector +12 V pins
   |                         + ULN2003A COM / flyback-clamp rail
   |
   +---- switched rail test point

P-MOS gate ---- 100 kOhm ---- RAW +12V       (default OFF)
     |
     +---- AO3400A drain
               source ---- GND
               gate  <---- 10 kOhm ---- SOLENOID_PWR_EN / GPIO21
                  |
                100 kOhm
                  |
                 GND
```

GPIO21 is active HIGH:

- GPIO21 low: AO3400A OFF, P-MOS gate pulled to its source, `SOLENOID_12V_SW` OFF.
- GPIO21 high: AO3400A ON, P-MOS gate pulled low, `SOLENOID_12V_SW` ON.
- GPIO21 floating/unpowered/reset: the 100 kOhm AO3400A gate pulldown holds the N-MOS OFF; the P-MOS source-to-gate pullup therefore keeps solenoid power OFF.

This is intentionally a hardware interlock rather than relying only on MCP23017 register state.

## Parts

### High-side switch

**LP9435LT1G**

- P-channel MOSFET
- SOT-23
- LCSC C383257
- VDS: -30 V
- ID: -5.3 A
- VGS absolute maximum: +/-20 V
- RDS(on) max: 70 mOhm at VGS=-10 V, ID=-5.3 A

The source is connected to RAW +12 V and drain to `SOLENOID_12V_SW`. This orientation keeps the intrinsic body diode from powering the switched rail from RAW +12 V while the MOSFET is OFF.

### Gate pull-down device

**AO3400A**

- N-channel MOSFET
- SOT-23
- existing AYAB BOM part / LCSC C20917
- VDS: 30 V
- logic-level gate operation

The AO3400A only sinks the P-MOS gate current and does not carry solenoid current.

### Passive defaults

- P-MOS source-to-gate pullup: 100 kOhm, 0603.
- GPIO21-to-AO3400A gate series resistor: 10 kOhm, 0603.
- AO3400A gate pulldown: 100 kOhm, 0603.

The source-to-gate pullup is the primary hardware OFF mechanism. The N-MOS gate pulldown prevents an unpowered/floating ESP32 pin from accidentally turning the power gate on.

## Current and thermal margin

Brother KH-910 service information specifies approximately 140–150 ohm per selector solenoid. At 12 V this is approximately 80–86 mA per energized coil.

A deliberately conservative 16-coil simultaneous case is therefore approximately 1.28–1.37 A. At 1.37 A and 70 mOhm worst-case RDS(on), the high-side MOSFET conduction loss is approximately 0.13 W and the voltage drop approximately 0.10 V.

Actual firmware should never treat simultaneous activation of every selector as a normal operating state; this calculation is only the hardware-switch sizing envelope.

## Rail partitioning

The following must remain RAW +12 V:

- machine input / supply sensing;
- machine-derived logic regulators;
- any circuitry whose operation is required before solenoid enable.

The following must move to `SOLENOID_12V_SW`:

- KH-910/KH-950 solenoid connector common +12 V;
- compatible Brother-model solenoid connector common +12 V rails;
- all ULN2003A COM/flyback-clamp connections associated with those solenoids.

The ULN2003 COM rail must follow the switched coil-positive rail. Leaving COM on RAW +12 V while the coils use a switched rail is not the intended Rev A topology.

## Required boot sequence

Firmware must use this ordering:

1. boot with GPIO21 low / high-impedance;
2. initialize internal I2C;
3. reset/configure MCP23017;
4. explicitly write every solenoid output OFF;
5. verify machine power is present through `MACHINE_PWR_SENSE`;
6. only then drive `SOLENOID_PWR_EN` high;
7. on any fatal error, brownout handling path, machine-power loss, or shutdown request, drive `SOLENOID_PWR_EN` low before other teardown where possible.

Hardware must remain safe even before firmware reaches step 1 because the passive gate network defaults OFF.

## Required power-state behavior

| State | Controller logic | RAW +12 V | SOLENOID_12V_SW | Requirement |
|---|---|---:|---:|---|
| USB only | ON | ~0 V | ~0 V | solenoids physically unpowered |
| machine power, ESP reset | starting | 12 V | ~0 V | OFF by passive hardware |
| machine power, firmware booting | ON | 12 V | ~0 V | OFF until deliberate enable |
| machine power, ready + enable | ON | 12 V | ~12 V | normal operation |
| firmware crash with GPIO released | may be stalled | 12 V | returns OFF | hardware default |
| brownout/reset | unstable/resetting | falling/present | OFF | no unintended pulse |
| USB + machine | ON | 12 V | only ON after enable | USB state must not bypass gate |

## Prototype verification

Before fabrication sign-off, measure:

1. RAW +12 V;
2. `SOLENOID_12V_SW`;
3. P-MOS gate-to-source voltage;
4. GPIO21 / `SOLENOID_PWR_EN`;
5. at least one solenoid connector +12 V pin;
6. ULN2003 COM rail.

Tests:

- machine power applied while ESP32 held in reset;
- USB only;
- machine power only;
- both supplies;
- enable/disable transitions;
- repeated reset while machine power remains present;
- unplug/replug USB while enabled;
- remove/reapply machine power while USB remains connected.

Pass criterion: there is no measurable solenoid-rail pulse during reset/boot and no path that allows USB to energize `SOLENOID_12V_SW`.

## Fabrication gate

This stage is complete only when:

- GPIO21 is electrically mapped to `SOLENOID_PWR_EN`;
- the high-side gate is present in KiCad;
- all Brother solenoid +12 V feeds and ULN2003 COM rails use `SOLENOID_12V_SW`;
- raw +12 V remains available to the logic supply and machine-power sensing;
- ERC passes;
- DRC passes;
- PCB layout gives the high-current path appropriate copper width and minimal loop length;
- prototype state-table tests pass.
