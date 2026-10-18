#include "../src/reva_pins.h"
#include <cassert>
int main() {
  static_assert(reva::HALL_L_ADC == 1);
  static_assert(reva::HALL_R_ADC == 2);
  static_assert(reva::I2C0_SDA == 8);
  static_assert(reva::I2C0_SCL == 9);
  static_assert(reva::I2C1_SDA == 15);
  static_assert(reva::I2C1_SCL == 16);
  static_assert(reva::USB_D_MINUS == 19);
  static_assert(reva::USB_D_PLUS == 20);
  assert(reva::ENC_A != reva::ENC_B);
}
