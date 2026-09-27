# Multishotifier

Baut aus einem Ordner voller `.wav`-Samples eine `multishot.wav`, die auf dem
Korg Electribe SX/MX per Start-Position-Knob (0..127) angesteuert wird.
Reine Python-Stdlib, kein SoX nötig.

## Nutzung

```
python3 multishotifier.py <input_dir> <output.wav> [Optionen]
```

Optionen:

- `--max-shots N` maximale Anzahl Slots (default 128, ESX/EMX-Limit)
- `--pad silence|reversed` Auffüllung kürzerer Samples (default `silence`)
- `--gap-ms N` Stille-Lücke nach jedem Shot (default 10 ms, hilft
  Hardware-Autoslice)
- `--no-normalize` Peak-Normalisierung deaktivieren
- `--rate HZ` Ziel-Samplerate (default: Rate des ersten Samples)
- `--mono` / `--stereo` erzwingt Kanalzahl der Ausgabe
- `--manifest PATH` Pfad für die JSON-Manifest-Datei

Nach dem Lauf zeigt die Konsole für jede Datei den Start-Position-Knob-Wert
an, mit dem sie auf der Hardware angewählt wird (Slot-Index 0..N-1, nur
korrekt solange alle Slots gleich lang sind - deswegen das Padding).

## Bekannte Einschränkungen

- Ausgabeformat ist fest 16-bit linear PCM (Werkzeug-Voreinstellung, keine
  verifizierte ESX/EMX-Spezifikation).
- Nutzt das `audioop`-Modul, das in Python 3.13 aus der Stdlib entfernt wird.
  Auf neueren Pythons ggf. das Backport-Paket `audioop-lts` installieren.
- Kein Auto-Slice-Detection wie im Original-Konzept von
  `coderofsalvation/sample-multi-shotifier` - hier wird bewusst 1 Datei = 1
  Shot gehalten, für automatische Loop-Zerschneidung siehe die Slice-Engine
  in `docs/ARCHITECTURE.md`.
