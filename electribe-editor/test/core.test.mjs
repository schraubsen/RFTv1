import assert from "node:assert/strict";
import * as c from "../core.js";
for (const n of [0, 1, 6, 7, 8, 13, 14, 15, 100]) {
  const x = Uint8Array.from({ length: n }, (_, i) => (i * 37 + 200) & 255);
  const p = c.pack7(x);
  assert.ok(p.every(v => v < 128), "bit7 gesetzt");
  assert.deepEqual([...c.unpack7(p)], [...x], "roundtrip " + n);
}
const f = c.parseSchema("field a !0x2 u8 0 10 ; A\nfield n 4 ascii 4").fields;
assert.equal(f[0].verified, true); assert.equal(f[1].verified, false);
const b = new Uint8Array(16); c.writeField(b, f[0], 99); assert.equal(c.readField(b, f[0]), 10);
c.writeField(b, f[1], "KICK!"); assert.equal(c.readField(b, f[1]), "KICK");
assert.deepEqual(c.diff(Uint8Array.of(1, 2), Uint8Array.of(1, 3)), [{ offset: 1, a: 2, b: 3 }]);
const sine = Float32Array.from({ length: 4410 }, (_, i) => 0.3 * Math.sin(i / 10));
const wav = c.encodeWav16(44100, sine), s = c.toKorgSample(c.parseWav(wav));
assert.equal(s.rate, 32000); assert.ok(Math.abs(s.data.length - 3200) <= 1);
assert.ok(Math.max(...s.data) > 0.9);
assert.throws(() => c.sysexFrame(0, null, 0, []));
assert.deepEqual([...c.requestFrame(0, c.MODEL_ID.ESX1, 0x10)], [0xf0, 0x42, 0x30, 0x71, 0x10, 0xf7]);
{ // Tabellen, Bitfelder, Enums
  const sc = c.parseSchema("table t 4 8 3\nfield lo ~0 u8 @0:3 0 7\nfield hi ~0 u8 @4:2 0=a 1=b_c\nfield w ~2 u16be 0 999");
  const m = new Uint8Array(40); c.writeField(m, sc.fields[0], 5, 2); c.writeField(m, sc.fields[1], 1, 2); c.writeField(m, sc.fields[2], 300, 1);
  assert.equal(m[20], 5 | (1 << 4)); assert.equal(c.readField(m, sc.fields[0], 2), 5); assert.equal(c.readField(m, sc.fields[2], 1), 300);
  assert.equal(sc.fields[1].enum[1], "b c"); assert.equal(sc.fields[0].trust, "ref");
  assert.throws(() => c.readField(m, sc.fields[0], 3));
}
import("node:fs").then(({ existsSync, readFileSync }) => { // echte Datei, falls vorhanden
  const p = process.env.ESX_FILE || "/tmp/default.esx"; if (!existsSync(p)) return console.log("(default.esx fehlt: Realdatei-Test übersprungen)");
  const d = new Uint8Array(readFileSync(p)), sc = c.parseSchema(readFileSync(new URL("../schema/esx1.def", import.meta.url), "utf8"));
  const g = (t, id, i = 0) => c.readField(d, sc.fields.find(x => x.table === t && x.id === id), i);
  assert.equal(c.detectKind("x", d), "ESX-1"); assert.equal(g("pattern", "tempo_bpm"), 120); assert.equal(g("sample", "rate"), 44100);
  assert.equal(g("drum1", "pan"), 64); console.log("Realdatei-Test ok");
});
console.log("alle Tests ok");
