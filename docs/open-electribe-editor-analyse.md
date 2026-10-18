# Analyse: Open Electribe Editor (skratchdot)

Untersucht wurden alle hochgeladenen Builds (1.0.0 vom 07.03.2010 und 1.0.1 BETA vom 25.04.2010 für Windows, Linux und macOS), die p2-Metadaten (`content.jar`, `artifacts.jar`, `site.xml`) und die Wiki-Seiten. Nur statisch: Archive entpackt, Java-Bytecode mit `javap` disassembliert, nichts ausgeführt.

## Ergebnis

- Alle Builds enthalten dieselben sieben skratchdot-Plugins. Das Datei-Modell steckt in `com.skratchdot.electribe.model.esx` (EMF). Es gibt **nur ein ESX-Modell, kein EMX-Modell**.
- Lizenz: Eclipse Public License 1.0, Copyright 2009–2010 SKRATCHDOT.COM. Quellcode liegt laut Wiki auf github.com/skratchdot/open-electribe-editor.
- Das Update-Site (`site.xml`, p2 von 2013) nennt Version 1.1.0, aber ebenfalls nur ESX-Features.
- Mitgeliefert: `defaults/default.esx` (2 424 848 Bytes, leere Werksdatei). Daran wurde unsere Feldkarte geprüft: Tempo 120,0, Drum-Level 100, Pan 64, Cutoff 127, Drum 1 auf den Vierteln, MIDI-CC-Zuweisungen 89, 90, 87, 88 …

## Feldkarte

Steht vollständig in `schema/esx1.def` und wird vom Datei-Inspektor geladen. Kernpunkte:

| Bereich | Adresse | Größe |
|---|---|---|
| Kopf „KORG“ … 0x71 „ESX“ | 0x000000 | 32 |
| Global-Parameter | 0x000020 | 192 |
| Patterns (256 ×) | 0x000200 | je 4 280 |
| Songs (64 ×) | 0x130000 | je 528 |
| Song-Events | 0x138400 | je 8 |
| Zweiter Kopf „KORG“ | 0x1B0000 | |
| Anzahl Mono/Stereo-Samples | 0x1B0020 / 0x1B0024 | je 4 |
| Sample-Header Mono (256 ×) / Stereo (128 ×) | 0x1B0100 / 0x1B2900 | 40 / 44 |
| Slice-Daten | 0x1B4200 | je 2 048 |
| Audiodaten | 0x250000 | variabel |

Im Pattern: Name 8 Bytes, Tempo als 16-Bit-Wert (Bits 7–15 ganzzahlig, Bits 0–3 Zehntel), Swing (0 = 50 %), Länge/Beat/Roll als Bitfelder, FX-Kette, Last Step, Arpeggiator-Skala, vier 16-Bit-Masken (Mute, Swing, Output-Bus, Accent). Danach 9 Drum-Parts à 34, 2 Keyboard-Parts à 274, 3 Slice-Parts à 32, Audio In 156, Accent 18, 3 FX à 4 und 24 Motion-Spuren à 130 Bytes.

## Offen / Vermutungen

- Bit-Reihenfolge der Step-Bytes: Der Editor behandelt sie als Rohbytes. Unsere Annahme „LSB = erster Step“ ist am Gerät zu prüfen (Pattern mit nur Step 1 speichern).
- Keyboard-Noten: In der Werksdatei steht überall 0xBC. Annahme: Bit 7 = Step aus, Bits 0–6 = MIDI-Note.
- EMX-1: kein Layout vorhanden. Der Inspektor bietet für EMX-Dateien eine Struktur-Sonde (wiederkehrende Namen → Chunk-Größe), die an der ESX-Datei die bekannten 4 280 und 528 Bytes korrekt wiederfindet.
