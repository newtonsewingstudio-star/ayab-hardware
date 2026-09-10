# KH910 Rev A — Solenoid PCB Parity Audit (Pre-integration snapshot)

> Historical evidence only. This snapshot predates the integrated Rev A
> high-side gate in commit `350f7d0`; its “On PCB?” table is not current.
> The current authority is the `KH910 Rev A Solenoid Gate Validation`
> workflow, which checks the integrated PCB DRC and fail-safe topology.

- PCB bytes: **4,147,073**
- PCB footprints parsed: **246**
- PCB nets parsed: **839**

## New fail-safe schematic devices

| Project ref | Value | LCSC | Footprint | On PCB? | PCB at |
|---|---|---|---|---|---|
| Q805 | LP9435LT1G | C383257 | `Package_TO_SOT_SMD:SOT-23` | **NO** | — |
| Q806 | AO3400A | C20917 | `Package_TO_SOT_SMD:SOT-23` | **NO** | — |
| R820 | 100k | C25803 | `Resistor_SMD:R_0603_1608Metric` | **NO** | — |
| R821 | 10k | C25804 | `Resistor_SMD:R_0603_1608Metric` | **NO** | — |
| R822 | 100k | C25803 | `Resistor_SMD:R_0603_1608Metric` | **NO** | — |

## Interesting existing board nets

- net 4: `+12V`
- net 47: `/BROTHER-CONNECTORS/SOL_7`
- net 48: `/BROTHER-CONNECTORS/SOL_6`
- net 49: `/BROTHER-CONNECTORS/SOL_5`
- net 50: `/BROTHER-CONNECTORS/SOL_4`
- net 51: `/BROTHER-CONNECTORS/SOL_3`
- net 52: `/BROTHER-CONNECTORS/SOL_2`
- net 53: `/BROTHER-CONNECTORS/SOL_1`
- net 54: `/BROTHER-CONNECTORS/SOL_0`
- net 55: `/BROTHER-CONNECTORS/SOL_F`
- net 56: `/BROTHER-CONNECTORS/SOL_E`
- net 57: `/BROTHER-CONNECTORS/SOL_D`
- net 58: `/BROTHER-CONNECTORS/SOL_C`
- net 59: `/BROTHER-CONNECTORS/SOL_B`
- net 60: `/BROTHER-CONNECTORS/SOL_A`
- net 61: `/BROTHER-CONNECTORS/SOL_9`
- net 62: `/BROTHER-CONNECTORS/SOL_8`
- net 118: `/SOLENOID DRIVERS/MCU_SOL_0`
- net 119: `/SOLENOID DRIVERS/MCU_SOL_1`
- net 120: `/SOLENOID DRIVERS/MCU_SOL_2`
- net 121: `/SOLENOID DRIVERS/MCU_SOL_3`
- net 122: `/SOLENOID DRIVERS/MCU_SOL_4`
- net 123: `/SOLENOID DRIVERS/MCU_SOL_5`
- net 124: `/SOLENOID DRIVERS/MCU_SOL_6`
- net 125: `/SOLENOID DRIVERS/MCU_SOL_7`
- net 128: `/SOLENOID DRIVERS/MCU_SOL_8`
- net 129: `/SOLENOID DRIVERS/MCU_SOL_9`
- net 130: `/SOLENOID DRIVERS/MCU_SOL_A`
- net 131: `/SOLENOID DRIVERS/MCU_SOL_B`
- net 132: `/SOLENOID DRIVERS/MCU_SOL_C`
- net 133: `/SOLENOID DRIVERS/MCU_SOL_D`
- net 134: `/SOLENOID DRIVERS/MCU_SOL_E`
- net 135: `/SOLENOID DRIVERS/MCU_SOL_F`
- net 55: `/BROTHER-CONNECTORS/SOL_F`
- net 56: `/BROTHER-CONNECTORS/SOL_E`
- net 57: `/BROTHER-CONNECTORS/SOL_D`
- net 58: `/BROTHER-CONNECTORS/SOL_C`
- net 59: `/BROTHER-CONNECTORS/SOL_B`
- net 60: `/BROTHER-CONNECTORS/SOL_A`
- net 61: `/BROTHER-CONNECTORS/SOL_9`
- net 62: `/BROTHER-CONNECTORS/SOL_8`
- net 4: `+12V`
- net 4: `+12V`
- net 134: `/SOLENOID DRIVERS/MCU_SOL_E`
- net 133: `/SOLENOID DRIVERS/MCU_SOL_D`
- net 132: `/SOLENOID DRIVERS/MCU_SOL_C`
- net 131: `/SOLENOID DRIVERS/MCU_SOL_B`
- net 130: `/SOLENOID DRIVERS/MCU_SOL_A`
- net 129: `/SOLENOID DRIVERS/MCU_SOL_9`
- net 128: `/SOLENOID DRIVERS/MCU_SOL_8`
- net 4: `+12V`
- net 62: `/BROTHER-CONNECTORS/SOL_8`
- net 61: `/BROTHER-CONNECTORS/SOL_9`
- net 60: `/BROTHER-CONNECTORS/SOL_A`
- net 59: `/BROTHER-CONNECTORS/SOL_B`
- net 58: `/BROTHER-CONNECTORS/SOL_C`
- net 57: `/BROTHER-CONNECTORS/SOL_D`
- net 56: `/BROTHER-CONNECTORS/SOL_E`
- net 4: `+12V`
- net 118: `/SOLENOID DRIVERS/MCU_SOL_0`
- net 135: `/SOLENOID DRIVERS/MCU_SOL_F`
- net 4: `+12V`
- net 55: `/BROTHER-CONNECTORS/SOL_F`
- net 54: `/BROTHER-CONNECTORS/SOL_0`
- net 4: `+12V`
- net 4: `+12V`
- net 4: `+12V`
- net 55: `/BROTHER-CONNECTORS/SOL_F`
- net 56: `/BROTHER-CONNECTORS/SOL_E`
- net 57: `/BROTHER-CONNECTORS/SOL_D`
- net 58: `/BROTHER-CONNECTORS/SOL_C`
- net 59: `/BROTHER-CONNECTORS/SOL_B`
- net 60: `/BROTHER-CONNECTORS/SOL_A`
- net 61: `/BROTHER-CONNECTORS/SOL_9`
- net 62: `/BROTHER-CONNECTORS/SOL_8`
- net 4: `+12V`
- net 4: `+12V`
- net 4: `+12V`
- net 47: `/BROTHER-CONNECTORS/SOL_7`
- net 48: `/BROTHER-CONNECTORS/SOL_6`
- net 49: `/BROTHER-CONNECTORS/SOL_5`
- net 50: `/BROTHER-CONNECTORS/SOL_4`
- net 51: `/BROTHER-CONNECTORS/SOL_3`
- net 52: `/BROTHER-CONNECTORS/SOL_2`
- net 53: `/BROTHER-CONNECTORS/SOL_1`
- net 54: `/BROTHER-CONNECTORS/SOL_0`
- net 4: `+12V`
- net 4: `+12V`
- net 4: `+12V`
- net 47: `/BROTHER-CONNECTORS/SOL_7`
- net 48: `/BROTHER-CONNECTORS/SOL_6`
- net 49: `/BROTHER-CONNECTORS/SOL_5`
- net 50: `/BROTHER-CONNECTORS/SOL_4`
- net 51: `/BROTHER-CONNECTORS/SOL_3`
- net 52: `/BROTHER-CONNECTORS/SOL_2`
- net 53: `/BROTHER-CONNECTORS/SOL_1`
- net 54: `/BROTHER-CONNECTORS/SOL_0`
- net 4: `+12V`
- net 4: `+12V`
- net 47: `/BROTHER-CONNECTORS/SOL_7`
- net 48: `/BROTHER-CONNECTORS/SOL_6`
- net 49: `/BROTHER-CONNECTORS/SOL_5`
- net 50: `/BROTHER-CONNECTORS/SOL_4`
- net 51: `/BROTHER-CONNECTORS/SOL_3`
- net 52: `/BROTHER-CONNECTORS/SOL_2`
- net 53: `/BROTHER-CONNECTORS/SOL_1`
- net 54: `/BROTHER-CONNECTORS/SOL_0`
- net 4: `+12V`
- net 4: `+12V`
- net 4: `+12V`
- net 125: `/SOLENOID DRIVERS/MCU_SOL_7`
- net 124: `/SOLENOID DRIVERS/MCU_SOL_6`
- net 123: `/SOLENOID DRIVERS/MCU_SOL_5`
- net 122: `/SOLENOID DRIVERS/MCU_SOL_4`
- net 121: `/SOLENOID DRIVERS/MCU_SOL_3`
- net 120: `/SOLENOID DRIVERS/MCU_SOL_2`
- net 119: `/SOLENOID DRIVERS/MCU_SOL_1`
- net 4: `+12V`
- net 53: `/BROTHER-CONNECTORS/SOL_1`
- net 52: `/BROTHER-CONNECTORS/SOL_2`
- net 51: `/BROTHER-CONNECTORS/SOL_3`
- net 50: `/BROTHER-CONNECTORS/SOL_4`
- net 49: `/BROTHER-CONNECTORS/SOL_5`
- net 48: `/BROTHER-CONNECTORS/SOL_6`
- net 47: `/BROTHER-CONNECTORS/SOL_7`
- net 4: `+12V`
- net 125: `/SOLENOID DRIVERS/MCU_SOL_7`
- net 124: `/SOLENOID DRIVERS/MCU_SOL_6`
- net 123: `/SOLENOID DRIVERS/MCU_SOL_5`
- net 122: `/SOLENOID DRIVERS/MCU_SOL_4`
- net 121: `/SOLENOID DRIVERS/MCU_SOL_3`
- net 120: `/SOLENOID DRIVERS/MCU_SOL_2`
- net 119: `/SOLENOID DRIVERS/MCU_SOL_1`
- net 118: `/SOLENOID DRIVERS/MCU_SOL_0`
- net 128: `/SOLENOID DRIVERS/MCU_SOL_8`
- net 129: `/SOLENOID DRIVERS/MCU_SOL_9`
- net 130: `/SOLENOID DRIVERS/MCU_SOL_A`
- net 131: `/SOLENOID DRIVERS/MCU_SOL_B`
- net 132: `/SOLENOID DRIVERS/MCU_SOL_C`
- net 133: `/SOLENOID DRIVERS/MCU_SOL_D`
- net 134: `/SOLENOID DRIVERS/MCU_SOL_E`
- net 135: `/SOLENOID DRIVERS/MCU_SOL_F`
- net 4: `+12V`
- net 4: `+12V`
- net 4: `+12V`
- net 55: `/BROTHER-CONNECTORS/SOL_F`
- net 56: `/BROTHER-CONNECTORS/SOL_E`
- net 57: `/BROTHER-CONNECTORS/SOL_D`
- net 58: `/BROTHER-CONNECTORS/SOL_C`
- net 59: `/BROTHER-CONNECTORS/SOL_B`
- net 60: `/BROTHER-CONNECTORS/SOL_A`
- net 61: `/BROTHER-CONNECTORS/SOL_9`
- net 62: `/BROTHER-CONNECTORS/SOL_8`
- net 4: `+12V`

## Relevant footprints already on PCB

### J401 — 900.965.CK35 SOLENOIDS A
- footprint: `Library:530141010`
- at: `132.84,153.7852`
- pad 1: net=/BROTHER-CONNECTORS/SOL_7 (#47) local_at=0,0
- pad 2: net=/BROTHER-CONNECTORS/SOL_6 (#48) local_at=-2,0
- pad 3: net=/BROTHER-CONNECTORS/SOL_5 (#49) local_at=-4,0
- pad 4: net=/BROTHER-CONNECTORS/SOL_4 (#50) local_at=-6,0
- pad 5: net=/BROTHER-CONNECTORS/SOL_3 (#51) local_at=-8,0
- pad 6: net=/BROTHER-CONNECTORS/SOL_2 (#52) local_at=-10,0
- pad 7: net=/BROTHER-CONNECTORS/SOL_1 (#53) local_at=-12,0
- pad 8: net=/BROTHER-CONNECTORS/SOL_0 (#54) local_at=-14,0
- pad 9: net=+12V (#4) local_at=-16,0
- pad 10: net=+12V (#4) local_at=-18,0

### J402 — 900.965.CK35 SOLENOIDS B
- footprint: `Library:530140810`
- at: `107.57,153.7852`
- pad 1: net=/BROTHER-CONNECTORS/SOL_F (#55) local_at=0,0
- pad 2: net=/BROTHER-CONNECTORS/SOL_E (#56) local_at=-2,0
- pad 3: net=/BROTHER-CONNECTORS/SOL_D (#57) local_at=-4,0
- pad 4: net=/BROTHER-CONNECTORS/SOL_C (#58) local_at=-6,0
- pad 5: net=/BROTHER-CONNECTORS/SOL_B (#59) local_at=-8,0
- pad 6: net=/BROTHER-CONNECTORS/SOL_A (#60) local_at=-10,0
- pad 7: net=/BROTHER-CONNECTORS/SOL_9 (#61) local_at=-12,0
- pad 8: net=/BROTHER-CONNECTORS/SOL_8 (#62) local_at=-14,0

### J403 — 910.950 SOLENOIDS A
- footprint: `Library:HNC2-2.5P-10DS`
- at: `320.91,138.83`
- pad 1: net=/BROTHER-CONNECTORS/SOL_7 (#47) local_at=-10,0
- pad 2: net=/BROTHER-CONNECTORS/SOL_6 (#48) local_at=-7.5,0
- pad 3: net=/BROTHER-CONNECTORS/SOL_5 (#49) local_at=-5,0
- pad 4: net=/BROTHER-CONNECTORS/SOL_4 (#50) local_at=-2.5,0
- pad 5: net=/BROTHER-CONNECTORS/SOL_3 (#51) local_at=0,0
- pad 6: net=/BROTHER-CONNECTORS/SOL_2 (#52) local_at=2.5,0
- pad 7: net=/BROTHER-CONNECTORS/SOL_1 (#53) local_at=5,0
- pad 8: net=/BROTHER-CONNECTORS/SOL_0 (#54) local_at=7.5,0
- pad 9: net=+12V (#4) local_at=10,0
- pad 10: net=+12V (#4) local_at=12.5,0

### J404 — 910.950 SOLENOIDS B
- footprint: `Library:HNC2-2.5P-8DS`
- at: `322.2,145.3`
- pad 1: net=/BROTHER-CONNECTORS/SOL_F (#55) local_at=-8.75,0
- pad 2: net=/BROTHER-CONNECTORS/SOL_E (#56) local_at=-6.25,0
- pad 3: net=/BROTHER-CONNECTORS/SOL_D (#57) local_at=-3.75,0
- pad 4: net=/BROTHER-CONNECTORS/SOL_C (#58) local_at=-1.25,0
- pad 5: net=/BROTHER-CONNECTORS/SOL_B (#59) local_at=1.25,0
- pad 6: net=/BROTHER-CONNECTORS/SOL_A (#60) local_at=3.75,0
- pad 7: net=/BROTHER-CONNECTORS/SOL_9 (#61) local_at=6.25,0
- pad 8: net=/BROTHER-CONNECTORS/SOL_8 (#62) local_at=8.75,0

### J405 — 910.950 ENCODERS EOL R
- footprint: `Library:HNC2-2.5P-10DS`
- at: `280.93,145.17`
- pad 1: net=+5V (#5) local_at=-10,0
- pad 2: net=GND (#2) local_at=-7.5,0
- pad 3: net=unconnected-(J405-Pin_3-Pad3) (#20) local_at=-5,0
- pad 4: net=/BROTHER-CONNECTORS/ENC_V1 (#66) local_at=-2.5,0
- pad 5: net=/BROTHER-CONNECTORS/ENC_V2 (#65) local_at=0,0
- pad 6: net=/BROTHER-CONNECTORS/ENC_BELTPHASE (#67) local_at=2.5,0
- pad 7: net=/BROTHER-CONNECTORS/EOL_R_S (#70) local_at=5,0
- pad 8: net=/BROTHER-CONNECTORS/EOL_R_N (#69) local_at=7.5,0
- pad 9: net=Net-(J405-Pin_9) (#105) local_at=10,0
- pad 10: net=Net-(J405-Pin_10) (#106) local_at=12.5,0

### J406 — 930.940 SOLENOIDS A
- footprint: `Library:SHDR10W70P0X250_1X10_2740X490X590P`
- at: `116.74,146.28`
- pad 1: net=/BROTHER-CONNECTORS/SOL_7 (#47) local_at=22.5,0
- pad 2: net=/BROTHER-CONNECTORS/SOL_6 (#48) local_at=20,0
- pad 3: net=/BROTHER-CONNECTORS/SOL_5 (#49) local_at=17.5,0
- pad 4: net=/BROTHER-CONNECTORS/SOL_4 (#50) local_at=15,0
- pad 5: net=/BROTHER-CONNECTORS/SOL_3 (#51) local_at=12.5,0
- pad 6: net=/BROTHER-CONNECTORS/SOL_2 (#52) local_at=10,0
- pad 7: net=/BROTHER-CONNECTORS/SOL_1 (#53) local_at=7.5,0
- pad 8: net=/BROTHER-CONNECTORS/SOL_0 (#54) local_at=5,0
- pad 9: net=+12V (#4) local_at=2.5,0
- pad 10: net=+12V (#4) local_at=0,0

### J407 — 930.940 SOLENOIDS B
- footprint: `Library:SHDR8W65P0X250_1X8_2240X490X610P`
- at: `110.08,146.22`
- pad 1: net=/BROTHER-CONNECTORS/SOL_F (#55) local_at=0,0
- pad 2: net=/BROTHER-CONNECTORS/SOL_E (#56) local_at=-2.5,0
- pad 3: net=/BROTHER-CONNECTORS/SOL_D (#57) local_at=-5,0
- pad 4: net=/BROTHER-CONNECTORS/SOL_C (#58) local_at=-7.5,0
- pad 5: net=/BROTHER-CONNECTORS/SOL_B (#59) local_at=-10,0
- pad 6: net=/BROTHER-CONNECTORS/SOL_A (#60) local_at=-12.5,0
- pad 7: net=/BROTHER-CONNECTORS/SOL_9 (#61) local_at=-15,0
- pad 8: net=/BROTHER-CONNECTORS/SOL_8 (#62) local_at=-17.5,0

### J408 — 910.950 EOL L
- footprint: `Library:HNC2-2.5P-3DS`
- at: `76.82,127.94`
- pad 1: net=+5V (#5) local_at=-2.5,0
- pad 2: net=GND (#2) local_at=0,0
- pad 3: net=/BROTHER-CONNECTORS/EOL_L (#63) local_at=2.5,0

### J409 — 930.940 EOL R
- footprint: `easyeda2kicad:CONN-TH_3P-P2.50_X2564WV-03-N0SN`
- at: `338.345,157.7325`
- pad 1: net=+5V (#5) local_at=2.54,0
- pad 2: net=GND (#2) local_at=0,0
- pad 3: net=/BROTHER-CONNECTORS/EOL_R (#64) local_at=-2.54,0

### J410 — 930.940 ENCODERS
- footprint: `easyeda2kicad:CONN-TH_X2564WV-05-N0SN`
- at: `161.86,153.81`
- pad 1: net=+5V (#5) local_at=5,0
- pad 2: net=GND (#2) local_at=2.5,0
- pad 3: net=/BROTHER-CONNECTORS/ENC_V2 (#65) local_at=0,0
- pad 4: net=/BROTHER-CONNECTORS/ENC_V1 (#66) local_at=-2.5,0
- pad 5: net=/BROTHER-CONNECTORS/ENC_BELTPHASE (#67) local_at=-5,0

### J411 — 900.965 EOL L
- footprint: `Library:CONN-TH_3P-P2.00_A2004WV-3P`
- at: `72.76,146.45`
- pad 1: net=+5V (#5) local_at=2,0
- pad 2: net=GND (#2) local_at=0,0
- pad 3: net=/BROTHER-CONNECTORS/EOL_L (#63) local_at=-2,0

### J412 — 900.965 EOL R
- footprint: `Library:CONN-TH_3P-P2.00_A2004WV-3P`
- at: `339.35905,152.03381`
- pad 1: net=+5V (#5) local_at=2,0
- pad 2: net=GND (#2) local_at=0,0
- pad 3: net=/BROTHER-CONNECTORS/EOL_R (#64) local_at=-2,0

### J413 — 900.965 ENCODERS
- footprint: `Library:530140510`
- at: `163.84,159.75`
- pad 1: net=+5V (#5) local_at=0,0
- pad 2: net=GND (#2) local_at=-2,0
- pad 3: net=/BROTHER-CONNECTORS/ENC_V2 (#65) local_at=-4,0
- pad 4: net=/BROTHER-CONNECTORS/ENC_V1 (#66) local_at=-6,0
- pad 5: net=/BROTHER-CONNECTORS/ENC_BELTPHASE (#67) local_at=-8,0

### J414 — 930.940 EOL L
- footprint: `easyeda2kicad:CONN-TH_3P-P2.50_X2564WV-03-N0SN`
- at: `73.76,139.475`
- pad 1: net=+5V (#5) local_at=2.54,0
- pad 2: net=GND (#2) local_at=0,0
- pad 3: net=/BROTHER-CONNECTORS/EOL_L (#63) local_at=-2.54,0

### J601 — VIN
- footprint: `easyeda2kicad:DC-IN-TH_DC-005-5A-2.0-SMT`
- at: `292.105,156.0848`
- pad : net=<none> (#-) local_at=-3.05,0
- pad : net=<none> (#-) local_at=1.45,0
- pad 1: net=/PSU/INP_1 (#149) local_at=-3.05,-5.5
- pad 1: net=/PSU/INP_1 (#149) local_at=3.05,-5.5
- pad 2: net=/PSU/INP_2 (#150) local_at=-3.05,5.5
- pad 3: net=/PSU/INP_2 (#150) local_at=3.05,5.5

### J602 — Brother_5P
- footprint: `Library:Brother_5P`
- at: `62.9,120.62`
- pad 1: net=unconnected-(J602-Pin_1-Pad1) (#152) local_at=27.7,-2
- pad 2: net=+12V (#4) local_at=19.7,-2
- pad 3: net=GND (#2) local_at=14.7,-2
- pad 4: net=GND (#2) local_at=9.7,-2
- pad 5: net=+5V (#5) local_at=4.7,-2

### J604 — Brother_4R
- footprint: `Library:Brother_4P`
- at: `341.95,145.16`
- pad 1: net=+12V (#4) local_at=21.005,-2
- pad 2: net=GND (#2) local_at=13.505,-2
- pad 3: net=GND (#2) local_at=8.505,-2
- pad 4: net=+5V (#5) local_at=3.505,-2

### Q201 — AO3400A
- footprint: `Package_TO_SOT_SMD:SOT-23`
- at: `240.7725,152.37`
- pad 1: net=/ESP32/BUZZER (#21) local_at=-0.9375,-0.95
- pad 2: net=GND (#2) local_at=-0.9375,0.95
- pad 3: net=Net-(Q201-D) (#22) local_at=0.9375,0

### Q501 — BCM857BV
- footprint: `Package_TO_SOT_SMD:SOT-363_SC-70-6`
- at: `258.35,157.4225`
- pad 1: net=Net-(Q501A-E1) (#24) local_at=-0.95,-0.65
- pad 2: net=Net-(Q501A-B1) (#83) local_at=-0.95,0
- pad 3: net=Net-(Q501B-C2) (#23) local_at=-0.95,0.65
- pad 4: net=+5V (#5) local_at=0.95,0.65
- pad 5: net=Net-(Q501A-B1) (#83) local_at=0.95,0
- pad 6: net=Net-(Q501A-B1) (#83) local_at=0.95,-0.65

### Q502 — LP9435LT1G
- footprint: `Package_TO_SOT_SMD:SOT-23`
- at: `258.45,154.035`
- pad 1: net=Net-(Q501B-C2) (#23) local_at=-0.9375,-0.95
- pad 2: net=+5V (#5) local_at=-0.9375,0.95
- pad 3: net=Net-(Q501A-E1) (#24) local_at=0.9375,0

### Q801 — AO3400A
- footprint: `Package_TO_SOT_SMD:SOT-23`
- at: `275.5746,155.0175`
- pad 1: net=+3V3 (#6) local_at=-0.9375,-0.95
- pad 2: net=Net-(Q801-S) (#84) local_at=-0.9375,0.95
- pad 3: net=/AUX-CONNECTORS/AUX_SCL (#75) local_at=0.9375,0

### Q802 — AO3400A
- footprint: `Package_TO_SOT_SMD:SOT-23`
- at: `280.615,155.0475`
- pad 1: net=+3V3 (#6) local_at=-0.9375,-0.95
- pad 2: net=Net-(Q802-S) (#85) local_at=-0.9375,0.95
- pad 3: net=/AUX-CONNECTORS/AUX_SDA (#76) local_at=0.9375,0

### Q803 — AO3400A
- footprint: `Package_TO_SOT_SMD:SOT-23`
- at: `94.23,127.32`
- pad 1: net=+3V3 (#6) local_at=-0.9375,-0.95
- pad 2: net=Net-(Q803-S) (#86) local_at=-0.9375,0.95
- pad 3: net=/AUX-CONNECTORS/MCP_SCL (#81) local_at=0.9375,0

### Q804 — AO3400A
- footprint: `Package_TO_SOT_SMD:SOT-23`
- at: `97.75,127.33`
- pad 1: net=+3V3 (#6) local_at=-0.9375,-0.95
- pad 2: net=Net-(Q804-S) (#87) local_at=-0.9375,0.95
- pad 3: net=/AUX-CONNECTORS/MCP_SDA (#82) local_at=0.9375,0

### TP301 — MCP_INTA
- footprint: `TestPoint:TestPoint_Pad_D1.0mm`
- at: `99.24,133.68`
- pad 1: net=Net-(U301-INTA) (#104) local_at=0,0

### TP302 — MCP_INTB
- footprint: `TestPoint:TestPoint_Pad_D1.0mm`
- at: `97.05,133.69`
- pad 1: net=Net-(U301-INTB) (#103) local_at=0,0

### TP401 — 9
- footprint: `TestPoint:TestPoint_Pad_D1.0mm`
- at: `270.93,149.15`
- pad 1: net=Net-(J405-Pin_9) (#105) local_at=0,0

### TP402 — 10
- footprint: `TestPoint:TestPoint_Pad_D1.0mm`
- at: `268.42,149.14`
- pad 1: net=Net-(J405-Pin_10) (#106) local_at=0,0

### TP501 — USB_BUSV
- footprint: `TestPoint:TestPoint_Pad_D1.0mm`
- at: `251.33,148.96`
- pad 1: net=/USB/USB_VBUS (#14) local_at=0,0

### TP502 — USBM
- footprint: `TestPoint:TestPoint_Pad_D1.0mm`
- at: `249.16,148.98`
- pad 1: net=/ESP32/USB_M (#1) local_at=0,0

### TP503 — USBP
- footprint: `TestPoint:TestPoint_Pad_D1.0mm`
- at: `253.48,148.99`
- pad 1: net=/ESP32/USB_P (#3) local_at=0,0

### TP601 — 12V
- footprint: `TestPoint:TestPoint_Pad_D1.0mm`
- at: `305.32,149.98`
- pad 1: net=+12V (#4) local_at=0,0

### TP602 — 5V
- footprint: `TestPoint:TestPoint_Pad_D1.0mm`
- at: `306.863,134.5184`
- pad 1: net=/PSU/5V_SW (#109) local_at=0,0

### TP603 — 3V3
- footprint: `TestPoint:TestPoint_Pad_D1.0mm`
- at: `273.8374,134.5184`
- pad 1: net=/PSU/3V3_SW (#19) local_at=0,0

### TP701 — CMP-L
- footprint: `TestPoint:TestPoint_Pad_D1.0mm`
- at: `85.39,135`
- pad 1: net=/BROTHER-CONNECTORS/EOL_L (#63) local_at=0,0

### TP702 — CMP-R
- footprint: `TestPoint:TestPoint_Pad_D1.0mm`
- at: `321.66,160.16`
- pad 1: net=/BROTHER-CONNECTORS/EOL_R (#64) local_at=0,0

### U302 — ULN2003A
- footprint: `Package_SO:SOIC-16_3.9x9.9mm_P1.27mm`
- at: `128.45,139.325`
- pad 1: net=/SOLENOID DRIVERS/MCU_SOL_7 (#125) local_at=-2.475,-4.445
- pad 2: net=/SOLENOID DRIVERS/MCU_SOL_6 (#124) local_at=-2.475,-3.175
- pad 3: net=/SOLENOID DRIVERS/MCU_SOL_5 (#123) local_at=-2.475,-1.905
- pad 4: net=/SOLENOID DRIVERS/MCU_SOL_4 (#122) local_at=-2.475,-0.635
- pad 5: net=/SOLENOID DRIVERS/MCU_SOL_3 (#121) local_at=-2.475,0.635
- pad 6: net=/SOLENOID DRIVERS/MCU_SOL_2 (#120) local_at=-2.475,1.905
- pad 7: net=/SOLENOID DRIVERS/MCU_SOL_1 (#119) local_at=-2.475,3.175
- pad 8: net=GND (#2) local_at=-2.475,4.445
- pad 9: net=+12V (#4) local_at=2.475,4.445
- pad 10: net=/BROTHER-CONNECTORS/SOL_1 (#53) local_at=2.475,3.175
- pad 11: net=/BROTHER-CONNECTORS/SOL_2 (#52) local_at=2.475,1.905
- pad 12: net=/BROTHER-CONNECTORS/SOL_3 (#51) local_at=2.475,0.635
- pad 13: net=/BROTHER-CONNECTORS/SOL_4 (#50) local_at=2.475,-0.635
- pad 14: net=/BROTHER-CONNECTORS/SOL_5 (#49) local_at=2.475,-1.905
- pad 15: net=/BROTHER-CONNECTORS/SOL_6 (#48) local_at=2.475,-3.175
- pad 16: net=/BROTHER-CONNECTORS/SOL_7 (#47) local_at=2.475,-4.445

### U303 — ULN2003A
- footprint: `Package_SO:SOIC-16_3.9x9.9mm_P1.27mm`
- at: `115.9,139.325`
- pad 1: net=/SOLENOID DRIVERS/MCU_SOL_0 (#118) local_at=-2.475,-4.445
- pad 2: net=unconnected-(U303-I2-Pad2) (#136) local_at=-2.475,-3.175
- pad 3: net=unconnected-(U303-I3-Pad3) (#137) local_at=-2.475,-1.905
- pad 4: net=unconnected-(U303-I4-Pad4) (#138) local_at=-2.475,-0.635
- pad 5: net=unconnected-(U303-I5-Pad5) (#139) local_at=-2.475,0.635
- pad 6: net=unconnected-(U303-I6-Pad6) (#140) local_at=-2.475,1.905
- pad 7: net=/SOLENOID DRIVERS/MCU_SOL_F (#135) local_at=-2.475,3.175
- pad 8: net=GND (#2) local_at=-2.475,4.445
- pad 9: net=+12V (#4) local_at=2.475,4.445
- pad 10: net=/BROTHER-CONNECTORS/SOL_F (#55) local_at=2.475,3.175
- pad 11: net=unconnected-(U303-O6-Pad11) (#141) local_at=2.475,1.905
- pad 12: net=unconnected-(U303-O5-Pad12) (#142) local_at=2.475,0.635
- pad 13: net=unconnected-(U303-O4-Pad13) (#143) local_at=2.475,-0.635
- pad 14: net=unconnected-(U303-O3-Pad14) (#144) local_at=2.475,-1.905
- pad 15: net=unconnected-(U303-O2-Pad15) (#145) local_at=2.475,-3.175
- pad 16: net=/BROTHER-CONNECTORS/SOL_0 (#54) local_at=2.475,-4.445

### U304 — ULN2003A
- footprint: `Package_SO:SOIC-16_3.9x9.9mm_P1.27mm`
- at: `103.35,139.325`
- pad 1: net=/SOLENOID DRIVERS/MCU_SOL_E (#134) local_at=-2.475,-4.445
- pad 2: net=/SOLENOID DRIVERS/MCU_SOL_D (#133) local_at=-2.475,-3.175
- pad 3: net=/SOLENOID DRIVERS/MCU_SOL_C (#132) local_at=-2.475,-1.905
- pad 4: net=/SOLENOID DRIVERS/MCU_SOL_B (#131) local_at=-2.475,-0.635
- pad 5: net=/SOLENOID DRIVERS/MCU_SOL_A (#130) local_at=-2.475,0.635
- pad 6: net=/SOLENOID DRIVERS/MCU_SOL_9 (#129) local_at=-2.475,1.905
- pad 7: net=/SOLENOID DRIVERS/MCU_SOL_8 (#128) local_at=-2.475,3.175
- pad 8: net=GND (#2) local_at=-2.475,4.445
- pad 9: net=+12V (#4) local_at=2.475,4.445
- pad 10: net=/BROTHER-CONNECTORS/SOL_8 (#62) local_at=2.475,3.175
- pad 11: net=/BROTHER-CONNECTORS/SOL_9 (#61) local_at=2.475,1.905
- pad 12: net=/BROTHER-CONNECTORS/SOL_A (#60) local_at=2.475,0.635
- pad 13: net=/BROTHER-CONNECTORS/SOL_B (#59) local_at=2.475,-0.635
- pad 14: net=/BROTHER-CONNECTORS/SOL_C (#58) local_at=2.475,-1.905
- pad 15: net=/BROTHER-CONNECTORS/SOL_D (#57) local_at=2.475,-3.175
- pad 16: net=/BROTHER-CONNECTORS/SOL_E (#56) local_at=2.475,-4.445

### U501 — SRV05-4
- footprint: `Package_TO_SOT_SMD:SOT-23-6`
- at: `251.35,152.585`
- pad 1: net=/ESP32/USB_M (#1) local_at=-1.1375,-0.95
- pad 2: net=GND (#2) local_at=-1.1375,0
- pad 3: net=/ESP32/USB_P (#3) local_at=-1.1375,0.95
- pad 4: net=/ESP32/USB_P (#3) local_at=1.1375,0.95
- pad 5: net=/USB/USB_VBUS (#14) local_at=1.1375,0
- pad 6: net=/ESP32/USB_M (#1) local_at=1.1375,-0.95

### U601 — XL1509
- footprint: `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm`
- at: `310.7294,126.35`
- pad 1: net=+12V (#4) local_at=-2.475,-1.905
- pad 2: net=Net-(D605-K) (#12) local_at=-2.475,-0.635
- pad 3: net=Net-(U601-FB) (#7) local_at=-2.475,0.635
- pad 4: net=GND (#2) local_at=-2.475,1.905
- pad 5: net=GND (#2) local_at=2.475,1.905
- pad 6: net=GND (#2) local_at=2.475,0.635
- pad 7: net=GND (#2) local_at=2.475,-0.635
- pad 8: net=GND (#2) local_at=2.475,-1.905

### U602 — XL1509
- footprint: `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm`
- at: `277.8594,126.33`
- pad 1: net=+5V (#5) local_at=-2.475,-1.905
- pad 2: net=Net-(D606-K) (#13) local_at=-2.475,-0.635
- pad 3: net=Net-(U602-FB) (#8) local_at=-2.475,0.635
- pad 4: net=GND (#2) local_at=-2.475,1.905
- pad 5: net=GND (#2) local_at=2.475,1.905
- pad 6: net=GND (#2) local_at=2.475,0.635
- pad 7: net=GND (#2) local_at=2.475,-0.635
- pad 8: net=GND (#2) local_at=2.475,-1.905

## Representative raw footprint templates

### R0603
```text
(footprint "Resistor_SMD:R_0603_1608Metric" (layer "F.Cu")
(tstamp 04bae630-8fbb-4b37-987d-bc6f441de592)
(at 95.19 130.8025 90)
(property "LCSC ID" "C23182")
(path "/b41a48c7-b009-4c26-92ce-a01689c1d02b/de1177d7-b6ff-406c-ac52-73ab4f0fc570")
(fp_text reference "R809" (at 0 -1.43 90) (layer "F.SilkS") hide
(tstamp f09eecec-0b20-458c-8c97-83b05ef93787)
(fp_text value "47R" (at 0 1.43 90) (layer "F.Fab")
(tstamp bc4ef3c0-e95f-473b-bcd2-feac8f63885c)
(fp_text user "${REFERENCE}" (at 0 0 90) (layer "F.Fab")
(tstamp 72dfa224-9b3d-4373-830d-5864da185018)
(stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp 7849faf2-6552-485a-bc37-68467e42b291))
(stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp fd783bae-4712-4805-b448-42f94352ca37))
(stroke (width 0.05) (type solid)) (layer "F.CrtYd") (tstamp 1a40df49-d9c5-4afb-89bd-9d4fe2df4b3a))
(stroke (width 0.05) (type solid)) (layer "F.CrtYd") (tstamp a9970646-467f-40c5-ab4a-5754193ca3c0))
(stroke (width 0.05) (type solid)) (layer "F.CrtYd") (tstamp 5baa0706-ab97-4523-945b-00e005e34ee0))
(stroke (width 0.05) (type solid)) (layer "F.CrtYd") (tstamp a9c89d7c-ed25-4951-aea5-e1b6af78fcfd))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp 62b19b6e-f9b5-4433-af78-1d838644929e))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp 86d06f5a-298f-42d5-b22f-2e5a72b49fd5))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp 9eb6d65c-c8ef-4494-8ed4-9c54f1be38db))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp ef42d546-e25c-404b-8357-98522decd0e7))
(pad "1" smd roundrect (at -0.825 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25)
(net 88 "/AUX-CONNECTORS/AYAB_SCL") (pintype "passive") (tstamp bee97f7e-7cbc-4781-ace6-2133b05c4f5f))
(pad "2" smd roundrect (at 0.825 0 90) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25)
(net 86 "Net-(Q803-S)") (pintype "passive") (tstamp 676f12f9-1a35-4be9-b7f6-888e319e676a))
```

### TP
```text
(footprint "TestPoint:TestPoint_Pad_D1.0mm" (layer "F.Cu")
(tstamp 142ef7ec-f59c-4a67-83ea-4f13d29254a0)
(at 85.39 135)
(path "/a44519f5-2a17-4043-8636-a7b7c38f71bc/39534b31-5d54-4406-aac3-cc283b69e029")
(fp_text reference "TP701" (at 0 -1.448) (layer "F.SilkS") hide
(tstamp 9dbd95eb-6f8f-4bae-8bfb-edc7fa9ef490)
(fp_text value "CMP-L" (at 0 1.55) (layer "F.Fab")
(tstamp 832179c3-32ba-4fb0-b79c-0a78477355fb)
(stroke (width 0.12) (type solid)) (fill none) (layer "F.SilkS") (tstamp f427e188-48c0-445c-b2fb-27aa62cf14de))
(stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd") (tstamp e72ebf87-48e8-4d08-a94e-406233b5f6b8))
(pad "1" smd circle (at 0 0) (size 1 1) (layers "F.Cu" "F.Mask")
(net 63 "/BROTHER-CONNECTORS/EOL_L") (pinfunction "1") (pintype "passive") (tstamp e1f18bc8-acc3-48f4-b3a7-b9cb2c1a29d2))
```

### ULN
```text
(footprint "Package_SO:SOIC-16_3.9x9.9mm_P1.27mm" (layer "F.Cu")
(tstamp 274d3689-aad1-45ea-a4e3-a4c0015953db)
(at 103.35 139.325 -90)
(property "LCSC ID" "C7512")
(path "/5c12a608-dfd1-46fe-96db-4ec512a20774/abe06852-c45c-4b8d-884f-8a5af63d1852")
(fp_text reference "U304" (at 0 -5.9 90) (layer "F.SilkS") hide
(tstamp 9d37658d-bcb7-47bb-bebe-9129cafefe3c)
(fp_text value "ULN2003A" (at 0 5.9 90) (layer "F.Fab")
(tstamp fa8bf0ed-9f6d-4dd4-8a3b-26baf77012bc)
(fp_text user "${REFERENCE}" (at 0 0 90) (layer "F.Fab")
(tstamp 6653360c-782a-4a63-ba05-b4b859ca3820)
(stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp d8bad06c-5b4b-4b0c-8889-70eb71f2e677))
(stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp b9947e19-6528-4497-9047-48f021ef1f60))
(stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp f02b0453-f29f-4162-9503-fce90f0f0660))
(stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp f886d5c6-d0fb-4d3b-8536-8adb38e0e340))
(stroke (width 0.05) (type solid)) (layer "F.CrtYd") (tstamp 02f510c3-4d6b-45b1-9570-4da37c19e4d1))
(stroke (width 0.05) (type solid)) (layer "F.CrtYd") (tstamp 0b6128b3-3257-4704-9f6d-70362b6604ed))
(stroke (width 0.05) (type solid)) (layer "F.CrtYd") (tstamp 19468d2a-1bd9-4a4f-a98f-1e3d3c9d1539))
(stroke (width 0.05) (type solid)) (layer "F.CrtYd") (tstamp 489ebb62-18cb-4912-8b5d-1b453a16f37a))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp 22510b11-118b-4e3c-847c-c8c3fa373b32))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp c2927090-3945-4b67-8101-f693bf7d23ad))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp 02b9890e-767b-4071-92e6-e0c13c3441af))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp 60af2ae7-fa77-4a3b-917f-2c6fb1ff6eee))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp 4e44ab90-ea77-4eb3-9897-d947fa948b1f))
(pad "1" smd roundrect (at -2.475 -4.445 270) (size 1.95 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25)
(net 134 "/SOLENOID DRIVERS/MCU_SOL_E") (pinfunction "I1") (pintype "input") (tstamp a667ad10-1a1f-4e08-9ebd-ea91603b8d3e))
(pad "2" smd roundrect (at -2.475 -3.175 270) (size 1.95 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25)
(net 133 "/SOLENOID DRIVERS/MCU_SOL_D") (pinfunction "I2") (pintype "input") (tstamp 34c9e316-d3f0-405c-8d6c-1a8bf4f2d0ef))
(pad "3" smd roundrect (at -2.475 -1.905 270) (size 1.95 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25)
(net 132 "/SOLENOID DRIVERS/MCU_SOL_C") (pinfunction "I3") (pintype "input") (tstamp dbd7823b-a194-4ed3-b982-d1b64342c3e9))
(pad "4" smd roundrect (at -2.475 -0.635 270) (size 1.95 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25)
(net 131 "/SOLENOID DRIVERS/MCU_SOL_B") (pinfunction "I4") (pintype "input") (tstamp 98e88e8e-d9eb-483e-90b8-945f77e8604f))
(pad "5" smd roundrect (at -2.475 0.635 270) (size 1.95 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25)
(net 130 "/SOLENOID DRIVERS/MCU_SOL_A") (pinfunction "I5") (pintype "input") (tstamp dbae9131-b86b-4f0c-a1e9-5086c8ef4c28))
(pad "6" smd roundrect (at -2.475 1.905 270) (size 1.95 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25)
(net 129 "/SOLENOID DRIVERS/MCU_SOL_9") (pinfunction "I6") (pintype "input") (tstamp c498af32-0359-485c-b085-19a4f11c9693))
(pad "7" smd roundrect (at -2.475 3.175 270) (size 1.95 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25)
(net 128 "/SOLENOID DRIVERS/MCU_SOL_8") (pinfunction "I7") (pintype "input") (tstamp 505237bc-f86b-4c2a-a82f-7d0a6e639594))
(pad "8" smd roundrect (at -2.475 4.445 270) (size 1.95 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25)
(net 2 "GND") (pinfunction "GND") (pintype "power_in") (tstamp de8c3243-c770-48c8-b49a-e43a78acef43))
```

### SOT23
```text
(footprint "Package_TO_SOT_SMD:SOT-23" (layer "F.Cu")
(tstamp 4febda2b-1d6f-4510-9fa3-8716fa0d528e)
(at 258.45 154.035 90)
(property "LCSC ID" "C383257")
(path "/7889acbf-96cc-4a04-a98d-615c06d1b134/8a64e2db-c53d-4f80-864d-257592f83652")
(fp_text reference "Q502" (at 0 -2.4 90) (layer "F.SilkS") hide
(tstamp 6733b1a1-ac5b-4aed-8b95-6d59167a3084)
(fp_text value "LP9435LT1G" (at 0 2.4 90) (layer "F.Fab")
(tstamp b338d2ad-d80f-46a5-8824-dcc765564183)
(fp_text user "${REFERENCE}" (at 0 0 90) (layer "F.Fab")
(tstamp ec835fb6-87f9-4272-9635-750543f87e08)
(stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp 321cb45f-e16f-480d-8dd3-f707e3854344))
(stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp c56b2b22-ba38-4f4b-a9c7-196cb2757f94))
(stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp 95f2cd35-427b-4a1c-a28b-e86958553d4b))
(stroke (width 0.12) (type solid)) (layer "F.SilkS") (tstamp 4d8414e1-fd87-40c4-b56c-fef8ff008479))
(stroke (width 0.05) (type solid)) (layer "F.CrtYd") (tstamp 8fa3aea2-4213-4b42-a7fa-4ee2c7167d32))
(stroke (width 0.05) (type solid)) (layer "F.CrtYd") (tstamp 43c5feb5-e22c-4803-b4a7-b271a3d84f35))
(stroke (width 0.05) (type solid)) (layer "F.CrtYd") (tstamp 8f1bed7e-ce19-4c92-ad39-20ef5e3c1feb))
(stroke (width 0.05) (type solid)) (layer "F.CrtYd") (tstamp 0009b849-ca17-4146-83c8-b63f3d93a38b))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp 88e004e3-caef-41fa-afc0-9f01d5c55b2b))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp b003cc91-c9b7-42af-ab43-8a534c11c674))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp 242cc2a1-3f68-4dd2-bd78-27f0351ae4d3))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp 30d4e738-b147-4395-858f-c3cf0092cd28))
(stroke (width 0.1) (type solid)) (layer "F.Fab") (tstamp 5f6e9d4e-657c-42d3-bdfe-cfc0c69a20b6))
(pad "1" smd roundrect (at -0.9375 -0.95 90) (size 1.475 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25)
(net 23 "Net-(Q501B-C2)") (pinfunction "G") (pintype "input") (tstamp 48dbf9a4-ce68-41b1-8dd8-211535e59852))
(pad "2" smd roundrect (at -0.9375 0.95 90) (size 1.475 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25)
(net 5 "+5V") (pinfunction "S") (pintype "passive") (tstamp c20e05b0-b2fe-4eb6-80ee-4514a3d0193a))
(pad "3" smd roundrect (at 0.9375 0 90) (size 1.475 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25)
(net 24 "Net-(Q501A-E1)") (pinfunction "D") (pintype "passive") (tstamp 3ba6a323-176d-45a1-9bfe-1449da09d400))
```

## Parity result

**PCB update required.** Missing fail-safe schematic device footprints: Q805, Q806, R820, R821, R822
