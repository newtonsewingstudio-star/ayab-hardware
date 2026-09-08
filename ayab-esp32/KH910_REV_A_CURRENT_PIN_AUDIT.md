# AYAB-ESP32 KH910 Rev A — Current MCU Pin Audit

Generated automatically from `mcu.kicad_sch` by `tools/audit_esp32_pinmap.py`.

This report describes the **current electrical connectivity**, not the desired Rev A design. The target column comes from `KH910_REV_A_IO_MAP.md`.

- ESP32 instance origin: `139.7, 92.71`, rotation `0`
- GPIOs extracted: **39**
- Target-function mismatches: **8**
- Native USB GPIO19 current labels: `USB_M`
- Native USB GPIO20 current labels: `USB_P`

| GPIO | Sheet coordinate | Module pin | ESP32 symbol function | Current attached net/label(s) | Rev A target | Status |
|---:|---|---:|---|---|---|---|
| 0 | `185.42, 72.39` | 4 | `GPIO0/BOOT` | `BOOT0` | `—` | **review** |
| 1 | `185.42, 74.93` | 5 | `GPIO1/TOUCH1/ADC1_CH0` | `HALL_L_ADC` | `HALL_L_ADC` | **OK** |
| 2 | `185.42, 77.47` | 6 | `GPIO2/TOUCH2/ADC1_CH1` | `HALL_R_ADC` | `HALL_R_ADC` | **OK** |
| 3 | `185.42, 80.01` | 7 | `GPIO3/TOUCH3/ADC1_CH2` | — | `RESERVED_STRAP` | **open** |
| 4 | `185.42, 82.55` | 8 | `GPIO4/TOUCH4/ADC1_CH3` | — | `MACHINE_PWR_SENSE` | **MISMATCH** |
| 5 | `185.42, 85.09` | 9 | `GPIO5/TOUCH5/ADC1_CH4` | `ENC_A` | `ENC_A` | **OK** |
| 6 | `185.42, 87.63` | 10 | `GPIO6/TOUCH6/ADC1_CH5` | `ENC_B` | `ENC_B` | **OK** |
| 7 | `185.42, 90.17` | 11 | `GPIO7/TOUCH7/ADC1_CH6` | `ENC_BP` | `ENC_C` | **OK** |
| 8 | `185.42, 92.71` | 12 | `GPIO8/TOUCH8/ADC1_CH7/SUBSPICS1` | `I2C0_SDA` | `I2C0_SDA` | **OK** |
| 9 | `185.42, 95.25` | 13 | `GPIO9/TOUCH9/ADC1_CH8/FSPIHD/SUBSPIHD` | `I2C0_SCL` | `I2C0_SCL` | **OK** |
| 10 | `185.42, 97.79` | 14 | `GPIO10/TOUCH10/ADC1_CH9/FSPICS0/FSPIIO4/SUBSPICS0` | `DISPLAY_CS` | `DISPLAY_CS` | **OK** |
| 11 | `185.42, 100.33` | 15 | `GPIO11/TOUCH11/ADC2_CH0/FSPID/FSPIIO5/SUBSPID` | `SPI0_CIPO`, `SPI0_COPI`, `SPI0_SCK` | `SPI0_CIPO` | **OK** |
| 12 | `185.42, 102.87` | 16 | `GPIO12/TOUCH12/ADC2_CH1/FSPICLK/FSPIIO6/SUBSPICLK` | `SPI0_CIPO`, `SPI0_COPI`, `SPI0_SCK` | `SPI0_COPI` | **OK** |
| 13 | `185.42, 105.41` | 17 | `GPIO13/TOUCH13/ADC2_CH2/FSPIQ/FSPIIO7/SUBSPIQ` | `SPI0_CIPO`, `SPI0_COPI`, `SPI0_SCK` | `SPI0_SCK` | **OK** |
| 14 | `185.42, 107.95` | 18 | `GPIO14/TOUCH14/ADC2_CH3/FSPIWP/FSPIDQS/SUBSPIWP` | — | `FRONT_PANEL_AUX` | **MISMATCH** |
| 15 | `93.98, 62.23` | 19 | `GPIO15/U0RTS/ADC2_CH4/XTAL_32K_P` | `I2C1_SDA` | `I2C1_SDA` | **OK** |
| 16 | `93.98, 64.77` | 20 | `GPIO16/U0CTS/ADC2_CH5/XTAL_32K_N` | `I2C1_SCL` | `I2C1_SCL` | **OK** |
| 17 | `185.42, 110.49` | 21 | `GPIO17/U1TXD/ADC2_CH6` | `KH910_R_K` | `KH910_R_K` | **OK** |
| 18 | `185.42, 113.03` | 22 | `GPIO18/U1RXD/ADC2_CH7/CLK_OUT3` | `KH910_R_L` | `KH910_R_L` | **OK** |
| 19 | `185.42, 67.31` | 23 | `GPIO19/U1RTS/ADC2_CH8/CLK_OUT2/USB_D-` | `USB_M` | `USB_M` | **OK** |
| 20 | `185.42, 64.77` | 24 | `GPIO20/U1CTS/ADC2_CH9/CLK_OUT1/USB_D+` | `USB_P` | `USB_P` | **OK** |
| 21 | `185.42, 115.57` | 25 | `GPIO21` | — | `SOLENOID_PWR_EN` | **MISMATCH** |
| 26 | `93.98, 115.57` | 26 | `GPIO26` | — | `—` | **open** |
| 33 | `93.98, 118.11` | 28 | `SPIIO4/GPIO33/FSPIHD/SUBSPIHD` | `RED` | `LED_R` | **MISMATCH** |
| 34 | `93.98, 120.65` | 29 | `SPIIO5/GPIO34/FSPICS0/SUBSPICS0` | `GRN` | `LED_G` | **MISMATCH** |
| 35 | `93.98, 123.19` | 31 | `SPIIO6/GPIO35/FSPID/SUBSPID` | `YEL` | `LED_B` | **MISMATCH** |
| 36 | `93.98, 125.73` | 32 | `SPIIO7/GPIO36/FSPICLK/SUBSPICLK` | — | `USER_BUTTON` | **MISMATCH** |
| 37 | `93.98, 128.27` | 33 | `SPIDQS/GPIO37/FSPIQ/SUBSPIQ` | — | `—` | **open** |
| 38 | `185.42, 118.11` | 34 | `GPIO38/FSPIWP/SUBSPIWP` | `BUZZER` | `BUZZER` | **OK** |
| 39 | `93.98, 69.85` | 35 | `MTCK/GPIO39/CLK_OUT3/SUBSPICS1` | — | `PANEL_INT` | **MISMATCH** |
| 40 | `93.98, 72.39` | 36 | `MTDO/GPIO40/CLK_OUT2` | — | `SPARE` | **open** |
| 41 | `93.98, 74.93` | 37 | `MTDI/GPIO41/CLK_OUT1` | — | `SPARE` | **open** |
| 42 | `93.98, 77.47` | 38 | `MTMS/GPIO42` | — | `SPARE` | **open** |
| 43 | `185.42, 57.15` | 39 | `U0TXD/GPIO43/CLK_OUT1` | `UART_TX` | `UART_TX` | **OK** |
| 44 | `185.42, 59.69` | 40 | `U0RXD/GPIO44/CLK_OUT2` | `UART_RX` | `UART_RX` | **OK** |
| 45 | `185.42, 120.65` | 41 | `GPIO45` | `VCC_SPI` | `RESERVED_STRAP` | **review** |
| 46 | `185.42, 123.19` | 44 | `GPIO46` | `BOOT1` | `RESERVED_STRAP` | **review** |
| 47 | `185.42, 125.73` | 27 | `GPIO47/SPICLK_P/SUBSPICLK_P_DIFF` | — | `SPARE` | **open** |
| 48 | `185.42, 128.27` | 30 | `GPIO48/SPICLK_N/SUBSPICLK_N_DIFF` | — | `SPARE` | **open** |

## Interpretation rules

- **OK** means the current named net matches the Rev A target or an explicit compatibility alias.
- **MISMATCH** means the GPIO is occupied by a different function or the expected function is absent.
- **review** means a pin intended to be spare/reserved is currently labeled and must be examined before reuse.
- **open** means a spare/reserved pin has no meaningful label on the MCU sheet.

## Fabrication rule

Do not fabricate while any critical target (USB, encoder, KH-910 K/L, Hall ADC, power enable, internal I2C) remains `MISMATCH`.
