#include "../src/protocol.h"
#include <cassert>
#include <vector>
int main() {
  const uint8_t request[]={3}; uint8_t reply[22];
  assert(ayab::handle(request,1,reply,sizeof(reply))==22);
  assert(reply[0]==0xC3 && reply[1]==6 && reply[4]==3);
  assert(ayab::handle(request,1,reply,21)==0);
  assert(ayab::crc8(request,1)==ayab::crc8(request,1));
  std::vector<std::vector<uint8_t>> received;
  ayab::Decoder decoder;
  auto onPacket=[&](const uint8_t* b,size_t n){received.emplace_back(b,b+n);};
  for(uint8_t b:{0xC0,0x03,0xC0}) decoder.feed(b,onPacket);
  assert(received.size()==1 && received[0]==std::vector<uint8_t>{3});
  received.clear();
  for(uint8_t b:{0xC0,0xDB,0xDC,0xDB,0xDD,0xC0}) decoder.feed(b,onPacket);
  assert(received.size()==1 && received[0]==(std::vector<uint8_t>{0xC0,0xDB}));
  received.clear();
  for(uint8_t b:{0xC0,0xDB,0x01,0xC0}) decoder.feed(b,onPacket);
  assert(received.empty());
  for(uint8_t b:{0xC0,0x03,0xC0}) decoder.feed(b,onPacket);
  assert(received.size()==1);
  received.clear(); decoder.feed(0xC0,onPacket);
  for(int i=0;i<65;i++) decoder.feed(0x44,onPacket);
  decoder.feed(0xC0,onPacket); assert(received.empty());
  for(uint8_t b:{0xC0,0x03,0xC0}) decoder.feed(b,onPacket);
  assert(received.size()==1);
}
