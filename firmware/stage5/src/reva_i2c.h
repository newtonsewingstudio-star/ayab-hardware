#pragma once
// Read-only I2C probing. NO expander writes; no solenoid operation.
#ifdef ARDUINO
#include <Arduino.h>
#include <Wire.h>
#include "reva_pins.h"
namespace reva {
inline void initI2C0() { Wire.begin(I2C0_SDA,I2C0_SCL,100000); }
inline bool probeI2C0(uint8_t address) {
  if(address < 0x08 || address > 0x77) return false;
  Wire.beginTransmission(address);
  return Wire.endTransmission() == 0;
}
}
#endif
