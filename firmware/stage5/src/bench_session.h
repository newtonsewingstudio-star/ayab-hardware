#pragma once
// Bench-only AYAB row/session model; no GPIO, I2C or solenoid actuation.
// Kept separate from the live USB command handler until machine firmware is validated.
#include <array>
#include <cstddef>
#include <cstdint>

namespace ayab {
namespace bench {
enum class Status : uint8_t { OK, NOT_INITIALIZED, BAD_ARGUMENT, WRONG_LINE, BAD_CRC, COMPLETE };
struct Snapshot {
  bool initialized=false;
  bool started=false;
  bool has_line=false;
  bool last_line=false;
  uint8_t expected_line=0;
  uint32_t simulated_passes=0;
};
class Session {
public:
  static constexpr size_t kLineBytes=25;
  Status initialize(uint8_t machine) {
    reset();
    // This is only a provisional KH910 test-machine identifier; the live
    // protocol must use the exact upstream machine enum after verification.
    if (machine!=kBenchMachine) return Status::BAD_ARGUMENT;
    state_.initialized=true;
    return Status::OK;
  }
  Status start(uint8_t first, uint8_t last) {
    if(!state_.initialized) return Status::NOT_INITIALIZED;
    if(first>=last || last>=200) return Status::BAD_ARGUMENT;
    state_.started=true; state_.expected_line=0;
    first_=first; last_=last; return Status::OK;
  }
  Status line(uint8_t index,const uint8_t* bytes,size_t len,bool last) {
    if(!state_.started) return Status::NOT_INITIALIZED;
    if(state_.last_line) return Status::COMPLETE;
    if(!bytes || len!=kLineBytes) return Status::BAD_ARGUMENT;
    if(index!=state_.expected_line) return Status::WRONG_LINE;
    for(size_t i=0;i<len;i++) line_[i]=bytes[i];
    state_.has_line=true; state_.last_line=last;
    return Status::OK;
  }
  Status simulate_pass() {
    if(!state_.started || !state_.has_line) return Status::NOT_INITIALIZED;
    state_.simulated_passes++;
    state_.has_line=false;
    if(state_.last_line) {state_.started=false;return Status::COMPLETE;}
    state_.expected_line=static_cast<uint8_t>(state_.expected_line+1);
    return Status::OK;
  }
  void reset(){state_=Snapshot{};line_.fill(0);first_=last_=0;}
  Snapshot snapshot() const {return state_;}
  uint8_t first() const {return first_;}
  uint8_t last() const {return last_;}
  const std::array<uint8_t,kLineBytes>& current_line() const {return line_;}
  static constexpr uint8_t kBenchMachine=0x91; // synthetic, NOT upstream ID
private:
  Snapshot state_{};
  std::array<uint8_t,kLineBytes> line_{};
  uint8_t first_=0,last_=0;
};
}
}
