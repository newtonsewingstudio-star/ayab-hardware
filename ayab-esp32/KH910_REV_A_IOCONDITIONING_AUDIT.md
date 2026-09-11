# KH910 Rev A — I/O Conditioning Netlist Audit

Generated from the full hierarchical KiCad netlist. This is the electrical source of truth for the legacy LM393 section before Rev A removal/rework.

- components in netlist: **191**
- nets in netlist: **152**
- nets touching U702/U703: **0**
- refs electrically adjacent to U702/U703: **2**

## Comparator devices

| Ref | Value | Footprint |
|---|---|---|
| U702 | <missing> | `` |
| U703 | <missing> | `` |

## Every net touching U702/U703

## Hall / EOL / encoder named nets

- `/BROTHER-CONNECTORS/ENC_BELTPHASE`: J405:6, J410:5, J413:5, J702:3, R705:1, R706:2, U701:5
- `/BROTHER-CONNECTORS/ENC_V1`: J405:4, J410:4, J413:4, J702:1, R701:1, R702:2, U701:3
- `/BROTHER-CONNECTORS/ENC_V2`: J405:5, J410:3, J413:3, J702:2, R703:1, R704:2, U701:4
- `/BROTHER-CONNECTORS/EOL_L`: J408:3, J411:3, J414:3, R735:1, TP701:1
- `/BROTHER-CONNECTORS/EOL_R`: J409:3, J412:3, R737:1, TP702:1
- `/BROTHER-CONNECTORS/EOL_R_N`: J202:2, J405:8, R213:2, U201:21
- `/BROTHER-CONNECTORS/EOL_R_S`: J202:3, J405:7, R214:2, U201:22
- `/ESP32/ENC_A`: J701:1, U201:9, U701:21
- `/ESP32/ENC_B`: J701:2, U201:10, U701:20
- `/ESP32/ENC_BP`: J701:3, U201:11, U701:19
- `/ESP32/HALL_L_ADC`: R735:2, R736:1, U201:5
- `/ESP32/HALL_R_ADC`: R737:2, R738:1, U201:6
- `/IO CONDITIONING/EOL_L_K`: J702:4, R707:1, R708:2, U701:6
- `/IO CONDITIONING/EOL_L_L`: J702:5, R709:1, R710:2, U701:7

## Local conditioning component topology

This table lists every connected pin for U701-U703, C701-C704, TP701/TP702 and R701-R738. It is the removal decision table.

| Ref | Value | Pin 1 / net | Pin 2 / net | Other pins / nets |
|---|---|---|---|---|
| C701 | 100n | `+3V3` | `GND` | — |
| C702 | 100n | `+5V` | `GND` | — |
| R701 | 10k | `/BROTHER-CONNECTORS/ENC_V1` | `GND` | — |
| R702 | 10k | `+5V` | `/BROTHER-CONNECTORS/ENC_V1` | — |
| R703 | 10k | `/BROTHER-CONNECTORS/ENC_V2` | `GND` | — |
| R704 | 10k | `+5V` | `/BROTHER-CONNECTORS/ENC_V2` | — |
| R705 | 10k | `/BROTHER-CONNECTORS/ENC_BELTPHASE` | `GND` | — |
| R706 | 10k | `+5V` | `/BROTHER-CONNECTORS/ENC_BELTPHASE` | — |
| R707 | 10k | `/IO CONDITIONING/EOL_L_K` | `GND` | — |
| R708 | 10k | `+5V` | `/IO CONDITIONING/EOL_L_K` | — |
| R709 | 10k | `/IO CONDITIONING/EOL_L_L` | `GND` | — |
| R710 | 10k | `+5V` | `/IO CONDITIONING/EOL_L_L` | — |
| R711 | 10k | `Net-(J702-Pin_6)` | `GND` | — |
| R712 | 10k | `+5V` | `Net-(J702-Pin_6)` | — |
| R713 | 10k | `Net-(J702-Pin_7)` | `GND` | — |
| R714 | 10k | `+5V` | `Net-(J702-Pin_7)` | — |
| R735 | 10k | `/BROTHER-CONNECTORS/EOL_L` | `/ESP32/HALL_L_ADC` | — |
| R736 | 10k | `/ESP32/HALL_L_ADC` | `GND` | — |
| R737 | 10k | `/BROTHER-CONNECTORS/EOL_R` | `/ESP32/HALL_R_ADC` | — |
| R738 | 10k | `/ESP32/HALL_R_ADC` | `GND` | — |
| TP701 | HALL-L-RAW | `/BROTHER-CONNECTORS/EOL_L` (1) | — | — |
| TP702 | HALL-R-RAW | `/BROTHER-CONNECTORS/EOL_R` (1) | — | — |
| U701 | SN74LVC4245 | `+5V` (5V) | `+5V` (DIR) | 3: `/BROTHER-CONNECTORS/ENC_V1` (A1); 4: `/BROTHER-CONNECTORS/ENC_V2` (A2); 5: `/BROTHER-CONNECTORS/ENC_BELTPHASE` (A3); 6: `/IO CONDITIONING/EOL_L_K` (A4); 7: `/IO CONDITIONING/EOL_L_L` (A5); 8: `Net-(J702-Pin_6)` (A6); 9: `Net-(J702-Pin_7)` (A7); 10: `Net-(J702-Pin_8)` (A8); 11: `GND` (GND); 12: `GND` (GND); 13: `GND` (GND); 14: `Net-(J701-Pin_8)` (B8); 15: `Net-(J701-Pin_7)` (B7); 16: `Net-(J701-Pin_6)` (B6); 17: `Net-(J701-Pin_5)` (B5); 18: `Net-(J701-Pin_4)` (B4); 19: `/ESP32/ENC_BP` (B3); 20: `/ESP32/ENC_B` (B2); 21: `/ESP32/ENC_A` (B1); 22: `GND` (~{OE}); 23: `+3V3` (3V3); 24: `+3V3` (3V3) |

## Adjacent component inventory

| Ref | Value | Footprint |
|---|---|---|
| U702 |  | `` |
| U703 |  | `` |

## Rev A interpretation gate

Do not delete U702/U703 by reference alone. The removal patch must preserve the passive HALL_L_ADC/HALL_R_ADC dividers and the encoder path, then be verified by ERC plus a regenerated netlist.
