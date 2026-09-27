# Schema-Dateiformat (`.def`)

Die Byte-Layouts von `.esx`/`.emx` sind von Korg nicht dokumentiert. Alles, was
wir darüber wissen, ist reverse engineered und kann falsch sein. Deshalb landet
kein Offset im C++-Code — nur in diesen Textdateien, die `electribe_core` zur
Laufzeit lädt.

## Zeilenformat

```
<offset> <length> <name> <type> [# notes]
```

- **offset**: Hex-Adresse ab Dateianfang, z.B. `0x0010`.
  - Mit `!`-Präfix direkt vor dem Offset (`!0x0010`) heißt: **auf echter
    Hardware verifiziert** (per `etx diff`, siehe `docs/ARCHITECTURE.md`).
  - Ohne `!`-Präfix: **Vermutung, unbestätigt**. Jede Ausgabe, die dieses Feld
    anzeigt, muss das als unbestätigt kennzeichnen.
- **length**: Feldlänge in Bytes.
- **name**: Bezeichner (ohne Leerzeichen), z.B. `pattern_length`.
- **type**: eines von `u8`, `u16le`, `u16be`, `ascii`, `bytes`, `bitfield`.
- **notes** (optional): freier Text nach `#`. Bei verifizierten Feldern das
  Verifikationsdatum eintragen, z.B. `# verified 2026-09-27, 2x etx diff`.

Leerzeilen und Zeilen, die mit `#` beginnen, sind Kommentare.

## Status

Aktuell sind **keine** Offsets verifiziert — die Dateien enthalten nur eine
`EXAMPLE`-Zeile zur Illustration des Formats. Die eigentliche Befüllung
passiert über den in `docs/ARCHITECTURE.md` beschriebenen Offset-Discovery-
Workflow (`etx diff before.esx after.esx`, ein Parameter pro Durchgang).

Erfundene Offsets aus dem Gedächtnis einzutragen wäre schlimmer als eine
leere Datei — sie würden als Tatsache missverstanden. Lieber leer lassen, bis
echte Hardware-Diffs vorliegen.
