# Tekk-Profil aus echten ESX-Sets

Ausgewertet wurden die hochgeladenen Sets CHARTTK24, OLDTEK24, iRRe2LOVEu, 2XETEKK, tekk_terror und CATTY. Doppelte Patterns (die Sets sind teils Versionen desselben Banks) und leere Init-Patterns sind herausgerechnet. Übrig bleiben 138 einzigartige Patterns, davon 136 im Tempo 150–200 BPM. ADRNALZE (Dub/House, 106–140 BPM) und error1 (nur Samples, alle Patterns leer) sind nicht enthalten. Gespeichert werden im Tool nur diese Statistiken, keine Patterns und keine Samples der Urheber.

## Tempo, Raster, Länge

- Zwei Tempo-Lager: 158–168 BPM (Schwerpunkt 159) und 188–192 BPM (Schwerpunkt 188). Dazwischen kaum etwas.
- Swing: in allen 136 Patterns 0 (gerade). Beat: immer 16tel.
- Länge: 8 Takte (71), 4 Takte (42), 3 Takte (12), 2 Takte (10), 5 Takte (1).

## Trefferwahrscheinlichkeit pro Step (1–16)

| Part | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Drum 1 (Kick) | .54 | 0 | .05 | 0 | .81 | 0 | .14 | 0 | .46 | 0 | .08 | 0 | .79 | 0 | .07 | 0 |
| Drum 6A (Hat) | .70 | .16 | .64 | .16 | .70 | .16 | .66 | .15 | .70 | .15 | .59 | .20 | .70 | .20 | .61 | .15 |
| Drum 7A | .53 | 0 | .01 | 0 | .33 | 0 | .02 | 0 | .33 | 0 | .02 | 0 | .33 | 0 | .01 | 0 |
| Accent | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| Keyboard 1 (Bass) | .35 | .56 | .45 | .43 | .43 | .57 | .46 | .52 | .24 | .56 | .52 | .47 | .38 | .57 | .41 | .58 |

Werte für alle Parts stehen im Stil „Tekk gelernt“ im Random-Tab.

## Bass

Keyboard 1 spielt rollende 16tel, 84 % der Noten auf demselben Ton (Keyboard 2: 92 %). Auf Step 1 und vor allem Step 9 seltener: Der Bass weicht der Kick aus.

## Kicks (Samples auf Drum 1, Grundton unter 80 Hz)

16 einzigartige Kick-Samples: Grundton Median 49,8 Hz (G1), Bereich 39–57 Hz; Tail Median 303 ms, Bereich 141–557 ms. Das bestätigt die bisherigen Szene-Messwerte (41–58 Hz, Median 51,9 Hz). Auf Drum 1 liegen in manchen Patterns auch Snares oder Breaks; die sind hier ausgefiltert.

## Datei-Diagnose

- Alle Dateien sind strukturell gültig (Köpfe, Zähler, keine überlappenden Samples, Vorspann an jedem Sample).
- Samplenummer 0x8000 bedeutet „kein Sample“ (auch in Werksdateien).
- CHARTTK24/OLDTEK24/iRRe2LOVEu: Mono-Sample 042 „Recovred“ ist leer (Länge 0xFFFFFFFF); das Tool überspringt es.
- error1.esx: alle 256 Patterns identisch leer, 40 Mono- und 51 Stereo-Samples, Sample-Speicher zu 99,996 % belegt (1092 Bytes frei). Welche Fehlermeldung das Gerät zeigte, lässt sich aus der Datei allein nicht ablesen.
- ESX_ALT_07.zip enthält eine Kopie von ADRNALZE.ESX (bytegleich).
