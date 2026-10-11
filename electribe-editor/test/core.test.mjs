import assert from "node:assert/strict";
import * as c from "../core.js";
for (const n of [0, 1, 6, 7, 8, 13, 14, 15, 100]) {
  const x = Uint8Array.from({ length: n }, (_, i) => (i * 37 + 200) & 255);
  const p = c.pack7(x);
  assert.ok(p.every(v => v < 128), "bit7 gesetzt");
  assert.deepEqual([...c.unpack7(p)], [...x], "roundtrip " + n);
}
const f = c.parseSchema("field a !0x2 u8 0 10 ; A\nfield n 4 ascii 4");
assert.equal(f[0].verified, true); assert.equal(f[1].verified, false);
const b = new Uint8Array(16); c.writeField(b, f[0], 99); assert.equal(c.readField(b, f[0]), 10);
c.writeField(b, f[1], "KICK!"); assert.equal(c.readField(b, f[1]), "KICK");
assert.deepEqual(c.diff(Uint8Array.of(1, 2), Uint8Array.of(1, 3)), [{ offset: 1, a: 2, b: 3 }]);
const sine = Float32Array.from({ length: 4410 }, (_, i) => 0.3 * Math.sin(i / 10));
const wav = c.encodeWav16(44100, sine), s = c.toKorgSample(c.parseWav(wav));
assert.equal(s.rate, 32000); assert.ok(Math.abs(s.data.length - 3200) <= 1);
assert.ok(Math.max(...s.data) > 0.9);
assert.throws(() => c.sysexFrame(0, null, 0, []));
console.log("alle Tests ok");
