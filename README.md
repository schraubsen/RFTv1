# RFT Designer EMX-1

Browser-Tool (eine Datei, `index.html`) für Hardtekk/RFT-Patterns auf der Korg EMX-1. Kein Build, keine Abhängigkeiten. Optik im Blau der EMX-1 (weiße Tasten, orange = aktiv).

## Bereiche

- **Panel (Startseite):** Frontplatte nach dem echten EMX-1-Layout, Handy zuerst. Orange LCD, Part-Tasten (Drum 1–5, 6A/6B, 7A/7B, Accent, Synth 1–5), 16 Step-Tasten mit Seiten pro Takt und Playhead-LEDs, Pattern-Übersicht, Drehregler (Ziehen, Mausrad, Pfeiltasten, Doppelklick = Standard) für Tempo, Swing, Master, Tube, Part-Level, Osc Type (16 Typen vom Bedienfeld), Edit 1/2, Filter-Typ, Cutoff, Resonanz, EG Int, Drive, Attack, EG Time sowie Effect-Typ (16) mit FX Edit 1/2. Tap-Tempo, Mute, Solo, Clear Part, Undo, Template und Tonart. Motion Rec wie am Gerät: bei laufendem Pattern Cutoff oder Level drehen, die Werte landen pro Step in der Motion-Spur (Clear Motion löscht sie). „▶ Emulation“ spielt den Patch mit der Klang-Labor-Engine. Synth-Klang im Browser ist eine Näherung.
- **Zoom:** auf dem Handy Standard 80 %, per − / + im Kopf einstellbar (60–125 %), wird gemerkt. Tab-Leiste scrollt in einer Zeile, weitere Regler hinter „⋯“.

- **Raster (früher Pattern):** 14 EMX-Parts + Accent, 1–8 Takte, Templates (Intro bis Outro), Tonart/Skala, Akkordfolge, Lead-Motiv, Euclid, Mutation, Undo. Der Musik-Check prüft Tonart, Kick-Grundton, Bass/Kick-Kollision, Tail-Budget u. a.
- **Random:** Pattern-Würfel mit Stilen (Tekk gelernt aus 136 echten ESX-Patterns, Hardtekk rollend, Osttekk, Hardtechno/Schranz, Minimal, Chaos), Dichte und Sperre pro Part, Chaos, Fills, Variation. Regeln bleiben: Kick 4/4, Bass nie auf der Hauptkick, Hats nie gleichzeitig, alles in Tonart. Dazu ein Patch-Würfel für Synth 1–5 mit Knopf-Uhrzeiten und das Hi-Hat-Rezept von sequencer.de.
- **Custom Build:** Pattern mit Schiebereglern formen: Master-Fader für Tempo, Swing, Chaos, Fills, dazu pro Part ein Kanalzug mit Muster, Dichte, Pegel, Swing an/aus, Mute und Sperre. Jede Änderung baut das Pattern sofort neu, die Regeln bleiben.
- **Swing:** Off-16tel werden um (Swing/50 − 1) × Step verschoben, in der Vorschau und im MIDI-Export (50 % gerade, 66 % triolisch).
- **Evolution:** 8 Varianten aus dem aktuellen Pattern, Bewertung ▲/▼, nächste Generation aus Favoriten (Kreuzung + Mutation), feste Parts. Call & Response zwischen zwei Parts (Halbtakt oder taktweise).
- **Klang-Labor:** EMX-Synth-Emulation (alle 16 Oszillatortypen vom Bedienfeld inkl. PCM+Comb, PCM+WS und Audio In+Comb als Näherung, TPT-Filter, EG, LFO, Drive) mit Chaos und Psycho, Presets, Datenblatt mit Knopfstellungen.
- **Generatoren:** Hoover/Goa, Shepard-Riser, Phantom-Bass, Kombinationston, Terror-Kick als WAV oder Sample-Part (für ESX/DAW, die EMX lädt keine Samples).
- **Kick-Designer:** Synthese mit Messung (Grundton per Autokorrelation 35–200 ms, Tail), Auto-Einmessen, vier Verzerrungsmodi, WAV-Export.
- **Sample-Lab:** ZIP/WAV laden, analysieren, klassifizieren, RFT-Score für Kicks, Kit bauen, ESX-fertig exportieren (mono, 44,1 kHz, −1 dBFS, 8.3-Namen). Sample-Editor mit Schnitt (Nulldurchgang), Fades, Attack/Punch/Klick, Pitch, Reverse. Ein Pack mit 207 Dateien wird als EMX-PCM-Satz erkannt (Nummer = vermutlich PCM-Nummer am Gerät). Dateinamen aus Slopes ReFill („PRC - EMX-1 ([138] Bng…)“) und dem Schema „EMX-1 BD-25“ liefern Kategorie und PCM-Nummer; die Messung bleibt sichtbar.
- **Spektrum:** Analyzer im SPAN-Stil (FFT bis 32768, Glättung, 4,5 dB/Okt-Neigung, Peak-Hold, Einfrieren, Maus-Readout mit Note), Pegel/RMS/Crest/Korrelation, Clip-Zähler und Bus-Headroom vor der Röhre, Bänder gegen Ziel, Low-End-Balance und Sweetspot (Kick gegen Bass-Töne, Intervalle, Sub-Verteilung live). Alle Zeichenflächen in HiDPI.
- **RFT-Analyse:** Referenztracks messen (Tempo über Kick-Raster, Kick-Grundton, Tail, Bänder, Bassmauer, Bass-Mono-Kompatibilität, Groove-Profil, Transienten, Clipping) und auf den Designer anwenden. Die Arrangement-Erkennung teilt den Track in Takte und Abschnitte (Intro, Groove, Break, Build, Drop, Outro). „Arrangement als Set-Kette übernehmen“ legt dafür Slots und die Song-Kette an.
- **Datei-Inspektor:** .esx/.emx laden, ASCII-Scan (Pattern-/Sample-Namen), Hex-Viewer, Diff zweier Speicherstände, Schema mit `!` = verifiziert. ESX-Dateien werden komplett decodiert (256 Patterns mit Tempo, Swing, Länge, Beat, FX-Kette, Part-Parametern und Step-Raster, Samples, Songs); Feldkarte in `schema/esx1.def`, abgeleitet aus dem Open Electribe Editor (siehe `docs/open-electribe-editor-analyse.md`). Ein ESX-Pattern lässt sich in den Designer übernehmen oder als MIDI-Datei exportieren (einzeln oder alle belegten als ZIP); Motion-Spuren werden mit Part und Verlauf angezeigt. Samples der .esx lassen sich anhören, einzeln oder gesammelt als WAV (ZIP) exportieren und ins Sample-Lab übernehmen; an echten Werksdaten Sample für Sample bestätigt. Für EMX- und unbekannte Dateien schätzt eine Struktur-Sonde Chunk-Größe und Startadresse.
- **MIDI-Live:** EMX per Web MIDI steuern (Clock + Start/Stop, Noten, CC, Program Change, Panic), eingehende Clock anzeigen, SysEx-Dumps mitschneiden, als .syx speichern, entpackt vergleichen und senden. Chrome/Edge am Rechner mit DIN-MIDI-Interface; in der Artifact-Vorschau meist gesperrt. Übersicht der Möglichkeiten: `docs/emx1-moeglichkeiten.md`.
- **Tempo:** 20–300 BPM wie am Gerät, Kommastellen erlaubt.
- **FX-Vorschau:** Jeder Effekt-Bus wird nach seinem Typ gebaut; die Vorschau rechnet Short Delay, BPM Sync Delay und Reverb, andere Typen bleiben stumm statt falsch zu klingen.
- **Motion, FX, Set/Song, Export:** MIDI (Drums Kanal 10), Step-Sheet, Projekt-JSON.

## Tekk-Profil aus echten Sets

136 einzigartige Patterns aus 6 ESX-Sets: Tempo-Lager 158–168 und 188–192 BPM, Swing 0, rollender 16tel-Bass auf einem Ton, FX-Kette Compressor → EQ → Ring Mod/BPM Delay auf Maximum, Kick-Samples mit Grundton um 50 Hz (39–57 Hz) und Tail um 300 ms. Details in `docs/tekk-profil-esx.md`.

## Messbefund Röhre

Vergleich zweier Aufnahmen derselben 207 EMX-Sounds (ohne Angabe gegen Tube 50): +2,7 dB RMS bei +0,4 dB Peak, Crest −2,1 dB, Frequenzbalance unverändert. Details in `docs/open-electribe-editor-analyse.md`.

## Bekannte Grenzen

- EMX-MIDI-Noten und CC-Nummern sind Platzhalter, bis sie aus Korgs MIDI-Implementation übernommen werden.
- Kein `.emx`-Schreiben (Offsets nicht verifiziert). Für die EMX gibt es noch keine Feldkarte; die ESX-Karte stammt aus dem Open Electribe Editor und ist nicht von uns am Gerät geprüft. Step-Reihenfolge und Keyboard-Noten-Flag sind an fünf echten Dateien statistisch belegt, aber nicht per Einzeltest am Gerät.
- Szene-Zielwerte stammen aus acht vermessenen Tracks; Bandanteile sind bei Live-Mitschnitten/MP3 nur grob.
- Die Stil-Vorgaben sind Mittelwerte aus Szene-Tracks, nicht an RFT-Record-Veröffentlichungen gemessen. Für echte RFT-Werte eigene Tracks in der RFT-Analyse laden.
- Arrangement-Erkennung: Im Test (170 BPM, 64 Takte) lagen Intro, Groove, Break und Outro taktgenau. Build und Drop waren um 2 Takte verschoben, weil laute Snare-Rolls wie ein Drop wirken.
- Die Onset-Tempomessung des Skills verwechselt Tempo bei Offbeat-Bass (Test: 170 BPM wurde als 136 geschätzt); maßgeblich ist das Kick-Raster.
