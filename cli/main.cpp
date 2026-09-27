// etx - offset-discovery CLI for Korg Electribe .esx/.emx files.
// See docs/ARCHITECTURE.md for the workflow this tool supports.

#include "electribe/pattern_file.hpp"
#include "electribe/schema.hpp"

#include <cstdio>
#include <exception>
#include <string>

using namespace electribe;

namespace {

void printHex(const std::vector<uint8_t>& bytes) {
    for (uint8_t b : bytes) {
        std::printf("%02x ", b);
    }
}

int cmdDiff(int argc, char** argv) {
    if (argc < 4) {
        std::fprintf(stderr, "usage: etx diff <before-file> <after-file>\n");
        return 1;
    }
    const auto before = readFile(argv[2]);
    const auto after = readFile(argv[3]);
    const auto ranges = diffBytes(before, after);

    if (ranges.empty()) {
        std::printf("no differences\n");
        return 0;
    }

    for (const auto& r : ranges) {
        std::printf("@0x%04llx (%zu byte(s))\n", static_cast<unsigned long long>(r.offset), r.before.size());
        std::printf("  before: ");
        printHex(r.before);
        std::printf("\n  after:  ");
        printHex(r.after);
        std::printf("\n");
    }
    std::printf(
        "\n%zu differing range(s). Change exactly ONE parameter per capture pass -\n"
        "with more than one range here, this diff can't be attributed to a single\n"
        "field unambiguously.\n",
        ranges.size());
    return 0;
}

int cmdScan(int argc, char** argv) {
    if (argc < 3) {
        std::fprintf(stderr, "usage: etx scan <file> [min-run-length=4]\n");
        return 1;
    }
    const size_t minLength = argc >= 4 ? static_cast<size_t>(std::stoul(argv[3])) : 4;
    const auto data = readFile(argv[2]);
    const auto runs = scanAsciiRuns(data, minLength);

    for (const auto& run : runs) {
        std::printf("0x%04llx: \"%s\"\n", static_cast<unsigned long long>(run.offset), run.text.c_str());
    }
    std::printf("%zu ASCII run(s) found\n", runs.size());
    return 0;
}

int cmdDump(int argc, char** argv) {
    if (argc < 4) {
        std::fprintf(stderr, "usage: etx dump <file> <schema.def>\n");
        return 1;
    }
    const auto raw = readFile(argv[2]);
    const Schema schema = Schema::loadFromFile(argv[3]);

    for (const auto& field : schema.fields()) {
        std::printf("%s\n", formatField(raw, field).c_str());
    }
    return 0;
}

void printUsage() {
    std::fprintf(stderr,
        "etx - Korg Electribe .esx/.emx offset-discovery tool\n"
        "\n"
        "usage:\n"
        "  etx diff <before-file> <after-file>\n"
        "  etx scan <file> [min-run-length]\n"
        "  etx dump <file> <schema.def>\n");
}

} // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        printUsage();
        return 1;
    }

    const std::string cmd = argv[1];
    try {
        if (cmd == "diff") return cmdDiff(argc, argv);
        if (cmd == "scan") return cmdScan(argc, argv);
        if (cmd == "dump") return cmdDump(argc, argv);
    } catch (const std::exception& e) {
        std::fprintf(stderr, "error: %s\n", e.what());
        return 1;
    }

    printUsage();
    return 1;
}
