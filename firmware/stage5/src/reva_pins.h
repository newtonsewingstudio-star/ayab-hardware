#pragma once
// Derived from newtonsewingstudio-star/ayab-hardware commit ae8f7eb,
// ayab-esp32/mcu.kicad_sch. Names describe electrical nets, not polarities.
namespace reva {
constexpr int HALL_L_ADC=1, HALL_R_ADC=2, MACHINE_PWR_SENSE=4;
constexpr int ENC_A=5, ENC_B=6, ENC_BP=7;
constexpr int I2C0_SDA=8, I2C0_SCL=9;
constexpr int DISPLAY_CS=10, SPI0_CIPO=11, SPI0_COPI=12, SPI0_SCK=13;
constexpr int FRONT_PANEL_AUX=14, I2C1_SDA=15, I2C1_SCL=16;
constexpr int KH910_R_K=17, KH910_R_L=18;
constexpr int USB_D_MINUS=19, USB_D_PLUS=20;
constexpr int LED_RED=33, LED_GREEN=34, LED_YELLOW=35;
constexpr int USER_BUTTON=36, BUZZER=38, PANEL_INT=39;
constexpr int UART_TX=43, UART_RX=44, BOOT0=0, BOOT1=46;
// ESP40, ESP41, ESP42 are schematic net labels on GPIO 40,41,42.
constexpr int ESP40=40, ESP41=41, ESP42=42;
// GPIOs with no direct named net found: 3,21,26,37,47,48.
}