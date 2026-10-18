// ESP32-S3 USB-only bring-up firmware. GPL-3.0-or-later.
// DANGER: Do not use as a knitting-machine controller.
// GPIO and MCP23017 drivers intentionally NOT initialized.
#include <Arduino.h>
#include "protocol.h"
namespace {
ayab::Decoder decoder;
void sendSlip(const uint8_t* data, size_t length) {
  Serial.write(ayab::END);
  for(size_t i=0;i<length;i++) {
    if(data[i]==ayab::END) {Serial.write(ayab::ESC);Serial.write(ayab::ESC_END);}
    else if(data[i]==ayab::ESC) {Serial.write(ayab::ESC);Serial.write(ayab::ESC_ESC);}
    else Serial.write(data[i]);
  }
  Serial.write(ayab::END);
}
void onPacket(const uint8_t* packet,size_t n) {
  uint8_t response[22]{};
  size_t responseLen=ayab::handle(packet,n,response,sizeof(response));
  if(responseLen) sendSlip(response,responseLen);
}
}
void setup() {Serial.begin(115200);}
void loop() {
  while(Serial.available()) decoder.feed(static_cast<uint8_t>(Serial.read()),onPacket);
  delay(1);
}
