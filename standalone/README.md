# Standalone-App: SysEx-Librarian

Bulk-Backup und -Restore von Pattern-/Song-/Global-Daten der ESX-1/EMX-1 über
MIDI-SysEx. Läuft als eigene Anwendung (nicht im VST-Plugin), weil viele DAWs
SysEx aus Plugins filtern oder zerstückeln - siehe die Architekturregel in
`docs/ARCHITECTURE.md`.

## Aktueller Stand

`src/main.cpp` ist ein Skeleton mit den Subcommands `backup` und `restore`.
Beide brechen aktuell bewusst mit einer klaren Meldung ab, statt SysEx-Frames
mit erfundenen Werten zu senden:

- Die konkreten Model-IDs für ESX-1/EMX-1 sind noch nicht verifiziert
  (`electribe_core/include/electribe/model_ids.hpp`, `TODO: verifizieren`).
  Ohne sie wäre jeder gesendete SysEx-Frame Raten, kein Backup.
- Ein echter Dump-Test braucht ein MIDI-Interface mit DIN-Buchsen (kein
  Focusrite Scarlett 2i2/Solo) und ein zuverlässiges USB-MIDI-Kabel.

## Nächste Schritte

1. Model-IDs aus Korgs `ESX1midiimp.txt` bzw. der MIDI-Implementation-Chart
   im Handbuch-Anhang eintragen (nicht raten).
2. Mit echtem Hardware-Dump (`All Data` -> Bulk Dump) einen Roundtrip gegen
   `electribe_core::pack7`/`unpack7` verifizieren.
3. `backup`/`restore` gegen die dann bekannten Model-IDs implementieren.

## Build

Baut als `electribe-librarian` mit dem Haupt-CMake-Projekt. Beide Subcommands
brechen zur Laufzeit kontrolliert ab (siehe oben) - es wird nichts gebaut,
was SysEx mit Platzhalter-IDs sendet.
