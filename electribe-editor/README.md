# Electribe Matrix Studio (ESX-1 / EMX-1 Editor)

Start: `python3 -m http.server -d electribe-editor 8000` → http://localhost:8000 · Tests: `node test/core.test.mjs`

Funktional: .esx/.emx laden/speichern, schema-getriebene Parameter-Editoren, Hex-Editor, Diff (Offset-Discovery),
ASCII-Scan, WAV→32 kHz/mono/16 Bit/normalisiert, Korg pack7/unpack7.

Ehrlich offen: Das Dateiformat ist undokumentiert; `schema/*.def` enthält bewusst **keine geratenen Offsets**.
Per Diff-Tab (before/after, ein Parameter) ermitteln und mit `!` eintragen. SysEx-Model-IDs: TODO verifizieren.
