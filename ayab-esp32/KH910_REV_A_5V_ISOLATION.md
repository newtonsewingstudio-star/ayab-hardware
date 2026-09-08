# AYAB-ESP32 KH910 Rev A — 5 V Reverse-Current Isolation

Status: implementation decision for Rev A power redesign.

## Problem being solved

Upstream bring-up issue #28 records the nominal 12 V rail rising to approximately 4 V when the board is powered only from USB. The issue identifies the XL1509 protection-diode path as the cause.

The existing topology lets USB-supplied system 5 V reach the output side of the machine-powered XL1509 5 V buck. Reverse conduction through the regulator then lifts its input / machine 12 V domain.

Rev A requirement: **USB-only operation must not raise the machine 12 V or solenoid domains above leakage-level voltage.**

## Selected Rev A architecture

Do not replace the complete USB-C/data circuit merely to solve the XL1509 reverse path.

Instead, split the 5 V nets into:

- `MACHINE_5V_RAW`: filtered output of the machine-powered U401 5 V buck;
- `+5V` / `SYS_5V`: controller logic rail used by the rest of the board and by the existing USB power path.

Insert a reverse-blocking ideal diode between those rails:

`U401 5 V filtered output -> MACHINE_5V_RAW -> LM66100 -> SYS_5V / +5V`

Selected part:

- **TI LM66100DCKR**
- LCSC / JLCPCB: **C2869734**
- Package: SC-70-6 / SOT-363
- Operating input: 1.5 V to 5.5 V
- Maximum continuous current: 1.5 A
- Typical on resistance at 5 V: approximately 79 mOhm
- Integrated reverse-current blocking and reverse-polarity protection
- Active / current-production TI part

## Exact insertion point in the existing schematic

The current 5 V power stage already contains the ideal break point:

- U401 feeds the existing output inductor/filter network;
- the filtered 5 V node has an existing **10 uF ceramic capacitor** (`C15850`, Samsung `CL21A106KAYNNNE`);
- that filtered node then passes through **R406, a 0 ohm 0603 jumper**;
- the far side of R406 feeds the PSU sheet hierarchical `5V` output and system rail.

Rev A therefore replaces **R406's electrical function** with the LM66100 stage:

`filtered 5 V / C15850 side -> MACHINE_5V_RAW -> LM66100 -> existing 5V output side`

This is intentionally *after* the XL1509 switching inductor and output filtering. The LM66100 must never be inserted in the XL1509 switching node.

The existing 10 uF ceramic remains on the LM66100 VIN / `MACHINE_5V_RAW` side. It already exceeds the LM66100's typical 1 uF local input-capacitance recommendation; do not add redundant capacitance merely to satisfy a nominal value. PCB placement must keep the existing capacitor and LM66100 current loop compact.

## Why this part

A Schottky diode would also stop the reverse path but would impose a larger, load-dependent voltage drop on the machine-powered 5 V rail.

The LM66100 behaves as an integrated ideal diode:

- low forward drop;
- blocks reverse current from USB-powered `SYS_5V` into `MACHINE_5V_RAW`;
- no external power MOSFET is required;
- factory-assemblable compact package;
- 1.5 A rating is well above the few-hundred-mA logic consumption reported during upstream bring-up.

The 1.5 A limit becomes a formal Rev A logic-domain budget. If the final display/front-panel design would push worst-case continuous 5 V demand close to this limit, the design must be reevaluated before fabrication rather than assuming margin.

## Locked LM66100 pin configuration

TI defines the DCK / SC-70-6 pinout as:

| Pin | Name | Rev A connection |
|---:|---|---|
| 1 | VIN | `MACHINE_5V_RAW` |
| 2 | GND | board GND |
| 3 | CE | **tie to VOUT / `SYS_5V` for reverse-current blocking** |
| 4 | N/C | leave unconnected |
| 5 | ST | tie to GND when status output is not used |
| 6 | VOUT | `SYS_5V` / existing `5V` output |

The CE connection is intentional and important. TI specifies that CE is active-low relative to VIN and explicitly allows CE to be connected to VOUT for reverse-current protection. Rev A will use that configuration so USB-powered `SYS_5V` cannot force current backward into `MACHINE_5V_RAW`.

`ST` is an active-low open-drain status output. TI permits connecting it to GND if status reporting is not required; Rev A does that rather than consuming another MCU pin for a redundant indication.

## Required schematic changes

1. Remove/bypass R406 as the conductive link between the two power domains.
2. Name the R406 input/filter side `MACHINE_5V_RAW`.
3. Insert LM66100 between the former R406 input and output nodes using the locked pin configuration above.
4. Preserve C15850 on the `MACHINE_5V_RAW` side.
5. Preserve the existing USB power circuit on the system side during this stage.
6. Use KiCad footprint `Package_TO_SOT_SMD:SOT-363_SC-70-6` for the DCK package.
7. Add test points for `MACHINE_5V_RAW`, `SYS_5V`, machine `12V`, and USB VBUS where layout permits.
8. Re-run ERC/DRC and then review every other possible machine-domain backfeed path.

## Required power-state results

### USB only

- USB VBUS: approximately 5 V;
- SYS_5V: powered;
- 3.3 V logic: powered;
- MACHINE_5V_RAW: approximately 0 V except leakage;
- machine 12 V: approximately 0 V except leakage;
- solenoid power: 0 V / disabled.

### Machine only

- machine 12 V: normal;
- MACHINE_5V_RAW: approximately 5 V;
- SYS_5V: approximately 5 V minus only the ideal-diode conduction loss;
- USB VBUS connector must not be driven by the board.

### USB + machine

- no source fighting;
- no reverse current into the machine 5 V buck;
- no reverse current toward the USB host;
- logic remains stable during USB connect/disconnect.

## Fabrication gate

This change is not considered proven merely because ERC/DRC passes. Prototype bring-up must explicitly measure the four nodes above under USB-only, machine-only, and combined power.

The USB-only machine 12 V measurement that was approximately 4 V on the upstream prototype is a direct regression test for Rev A.

## Primary references

- TI LM66100 datasheet, Rev. A, especially Section 5 (Pin Configuration and Functions) and Section 8.3.2 (Always-ON Reverse Current Blocking).
- Upstream AYAB hardware issue #28, prototype-board revisions / USB-only 12 V backfeed observation.
