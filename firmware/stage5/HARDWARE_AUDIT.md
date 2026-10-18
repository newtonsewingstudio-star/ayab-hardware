# Rev A hardware audit (source-locked)

## Source of truth

* Repository: https://github.com/newtonsewingstudio-star/ayab-hardware
* Branch: `ayab-esp32-kh910-rev-a`
* **Fabrication commit: `ae8f7eb`** — do not substitute `main`.
* Exact design folder: `ayab-esp32/`.
* Uploaded production files: `AYAB_KH910_RevA_ae8f7eb_BOM_JLC.csv` and `...CPL_JLC.csv`.

## Facts verified from fabrication BOM

| Ref | Part | Meaning |
|---|---|---|
| U201 | ESP32-S3-MINI-1 | MCU/module to target (flash-size subvariant remains to be checked) |
| U301 | MCP23017_SS | I2C port expander; do NOT assume direct GPIO solenoid drive |
| J501 | USB_C_Receptacle_USB2.0 | Physical USB connector; D+/D- wiring requires schematic verification |

## Design hierarchy verified at commit ae8f7eb

* `ayab-esp32.kicad_sch` parent
* `mcu.kicad_sch` — ESP32 and signal interfaces
* `usb.kicad_sch` — USB circuit
* `psu.kicad_sch` — power supply
* `solenoids.kicad_sch` — output circuitry / expander interfaces
* `ioconditioning.kicad_sch` — conditioned Hall/encoder inputs
* `brother-connectors.kicad_sch` — Brother headers
* `aux-connectors.kicad_sch` — expansions

## Exact hierarchical signal names observed in MCU schematic

`KH910_R_L`, `KH910_R_K`, `SPI0_COPI`, `SPI0_CIPO`, `SPI0_SCK`,
`I2C0_SDA`, `I2C0_SCL`, `I2C1_SDA`, `I2C1_SCL`, `HALL_R_ADC`,
`HALL_L_ADC`, `ENC_A`, `ENC_B`, `ENC_BP`, `USB_M`, `USB_P`,
`UART_RX`, `UART_TX`, `DISPLAY_CS`.

## Previously documented GPIO assignments — pending revalidation from the locked electrical netlist

| Pin | Signal |
|---|---|
| GPIO1 | HALL_L_ADC |
| GPIO2 | HALL_R_ADC |
| GPIO17 | KH910_R_K |
| GPIO18 | KH910_R_L |

**These four associations were recorded in the earlier design work, but have not yet been electrically independently verified against a generated KiCad netlist. Do not use them to drive hardware.**

## Outstanding before machine I/O firmware

1. Generate ERC and a KiCad XML/netlist from *this exact* revision.
2. Resolve ESP32-S3 module part variant, USB CDC channel, D+/D- pads, strapping/boot/reset nets.
3. Derive a complete GPIO-to-net table (including encoder interrupts and ADC channel scaling).
4. Resolve MCP23017 address pins, I2C bus, reset, output polarity and all 16 solenoid channels.
5. Determine active-low/high for every machine-facing signal and verify voltage domains.
6. Bench-test with controlled safe supply and output-disabled firmware before Brother connection.

These details must not be guessed from placement/BOM tables. The stage-0 build initializes no GPIOs.

## Stage 2 source recheck

Retrieved `mcu.kicad_sch` from exact commit `ae8f7eb`. Signal labels including `HALL_L_ADC`, `HALL_R_ADC`, `KH910_R_K`, `KH910_R_L`, `I2C0_SDA`, `I2C0_SCL` are present. **Merely finding a label is not proof of its ESP32 pin number.** Pin-map and electrical characteristics remain gated on a derived, validated netlist.

Stage 2 code uses **zero machine-facing GPIOs**. API v6 info response is a diagnostic compatibility test, *not* a claim of operational support. The physical board is not tested.
