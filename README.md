# RFTv1 - Electribe-Tools für Korg ESX-1 / EMX-1

Software für den Korg Electribe SX (ESX-1) und MX (EMX-1): ein
Multisample-Tool, die Grundlage für einen `.esx`/`.emx`-Datei-Editor und ein
Skeleton für einen SysEx-Librarian. Details und offene TODOs stehen in
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Inhalt

- `tools/multishotifier/` - Python-Tool, baut aus einem Sample-Ordner eine
  `multishot.wav` für den Start-Position-Knob-Trick (0..127 Slots).
- `electribe_core/` - C++17-Bibliothek: 7-bit-SysEx-Codec, Schema-Loader für
  `.esx`/`.emx`, keine JUCE-Abhängigkeit.
- `cli/` (`etx`) - Offset-Discovery-Tool: `diff`, `scan`, `dump`.
- `schema/` - Textschema für Datei-Layouts (`!` = hardware-verifiziert, ohne
  `!` = unbestätigte Vermutung). Aktuell leer bis auf ein Format-Beispiel.
- `standalone/` - Skeleton für den SysEx-Librarian (Bulk-Backup/-Restore).
- `plugin/` - Plan für ein künftiges VST3-Plugin (Realtime-Control per CC).

## Build (C++)

```sh
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

## Multishotifier (Python, keine Abhängigkeiten)

```sh
python3 tools/multishotifier/multishotifier.py <sample-ordner> multishot.wav
```
