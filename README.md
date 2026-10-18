# RFT Designer EMX-1

Browser-Tool (eine Datei, `index.html`) für Hardtekk/RFT-Patterns auf der Korg EMX-1. Kein Build, keine Abhängigkeiten.

## Bereiche

- **Pattern:** 14 EMX-Parts + Accent, 1–8 Takte, Templates (Intro bis Outro), Tonart/Skala, Akkordfolge, Lead-Motiv, Euclid, Mutation, Undo. Der Musik-Check prüft Tonart, Kick-Grundton, Bass/Kick-Kollision, Tail-Budget u. a.
- **Random:** Pattern-Würfel mit Stilen (RFT Hardtekk, Osttekk, Hardtechno/Schranz, Minimal, Chaos), Dichte und Sperre pro Part, Chaos, Fills, Variation. Regeln bleiben: Kick 4/4, Bass nie auf der Hauptkick, Hats nie gleichzeitig, alles in Tonart. Dazu ein Patch-Würfel für Synth 1–5 mit Knopf-Uhrzeiten und das Hi-Hat-Rezept von sequencer.de.
- **Evolution:** 8 Varianten aus dem aktuellen Pattern, Bewertung ▲/▼, nächste Generation aus Favoriten (Kreuzung + Mutation), feste Parts. Call & Response zwischen zwei Parts (Halbtakt oder taktweise).
- **Klang-Labor:** Hoover/Goa, Shepard-Riser, Phantom-Bass, Kombinationston, Terror-Kick als WAV oder Sample-Part (für ESX/DAW, die EMX lädt keine Samples).
- **Kick-Designer:** Synthese mit Messung (Grundton per Autokorrelation 35–200 ms, Tail), Auto-Einmessen, vier Verzerrungsmodi, WAV-Export.
- **Sample-Lab:** ZIP/WAV laden, analysieren, klassifizieren, RFT-Score für Kicks, Kit bauen, ESX-fertig exportieren (mono, 44,1 kHz, −1 dBFS, 8.3-Namen). Sample-Editor mit Schnitt (Nulldurchgang), Fades, Attack/Punch/Klick, Pitch, Reverse. Ein Pack mit 207 Dateien wird als EMX-PCM-Satz erkannt (Nummer = vermutlich PCM-Nummer am Gerät).
- **Spektrum:** Live-Analyse (Mix, Drums, Bass, Musik) gegen Szene-Median oder Referenz-Profil.
- **RFT-Analyse:** Referenztracks messen (Tempo über Kick-Raster, Kick-Grundton, Tail, Bänder, Bassmauer, Bass-Mono-Kompatibilität, Groove-Profil) und auf den Designer anwenden.
- **Datei-Inspektor:** .esx/.emx laden, ASCII-Scan (Pattern-/Sample-Namen), Hex-Viewer, Diff zweier Speicherstände, Schema mit `!` = verifiziert. Keine geratenen Offsets.
- **Motion, FX, Set/Song, Export:** MIDI (Drums Kanal 10), Step-Sheet, Projekt-JSON.

## Bekannte Grenzen

- EMX-MIDI-Noten und CC-Nummern sind Platzhalter, bis sie aus Korgs MIDI-Implementation übernommen werden.
- Kein `.emx`-Schreiben (Offsets nicht verifiziert).
- Szene-Zielwerte stammen aus acht vermessenen Tracks; Bandanteile sind bei Live-Mitschnitten/MP3 nur grob.
- Die Onset-Tempomessung des Skills verwechselt Tempo bei Offbeat-Bass (Test: 170 BPM wurde als 136 geschätzt); maßgeblich ist das Kick-Raster.
