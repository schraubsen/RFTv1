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

## Gegenprobe an echten Dateien

Geprüft an fünf echten `.esx` (ESX-Werksdaten mit 256 Patterns, 200 Samples und 4 Songs; ES-1-Werksdaten; ES-1 Sound Designer; zwei Nutzer-Sets) und elf aus der Werksdatei exportierten WAVs:

- Kopf „KORG … q ESX“ und zweiter Kopf „KORG … q BPS“ bei 0x1B0000 in allen Dateien.
- Pattern-Namen (House1 …, ES1_A.01 …), Tempi (69–183 BPM), Swing-Werte, Songs (PartyOn!, WhusHot, D&B mix, >AsTrAl<) plausibel.
- Step-Bits: LSB = erster Step. Drum 1 hat über alle Dateien 3960 Treffer auf den Zählzeiten gegenüber 594, 1591 und 904 auf den anderen Positionen; MSB-zuerst ergäbe genau das gespiegelte, unplausible Bild.
- Keyboard-Noten: Bit 7 gesetzt = Step aus. Belegte Noten liegen bevorzugt auf Zählzeiten, im Bereich MIDI 16–101, am häufigsten A1, rund 27 % der Steps.
- Sample-Audio: 16-Bit-PCM Big-Endian ab 0x250000 + `off1start` + 16 Byte Vorspann (beginnt immer mit `80 00 7F FF`), Frames = `end` + 1, Rate aus dem Header (31 250, 32 000 oder 44 100 Hz). Alle elf WAVs stimmen Sample für Sample überein.
- Sample-Tune: 32-kHz-Samples tragen −5,55 Halbtöne (= 12·log2(32000/44100)), 44,1-kHz-Samples 0.

## Tiefer: Motion, unbekannte Bereiche, Song-Events

- **Motion-Nummer = Part × 32 + Parameter.** Die oberen Bits (0–15) entsprechen genau den 16 Parts (Drum 1–7B, Keyboard 1–2, Slice 1–3, Audio In, Accent; Accent hat die meisten Spuren). Welcher Parameter-Index welcher Regler ist, ließ sich statistisch nicht eindeutig klären (Kandidaten: 6 = Cutoff, 10 = Level). Der Wert 128 heißt „an diesem Step keine Bewegung“, 65535 als Nummer = leere Spur. Die Hypothese „Nummer = Byte-Offset im Pattern“ ist widerlegt (nur 5 % Übereinstimmung).
- **Unbekannte Bereiche:** U1 (0xE0–0x1FF) ist in allen 13 Dateien leer. U2 (0x10BA00–0x12FFFF) und U3 (0x15F500–0x1AFFFF) enthalten zufällig wirkende Bitmuster, in allen Werksdateien identisch: vermutlich uninitialisierter Speicher, kein Nutzinhalt. U4 (0x1B3E00) beginnt mit 0xFF, sonst leer.
- **Zweiter Kopf** bei 0x1B0000: „KORG … q“ gefolgt von „BPS “ oder „BPA “ und einer ASCII-Ziffernfolge.
- **Song-Events:** 8 Bytes je Ereignis ab 0x138400 (z. B. „PartyOn!“ mit 293 Events); Aufbau noch nicht entschlüsselt.

## Offen / Vermutungen

- Bedeutung der Bytes 4–12 im 16-Byte-Vorspann der Samples und des Bereichs „BPS“ bei 0x1B0000.
- EMX-1: kein Layout vorhanden. Der Inspektor bietet für EMX-Dateien eine Struktur-Sonde (wiederkehrende Namen → Chunk-Größe), die an der ESX-Datei die bekannten 4 280 und 528 Bytes korrekt wiederfindet.

## Nebenbefund: Röhreneinfluss der EMX-1, gemessen an zwei Sample-Packs

Zwei Aufnahmen derselben 207 EMX-PCM-Sounds (Pack von Rodrigo López Dato, einmal ohne Angabe zur Röhre, einmal „50tube“). Verglichen wurden 206 Paare bei 44,1 kHz (Medianwerte):

| Messwert | ohne Angabe | Tube 50 | Differenz |
|---|---|---|---|
| Peak | −2,47 dBFS | −2,09 dBFS | +0,4 dB |
| RMS | −17,6 dBFS | −15,0 dBFS | +2,7 dB |
| Crest-Faktor | 15,5 dB | 12,9 dB | −2,1 dB |
| Energie über 4 kHz | 6,4 % | 6,3 % | ±0 |
| Energie unter 120 Hz | 0,7 % | 0,7 % | ±0 |

Die Röhre wirkt bei Tube Gain 50 also vor allem als sanfter Kompressor/Limiter: gut 2,5 dB mehr Lautheit bei fast gleichem Peak, die Frequenzbalance bleibt gleich. Einschränkung: Für das erste Pack ist die Röhrenstellung nicht dokumentiert.
