#pragma once
// AYAB API v6 read-only stage-2 transport. GPL-3.0-or-later.
// Reference: AllYarnsAreBeautiful/ayab-firmware src/ayab/com.h, com.cpp.
#include <cstddef>
#include <cstdint>

namespace ayab {
constexpr uint8_t END=0xC0, ESC=0xDB, ESC_END=0xDC, ESC_ESC=0xDD;
constexpr size_t MAX_PACKET=64;
constexpr uint8_t API_VERSION=6;
constexpr uint8_t REQ_INFO=0x03, CNF_INFO=0xC3;
constexpr uint8_t REQ_INIT=0x05, CNF_INIT=0xC5;
constexpr uint8_t REQ_START=0x01, CNF_START=0xC1;
constexpr uint8_t REQ_TEST=0x04, CNF_TEST=0xC4;
constexpr uint8_t ERR_NOT_READY=0xEF, ERR_SHORT=0x01, ERR_CRC=0x04;

inline uint8_t crc8(const uint8_t* data, size_t n) {
  uint8_t crc=0;
  while(n--) {
    uint8_t value=*data++;
    for(unsigned i=0;i<8;i++) {
      const uint8_t sum=(crc^value)&1U;
      crc >>= 1;
      if(sum) crc ^= 0x8c;
      value >>= 1;
    }
  }
  return crc;
}

// Emulates upstream cnfInfo shape; prototype cannot imply knitting readiness.
inline size_t handle(const uint8_t* packet, size_t len, uint8_t* reply, size_t capacity) {
  if(!packet || !reply || len==0) return 0;
  if(packet[0]==REQ_INFO && len==1 && capacity>=22) {
    for(size_t i=0;i<22;i++) reply[i]=0;
    reply[0]=CNF_INFO; reply[1]=API_VERSION;
    reply[2]=0; reply[3]=0; reply[4]=3;
    const char suffix[]="bench-no-io";
    for(size_t i=0;i<sizeof(suffix);i++) reply[5+i]=static_cast<uint8_t>(suffix[i]);
    return 22;
  }
  // Explicit NACKs ensure the desktop cannot mistake this for an
  // operational knitting controller. GPIO and machine power stay untouched.
  uint8_t confirm=0, error=ERR_NOT_READY;
  if(packet[0]==REQ_INIT) {
    confirm=CNF_INIT;
    if(len<3) error=ERR_SHORT;
    else if(packet[2]!=crc8(packet,2)) error=ERR_CRC;
  } else if(packet[0]==REQ_START) {
    confirm=CNF_START;
    if(len<5) error=ERR_SHORT;
    else if(packet[4]!=crc8(packet,4)) error=ERR_CRC;
  } else if(packet[0]==REQ_TEST) { confirm=CNF_TEST; }
  if(confirm && capacity>=2){reply[0]=confirm; reply[1]=error;return 2;}
  return 0;
}

class Decoder {
 public:
  template<typename Handler> void feed(uint8_t byte, Handler handler) {
    if(byte==END) {
      if(length_ && !invalid_ && !escaped_) handler(buffer_,length_);
      reset();
      return;
    }
    if(invalid_) return;
    if(escaped_) {
      escaped_=false;
      if(byte==ESC_END) byte=END;
      else if(byte==ESC_ESC) byte=ESC;
      else {invalid_=true;return;}
    } else if(byte==ESC) { escaped_=true;return; }
    if(length_<MAX_PACKET) buffer_[length_++]=byte;
    else invalid_=true;
  }
  void reset() {length_=0;escaped_=false;invalid_=false;}
 private:
  uint8_t buffer_[MAX_PACKET]{};
  size_t length_=0;
  bool escaped_=false,invalid_=false;
};
}