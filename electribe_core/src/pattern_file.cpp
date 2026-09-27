#include "electribe/pattern_file.hpp"

#include <algorithm>
#include <cctype>
#include <fstream>
#include <stdexcept>

namespace electribe {

std::vector<uint8_t> readFile(const std::string& path) {
    std::ifstream in(path, std::ios::binary | std::ios::ate);
    if (!in) {
        throw std::runtime_error("cannot open " + path);
    }
    const std::streamsize size = in.tellg();
    if (size < 0) {
        throw std::runtime_error("cannot determine size of " + path);
    }
    std::vector<uint8_t> data(static_cast<size_t>(size));
    in.seekg(0);
    if (size > 0 && !in.read(reinterpret_cast<char*>(data.data()), size)) {
        throw std::runtime_error("failed reading " + path);
    }
    return data;
}

std::vector<DiffRange> diffBytes(const std::vector<uint8_t>& before, const std::vector<uint8_t>& after) {
    std::vector<DiffRange> ranges;
    const size_t common = std::min(before.size(), after.size());

    size_t i = 0;
    while (i < common) {
        if (before[i] == after[i]) {
            ++i;
            continue;
        }
        size_t start = i;
        while (i < common && before[i] != after[i]) {
            ++i;
        }
        DiffRange r;
        r.offset = start;
        r.before.assign(before.begin() + start, before.begin() + i);
        r.after.assign(after.begin() + start, after.begin() + i);
        ranges.push_back(std::move(r));
    }

    if (before.size() != after.size()) {
        DiffRange r;
        r.offset = common;
        r.before.assign(before.begin() + common, before.end());
        r.after.assign(after.begin() + common, after.end());
        ranges.push_back(std::move(r));
    }

    return ranges;
}

std::vector<AsciiRun> scanAsciiRuns(const std::vector<uint8_t>& data, size_t minLength) {
    std::vector<AsciiRun> runs;
    size_t i = 0;
    while (i < data.size()) {
        if (std::isprint(data[i]) && data[i] != 0x7F) {
            size_t start = i;
            while (i < data.size() && std::isprint(data[i]) && data[i] != 0x7F) {
                ++i;
            }
            if (i - start >= minLength) {
                AsciiRun run;
                run.offset = start;
                run.text.assign(reinterpret_cast<const char*>(data.data() + start), i - start);
                runs.push_back(std::move(run));
            }
        } else {
            ++i;
        }
    }
    return runs;
}

} // namespace electribe
