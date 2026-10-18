#pragma once
#include <stdint.h>
#include "reva_pins.h"
// Safe input-only abstraction. Never connects pins to power or solenoids.
#ifdef ARDUINO
#include <Arduino.h>
namespace reva {
struct Snapshot {
  uint16_t hall_left, hall_right, machine_power;
  bool encoder_a, encoder_b, encoder_bp, kh910_r_k, kh910_r_l;
};
inline void initInputs() {
  pinMode(ENC_A, INPUT); pinMode(ENC_B, INPUT); pinMode(ENC_BP, INPUT);
  pinMode(KH910_R_K, INPUT); pinMode(KH910_R_L, INPUT);
  pinMode(USER_BUTTON, INPUT);
  analogReadResolution(12);
}
inline Snapshot readInputs() {
  return {static_cast<uint16_t>(analogRead(HALL_L_ADC)),
          static_cast<uint16_t>(analogRead(HALL_R_ADC)),
          static_cast<uint16_t>(analogRead(MACHINE_PWR_SENSE)),
          bool(digitalRead(ENC_A)),bool(digitalRead(ENC_B)),
          bool(digitalRead(ENC_BP)),bool(digitalRead(KH910_R_K)),
          bool(digitalRead(KH910_R_L))};
}
}
#endif