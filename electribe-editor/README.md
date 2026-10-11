# Electribe Matrix Studio (ESX-1 / EMX-1 Editor)

Start: `python3 -m http.server -d electribe-editor 8000` → http://localhost:8000 (nicht per file://)
Tests: `node test/core.test.mjs` · UI: `node test/ui.test.mjs` (Playwright; `default.esx` aus open-electribe-editor als `/tmp/default.esx` für den Realdatei-Test)

## Funktionen
- `.esx` **und `.emx`** laden/speichern (Erkennung per Magic); ESX-1: Parameter-Editor für alle 256 Pattern (A01–D64): Name, Tempo, Swing, Länge, Beat, Roll, FX-Kette, Last Step, Arp; 9 Drum-Parts (Cutoff, Reso, Pitch, Level, Pan …); Sample-Header (Name, Rate, Tune, Play Level)
- ESX-1 Schema vollständig bis auf Motion-Sequenzen: Global, Pattern, 9 Drum-, 2 Keyboard-, 2 Stretch-, 1 Slice-, Audio-In-, Accent-Part, 3 FX, Sample-Header
- **Noten-Tab:** Keyboard-Noten/Gates und Audio-In-Gates je Step (`arr`-Direktive)
- **Steps-Tab:** 128-Step-Sequenzen aller Drum-Parts (EMX zusätzlich Accent) per Klick editieren
- EMX-1: Pattern (Name, Tempo, Swing …), 9 Drum-Parts, 5 Synth-Parts, 64 Songs (Name, Tempo, Länge …)
- Hex-Editor, Diff (Offset-Discovery → Schema-Zeile per Klick), ASCII-Scan mit editierbaren Namen
- WAV → mono/32 kHz/16 Bit/normalisiert
- SysEx: pack7/unpack7, Request-Builder für ESX-1 (Model-ID 0x71), Web-MIDI Senden/Empfangen/.syx speichern

## Vertrauensstufen im Schema (`schema/esx1.def`)
- `~` Referenz: Korg `ESX1midiimp.txt` + lammas/electribe, gegen die Standard-`default.esx` plausibilisiert (120 BPM, Pan 64, 44100 Hz …). **Nicht von uns auf Hardware verifiziert.**
- `!` verifiziert (Hardware) · ohne Präfix = Vermutung

## EMX-1: Status
Quellen: Model-ID 0x69 und Song-Tabelle aus [themesser/EMiX](https://github.com/themesser/EMiX); Pattern/Part-Offsets aus [BerndPeuser/Korg-EMX-Editor](https://github.com/BerndPeuser/Korg-EMX-Editor).
**Gegen 5 echte `.EMX`-Bänke geprüft** (Nutzer-Uploads, nicht im Repo; `EMX_FILES=a:b node test/core.test.mjs`): 236 Felder, 0 Wertebereichs-Verstöße; Tempi 120–162, Arp Center 60, Song-Namen lesbar, Motion zu ~95 % `0xFFFF` (unbenutzt), Synth-Noten `0x3C`/Off `0xBC`. Korrekturen aus der Prüfung: Song-Tempo ist wie beim ESX bit-gepackt (nicht EMiX' `byte8 + byte9/10`), Arp-Scale nur 5 Bit. Roundtrip: Tempo + 1 Step ändern verändert genau 2 Bytes.
Weiterhin **nicht** auf Hardware getestet.

## Offen
- EMX-1-Request-Funktionscodes (SysEx) nicht belegt → Requests nur für ESX-1 freigegeben
- Web-MIDI/SysEx nicht an echter Hardware getestet
- ESX+EMX: Song-Events als Rohtabelle (Index 1–20000, Event-Typ-abhängige Felder); Motion, Songs, MIDI-Kanäle/CC/Drum-Noten sind im Schema (Noten-Tab)
- EMX: FX aus Quelle; Synth-Sequenzen und Motion sind **abgeleitet/UNBESTÄTIGT** (Partgröße 276 = 20+128+128, 1686+24×130 = 4806)
