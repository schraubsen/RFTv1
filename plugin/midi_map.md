# MIDI-Note/CC-Mapping: ESX-1 / EMX-1

Wie bei den Datei-Offsets gilt: nichts aus dem Gedächtnis raten. Alle Werte
hier kommen aus der MIDI-Implementation-Chart im Handbuch-Anhang bzw. aus
Korgs technischer Dokumentation. Solange eine Zeile mit `TODO` markiert ist,
ist sie **nicht** befüllt - nicht als 0 oder Platzhalterwert interpretieren.

## Status

Aktuell komplett leer. Befüllung ist Voraussetzung für `plugin/electribe.jsfx`
(siehe `plugin/README.md`, Schritt 1).

## Tabellenformat (sobald befüllt)

| Parameter | Kanal | Typ | Nummer | Wertebereich | Quelle/Notiz |
|---|---|---|---|---|---|
| TODO | TODO | note/cc | TODO | TODO | MIDI-Implementation-Chart, Handbuch-Anhang |

## Button-Grid (Electribome-Vorbild, noch nicht übernommen)

- ESX Drum-Parts: 16 Spalten × 9 Zeilen über die Keyboard-Matrix.
- EMX Keyboard-Parts: 16 Spalten × 5 Zeilen.
- Konkrete Notennummern pro Zelle: TODO, aus Handbuch bzw. eigenem
  MIDI-Monitoring beim Antippen der Keyboard-Matrix ableiten (analog zum
  `etx diff`-Workflow für Datei-Offsets: eine Taste pro Durchgang).
