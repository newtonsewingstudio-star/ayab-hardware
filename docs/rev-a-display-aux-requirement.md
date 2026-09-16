# Rev A future display / AUX expansion requirement

Before Rev A fabrication, evaluate whether the existing AUX connectors already provide a practical external-display interface. If not, add a small keyed expansion connector intended for a future external display/status panel without committing to a specific screen now.

Preferred interface goals:
- GND
- 3V3
- 5V
- I2C SDA/SCL where practical
- 2-3 spare ESP32 GPIOs so the same connector could also support SPI control/reset/backlight/buttons later
- Prefer an 8-pin keyed JST-style connector if board space, routing, and BOM suitability permit
- Label clearly on silkscreen, e.g. DISPLAY/AUX

Constraints:
- Do not disturb validated Hall, K/L, or solenoid safety work.
- This is a future-proofing convenience feature, not a blocker for current firmware functionality.
- If existing AUX connectors already expose equivalent rails/signals, document that and avoid redundant hardware.
- Any implementation must pass final DRC and release audit before fabrication.
