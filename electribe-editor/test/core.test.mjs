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
{ const sc = c.parseSchema("table t 0 4 2\nseq s 1 2"), b = new Uint8Array(8); c.setStep(b, sc.seqs[0], 1, 9, true);
  assert.equal(b[6], 2); assert.equal(c.getStep(b, sc.seqs[0], 1, 9), 1); c.setStep(b, sc.seqs[0], 1, 9, false); assert.equal(b[6], 0);
  assert.equal(c.getStep(b, sc.seqs[0], 2, 0), null); }
{ // EMX-Schema gegen synthetische Datei
  const fs = await import("node:fs"); const sc = c.parseSchema(fs.readFileSync(new URL("../schema/emx1.def", import.meta.url), "utf8"));
  const b = new Uint8Array(0x1a8000); b.set([..."KORG"].map(x => x.charCodeAt(0)), 0); b[7] = 0x69; b.set([..."EMX"].map(x => x.charCodeAt(0)), 8);
  assert.equal(c.detectKind("a.emx", b), "EMX-1");
  const f = (t, id) => sc.fields.find(x => x.table === t && x.id === id);
  c.writeField(b, f("synth2", "cutoff"), 99, 3); assert.equal(b[512 + 3 * 4806 + 534 + 7], 99);
  c.writeField(b, f("song", "name"), "TEKK", 5); assert.equal(String.fromCharCode(...b.subarray(0x130000 + 5 * 528, 0x130000 + 5 * 528 + 4)), "TEKK");
  c.setStep(b, sc.seqs.find(q => q.table === "drum3"), 0, 0, true); assert.equal(b[512 + 76 + 10], 1);
}
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
  assert.equal(g("drum1", "pan"), 64);
  const q = sc.seqs[0]; assert.equal(Array.from({ length: 16 }, (_, i) => c.getStep(d, q, 0, i)).join(""), "1000100010001000"); // Four-on-the-floor
  const kb = sc.arrs.find(a => a.table === "keyboard1" && a.id === "notes"); assert.ok(c.getArr(d, kb, 0, 0) >= 0);
  assert.equal(g("accent", "level"), 64); assert.equal(g("audioin", "level"), 100); assert.equal(g("keyboard1", "cutoff"), 127);
  c.setArr(d, kb, 3, 5, 60); assert.equal(c.getArr(d, kb, 3, 5), 60); assert.throws(() => c.setArr(d, kb, 3, 128, 1));
  console.log("Realdatei-Test ok");
});
console.log("alle Tests ok");
{ const fs = await import("node:fs");
  for (const f of ["esx1", "emx1"]) { // Events-Tabelle: Bitfelder Measure/Step
    const sc = c.parseSchema(fs.readFileSync(new URL(`../schema/${f}.def`, import.meta.url), "utf8")), b = new Uint8Array(0x130000 + 64 * 528 + 20000 * 8);
    const ff = id => sc.fields.find(x => x.table === "events" && x.id === id);
    c.writeField(b, ff("measure"), 5, 1000); c.writeField(b, ff("step"), 9, 1000);
    assert.equal(b[0x130000 + 64 * 528 + 8000 + 1], 0x59); assert.throws(() => c.readField(b, ff("op"), 20000));
  } console.log("Events-Test ok"); }

{ // Echte EMX-Bänke (EMX_FILES=pfad1:pfad2), falls vorhanden
  const fs = await import("node:fs"), list = (process.env.EMX_FILES || "").split(":").filter(p => p && fs.existsSync(p));
  if (!list.length) console.log("(keine echten .EMX: Realdatei-Test übersprungen)");
  const sc = c.parseSchema(fs.readFileSync(new URL("../schema/emx1.def", import.meta.url), "utf8"));
  for (const p of list) {
    const d = new Uint8Array(fs.readFileSync(p)); assert.equal(c.detectKind(p, d), "EMX-1"); assert.equal(d.length, 0x1a8000);
    let bad = 0, n = 0;
    for (const f of sc.fields) { if (f.type === "ascii" || ["events"].includes(f.table) || f.id === "length_tempo_mute" || f.id === "note_or_value") continue;
      for (let i = 0; i < Math.min(256, f.tbl.count); i++) { const v = c.readField(d, f, i); n++; if ((f.min != null && v < f.min) || (f.max != null && v > f.max)) bad++; } }
    assert.equal(bad, 0, p + ": Werte außerhalb Schema-Bereich: " + bad);
    const f = id => sc.fields.find(x => x.table === "pattern" && x.id === id);
    assert.ok(c.readField(d, f("tempo_bpm"), 0) >= 20); assert.match(c.readField(d, f("name"), 0), /^[\x20-\x7e]+$/);
    const sn = sc.fields.find(x => x.table === "song" && x.id === "name"); assert.equal(c.readField(d, sn, 1), "RFT GRVE");
  }
  if (list.length) console.log("Echte EMX-Bänke ok:", list.length);
}
