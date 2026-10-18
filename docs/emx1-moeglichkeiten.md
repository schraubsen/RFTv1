# Was mit der EMX-1 noch geht

Stand dieses Projekts, getrennt nach „im Tool“, „am Gerät möglich“ und „nicht möglich“.

## Im Tool

- **MIDI-Live** (Chrome/Edge am Rechner, DIN-MIDI-Interface): MIDI Clock mit Start/Stop (EMX auf Clock Ext), Steps als Noten, Panel-Regler und Motion als CC, Program Change, Panic. Kanäle, Drum-Noten und CC-Nummern wie im Export-Tab (an der EMX frei zuweisbar). Getestet mit einem simulierten Gerät: 24 Clock-Impulse pro Viertel, richtige Kanäle und Noten; an echter Hardware noch nicht.
- **SysEx-Mitschnitt**: Dumps der EMX empfangen, als .syx speichern, zwei Dumps nach Korg-7-Bit-Entpackung vergleichen, .syx an das Gerät senden (mit Rückfrage). Die Kopflänge vor den Nutzdaten ist eine Vermutung (Standard 5 Bytes) und am echten Dump zu prüfen.
- **ESX-1-Dateien**: komplett lesen, Samples als WAV exportieren, Patterns übernehmen (siehe `open-electribe-editor-analyse.md`).
- **Röhren-Messung**: Tube 50 wirkt wie ein sanfter Limiter (+2,7 dB RMS, Crest −2,1 dB, Klangbalance unverändert).

## Am Gerät möglich, als nächster Schritt

1. **EMX-Feldkarte**: Vorher/Nachher-Dumps oder .emx-Dateien mit genau einer Änderung vergleichen. Mit der Feldkarte könnte das Tool Patterns direkt als .emx oder SysEx schreiben.
2. **Stimmen über Audio In**: Vocal-Phrasen oder Klang-Labor-Sounds vom Rechner in den Audio-In der EMX spielen, getaktet über MIDI Clock. Filter, Effekte und Röhre der EMX formen den Klang.
3. **Mehrgeräte-Setup**: Tool als Clock-Master für EMX und ESX.
4. **Hardware**: RFT-Knöpfe und Frontplatten (3D-Druck), Röhrentausch.

## Nicht möglich

- Eigene Samples in die EMX laden (PCM fest im ROM). Ausweg: Audio In oder ESX-1.
- USB-MIDI direkt am Gerät; SmartMedia-Karten über 128 MB.
- Firmware-Eingriffe: nicht empfohlen.
