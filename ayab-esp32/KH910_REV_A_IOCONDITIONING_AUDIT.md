# KH910 Rev A — I/O Conditioning Netlist Audit

Generated from the full hierarchical KiCad netlist. This is the electrical source of truth for the legacy LM393 section before Rev A removal/rework.

- components in netlist: **212**
- nets in netlist: **160**
- nets touching U702/U703: **12**
- refs electrically adjacent to U702/U703: **136**

## Comparator devices

| Ref | Value | Footprint |
|---|---|---|
| U702 | LM393 | `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` |
| U703 | LM393 | `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` |

## Every net touching U702/U703

### `+5V` (code 2)

| Ref | Pin | Function | Type | Value |
|---|---:|---|---|---|
| C602 | 1 |  | passive | 10u |
| C609 | 1 |  | passive | 220u |
| C611 | 1 |  | passive | 10u |
| C702 | 1 |  | passive | 100n |
| C703 | 2 |  | passive | 100n |
| C704 | 2 |  | passive | 100n |
| J405 | 1 | Pin_1 | passive | 910.950 ENCODERS EOL R |
| J408 | 1 | Pin_1 | passive | 910.950 EOL L |
| J409 | 1 | Pin_1 | passive | 930.940 EOL R |
| J410 | 1 | Pin_1 | passive | 930.940 ENCODERS |
| J411 | 1 | Pin_1 | passive | 900.965 EOL L |
| J412 | 1 | Pin_1 | passive | 900.965 EOL R |
| J413 | 1 | Pin_1 | passive | 900.965 ENCODERS |
| J414 | 1 | Pin_1 | passive | 930.940 EOL L |
| J602 | 5 | Pin_5 | passive | Brother_5P |
| J604 | 4 | Pin_4 | passive | Brother_4R |
| J802 | 3 | Pin_3 | passive | I2C_VBUS |
| J804 | 3 | Pin_3 | passive | I2C_VBUS |
| Q501 | 4 | E2 | passive | BCM857BV |
| Q502 | 2 | S | passive | LP9435LT1G |
| R604 | 1 |  | passive | 5k1 |
| R702 | 1 |  | passive | 10k |
| R704 | 1 |  | passive | 10k |
| R706 | 1 |  | passive | 10k |
| R708 | 1 |  | passive | 10k |
| R710 | 1 |  | passive | 10k |
| R712 | 1 |  | passive | 10k |
| R714 | 1 |  | passive | 10k |
| R723 | 1 |  | passive | 4k7 |
| R725 | 1 |  | passive | 4k7 |
| R727 | 1 |  | passive | 3k3 |
| R729 | 1 |  | passive | 3k3 |
| R733 | 1 |  | passive | 47k |
| R734 | 1 |  | passive | 47k |
| U403 | 3 | CE | input | LM66100DCKR |
| U403 | 6 | VOUT | power_out | LM66100DCKR |
| U602 | 1 | VIN | input | XL1509 |
| U701 | 1 | 5V | power_in | SN74LVC4245 |
| U701 | 2 | DIR | input | SN74LVC4245 |
| U702 | 8 | V+ | power_in | LM393 |
| U703 | 8 | V+ | power_in | LM393 |

### `/BROTHER-CONNECTORS/EOL_L` (code 26)

| Ref | Pin | Function | Type | Value |
|---|---:|---|---|---|
| J408 | 3 | Pin_3 | passive | 910.950 EOL L |
| J411 | 3 | Pin_3 | passive | 900.965 EOL L |
| J414 | 3 | Pin_3 | passive | 930.940 EOL L |
| R731 | 1 |  | passive | 22k |
| R733 | 2 |  | passive | 47k |
| R735 | 1 |  | passive | 10k |
| TP701 | 1 | 1 | passive | CMP-L |
| U702 | 3 | + | input | LM393 |
| U702 | 6 | - | input | LM393 |

### `/BROTHER-CONNECTORS/EOL_R` (code 27)

| Ref | Pin | Function | Type | Value |
|---|---:|---|---|---|
| J409 | 3 | Pin_3 | passive | 930.940 EOL R |
| J412 | 3 | Pin_3 | passive | 900.965 EOL R |
| R732 | 1 |  | passive | 22k |
| R734 | 2 |  | passive | 47k |
| R737 | 1 |  | passive | 10k |
| TP702 | 1 | 1 | passive | CMP-R |
| U703 | 3 | + | input | LM393 |
| U703 | 6 | - | input | LM393 |

### `/IO CONDITIONING/EOL_L_K` (code 68)

| Ref | Pin | Function | Type | Value |
|---|---:|---|---|---|
| J702 | 4 | Pin_4 | passive | CTRL_5V |
| R707 | 1 |  | passive | 10k |
| R708 | 2 |  | passive | 10k |
| R715 | 1 |  | passive | 100k |
| U701 | 6 | A4 | bidirectional | SN74LVC4245 |
| U702 | 1 |  | open_collector | LM393 |

### `/IO CONDITIONING/EOL_L_L` (code 69)

| Ref | Pin | Function | Type | Value |
|---|---:|---|---|---|
| J702 | 5 | Pin_5 | passive | CTRL_5V |
| R709 | 1 |  | passive | 10k |
| R710 | 2 |  | passive | 10k |
| R716 | 2 |  | passive | 100k |
| U701 | 7 | A5 | bidirectional | SN74LVC4245 |
| U702 | 7 |  | open_collector | LM393 |

### `GND` (code 93)

| Ref | Pin | Function | Type | Value |
|---|---:|---|---|---|
| C201 | 2 |  | passive | 100n |
| C202 | 2 |  | passive | 100n |
| C203 | 2 |  | passive | 100n |
| C204 | 2 |  | passive | 100n |
| C205 | 2 |  | passive | 10u |
| C301 | 2 |  | passive | 100n |
| C302 | 2 |  | passive | 10u |
| C303 | 2 |  | passive | 10u |
| C304 | 2 |  | passive | 10u |
| C305 | 2 |  | passive | 100n |
| C501 | 2 |  | passive | 47p |
| C502 | 2 |  | passive | 47p |
| C601 | 2 |  | passive | 10u |
| C602 | 2 |  | passive | 10u |
| C603 | 2 |  | passive | 10u |
| C604 | 2 |  | passive | 10u |
| C605 | 2 |  | passive | 10u |
| C606 | 2 |  | passive | 220u |
| C607 | 2 |  | passive | 220u |
| C609 | 2 |  | passive | 220u |
| C610 | 2 |  | passive | 10u |
| C611 | 2 |  | passive | 10u |
| C612 | 2 |  | passive | 220u |
| C613 | 2 |  | passive | 220u |
| C616 | 2 |  | passive | 10u |
| C617 | 2 |  | passive | 10u |
| C618 | 2 |  | passive | 10u |
| C619 | 2 |  | passive | 10u |
| C620 | 2 |  | passive | 10u |
| C621 | 2 |  | passive | 10u |
| C701 | 2 |  | passive | 100n |
| C702 | 2 |  | passive | 100n |
| C703 | 1 |  | passive | 100n |
| C704 | 1 |  | passive | 100n |
| D601 | 4 | - | passive | KMB14F |
| D602 | 1 | K | passive | 12VOK |
| D603 | 1 | K | passive | 5VOK |
| D604 | 1 | K | passive | 3V3OK |
| D605 | 2 | A | passive | SS54 |
| D606 | 2 | A | passive | SS54 |
| H101 | 1 | 1 | input | M3 |
| H102 | 1 | 1 | input | M3 |
| H103 | 1 | 1 | input | M3 |
| H104 | 1 | 1 | input | M3 |
| H106 | 1 | 1 | input | M3 |
| H108 | 1 | 1 | input | M3 |
| J405 | 2 | Pin_2 | passive | 910.950 ENCODERS EOL R |
| J408 | 2 | Pin_2 | passive | 910.950 EOL L |
| J409 | 2 | Pin_2 | passive | 930.940 EOL R |
| J410 | 2 | Pin_2 | passive | 930.940 ENCODERS |
| J411 | 2 | Pin_2 | passive | 900.965 EOL L |
| J412 | 2 | Pin_2 | passive | 900.965 EOL R |
| J413 | 2 | Pin_2 | passive | 900.965 ENCODERS |
| J414 | 2 | Pin_2 | passive | 930.940 EOL L |
| J501 | A1 | GND | passive | USB_C_Receptacle_USB2.0 |
| J501 | A12 | GND | passive | USB_C_Receptacle_USB2.0 |
| J501 | B1 | GND | passive | USB_C_Receptacle_USB2.0 |
| J501 | B12 | GND | passive | USB_C_Receptacle_USB2.0 |
| J501 | S1 | SHIELD | passive | USB_C_Receptacle_USB2.0 |
| J602 | 3 | Pin_3 | passive | Brother_5P |
| J602 | 4 | Pin_4 | passive | Brother_5P |
| J604 | 2 | Pin_2 | passive | Brother_4R |
| J604 | 3 | Pin_3 | passive | Brother_4R |
| J801 | 4 | Pin_4 | passive | AYAB_UART |
| J803 | 4 | Pin_4 | passive | USER_I2C |
| J805 | 6 | Pin_6 | passive | AYAB_SPI |
| J806 | 4 | Pin_4 | passive | AYAB_I2C |
| Q201 | 2 | S | passive | AO3400A |
| Q806 | 2 | S | passive | AO3400A |
| R101 | 2 |  | passive | 5k1 |
| R102 | 2 |  | passive | 5k1 |
| R207 | 2 |  | passive | 10k |
| R208 | 2 |  | passive | 10k |
| R211 | 2 |  | passive | 10k |
| R216 | 2 |  | passive | 10k |
| R502 | 2 |  | passive | 100k |
| R503 | 2 |  | passive | 68k |
| R606 | 2 |  | passive | 1k |
| R607 | 2 |  | passive | 1k |
| R701 | 2 |  | passive | 10k |
| R703 | 2 |  | passive | 10k |
| R705 | 2 |  | passive | 10k |
| R707 | 2 |  | passive | 10k |
| R709 | 2 |  | passive | 10k |
| R711 | 2 |  | passive | 10k |
| R713 | 2 |  | passive | 10k |
| R724 | 2 |  | passive | 1k |
| R726 | 2 |  | passive | 1k |
| R728 | 2 |  | passive | 4k7 |
| R730 | 2 |  | passive | 4k7 |
| R731 | 2 |  | passive | 22k |
| R732 | 2 |  | passive | 22k |
| R736 | 2 |  | passive | 10k |
| R738 | 2 |  | passive | 10k |
| R815 | 2 |  | passive | 10k |
| R822 | 1 |  | passive | 100k |
| SW201 | 2 | 2 | passive | USER |
| SW202 | 2 | 2 | passive | RESET |
| SW203 | 2 | 2 | passive | BOOTSEL |
| U201 | 1 | GND | power_in | ESP32-S3-MINI-1 |
| U201 | 2 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 42 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 43 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 46 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 47 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 48 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 49 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 50 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 51 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 52 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 53 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 54 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 55 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 56 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 57 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 58 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 59 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 60 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 61 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 62 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 63 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 64 | GND | passive | ESP32-S3-MINI-1 |
| U201 | 65 | GND | passive | ESP32-S3-MINI-1 |
| U301 | 10 | VSS | power_in | MCP23017_SS |
| U301 | 15 | A0 | input | MCP23017_SS |
| U301 | 16 | A1 | input | MCP23017_SS |
| U301 | 17 | A2 | input | MCP23017_SS |
| U302 | 8 | GND | power_in | ULN2003A |
| U303 | 8 | GND | power_in | ULN2003A |
| U304 | 8 | GND | power_in | ULN2003A |
| U403 | 2 | GND | power_in | LM66100DCKR |
| U403 | 5 | ST | passive | LM66100DCKR |
| U501 | 2 | VN | passive | SRV05-4 |
| U601 | 4 | EN | input | XL1509 |
| U601 | 5 | GND | input | XL1509 |
| U601 | 6 | GND | input | XL1509 |
| U601 | 7 | GND | input | XL1509 |
| U601 | 8 | GND | input | XL1509 |
| U602 | 4 | EN | input | XL1509 |
| U602 | 5 | GND | input | XL1509 |
| U602 | 6 | GND | input | XL1509 |
| U602 | 7 | GND | input | XL1509 |
| U602 | 8 | GND | input | XL1509 |
| U701 | 11 | GND | power_in | SN74LVC4245 |
| U701 | 12 | GND | power_in | SN74LVC4245 |
| U701 | 13 | GND | power_in | SN74LVC4245 |
| U701 | 22 | ~{OE} | input | SN74LVC4245 |
| U702 | 4 | V- | power_in | LM393 |
| U703 | 4 | V- | power_in | LM393 |

### `Net-(J702-Pin_6)` (code 110)

| Ref | Pin | Function | Type | Value |
|---|---:|---|---|---|
| J702 | 6 | Pin_6 | passive | CTRL_5V |
| R711 | 1 |  | passive | 10k |
| R712 | 2 |  | passive | 10k |
| R717 | 1 |  | passive | 100k |
| U701 | 8 | A6 | bidirectional | SN74LVC4245 |
| U703 | 1 |  | open_collector | LM393 |

### `Net-(J702-Pin_7)` (code 111)

| Ref | Pin | Function | Type | Value |
|---|---:|---|---|---|
| J702 | 7 | Pin_7 | passive | CTRL_5V |
| R713 | 1 |  | passive | 10k |
| R714 | 2 |  | passive | 10k |
| R718 | 2 |  | passive | 100k |
| U701 | 9 | A7 | bidirectional | SN74LVC4245 |
| U703 | 7 |  | open_collector | LM393 |

### `Net-(U702A--)` (code 132)

| Ref | Pin | Function | Type | Value |
|---|---:|---|---|---|
| R715 | 2 |  | passive | 100k |
| R719 | 1 |  | passive | 10k |
| U702 | 2 | - | input | LM393 |

### `Net-(U702B-+)` (code 133)

| Ref | Pin | Function | Type | Value |
|---|---:|---|---|---|
| R716 | 1 |  | passive | 100k |
| R720 | 2 |  | passive | 10k |
| U702 | 5 | + | input | LM393 |

### `Net-(U703A--)` (code 134)

| Ref | Pin | Function | Type | Value |
|---|---:|---|---|---|
| R717 | 2 |  | passive | 100k |
| R721 | 1 |  | passive | 10k |
| U703 | 2 | - | input | LM393 |

### `Net-(U703B-+)` (code 135)

| Ref | Pin | Function | Type | Value |
|---|---:|---|---|---|
| R718 | 1 |  | passive | 100k |
| R722 | 2 |  | passive | 10k |
| U703 | 5 | + | input | LM393 |

## Hall / EOL / encoder named nets

- `/BROTHER-CONNECTORS/ENC_BELTPHASE`: J405:6, J410:5, J413:5, J702:3, R705:1, R706:2, U701:5
- `/BROTHER-CONNECTORS/ENC_V1`: J405:4, J410:4, J413:4, J702:1, R701:1, R702:2, U701:3
- `/BROTHER-CONNECTORS/ENC_V2`: J405:5, J410:3, J413:3, J702:2, R703:1, R704:2, U701:4
- `/BROTHER-CONNECTORS/EOL_L`: J408:3, J411:3, J414:3, R731:1, R733:2, R735:1, TP701:1, U702:3, U702:6
- `/BROTHER-CONNECTORS/EOL_R`: J409:3, J412:3, R732:1, R734:2, R737:1, TP702:1, U703:3, U703:6
- `/BROTHER-CONNECTORS/EOL_R_N`: J202:2, J405:8, R213:2, U201:21
- `/BROTHER-CONNECTORS/EOL_R_S`: J202:3, J405:7, R214:2, U201:22
- `/ESP32/ENC_A`: J701:1, U201:9, U701:21
- `/ESP32/ENC_B`: J701:2, U201:10, U701:20
- `/ESP32/ENC_BP`: J701:3, U201:11, U701:19
- `/ESP32/HALL_L_ADC`: R735:2, R736:1, U201:5
- `/ESP32/HALL_R_ADC`: R737:2, R738:1, U201:6
- `/IO CONDITIONING/EOL_L_K`: J702:4, R707:1, R708:2, R715:1, U701:6, U702:1
- `/IO CONDITIONING/EOL_L_L`: J702:5, R709:1, R710:2, R716:2, U701:7, U702:7

## Local conditioning component topology

This table lists every connected pin for U701-U703, C701-C704, TP701/TP702 and R701-R738. It is the removal decision table.

| Ref | Value | Pin 1 / net | Pin 2 / net | Other pins / nets |
|---|---|---|---|---|
| C701 | 100n | `+3V3` | `GND` | — |
| C702 | 100n | `+5V` | `GND` | — |
| C703 | 100n | `GND` | `+5V` | — |
| C704 | 100n | `GND` | `+5V` | — |
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
| R715 | 100k | `/IO CONDITIONING/EOL_L_K` | `Net-(U702A--)` | — |
| R716 | 100k | `Net-(U702B-+)` | `/IO CONDITIONING/EOL_L_L` | — |
| R717 | 100k | `Net-(J702-Pin_6)` | `Net-(U703A--)` | — |
| R718 | 100k | `Net-(U703B-+)` | `Net-(J702-Pin_7)` | — |
| R719 | 10k | `Net-(U702A--)` | `Net-(R719-Pad2)` | — |
| R720 | 10k | `Net-(R720-Pad1)` | `Net-(U702B-+)` | — |
| R721 | 10k | `Net-(U703A--)` | `Net-(R721-Pad2)` | — |
| R722 | 10k | `Net-(R722-Pad1)` | `Net-(U703B-+)` | — |
| R723 | 4k7 | `+5V` | `Net-(R720-Pad1)` | — |
| R724 | 1k | `Net-(R720-Pad1)` | `GND` | — |
| R725 | 4k7 | `+5V` | `Net-(R722-Pad1)` | — |
| R726 | 1k | `Net-(R722-Pad1)` | `GND` | — |
| R727 | 3k3 | `+5V` | `Net-(R719-Pad2)` | — |
| R728 | 4k7 | `Net-(R719-Pad2)` | `GND` | — |
| R729 | 3k3 | `+5V` | `Net-(R721-Pad2)` | — |
| R730 | 4k7 | `Net-(R721-Pad2)` | `GND` | — |
| R731 | 22k | `/BROTHER-CONNECTORS/EOL_L` | `GND` | — |
| R732 | 22k | `/BROTHER-CONNECTORS/EOL_R` | `GND` | — |
| R733 | 47k | `+5V` | `/BROTHER-CONNECTORS/EOL_L` | — |
| R734 | 47k | `+5V` | `/BROTHER-CONNECTORS/EOL_R` | — |
| R735 | 10k | `/BROTHER-CONNECTORS/EOL_L` | `/ESP32/HALL_L_ADC` | — |
| R736 | 10k | `/ESP32/HALL_L_ADC` | `GND` | — |
| R737 | 10k | `/BROTHER-CONNECTORS/EOL_R` | `/ESP32/HALL_R_ADC` | — |
| R738 | 10k | `/ESP32/HALL_R_ADC` | `GND` | — |
| TP701 | CMP-L | `/BROTHER-CONNECTORS/EOL_L` (1) | — | — |
| TP702 | CMP-R | `/BROTHER-CONNECTORS/EOL_R` (1) | — | — |
| U701 | SN74LVC4245 | `+5V` (5V) | `+5V` (DIR) | 3: `/BROTHER-CONNECTORS/ENC_V1` (A1); 4: `/BROTHER-CONNECTORS/ENC_V2` (A2); 5: `/BROTHER-CONNECTORS/ENC_BELTPHASE` (A3); 6: `/IO CONDITIONING/EOL_L_K` (A4); 7: `/IO CONDITIONING/EOL_L_L` (A5); 8: `Net-(J702-Pin_6)` (A6); 9: `Net-(J702-Pin_7)` (A7); 10: `Net-(J702-Pin_8)` (A8); 11: `GND` (GND); 12: `GND` (GND); 13: `GND` (GND); 14: `Net-(J701-Pin_8)` (B8); 15: `Net-(J701-Pin_7)` (B7); 16: `Net-(J701-Pin_6)` (B6); 17: `Net-(J701-Pin_5)` (B5); 18: `Net-(J701-Pin_4)` (B4); 19: `/ESP32/ENC_BP` (B3); 20: `/ESP32/ENC_B` (B2); 21: `/ESP32/ENC_A` (B1); 22: `GND` (~{OE}); 23: `+3V3` (3V3); 24: `+3V3` (3V3) |
| U702 | LM393 | `/IO CONDITIONING/EOL_L_K` | `Net-(U702A--)` (-) | 3: `/BROTHER-CONNECTORS/EOL_L` (+); 4: `GND` (V-); 5: `Net-(U702B-+)` (+); 6: `/BROTHER-CONNECTORS/EOL_L` (-); 7: `/IO CONDITIONING/EOL_L_L`; 8: `+5V` (V+) |
| U703 | LM393 | `Net-(J702-Pin_6)` | `Net-(U703A--)` (-) | 3: `/BROTHER-CONNECTORS/EOL_R` (+); 4: `GND` (V-); 5: `Net-(U703B-+)` (+); 6: `/BROTHER-CONNECTORS/EOL_R` (-); 7: `Net-(J702-Pin_7)`; 8: `+5V` (V+) |

## Adjacent component inventory

| Ref | Value | Footprint |
|---|---|---|
| C201 | 100n | `Capacitor_SMD:C_0603_1608Metric` |
| C202 | 100n | `Capacitor_SMD:C_0603_1608Metric` |
| C203 | 100n | `Capacitor_SMD:C_0603_1608Metric` |
| C204 | 100n | `Capacitor_SMD:C_0603_1608Metric` |
| C205 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C301 | 100n | `Capacitor_SMD:C_0603_1608Metric` |
| C302 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C303 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C304 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C305 | 100n | `Capacitor_SMD:C_0603_1608Metric` |
| C501 | 47p | `Capacitor_SMD:C_0603_1608Metric` |
| C502 | 47p | `Capacitor_SMD:C_0603_1608Metric` |
| C601 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C602 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C603 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C604 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C605 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C606 | 220u | `Capacitor_THT:CP_Radial_D6.3mm_P2.50mm` |
| C607 | 220u | `Capacitor_THT:CP_Radial_D6.3mm_P2.50mm` |
| C609 | 220u | `Capacitor_THT:CP_Radial_D6.3mm_P2.50mm` |
| C610 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C611 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C612 | 220u | `Capacitor_THT:CP_Radial_D6.3mm_P2.50mm` |
| C613 | 220u | `Capacitor_THT:CP_Radial_D6.3mm_P2.50mm` |
| C616 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C617 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C618 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C619 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C620 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C621 | 10u | `Capacitor_SMD:C_0805_2012Metric` |
| C701 | 100n | `Capacitor_SMD:C_0603_1608Metric` |
| C702 | 100n | `Capacitor_SMD:C_0603_1608Metric` |
| C703 | 100n | `Capacitor_SMD:C_0603_1608Metric` |
| C704 | 100n | `Capacitor_SMD:C_0603_1608Metric` |
| D601 | KMB14F | `easyeda2kicad:MBF-SMD_L4.8-W3.8-P2.54-LS6.8-TL` |
| D602 | 12VOK | `Diode_SMD:D_0603_1608Metric` |
| D603 | 5VOK | `Diode_SMD:D_0603_1608Metric` |
| D604 | 3V3OK | `Diode_SMD:D_0603_1608Metric` |
| D605 | SS54 | `Diode_SMD:D_SMA` |
| D606 | SS54 | `Diode_SMD:D_SMA` |
| H101 | M3 | `MountingHole:MountingHole_2.2mm_M2_DIN965_Pad` |
| H102 | M3 | `MountingHole:MountingHole_2.2mm_M2_DIN965_Pad` |
| H103 | M3 | `MountingHole:MountingHole_2.2mm_M2_DIN965_Pad` |
| H104 | M3 | `MountingHole:MountingHole_2.2mm_M2_DIN965_Pad` |
| H106 | M3 | `MountingHole:MountingHole_2.2mm_M2_DIN965_Pad` |
| H108 | M3 | `MountingHole:MountingHole_2.2mm_M2_DIN965_Pad` |
| J405 | 910.950 ENCODERS EOL R | `Library:HNC2-2.5P-10DS` |
| J408 | 910.950 EOL L | `Library:HNC2-2.5P-3DS` |
| J409 | 930.940 EOL R | `easyeda2kicad:CONN-TH_3P-P2.50_X2564WV-03-N0SN` |
| J410 | 930.940 ENCODERS | `easyeda2kicad:CONN-TH_X2564WV-05-N0SN` |
| J411 | 900.965 EOL L | `Library:CONN-TH_3P-P2.00_A2004WV-3P` |
| J412 | 900.965 EOL R | `Library:CONN-TH_3P-P2.00_A2004WV-3P` |
| J413 | 900.965 ENCODERS | `Library:530140510` |
| J414 | 930.940 EOL L | `easyeda2kicad:CONN-TH_3P-P2.50_X2564WV-03-N0SN` |
| J501 | USB_C_Receptacle_USB2.0 | `Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12` |
| J602 | Brother_5P | `Library:Brother_5P` |
| J604 | Brother_4R | `Library:Brother_4P` |
| J702 | CTRL_5V | `Connector_PinHeader_2.54mm:PinHeader_2x04_P2.54mm_Vertical` |
| J801 | AYAB_UART | `Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Horizontal` |
| J802 | I2C_VBUS | `Jumper:SolderJumper-3_P1.3mm_Bridged12_RoundedPad1.0x1.5mm` |
| J803 | USER_I2C | `Connector_JST:JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal` |
| J804 | I2C_VBUS | `Jumper:SolderJumper-3_P1.3mm_Bridged12_RoundedPad1.0x1.5mm` |
| J805 | AYAB_SPI | `Connector_JST:JST_SH_SM06B-SRSS-TB_1x06-1MP_P1.00mm_Horizontal` |
| J806 | AYAB_I2C | `Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Horizontal` |
| Q201 | AO3400A | `Package_TO_SOT_SMD:SOT-23` |
| Q501 | BCM857BV | `Package_TO_SOT_SMD:SOT-363_SC-70-6` |
| Q502 | LP9435LT1G | `Package_TO_SOT_SMD:SOT-23` |
| Q806 | AO3400A | `Package_TO_SOT_SMD:SOT-23` |
| R101 | 5k1 | `Resistor_SMD:R_0603_1608Metric` |
| R102 | 5k1 | `Resistor_SMD:R_0603_1608Metric` |
| R207 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R208 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R211 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R216 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R502 | 100k | `Resistor_SMD:R_0603_1608Metric` |
| R503 | 68k | `Resistor_SMD:R_0603_1608Metric` |
| R604 | 5k1 | `Resistor_SMD:R_0603_1608Metric` |
| R606 | 1k | `Resistor_SMD:R_0603_1608Metric` |
| R607 | 1k | `Resistor_SMD:R_0603_1608Metric` |
| R701 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R702 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R703 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R704 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R705 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R706 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R707 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R708 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R709 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R710 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R711 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R712 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R713 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R714 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R715 | 100k | `Resistor_SMD:R_0603_1608Metric` |
| R716 | 100k | `Resistor_SMD:R_0603_1608Metric` |
| R717 | 100k | `Resistor_SMD:R_0603_1608Metric` |
| R718 | 100k | `Resistor_SMD:R_0603_1608Metric` |
| R719 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R720 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R721 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R722 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R723 | 4k7 | `Resistor_SMD:R_0603_1608Metric` |
| R724 | 1k | `Resistor_SMD:R_0603_1608Metric` |
| R725 | 4k7 | `Resistor_SMD:R_0603_1608Metric` |
| R726 | 1k | `Resistor_SMD:R_0603_1608Metric` |
| R727 | 3k3 | `Resistor_SMD:R_0603_1608Metric` |
| R728 | 4k7 | `Resistor_SMD:R_0603_1608Metric` |
| R729 | 3k3 | `Resistor_SMD:R_0603_1608Metric` |
| R730 | 4k7 | `Resistor_SMD:R_0603_1608Metric` |
| R731 | 22k | `Resistor_SMD:R_0603_1608Metric` |
| R732 | 22k | `Resistor_SMD:R_0603_1608Metric` |
| R733 | 47k | `Resistor_SMD:R_0603_1608Metric` |
| R734 | 47k | `Resistor_SMD:R_0603_1608Metric` |
| R735 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R736 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R737 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R738 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R815 | 10k | `Resistor_SMD:R_0603_1608Metric` |
| R822 | 100k | `Resistor_SMD:R_0603_1608Metric` |
| SW201 | USER | `easyeda2kicad:KEY-TH_4P-L7.5-W11.5-P4.5` |
| SW202 | RESET | `easyeda2kicad:KEY-TH_4P-L7.5-W11.5-P4.5` |
| SW203 | BOOTSEL | `easyeda2kicad:KEY-TH_4P-L7.5-W11.5-P4.5` |
| TP701 | CMP-L | `TestPoint:TestPoint_Pad_D1.0mm` |
| TP702 | CMP-R | `TestPoint:TestPoint_Pad_D1.0mm` |
| U201 | ESP32-S3-MINI-1 | `Espressif:ESP32-S3-MINI-1` |
| U301 | MCP23017_SS | `Package_SO:SSOP-28_5.3x10.2mm_P0.65mm` |
| U302 | ULN2003A | `Package_SO:SOIC-16_3.9x9.9mm_P1.27mm` |
| U303 | ULN2003A | `Package_SO:SOIC-16_3.9x9.9mm_P1.27mm` |
| U304 | ULN2003A | `Package_SO:SOIC-16_3.9x9.9mm_P1.27mm` |
| U403 | LM66100DCKR | `Package_TO_SOT_SMD:SOT-363_SC-70-6` |
| U501 | SRV05-4 | `Package_TO_SOT_SMD:SOT-23-6` |
| U601 | XL1509 | `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` |
| U602 | XL1509 | `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` |
| U701 | SN74LVC4245 | `Package_SO:TSSOP-24_4.4x7.8mm_P0.65mm` |
| U702 | LM393 | `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` |
| U703 | LM393 | `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` |

## Rev A interpretation gate

Do not delete U702/U703 by reference alone. The removal patch must preserve the passive HALL_L_ADC/HALL_R_ADC dividers and the encoder path, then be verified by ERC plus a regenerated netlist.
