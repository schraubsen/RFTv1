#include "electribe/schema.hpp"

#include <algorithm>
#include <cctype>
#include <cstdio>
#include <fstream>
#include <sstream>
#include <stdexcept>

namespace electribe {

namespace {

std::string trim(const std::string& s) {
    const size_t start = s.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) {
        return "";
    }
    const size_t end = s.find_last_not_of(" \t\r\n");
    return s.substr(start, end - start + 1);
}

} // namespace

Schema Schema::loadFromFile(const std::string& path) {
    std::ifstream in(path);
    if (!in) {
        throw std::runtime_error("schema: cannot open " + path);
    }

    Schema schema;
    std::string line;
    size_t lineNo = 0;

    while (std::getline(in, line)) {
        ++lineNo;
        std::string trimmed = trim(line);
        if (trimmed.empty() || trimmed[0] == '#') {
            continue;
        }

        std::string notes;
        const auto hashPos = trimmed.find('#');
        if (hashPos != std::string::npos) {
            notes = trim(trimmed.substr(hashPos + 1));
            trimmed = trim(trimmed.substr(0, hashPos));
        }
        if (trimmed.empty()) {
            continue;
        }

        std::istringstream iss(trimmed);
        std::string offsetTok, lengthTok, name, type;
        if (!(iss >> offsetTok >> lengthTok >> name >> type)) {
            throw std::runtime_error("schema: malformed line " + std::to_string(lineNo) + " in " + path);
        }

        Field f;
        f.verified = !offsetTok.empty() && offsetTok[0] == '!';
        if (f.verified) {
            offsetTok.erase(0, 1);
        }

        try {
            f.offset = std::stoull(offsetTok, nullptr, 0);
            f.length = static_cast<uint32_t>(std::stoul(lengthTok, nullptr, 0));
        } catch (const std::exception&) {
            throw std::runtime_error("schema: bad offset/length on line " + std::to_string(lineNo) + " in " + path);
        }

        f.name = name;
        f.type = type;
        f.notes = notes;
        schema.fields_.push_back(std::move(f));
    }

    return schema;
}

std::string formatField(const std::vector<uint8_t>& raw, const Field& field) {
    std::ostringstream out;
    if (!field.verified) {
        out << "[UNVERIFIED] ";
    }
    out << field.name << " = ";

    if (field.offset + field.length > raw.size()) {
        out << "<out of range>";
        return out.str();
    }

    const uint8_t* p = raw.data() + field.offset;

    if (field.type == "ascii") {
        out << '"';
        for (uint32_t i = 0; i < field.length; ++i) {
            const char c = static_cast<char>(p[i]);
            out << (std::isprint(static_cast<unsigned char>(c)) ? c : '.');
        }
        out << '"';
    } else if (field.type == "u8" && field.length >= 1) {
        out << static_cast<unsigned>(p[0]);
    } else if (field.type == "u16le" && field.length >= 2) {
        out << (static_cast<unsigned>(p[0]) | (static_cast<unsigned>(p[1]) << 8));
    } else if (field.type == "u16be" && field.length >= 2) {
        out << (static_cast<unsigned>(p[1]) | (static_cast<unsigned>(p[0]) << 8));
    } else {
        out << "0x";
        for (uint32_t i = 0; i < field.length; ++i) {
            char buf[3];
            std::snprintf(buf, sizeof(buf), "%02x", p[i]);
            out << buf;
        }
    }
    return out.str();
}

} // namespace electribe
