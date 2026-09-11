# KH910 Rev A — Electrical Fail-Safe Review

Review date: 2026-09-10

Verdict: **PASS for manufacture and supervised bring-up of one Rev A prototype.** The protected machine-sense correction is integrated, KiCad DRC/ERC and topology checks pass, and the PCB has been visually reviewed. This is an electrical design release—not permission to operate solenoids before the no-coil physical power-state tests below, not a production release, and not a machinery-safety certification.

## Evidence reviewed

- Schematic-derived and PCB pin-level topology report: `KH910_REV_A_POWER_TOPOLOGY.md`
- Integrated-board DRC report: `KH910_REV_A_INTEGRATED_DRC.rpt`
- Solenoid source audit and physical PCB topology validator
- TI LM66100 Rev. A data sheet, including the DCK pinout and always-on reverse-current-blocking configuration
- AOS AO3400A data sheet and the LRC LP9435LT1G device ratings recorded in the design
- Top, bottom, and copper review renders in this directory

## Machine-derived 5 V isolation

U403 is a TI LM66100DCKR in the correct DCK / SC-70-6 footprint.

| Pin | Function | PCB net | Review |
|---:|---|---|---|
| 1 | VIN | `/PSU/5V_SW` | filtered machine-derived 5 V input |
| 2 | GND | `GND` | correct |
| 3 | CE | `+5V` | tied to VOUT as TI specifies for reverse-current blocking |
| 4 | N/C | unconnected | correct |
| 5 | ST | `GND` | permitted when status is unused |
| 6 | VOUT | `+5V` | system 5 V output |

The former R611 zero-ohm bypass is absent, so USB-powered system 5 V no longer has that conductive path back into the machine buck output. U403's 5.5 V input rating and 1.5 A continuous rating cover the nominal 5 V logic rail and the documented few-hundred-milliamp logic load.

## Machine-power sensing

R215/R216 form the intended `+12V -> 47k -> MACHINE_PWR_SENSE -> 10k -> GND` divider, and GPIO4 is connected to the divider output.

- Divider ratio: 0.17544.
- At 12.0 V input: 2.105 V at GPIO4 and 0.211 mA divider current.
- At 15.0 V input: 2.632 V at GPIO4 and 0.263 mA divider current.
- The divider reaches 3.6 V only at approximately 20.5 V input.

The divider alone is suitable for detecting the nominal machine rail, but it is not sufficient input protection: an open R216 would leave the ESP32 input supplied through R215, and Espressif does not specify an allowable GPIO injection current for that condition. The release correction adds D205/D206 Schottky clamps to `+3V3` and ground plus C206 100 nF to ground. R215 then limits positive-clamp current to approximately 0.179 mA at 12 V, 0.243 mA at 15 V, and 0.774 mA at a conservative 40 V disturbance (using a 3.6 V node bound). C206 filters fast switching noise; D206 clamps negative excursions.

This closes the auditor's R216-open and ordinary transient concerns without claiming surge immunity. An R215 short, a clamp installed with the wrong polarity, or loss of the 3.3 V clamp reference remains outside the single-fault claim and is covered by assembly inspection and current-limited first-power tests. Initial bring-up must still record the real machine-rail peak and ADC reading before solenoid enable is allowed.

## Solenoid hardware default-OFF behavior

The validated PCB topology is:

- Q805 LP9435LT1G P-channel MOSFET source on raw `+12V`, drain on `SOLENOID_12V_SW`.
- R820 100 kΩ from Q805 gate to source, holding Q805 OFF without active control.
- Q806 AO3400A pulls the Q805 gate low only when commanded.
- R822 100 kΩ holds the Q806 gate low while GPIO21 is floating, reset, or unpowered.
- R821 10 kΩ limits/isolate the GPIO21 drive.
- All checked solenoid common pins and ULN2003 flyback COM loads are on `SOLENOID_12V_SW`, not raw `+12V`.

At 12 V, Q805 gate pull-down current is approximately 120 µA. A 3.3 V GPIO21 high produces approximately 3.0 V at the Q806 gate through the 10 kΩ/100 kΩ network, within the AO3400A's characterized logic-level range. Q805 sees approximately -12 V VGS when enabled, within its ±20 V rating.

Using the documented conservative 1.37 A all-coil envelope and 70 mΩ Q805 resistance gives approximately 0.096 V drop and 0.131 W conduction loss. The switched rail uses broad trunk copper, with narrow branches confined to individual low-current loads.

## State review

| State | Result |
|---|---|
| Fully off | passive resistors hold both MOSFETs OFF |
| USB only | raw machine 12 V is absent; the gate cannot energize a solenoid rail |
| Machine power during reset/boot | GPIO21 is high-impedance/input by default; R822 and R820 hold the gate OFF |
| Valid machine power and deliberate enable | GPIO21 high turns Q806 and then Q805 ON |
| Brownout or watchdog reset | GPIO21 releases; passive hardware returns the gate OFF |
| Machine power removed while USB remains | the switched rail collapses while logic may remain powered |

## Solenoid-gate component fault tree

The gate is hardware-default-OFF for normal reset, boot, brownout, unpowered-MCU, and released-GPIO states. It is not a redundant or safety-rated single-fault shutdown circuit. The explicit component-level review is:

| Fault | Expected result | Classification |
|---|---|---|
| R820 open | Q805 gate can float; leakage or coupling can enable the switched rail | unsafe residual; inspect/continuity-test before coils |
| R820 short | Q805 gate is held at source | safe OFF |
| R821 open | Q806 cannot be driven on | safe OFF |
| R821 short | enable remains functional but GPIO current limiting/isolation is lost; R822 still pulls down | degraded, not an automatic enable |
| R822 open | Q806 gate can float during reset or while the MCU is unpowered | unsafe residual; inspect/continuity-test before coils |
| R822 short | Q806 gate is held low | safe OFF |
| Q806 drain-source short | Q805 is forced on whenever machine 12 V is present | unsafe residual; rail gate lost |
| Q806 open | Q805 remains pulled off by R820 | safe OFF |
| Q805 drain-source short | `SOLENOID_12V_SW` is permanently live; ULN2003 input defaults become the remaining barrier | unsafe residual; rail gate lost |
| Q805 open | switched solenoid rail remains off | safe OFF |
| GPIO21 stuck high | rail remains enabled until firmware/watchdog/reset releases it | known software/control residual |

The one-off prototype therefore relies on correct assembly of R820/R822 and both MOSFETs, followed by continuity checks and powered reset/brownout tests before any coil connector is attached. No SIL, machinery-safety, or comprehensive single-fault rating is claimed.

## Safety envelope and required bring-up tests

The passive network protects reset, boot, unpowered-MCU, and released-GPIO states. It is not an independent timed watchdog: a software fault that leaves GPIO21 actively latched high can leave the gate enabled until the ESP32 watchdog resets the device. Firmware must therefore keep watchdogs enabled, drive GPIO21 low before teardown, and require a fresh valid `MACHINE_PWR_SENSE` reading after every reset.

Before attaching solenoids for operational use, measure USB-only, machine-only, and combined-power states. Confirm:

1. raw `+12V`, `SOLENOID_12V_SW`, and the machine connector remain near 0 V under USB-only power;
2. no solenoid-rail pulse occurs during reset, boot, watchdog reset, or brownout;
3. machine-derived 5 V does not drive USB VBUS, and USB 5 V does not lift the raw machine/buck domain;
4. GPIO4 voltage agrees with the divider calculation and remains below the ESP32 input limit at the measured maximum rail/transient;
5. Q805 temperature and switched-rail voltage drop are acceptable under the maximum intended coil pattern.

These measurements are a post-assembly bring-up gate. They cannot be completed before the first physical prototype exists and are not represented as passed here.
