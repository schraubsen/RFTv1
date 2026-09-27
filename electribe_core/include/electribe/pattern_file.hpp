#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace electribe {

// Reads a whole file into memory. Throws std::runtime_error if it can't be
// opened. Used for raw .esx/.emx bytes - no format assumptions here.
std::vector<uint8_t> readFile(const std::string& path);

struct DiffRange {
    uint64_t offset = 0;
    std::vector<uint8_t> before;
    std::vector<uint8_t> after;
};

// Byte-level diff between two buffers, collapsed into contiguous differing
// ranges. This is the core of the offset-discovery workflow: dump `before`,
// change exactly one parameter on the hardware, dump `after`, diff them.
std::vector<DiffRange> diffBytes(const std::vector<uint8_t>& before, const std::vector<uint8_t>& after);

struct AsciiRun {
    uint64_t offset = 0;
    std::string text;
};

// Finds printable-ASCII runs of at least `minLength` bytes. Useful for
// locating pattern/sample name tables as structural anchors.
std::vector<AsciiRun> scanAsciiRuns(const std::vector<uint8_t>& data, size_t minLength = 4);

} // namespace electribe
