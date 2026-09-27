#pragma once

#include <cstdint>
#include <vector>

namespace electribe {

// Korg 7-bit SysEx packing: groups of up to 8 transmitted bytes per group.
// The first byte of a group is a carrier byte holding the original MSB
// (bit 7) of each of the following up to 7 data bytes. Bit i of the
// carrier is the MSB of data byte i within that group. No transmitted byte
// may have bit 7 set, which SysEx requires.
std::vector<uint8_t> pack7(const std::vector<uint8_t>& data);

// Inverse of pack7. Consumes the full packed buffer group by group; the
// last group may hold fewer than 7 data bytes.
std::vector<uint8_t> unpack7(const std::vector<uint8_t>& packed);

} // namespace electribe
