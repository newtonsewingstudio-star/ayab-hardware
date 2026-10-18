#include "../src/bench_session.h"
#include <cassert>
#include <cstdint>
#include <cstdio>
using ayab::bench::Session;
using ayab::bench::Status;
int main(){
 Session s; uint8_t line[25]{}; line[0]=0x81; line[24]=0x55;
 assert(s.start(1,20)==Status::NOT_INITIALIZED);
 assert(s.initialize(0)==Status::BAD_ARGUMENT);
 assert(s.initialize(Session::kBenchMachine)==Status::OK);
 assert(s.start(20,20)==Status::BAD_ARGUMENT);
 assert(s.start(10,100)==Status::OK);
 assert(s.line(1,line,25,false)==Status::WRONG_LINE);
 assert(s.line(0,line,24,false)==Status::BAD_ARGUMENT);
 assert(s.simulate_pass()==Status::NOT_INITIALIZED);
 assert(s.line(0,line,25,false)==Status::OK);
 assert(s.current_line()[24]==0x55);
 assert(s.simulate_pass()==Status::OK);
 assert(s.snapshot().expected_line==1);
 assert(s.line(1,line,25,true)==Status::OK);
 assert(s.simulate_pass()==Status::COMPLETE);
 assert(s.snapshot().simulated_passes==2);
 assert(s.line(2,line,25,false)==Status::NOT_INITIALIZED);
 s.reset();assert(!s.snapshot().initialized);
 std::puts("bench session tests passed");
}