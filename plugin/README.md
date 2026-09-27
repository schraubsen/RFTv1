# VST3-Plugin: Realtime-Control

Geplantes Modul für Live-CC-Steuerung der ESX-1/EMX-1 aus der DAW heraus
(Filter, Effekte etc. während des Sets). Kein Datei-Backup - das läuft laut
Architekturregel in `docs/ARCHITECTURE.md` separat über die Standalone-App
(`standalone/`), weil DAWs SysEx aus Plugins oft filtern.

## Warum hier noch kein Code liegt

Ein VST3-Plugin braucht ein GUI-/Plugin-Framework (typischerweise JUCE) als
Wrapper um `electribe_core`. Das SDK ist in dieser Session nicht verfügbar
und wurde nicht heruntergeladen - ein Plugin-Grundgerüst ohne echtes SDK
würde nicht compilieren und nur Schein-Code erzeugen. Deshalb bleibt es bei
diesem Plan, bis das SDK eingebunden wird.

## Geplante Architektur

- `electribe_core` bleibt frei von JUCE (nicht-negotiable Regel). Das Plugin
  linkt `electribe_core` und legt JUCE/VST3-Code ausschließlich in diesem
  Verzeichnis ab.
- Realtime-Control-Mapping: MIDI-CC -> Electribe-Parameter, basierend auf der
  offiziellen MIDI-Implementation-Chart (CC-Zuordnung ist dort dokumentiert,
  im Gegensatz zu den Datei-Offsets).
- Kein Bulk-Dump/Restore im Plugin-Code.

## Nächste Schritte

1. JUCE SDK (oder Alternative) einbinden.
2. CC-Mapping-Tabelle aus der MIDI-Implementation-Chart übernehmen (mit
   Quellenverweis, keine Vermutungen).
3. Minimal-Plugin: ein Parameter, ein CC, End-to-End getestet mit echter
   Hardware.
