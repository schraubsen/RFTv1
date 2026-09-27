#include "electribe/sysex7.hpp"

#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

using electribe::pack7;
using electribe::unpack7;

namespace {

int failures = 0;

void check(bool condition, const char* what) {
    if (!condition) {
        std::fprintf(stderr, "FAILED: %s\n", what);
        ++failures;
    }
}

std::vector<uint8_t> makeTestData(size_t length) {
    std::vector<uint8_t> data(length);
    for (size_t i = 0; i < length; ++i) {
        // Deterministic pseudo-random byte covering the full 0..255 range,
        // including values with bit 7 set.
        data[i] = static_cast<uint8_t>((i * 137 + 199) & 0xFF);
    }
    return data;
}

void testRoundtripForLength(size_t length) {
    const auto data = makeTestData(length);
    const auto packed = pack7(data);
    const auto unpacked = unpack7(packed);

    check(unpacked == data, ("roundtrip length=" + std::to_string(length)).c_str());

    for (uint8_t b : packed) {
        if (b & 0x80) {
            std::fprintf(stderr, "FAILED: pack7 output has bit 7 set at length=%zu\n", length);
            ++failures;
            break;
        }
    }
}

} // namespace

int main() {
    for (size_t length : {0, 1, 6, 7, 8, 13, 14, 15, 100}) {
        testRoundtripForLength(length);
    }

    if (failures == 0) {
        std::printf("test_sysex7: all tests passed\n");
        return 0;
    }
    std::fprintf(stderr, "test_sysex7: %d failure(s)\n", failures);
    return 1;
}
