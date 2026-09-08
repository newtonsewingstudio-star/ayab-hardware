# AYAB-ESP32 KH910 Rev A — 5 V Reverse-Current Isolation

Status: implementation decision for Rev A power redesign.

## Problem being solved

Upstream bring-up issue #28 records the nominal 12 V rail rising to approximately 4 V when the board is powered only from USB. The issue identifies the XL1509 protection-diode path as the cause.

The existing topology lets USB-supplied system 5 V reach the output side of the machine-powered XL1509 5 V buck. Reverse conduction through the regulator then lifts its input / machine 12 V domain.

Rev A requirement: **USB-only operation must not raise the machine 12 V or solenoid domains above leakage-level voltage.**

## Selected Rev A architecture

Do not replace the complete USB-C/data circuit merely to solve the XL1509 reverse path.

Instead, split the 5 V nets into:

- `MACHINE_5V_RAW`: direct output of the machine-powered U401 5 V buck;
- `+5V` / `SYS_5V`: controller logic rail used by the rest of the board and by the existing USB power path.

Insert a reverse-blocking ideal diode between those rails:

`U401 5 V output -> MACHINE_5V_RAW -> LM66100 -> SYS_5V / +5V`

Selected part:

- **TI LM66100DCKR**
- LCSC / JLCPCB: **C2869734**
- Package: SC-70-6
- Operating input: 1.5 V to 5.5 V
- Maximum continuous current: 1.5 A
- Typical on resistance at 5 V: approximately 79 mOhm
- Integrated reverse-current blocking and reverse-polarity protection
- Active / current-production TI part

## Why this part

A Schottky diode would also stop the reverse path but would impose a larger, load-dependent voltage drop on the machine-powered 5 V rail.

The LM66100 behaves as an integrated ideal diode:

- low forward drop;
- blocks reverse current from USB-powered `SYS_5V` into `MACHINE_5V_RAW`;
- no external power MOSFET is required;
- factory-assemblable compact package;
- 1.5 A rating is well above the few-hundred-mA logic consumption reported during upstream bring-up.

The 1.5 A limit becomes a formal Rev A logic-domain budget. If the final display/front-panel design would push worst-case continuous 5 V demand close to this limit, the design must be reevaluated before fabrication rather than assuming margin.

## Intended connection

- `VIN`: `MACHINE_5V_RAW`.
- `VOUT`: `SYS_5V` / existing global `+5V`.
- `GND`: board ground.
- `CE`: held in the enabled state for normal machine-power operation according to the TI datasheet; implementation must not allow USB `SYS_5V` to force the part on backward.
- `ST`: optional diagnostic/status output; may be left unused if not needed, or routed to a test pad if layout permits.

Local input/output ceramic decoupling must follow the datasheet recommendation.

## Required schematic changes

1. Rename the current U401 output net from the system 5 V rail to `MACHINE_5V_RAW`.
2. Insert LM66100 between `MACHINE_5V_RAW` and the existing global system `+5V` rail.
3. Preserve the existing USB power circuit on the system side during this stage.
4. Add test points for:
   - `MACHINE_5V_RAW`;
   - `SYS_5V`;
   - machine `12V`;
   - USB VBUS.
5. Re-run ERC/DRC.
6. Review every other possible machine-domain backfeed path after this primary path is removed.

## Required power-state results

### USB only

Expected:

- USB VBUS: approximately 5 V;
- SYS_5V: powered;
- 3.3 V logic: powered;
- MACHINE_5V_RAW: approximately 0 V except leakage;
- machine 12 V: approximately 0 V except leakage;
- solenoid power: 0 V / disabled.

### Machine only

Expected:

- machine 12 V: normal;
- MACHINE_5V_RAW: approximately 5 V;
- SYS_5V: approximately 5 V minus only the ideal-diode conduction loss;
- USB VBUS connector must not be driven by the board.

### USB + machine

Expected:

- no source fighting;
- no reverse current into the machine 5 V buck;
- no reverse current toward the USB host;
- logic remains stable during USB connect/disconnect.

## Fabrication gate

This change is not considered proven merely because ERC/DRC passes. Prototype bring-up must explicitly measure the four nodes above under USB-only, machine-only, and combined power.

The USB-only machine 12 V measurement that was approximately 4 V on the upstream prototype is a direct regression test for Rev A.
