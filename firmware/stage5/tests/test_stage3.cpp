#include <cassert>
#include <cstdint>
#include <vector>
#include "../src/protocol.h"
int main(){
 uint8_t r[22]{};
 {uint8_t x[]={0x03};assert(ayab::handle(x,1,r,22)==22);assert(r[0]==0xC3&&r[1]==6);}
 {uint8_t x[]={0x05,0x00};assert(ayab::handle(x,2,r,22)==2);assert(r[0]==0xC5&&r[1]==1);}
 {uint8_t x[]={0x05,0x00,static_cast<uint8_t>(ayab::crc8((const uint8_t*)"\x05\x00",2)^0xFF)};assert(ayab::handle(x,3,r,22)==2);assert(r[1]==4);}
 {uint8_t x[]={0x05,0x00,ayab::crc8(x,2)};assert(ayab::handle(x,3,r,22)==2);assert(r[1]!=0);}
 {uint8_t x[]={0x01,0x00,0x10,0x00,0x00};x[4]=ayab::crc8(x,4);assert(ayab::handle(x,5,r,22)==2);assert(r[0]==0xC1&&r[1]!=0);}
 {uint8_t x[]={0x04};assert(ayab::handle(x,1,r,22)==2);assert(r[0]==0xC4&&r[1]!=0);}
 {uint8_t x[]={0x82};assert(ayab::handle(x,1,r,22)==0);}
 // Invalid lengths/inputs cannot claim success.
 assert(ayab::handle(nullptr,0,r,22)==0);
 uint8_t x[]={0x03};assert(ayab::handle(x,1,r,1)==0);
 std::vector<std::vector<uint8_t>> out;
 ayab::Decoder decoder;
 auto cb=[&](const uint8_t*d,size_t n){out.emplace_back(d,d+n);};
 for(uint8_t z:{uint8_t(0xC0),uint8_t(0x05),uint8_t(0xDB),uint8_t(0xDC),uint8_t(0xC0)})decoder.feed(z,cb);
 assert(out.size()==1&&out[0].size()==2&&out[0][1]==0xC0);
}