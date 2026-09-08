# AYAB-ESP32 KH910 Rev A — Current MCU Pin Audit

Generated automatically from `mcu.kicad_sch` by `tools/audit_esp32_pinmap.py`.

This report describes the **current electrical connectivity**, not the desired Rev A design. The target column comes from `KH910_REV_A_IO_MAP.md`.

- ESP32 instance origin: `139.7, 92.71`, rotation `0`
- GPIOs extracted: **39**
- Target-function mismatches: **24**
- Native USB GPIO19 current labels: `USB_M`
- Native USB GPIO20 current labels: `USB_P`

| GPIO | Module pin | ESP32 symbol function | Current attached net/label(s) | Rev A target | Status |
|---:|---:|---|---|---|---|
| 0 | 4 | `GPIO0/BOOT` | — | `—` | **open** |
| 1 | 5 | `GPIO1/TOUCH1/ADC1_CH0` | — | `HALL_L_ADC` | **MISMATCH** |
| 2 | 6 | `GPIO2/TOUCH2/ADC1_CH1` | — | `HALL_R_ADC` | **MISMATCH** |
| 3 | 7 | `GPIO3/TOUCH3/ADC1_CH2` | `SPI0_SCK` | `RESERVED_STRAP` | **review** |
| 4 | 8 | `GPIO4/TOUCH4/ADC1_CH3` | `SPI0_COPI` | `MACHINE_PWR_SENSE` | **MISMATCH** |
| 5 | 9 | `GPIO5/TOUCH5/ADC1_CH4` | `SPI0_CIPO` | `ENC_A` | **MISMATCH** |
| 6 | 10 | `GPIO6/TOUCH6/ADC1_CH5` | `DISPLAY_CS` | `ENC_B` | **MISMATCH** |
| 7 | 11 | `GPIO7/TOUCH7/ADC1_CH6` | `I2C0_SCL` | `ENC_C` | **MISMATCH** |
| 8 | 12 | `GPIO8/TOUCH8/ADC1_CH7/SUBSPICS1` | `I2C0_SDA` | `I2C0_SDA` | **OK** |
| 9 | 13 | `GPIO9/TOUCH9/ADC1_CH8/FSPIHD/SUBSPIHD` | `ENC_BP` | `I2C0_SCL` | **MISMATCH** |
| 10 | 14 | `GPIO10/TOUCH10/ADC1_CH9/FSPICS0/FSPIIO4/SUBSPICS0` | `ENC_B` | `DISPLAY_CS` | **MISMATCH** |
| 11 | 15 | `GPIO11/TOUCH11/ADC2_CH0/FSPID/FSPIIO5/SUBSPID` | `ENC_A` | `SPI0_CIPO` | **MISMATCH** |
| 12 | 16 | `GPIO12/TOUCH12/ADC2_CH1/FSPICLK/FSPIIO6/SUBSPICLK` | `EOL_R_N` | `SPI0_COPI` | **MISMATCH** |
| 13 | 17 | `GPIO13/TOUCH13/ADC2_CH2/FSPIQ/FSPIIO7/SUBSPIQ` | `EOL_R_P` | `SPI0_SCK` | **MISMATCH** |
| 14 | 18 | `GPIO14/TOUCH14/ADC2_CH3/FSPIWP/FSPIDQS/SUBSPIWP` | `EOL_L_N` | `FRONT_PANEL_AUX` | **MISMATCH** |
| 15 | 19 | `GPIO15/U0RTS/ADC2_CH4/XTAL_32K_P` | `YEL` | `I2C1_SDA` | **MISMATCH** |
| 16 | 20 | `GPIO16/U0CTS/ADC2_CH5/XTAL_32K_N` | `GRN` | `I2C1_SCL` | **MISMATCH** |
| 17 | 21 | `GPIO17/U1TXD/ADC2_CH6` | `EOL_L_P` | `KH910_R_K` | **MISMATCH** |
| 18 | 22 | `GPIO18/U1RXD/ADC2_CH7/CLK_OUT3` | `BOOT0` | `KH910_R_L` | **MISMATCH** |
| 19 | 23 | `GPIO19/U1RTS/ADC2_CH8/CLK_OUT2/USB_D-` | `USB_M` | `USB_M` | **OK** |
| 20 | 24 | `GPIO20/U1CTS/ADC2_CH9/CLK_OUT1/USB_D+` | `USB_P` | `USB_P` | **OK** |
| 21 | 25 | `GPIO21` | — | `SOLENOID_PWR_EN` | **MISMATCH** |
| 26 | 26 | `GPIO26` | — | `—` | **open** |
| 33 | 28 | `SPIIO4/GPIO33/FSPIHD/SUBSPIHD` | — | `LED_R` | **MISMATCH** |
| 34 | 29 | `SPIIO5/GPIO34/FSPICS0/SUBSPICS0` | `I2C1_SCL` | `LED_G` | **MISMATCH** |
| 35 | 31 | `SPIIO6/GPIO35/FSPID/SUBSPID` | `I2C1_SDA` | `LED_B` | **MISMATCH** |
| 36 | 32 | `SPIIO7/GPIO36/FSPICLK/SUBSPICLK` | — | `USER_BUTTON` | **MISMATCH** |
| 37 | 33 | `SPIDQS/GPIO37/FSPIQ/SUBSPIQ` | `nRST` | `—` | **review** |
| 38 | 34 | `GPIO38/FSPIWP/SUBSPIWP` | `BUZZER` | `BUZZER` | **OK** |
| 39 | 35 | `MTCK/GPIO39/CLK_OUT3/SUBSPICS1` | — | `PANEL_INT` | **MISMATCH** |
| 40 | 36 | `MTDO/GPIO40/CLK_OUT2` | — | `SPARE` | **open** |
| 41 | 37 | `MTDI/GPIO41/CLK_OUT1` | — | `SPARE` | **open** |
| 42 | 38 | `MTMS/GPIO42` | — | `SPARE` | **open** |
| 43 | 39 | `U0TXD/GPIO43/CLK_OUT1` | — | `UART_TX` | **MISMATCH** |
| 44 | 40 | `U0RXD/GPIO44/CLK_OUT2` | — | `UART_RX` | **MISMATCH** |
| 45 | 41 | `GPIO45` | — | `RESERVED_STRAP` | **open** |
| 46 | 44 | `GPIO46` | — | `RESERVED_STRAP` | **open** |
| 47 | 27 | `GPIO47/SPICLK_P/SUBSPICLK_P_DIFF` | `UART_RX` | `SPARE` | **review** |
| 48 | 30 | `GPIO48/SPICLK_N/SUBSPICLK_N_DIFF` | `UART_TX` | `SPARE` | **review** |

## Interpretation rules

- **OK** means the current named net matches the Rev A target or an explicit compatibility alias.
- **MISMATCH** means the GPIO is occupied by a different function or the expected function is absent.
- **review** means a pin intended to be spare/reserved is currently labeled and must be examined before reuse.
- **open** means a spare/reserved pin has no meaningful label on the MCU sheet.

## Fabrication rule

Do not fabricate while any critical target (USB, encoder, KH-910 K/L, Hall ADC, power enable, internal I2C) remains `MISMATCH`.
