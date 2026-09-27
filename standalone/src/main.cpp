// SysEx-Librarian Skeleton fuer ESX-1/EMX-1 Backup/Restore.
//
// Sendet bewusst KEINE SysEx-Frames: die Model-IDs sind noch nicht
// verifiziert (siehe electribe_core/include/electribe/model_ids.hpp und
// standalone/README.md). Ein Backup mit geratenen IDs waere kein Backup,
// sondern Datenmuell auf dem Geraet.

#include <cstdio>
#include <string>

namespace {

int cmdBackup() {
    std::fprintf(stderr,
        "backup: noch nicht implementiert - Model-IDs fuer ESX-1/EMX-1 sind\n"
        "noch nicht verifiziert (siehe electribe_core/include/electribe/model_ids.hpp).\n"
        "Naechster Schritt: ESX1midiimp.txt / MIDI-Implementation-Chart pruefen,\n"
        "siehe standalone/README.md.\n");
    return 1;
}

int cmdRestore() {
    std::fprintf(stderr,
        "restore: noch nicht implementiert - siehe standalone/README.md.\n");
    return 1;
}

void printUsage() {
    std::fprintf(stderr,
        "electribe-librarian - SysEx Bulk Backup/Restore fuer ESX-1/EMX-1\n"
        "\n"
        "usage:\n"
        "  electribe-librarian backup\n"
        "  electribe-librarian restore\n");
}

} // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        printUsage();
        return 1;
    }
    const std::string cmd = argv[1];
    if (cmd == "backup") return cmdBackup();
    if (cmd == "restore") return cmdRestore();
    printUsage();
    return 1;
}
