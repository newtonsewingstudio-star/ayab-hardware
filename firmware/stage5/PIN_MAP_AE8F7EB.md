# Rev A MCU pin map: fabrication commit ae8f7eb
Source: https://github.com/newtonsewingstudio-star/ayab-hardware/blob/ae8f7eb/ayab-esp32/mcu.kicad_sch

Mapping follows symbol pin coordinates, sheet hierarchical labels, and direct wires in the named MCU schematic, **not** the BOM or CPL. This is the MCU net map; expander and Brother connector signal mapping needs separate cross-sheet connectivity verification.

| GPIO | Net |
|---:|---|
| 0 | BOOT0 |
| 1 | HALL_L_ADC |
| 2 | HALL_R_ADC |
| 3 | No named signal identified |
| 4 | MACHINE_PWR_SENSE |
| 5 | ENC_A |
| 6 | ENC_B |
| 7 | ENC_BP |
| 8 | I2C0_SDA |
| 9 | I2C0_SCL |
| 10 | DISPLAY_CS |
| 11 | SPI0_CIPO |
| 12 | SPI0_COPI |
| 13 | SPI0_SCK |
| 14 | FRONT_PANEL_AUX |
| 15 | I2C1_SDA |
| 16 | I2C1_SCL |
| 17 | KH910_R_K |
| 18 | KH910_R_L |
| 19 | USB_M |
| 20 | USB_P |
| 21 | No named signal identified |
| 26 | No named signal identified |
| 33 | RED |
| 34 | GRN |
| 35 | YEL |
| 36 | USER_BUTTON |
| 37 | No named signal identified |
| 38 | BUZZER |
| 39 | PANEL_INT |
| 40 | ESP40 |
| 41 | ESP41 |
| 42 | ESP42 |
| 43 | UART_TX |
| 44 | UART_RX |
| 45 | VCC_SPI |
| 46 | BOOT1 |
| 47 | No named signal identified |
| 48 | No named signal identified |

CAUTION: GPIO45/46 have boot strapping implications. No outputs initialized. Do not infer voltage levels or enable outputs from net names alone.