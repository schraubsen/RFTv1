# Electribe Matrix Studio (ESX-1 / EMX-1 Editor)

Start: `python3 -m http.server -d electribe-editor 8000` → http://localhost:8000 (nicht per file://)
Tests: `node test/core.test.mjs` · UI: `node test/ui.test.mjs` (Playwright; `default.esx` aus open-electribe-editor als `/tmp/default.esx` für den Realdatei-Test)

## Funktionen
- `.esx` laden/speichern; Parameter-Editor für alle 256 Pattern (A01–D64): Name, Tempo, Swing, Länge, Beat, Roll, FX-Kette, Last Step, Arp; 9 Drum-Parts (Cutoff, Reso, Pitch, Level, Pan …); Sample-Header (Name, Rate, Tune, Play Level)
- Hex-Editor, Diff (Offset-Discovery → Schema-Zeile per Klick), ASCII-Scan mit editierbaren Namen
- WAV → mono/32 kHz/16 Bit/normalisiert
- SysEx: pack7/unpack7, Request-Builder für ESX-1 (Model-ID 0x71), Web-MIDI Senden/Empfangen/.syx speichern

## Vertrauensstufen im Schema (`schema/esx1.def`)
- `~` Referenz: Korg `ESX1midiimp.txt` + lammas/electribe, gegen die Standard-`default.esx` plausibilisiert (120 BPM, Pan 64, 44100 Hz …). **Nicht von uns auf Hardware verifiziert.**
- `!` verifiziert (Hardware) · ohne Präfix = Vermutung

## Offen
- EMX-1: Dateilayout und Model-ID noch nicht eingetragen (`schema/emx1.def` leer)
- Web-MIDI/SysEx nicht an echter Hardware getestet; Song-/Global-Felder fehlen im Schema
