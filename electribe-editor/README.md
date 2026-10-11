# Electribe Matrix Studio (ESX-1 / EMX-1 Editor)

Start: `python3 -m http.server -d electribe-editor 8000` → http://localhost:8000 (nicht per file://)
Tests: `node test/core.test.mjs` · UI: `node test/ui.test.mjs` (Playwright; `default.esx` aus open-electribe-editor als `/tmp/default.esx` für den Realdatei-Test)

## Funktionen
- `.esx` **und `.emx`** laden/speichern (Erkennung per Magic); ESX-1: Parameter-Editor für alle 256 Pattern (A01–D64): Name, Tempo, Swing, Länge, Beat, Roll, FX-Kette, Last Step, Arp; 9 Drum-Parts (Cutoff, Reso, Pitch, Level, Pan …); Sample-Header (Name, Rate, Tune, Play Level)
- **Steps-Tab:** 128-Step-Sequenzen aller Drum-Parts (EMX zusätzlich Accent) per Klick editieren
- EMX-1: Pattern (Name, Tempo, Swing …), 9 Drum-Parts, 5 Synth-Parts, 64 Songs (Name, Tempo, Länge …)
- Hex-Editor, Diff (Offset-Discovery → Schema-Zeile per Klick), ASCII-Scan mit editierbaren Namen
- WAV → mono/32 kHz/16 Bit/normalisiert
- SysEx: pack7/unpack7, Request-Builder für ESX-1 (Model-ID 0x71), Web-MIDI Senden/Empfangen/.syx speichern

## Vertrauensstufen im Schema (`schema/esx1.def`)
- `~` Referenz: Korg `ESX1midiimp.txt` + lammas/electribe, gegen die Standard-`default.esx` plausibilisiert (120 BPM, Pan 64, 44100 Hz …). **Nicht von uns auf Hardware verifiziert.**
- `!` verifiziert (Hardware) · ohne Präfix = Vermutung

## Quellen EMX-1
Model-ID 0x69 und Song-Tabelle: [themesser/EMiX](https://github.com/themesser/EMiX); Pattern/Part-Offsets: [BerndPeuser/Korg-EMX-Editor](https://github.com/BerndPeuser/Korg-EMX-Editor). Es lag **keine echte .emx** zum Gegentest vor (nur synthetische Testdatei); ESX-Felder dagegen sind an der echten default.esx plausibilisiert (Drum 1 = Four-on-the-Floor).

## Offen
- EMX-1-Request-Funktionscodes (SysEx) nicht verifiziert → Requests nur für ESX-1 freigegeben
- Web-MIDI/SysEx nicht an echter Hardware getestet; Song-/Global-Felder fehlen im Schema
