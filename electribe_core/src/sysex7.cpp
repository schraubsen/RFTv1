#include "electribe/sysex7.hpp"

#include <algorithm>

namespace electribe {

std::vector<uint8_t> pack7(const std::vector<uint8_t>& data) {
    std::vector<uint8_t> out;
    out.reserve(data.size() + (data.size() + 6) / 7);

    size_t i = 0;
    while (i < data.size()) {
        const size_t n = std::min<size_t>(7, data.size() - i);
        uint8_t carrier = 0;
        for (size_t j = 0; j < n; ++j) {
            if (data[i + j] & 0x80) {
                carrier |= static_cast<uint8_t>(1u << j);
            }
        }
        out.push_back(carrier);
        for (size_t j = 0; j < n; ++j) {
            out.push_back(static_cast<uint8_t>(data[i + j] & 0x7F));
        }
        i += n;
    }
    return out;
}

std::vector<uint8_t> unpack7(const std::vector<uint8_t>& packed) {
    std::vector<uint8_t> out;
    out.reserve(packed.size());

    size_t i = 0;
    while (i < packed.size()) {
        const uint8_t carrier = packed[i];
        const size_t remaining = packed.size() - i - 1;
        const size_t n = std::min<size_t>(7, remaining);
        for (size_t j = 0; j < n; ++j) {
            uint8_t v = static_cast<uint8_t>(packed[i + 1 + j] & 0x7F);
            if (carrier & (1u << j)) {
                v |= 0x80;
            }
            out.push_back(v);
        }
        i += 1 + n;
    }
    return out;
}

} // namespace electribe
