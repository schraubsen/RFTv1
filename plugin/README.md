# Realtime-Control: MIDI-Note/CC-Ansatz

Geplantes Modul für Live-Steuerung/Sequencing der ESX-1/EMX-1 aus der DAW
heraus. Kein Datei-Backup hier - das läuft laut Architekturregel in
`docs/ARCHITECTURE.md` separat über die Standalone-App (`standalone/`).

## Kurskorrektur gegenüber der ersten Version

Der ursprüngliche Plan sah ein volles VST3-Plugin mit JUCE vor und wartete
auf das JUCE-SDK. Die Referenz-Tools zeigen einen einfacheren, schon
bewährten Weg:

- **reaJS / "electribe-vstx-32/64"**: steuert/sequenziert ESX/EMX rein über
  normales MIDI (Noten + CC) via Kabel von der DAW zur Hardware. Kein SysEx,
  keine Audio-DSP, kein JUCE - nur ein MIDI-Router mit Mapping-Tabelle.
  Laut Disclaimer des Autors sind die EMX-Skripte dort nie fertig geworden
  (er besaß keine EMX) - das ist also selbst dort nur teilweise abgedeckt.
- **Electribome**: nutzt die MIDI-Keyboard-Matrix der ESX/EMX (16 Spalten,
  9 Zeilen bei ESX-Drum-Parts bzw. 5 Zeilen bei EMX-Keyboard-Parts) als
  Button-Grid, ähnlich einem Monome - reine Noten-Zuordnung, kein CC nötig.

Für uns heißt das: das Realtime-Modul braucht **kein VST3/JUCE**, um
brauchbar zu sein. Ein deutlich schnellerer erster Schritt ist ein
**JSFX-Skript für REAPER** (Text-Datei, kompiliert nichts, sendet direkt
MIDI) nach demselben Prinzip wie reaJS - plus optional ein schlankes
plattformunabhängiges MIDI-Routing-Tool in `electribe_core`-Nähe für
Nutzer ohne REAPER.

## Geplante Architektur

1. **`electribe.jsfx`** (REAPER-JSFX, kein SDK, kein Build-Schritt):
   nimmt DAW-Automation/CC entgegen und schickt passende MIDI-Note/CC-
   Nachrichten an den Hardware-MIDI-Ausgang. Direktes Äquivalent zu reaJS,
   aber von uns gepflegt statt nachgebaut aus einer alten Distribution.
2. **Note/CC-Mapping-Tabelle** (`plugin/midi_map.md`): genau wie bei den
   Datei-Offsets gilt hier die gleiche Regel - Werte nur aus der
   MIDI-Implementation-Chart im Handbuch-Anhang übernehmen, niemals raten.
   Aktuell ist die Tabelle ein leeres Template.
3. **Button-Grid-Modus** (später, nach Electribome-Vorbild): 16×9 (ESX) /
   16×5 (EMX) Notengrid für einen Step-/Pad-Controller-Modus, sobald die
   Note-Zuordnung aus Punkt 2 steht.
4. Ein "echtes" VST3/JUCE-Plugin bleibt eine mögliche spätere Ausbaustufe,
   ist aber kein Blocker mehr für ein nutzbares Realtime-Tool.

## Nächste Schritte

1. `plugin/midi_map.md` mit den echten Note-/CC-Nummern aus der
   MIDI-Implementation-Chart befüllen (ESX zuerst, EMX ggf. erst nach
   Zugriff auf echte Hardware - siehe Disclaimer oben, das ist auch anderen
   schon nicht gelungen).
2. `electribe.jsfx` gegen die Tabelle implementieren, mit echter Hardware
   testen (MIDI-Interface mit DIN-Buchsen, kein Scarlett 2i2/Solo).
3. Button-Grid-Modus nach Electribome-Vorbild ergänzen.
