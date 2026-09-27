# Architektur: RFTv1 Electribe-Tools

Software für den Korg Electribe SX (ESX-1) und MX (EMX-1): Multisample-Tool,
`.esx`/`.emx`-Editor-Basis, SysEx-Librarian. Ausgangspunkt war der
Sample-Multi-Shotifier-Ansatz (SoX-basiert, `startpos`-Offset-Trick) plus der
Wunsch nach direktem Datei-Zugriff und Bulk-Backup.

## Module und Status

| Modul | Verzeichnis | Status |
|---|---|---|
| Multisample-Tool | `tools/multishotifier/` | Fertig, getestet (pure Python) |
| `.esx`/`.emx`-Parser + Offset-Discovery-CLI | `electribe_core/`, `cli/` | Fertig: 7-bit-Codec, Schema-Loader, `etx diff/scan/dump`. Schema selbst noch leer (keine verifizierten Offsets) |
| SysEx-Librarian (Standalone) | `standalone/` | Skeleton, blockiert auf Model-ID-Verifikation |
| Realtime-Control (MIDI-Note/CC) | `plugin/` | Plan umgestellt: JSFX/MIDI-Ansatz statt JUCE-VST3, siehe `plugin/README.md`. Mapping-Tabelle noch leer |

## Nicht-negotiable Regeln (aus dem electribe-dev Skill)

1. **Offsets nur in Schema-Dateien** (`schema/*.def`), niemals im Code. `!`
   vor dem Offset heißt hardware-verifiziert, ohne `!` ist es eine
   unbestätigte Vermutung - jede Ausgabe muss das kennzeichnen
   (`electribe::formatField` macht das automatisch mit `[UNVERIFIED]`).
2. **Core bleibt frei von JUCE.** Reines C++17 in `electribe_core`,
   gemeinsam genutzt von CLI, Standalone-App und (künftigem) VST3-Plugin.
3. **Librarian/Backup nicht im VST-Plugin.** DAWs filtern/zerstückeln SysEx
   aus Plugins - Bulk-Dumps laufen ausschließlich über die Standalone-App.
4. **Sample-Audiodaten laufen nicht über MIDI/SysEx.** Die landen auf der
   SmartMedia-/SD-Karte, nicht im dokumentierten Korg-Dump.

## Offset-Discovery-Workflow

Voraussetzung: nur ein Kartenleser, kein MIDI-Interface nötig.

1. Auf dem Gerät „All Data" auf Karte speichern -> `before.esx` sichern.
2. **Genau einen** Parameter am Gerät ändern.
3. Erneut speichern -> `after.esx` sichern.
4. `./build/cli/etx diff before.esx after.esx` - zeigt die exakte
   Byte-Range(n).
5. Bei genau einer differierenden Range: Zeile ins passende `schema/*.def`
   eintragen, mit `!`-Präfix und Datum.
6. Bei mehreren Ranges: mehr als ein Parameter wurde geändert - Durchgang
   wiederholen, nicht raten welche Range zu welchem Parameter gehört.

`./build/cli/etx scan datei.esx` findet ASCII-Runs (z.B. Pattern-/Sample-
Namenstabellen) als Ankerpunkte für die Struktur.
`./build/cli/etx dump datei.esx schema/esx1.def` zeigt alle Felder aus dem
aktuellen Schema an (aktuell nur die `EXAMPLE`-Zeile, da noch nichts
verifiziert ist).

## Offene TODOs

- [ ] Erster echter `etx diff`-Durchgang mit realer Hardware, um das Schema
      zu befüllen.
- [ ] Model-IDs für ESX-1/EMX-1 aus Korgs `ESX1midiimp.txt` bzw. der
      MIDI-Implementation-Chart eintragen (`electribe_core/include/electribe/model_ids.hpp`).
- [ ] SysEx-Roundtrip (`pack7`/`unpack7`) gegen einen echten Hardware-Dump
      verifizieren, nicht nur gegen synthetische Testdaten.
- [ ] Standalone-Librarian `backup`/`restore` implementieren, sobald
      Model-IDs vorliegen.
- [ ] `plugin/midi_map.md` mit echten Note-/CC-Werten aus der
      MIDI-Implementation-Chart befüllen, dann `plugin/electribe.jsfx` bauen.
- [ ] MIDI-Interface mit DIN-Buchsen besorgen (kein Scarlett 2i2/Solo) für
      alle SysEx-Tests.

## Referenzen

- `skratchdot/open-electribe-editor` - detaillierteste Layout-Doku
- `lammas/electribe` - ESX-Format-Toolkit in Node.js
- `coderofsalvation/electribe-emx-esx-reverse-engineering` - Hardware/Firmware
- `coderofsalvation/sample-multi-shotifier` - Ursprungskonzept für
  `tools/multishotifier/`
- reaJS / "electribe-vstx-32/64" - MIDI-Note/CC-Steuerung per DAW,
  Vorbild für `plugin/electribe.jsfx` (EMX-Teil dort laut Autor nie
  fertiggestellt)
- Electribome (ewanhemingway.co.uk) - Monome-Emulator über die
  Keyboard-Matrix, Vorbild für den geplanten Button-Grid-Modus in
  `plugin/midi_map.md`
