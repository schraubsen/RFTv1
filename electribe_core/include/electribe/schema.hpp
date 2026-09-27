#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace electribe {

// One field description loaded from a schema/*.def file. Offsets are
// reverse-engineered guesses unless `verified` is true (the `!` prefix in
// the .def file). See schema/FORMAT.md for the file format and the
// electribe-dev workflow for how fields get verified.
struct Field {
    uint64_t offset = 0;
    uint32_t length = 0;
    std::string name;
    std::string type; // u8, u16le, u16be, ascii, bytes, bitfield
    std::string notes;
    bool verified = false;
};

class Schema {
public:
    // Parses a .def text file. Throws std::runtime_error on a malformed line
    // so a broken schema fails loudly instead of silently mis-mapping bytes.
    static Schema loadFromFile(const std::string& path);

    const std::vector<Field>& fields() const { return fields_; }

private:
    std::vector<Field> fields_;
};

// Renders one field's value from `raw` at `field.offset`/`field.length`.
// Every unverified field is prefixed with "[UNVERIFIED]" in the output so
// guessed offsets can never be mistaken for confirmed ones.
std::string formatField(const std::vector<uint8_t>& raw, const Field& field);

} // namespace electribe
