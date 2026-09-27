#include "electribe/schema.hpp"

#include <cstdio>
#include <string>

using electribe::Schema;

namespace {

int failures = 0;

void check(bool condition, const char* what) {
    if (!condition) {
        std::fprintf(stderr, "FAILED: %s\n", what);
        ++failures;
    }
}

} // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        std::fprintf(stderr, "usage: test_schema <path-to-esx1.def>\n");
        return 1;
    }

    const Schema schema = Schema::loadFromFile(argv[1]);
    check(schema.fields().size() == 1, "esx1.def has exactly one example field");

    if (!schema.fields().empty()) {
        const auto& f = schema.fields().front();
        check(f.name == "example_field", "field name is example_field");
        check(f.offset == 0, "field offset is 0");
        check(f.length == 4, "field length is 4");
        check(!f.verified, "example field is unverified");
    }

    if (failures == 0) {
        std::printf("test_schema: all tests passed\n");
        return 0;
    }
    std::fprintf(stderr, "test_schema: %d failure(s)\n", failures);
    return 1;
}
