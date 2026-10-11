// electribe core: kein DOM, läuft im Browser und in Node.
// ESX-1: 0x71 laut Korg ESX1midiimp.txt (Header F0,42,3g,71). EMX-1: TODO verifizieren (EMX1midiimp.txt).
export const MODEL_ID = { ESX1: 0x71, EMX1: 0x69 }; // EMX1: 0x69 aus EMiX (F0 42 3g 69 58 = Song-Load, Antwort 23h ok / 24h Fehler); Request-Funktionscodes des EMX nicht verifiziert
export const FUNC = { CURRENT_PATTERN_REQ: 0x10, PATTERN_REQ: 0x1c, CURRENT_SONG_REQ: 0x0a, ALL_SONG_REQ: 0x0b, GLOBAL_REQ: 0x0e };
export function requestFrame(channel, modelId, func, arg) {
  if (modelId == null) throw new Error("Model-ID unbekannt (TODO: verifizieren)");
  return Uint8Array.from([0xf0, 0x42, 0x30 | (channel & 15), modelId, func, ...(arg == null ? [] : [arg & 0x7f]), 0xf7]);
}

// ---- Korg 7-Bit-Kodierung: Carrier-Byte (MSBs) + bis zu 7 Nutzbytes ----
export function pack7(data) {
  const out = [];
  for (let i = 0; i < data.length; i += 7) {
    const n = Math.min(7, data.length - i);
    let msb = 0;
    for (let j = 0; j < n; j++) if (data[i + j] & 0x80) msb |= 1 << j;
    out.push(msb);
    for (let j = 0; j < n; j++) out.push(data[i + j] & 0x7f);
  }
  return Uint8Array.from(out);
}
export function unpack7(data) {
  const out = [];
  for (let i = 0; i < data.length; i += 8) {
    const msb = data[i], n = Math.min(7, data.length - i - 1);
    for (let j = 0; j < n; j++) out.push(data[i + 1 + j] | ((msb >> j) & 1 ? 0x80 : 0));
  }
  return Uint8Array.from(out);
}
export function sysexFrame(channel, modelId, func, payload) {
  if (modelId == null) throw new Error("Model-ID unbekannt (TODO: verifizieren)");
  return Uint8Array.from([0xf0, 0x42, 0x30 | (channel & 15), modelId, func, ...pack7(payload), 0xf7]);
}

// ---- Schema ----
// table <id> <base> <stride> <count> ; Titel   -> folgende fields sind relativ zu base + index*stride
// field <id> <offset> <type> [@lo:n] [min max] [wert=name ...] ; Label
// Vertrauen: "!off" verifiziert (Hardware) | "~off" Referenzquelle (Korg-Doku/lammas, in default.esx plausibilisiert) | "off" Vermutung
const TYPES = { u8: 1, u16le: 2, u16be: 2, u32be: 4, ascii: 0 };
export function parseSchema(text) {
  const fields = [], tables = [], seqs = [], arrs = []; let table = null;
  text.split(/\r?\n/).forEach((raw, i) => {
    const line = raw.trim(), err = m => new Error(`Schema Zeile ${i + 1}: ${m}`);
    if (!line || line[0] === "#") return;
    const [spec, label = ""] = line.split(";");
    const t = spec.trim().split(/\s+/);
    const num = x => { const n = Number(x); if (!Number.isInteger(n) || n < 0) throw err("Zahl " + x); return n; };
    if (t[0] === "table") {
      if (t.length < 5) throw err("table braucht id base stride count");
      table = { id: t[1], base: num(t[2]), stride: num(t[3]), count: num(t[4]), title: label.trim() || t[1] };
      tables.push(table); return;
    }
    if (t[0] === "seq") { // seq <id> <offset> <bytes> ; Label  (Bit0 = Step 1, laut Korg TABLE23)
      if (t.length < 4 || !table) throw err("seq braucht table, id, offset, bytes");
      let o = t[2], trust = "guess"; if (o[0] === "!") { trust = "verified"; o = o.slice(1); } else if (o[0] === "~") { trust = "ref"; o = o.slice(1); }
      seqs.push({ id: t[1], offset: num(o), bytes: num(t[3]), trust, label: label.trim() || t[1], table: table.id, tbl: table }); return;
    }
    if (t[0] === "arr") { // arr <id> <offset> <count> <min> <max> ; Label   (Byte-Array, z.B. Keyboard-Noten/Gates)
      if (t.length < 6 || !table) throw err("arr braucht table, id, offset, count, min, max");
      let o = t[2], trust = "guess"; if (o[0] === "!") { trust = "verified"; o = o.slice(1); } else if (o[0] === "~") { trust = "ref"; o = o.slice(1); }
      arrs.push({ id: t[1], offset: num(o), count: num(t[3]), min: num(t[4]), max: num(t[5]), trust, label: label.trim() || t[1], table: table.id, tbl: table }); return;
    }
    if (t[0] !== "field" || t.length < 4) throw err("ungültig");
    let off = t[2], trust = "guess";
    if (off[0] === "!") { trust = "verified"; off = off.slice(1); } else if (off[0] === "~") { trust = "ref"; off = off.slice(1); }
    const type = t[3];
    if (!(type in TYPES)) throw err("Typ " + type);
    const f = { id: t[1], offset: num(off), trust, verified: trust === "verified", type, label: label.trim() || t[1], table: table && table.id, tbl: table };
    const rest = t.slice(4), nums = [];
    for (const r of rest) {
      if (r[0] === "@") { const [lo, n] = r.slice(1).split(":").map(Number); if (!(n > 0) || lo < 0 || lo + n > TYPES[type] * 8) throw err("Bitbereich"); f.lo = lo; f.bits = n; }
      else if (r.includes("=")) { const [k, ...v] = r.split("="); (f.enum ||= {})[num(k)] = v.join("=").replace(/_/g, " "); }
      else nums.push(num(r));
    }
    if (type === "ascii") { f.len = nums[0]; if (!f.len) throw err("len"); } else { f.min = nums[0]; f.max = nums[1]; }
    fields.push(f);
  });
  return { fields, tables, seqs, arrs };
}
const size = f => (f.type === "ascii" ? f.len : TYPES[f.type]);
const absOff = (f, idx = 0) => {
  if (f.tbl && (idx < 0 || idx >= f.tbl.count)) throw new Error("Index außerhalb der Tabelle");
  return f.offset + (f.tbl ? f.tbl.base + idx * f.tbl.stride : 0);
};
export function readField(buf, f, idx = 0) {
  const o = absOff(f, idx);
  if (o + size(f) > buf.length) return null;
  if (f.type === "ascii") return String.fromCharCode(...buf.subarray(o, o + f.len)).replace(/[\0 ]+$/, "");
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  let v = f.type === "u8" ? buf[o] : f.type === "u16le" ? dv.getUint16(o, true) : f.type === "u16be" ? dv.getUint16(o, false) : dv.getUint32(o, false);
  if (f.bits) v = Math.floor(v / 2 ** f.lo) % 2 ** f.bits;
  return v;
}
export function writeField(buf, f, v, idx = 0) {
  const o = absOff(f, idx);
  if (o + size(f) > buf.length) throw new Error("Offset außerhalb der Datei");
  if (f.type === "ascii") { for (let i = 0; i < f.len; i++) buf[o + i] = i < v.length ? v.charCodeAt(i) & 0x7f : 0x20; return; }
  v = Number(v);
  if (!Number.isFinite(v)) throw new Error("Zahl erwartet");
  v = Math.round(v);
  const lim = f.bits ? 2 ** f.bits - 1 : 2 ** (TYPES[f.type] * 8) - 1;
  v = Math.max(f.min ?? 0, Math.min(f.max ?? lim, lim, v));
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength), n = TYPES[f.type], le = f.type === "u16le";
  let cur = 0; for (let i = 0; i < n; i++) cur = cur * 256 + buf[o + (le ? n - 1 - i : i)];
  if (f.bits) { const m = 2 ** f.bits, hi = Math.floor(cur / 2 ** (f.lo + f.bits)); cur = hi * 2 ** (f.lo + f.bits) + v * 2 ** f.lo + (cur % 2 ** f.lo); }
  else cur = v;
  for (let i = 0; i < n; i++) { buf[o + (le ? i : n - 1 - i)] = cur % 256; cur = Math.floor(cur / 256); }
}
export function getStep(buf, q, idx, step) {
  const o = q.offset + q.tbl.base + idx * q.tbl.stride + (step >> 3);
  if (idx < 0 || idx >= q.tbl.count || step < 0 || step >= q.bytes * 8 || o >= buf.length) return null;
  return (buf[o] >> (step & 7)) & 1;
}
export function setStep(buf, q, idx, step, on) {
  if (getStep(buf, q, idx, step) === null) throw new Error("Step außerhalb");
  const o = q.offset + q.tbl.base + idx * q.tbl.stride + (step >> 3), m = 1 << (step & 7);
  buf[o] = on ? buf[o] | m : buf[o] & ~m;
}
export function getArr(buf, a, idx, i) {
  const o = a.offset + a.tbl.base + idx * a.tbl.stride + i;
  return idx < 0 || idx >= a.tbl.count || i < 0 || i >= a.count || o >= buf.length ? null : buf[o];
}
export function setArr(buf, a, idx, i, v) {
  if (getArr(buf, a, idx, i) === null) throw new Error("Array-Index außerhalb");
  v = Math.round(Number(v)); if (!Number.isFinite(v)) throw new Error("Zahl erwartet");
  buf[a.offset + a.tbl.base + idx * a.tbl.stride + i] = Math.max(a.min, Math.min(a.max, v));
}
export function tempoBpm(buf, idx = 0, base = 0x200, stride = 4280) { // 9 Bit ganz (Bit7..) + 4 Bit Dezimal, laut lammas/Korg
  const v = (buf[base + idx * stride + 8] << 8) | buf[base + idx * stride + 9]; return ((v >> 7) & 0x1ff) + (v & 15) / 10;
}

// ---- Analyse ----
export function diff(a, b) {
  const res = [], n = Math.max(a.length, b.length);
  for (let i = 0; i < n; i++) if (a[i] !== b[i]) res.push({ offset: i, a: a[i], b: b[i] });
  return res;
}
export function scanAscii(buf, minLen = 4) {
  const res = []; let s = -1;
  for (let i = 0; i <= buf.length; i++) {
    const p = i < buf.length && buf[i] >= 32 && buf[i] < 127;
    if (p && s < 0) s = i;
    if (!p && s >= 0) {
      if (i - s >= minLen) res.push({ offset: s, text: String.fromCharCode(...buf.subarray(s, i)) });
      s = -1;
    }
  }
  return res;
}
export function detectKind(name, buf) {
  const ext = (name.split(".").pop() || "").toLowerCase();
  if (buf.length > 11 && String.fromCharCode(...buf.subarray(0, 4)) === "KORG" && buf[7] === 0x71 && String.fromCharCode(...buf.subarray(8, 11)) === "ESX") return "ESX-1";
  if (buf.length > 11 && String.fromCharCode(...buf.subarray(0, 4)) === "KORG" && buf[7] === 0x69 && String.fromCharCode(...buf.subarray(8, 11)) === "EMX") return "EMX-1";
  if (ext === "esx") return "ESX-1";
  if (ext === "emx") return "EMX-1";
  if (buf[0] === 0xf0) return "SysEx";
  return "unbekannt";
}

// ---- WAV -> Korg-tauglich (mono, 32 kHz, 16 bit, normalisiert) ----
export function parseWav(buf) {
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  const tag = o => String.fromCharCode(...buf.subarray(o, o + 4));
  if (tag(0) !== "RIFF" || tag(8) !== "WAVE") throw new Error("Keine WAV-Datei");
  let fmt, dataOff, dataLen;
  for (let o = 12; o + 8 <= buf.length;) {
    const id = tag(o), len = dv.getUint32(o + 4, true);
    if (id === "fmt ") fmt = { code: dv.getUint16(o + 8, true), ch: dv.getUint16(o + 10, true), rate: dv.getUint32(o + 12, true), bits: dv.getUint16(o + 22, true) };
    if (id === "data") { dataOff = o + 8; dataLen = Math.min(len, buf.length - dataOff); break; }
    o += 8 + len + (len & 1);
  }
  if (!fmt || dataOff == null) throw new Error("WAV: fmt/data fehlt");
  if (fmt.code !== 1 && fmt.code !== 3 && fmt.code !== 0xfffe) throw new Error("WAV-Codec nicht unterstützt");
  const bps = fmt.bits / 8, frames = Math.floor(dataLen / (bps * fmt.ch));
  const ch = Array.from({ length: fmt.ch }, () => new Float32Array(frames));
  for (let i = 0; i < frames; i++) for (let c = 0; c < fmt.ch; c++) {
    const o = dataOff + (i * fmt.ch + c) * bps; let v;
    if (fmt.code === 3) v = fmt.bits === 32 ? dv.getFloat32(o, true) : dv.getFloat64(o, true);
    else if (fmt.bits === 8) v = (buf[o] - 128) / 128;
    else if (fmt.bits === 16) v = dv.getInt16(o, true) / 32768;
    else if (fmt.bits === 24) v = (((buf[o] | (buf[o + 1] << 8) | (buf[o + 2] << 16)) << 8) >> 8) / 8388608;
    else if (fmt.bits === 32) v = dv.getInt32(o, true) / 2147483648;
    else throw new Error("Bittiefe nicht unterstützt");
    ch[c][i] = v;
  }
  return { rate: fmt.rate, channels: ch };
}
export function toKorgSample({ rate, channels }, { targetRate = 32000, normalize = true, peak = 0.97 } = {}) {
  const frames = channels[0].length, mono = new Float32Array(frames);
  for (let i = 0; i < frames; i++) { let s = 0; for (const c of channels) s += c[i]; mono[i] = s / channels.length; }
  let out = mono;
  if (rate !== targetRate) {
    const ratio = rate / targetRate, n = Math.floor(frames / ratio);
    out = new Float32Array(n);
    const half = 16, fc = Math.min(1, targetRate / rate) * 0.95; // windowed-sinc, Anti-Alias beim Downsampling
    for (let i = 0; i < n; i++) {
      const x = i * ratio, c = Math.floor(x); let s = 0;
      for (let k = c - half + 1; k <= c + half; k++) {
        if (k < 0 || k >= frames) continue;
        const d = x - k, a = Math.PI * d * fc;
        const sinc = d === 0 ? fc : Math.sin(a) / (Math.PI * d);
        s += mono[k] * sinc * (0.5 + 0.5 * Math.cos(Math.PI * d / half));
      }
      out[i] = s;
    }
  }
  if (normalize) {
    let m = 0; for (const v of out) m = Math.max(m, Math.abs(v));
    if (m > 0) { const g = peak / m; for (let i = 0; i < out.length; i++) out[i] *= g; }
  }
  return { rate: targetRate, data: out };
}
export function encodeWav16(rate, f32) {
  const b = new Uint8Array(44 + f32.length * 2), dv = new DataView(b.buffer);
  const w = (o, s) => [...s].forEach((c, i) => (b[o + i] = c.charCodeAt(0)));
  w(0, "RIFF"); dv.setUint32(4, 36 + f32.length * 2, true); w(8, "WAVEfmt ");
  dv.setUint32(16, 16, true); dv.setUint16(20, 1, true); dv.setUint16(22, 1, true);
  dv.setUint32(24, rate, true); dv.setUint32(28, rate * 2, true); dv.setUint16(32, 2, true); dv.setUint16(34, 16, true);
  w(36, "data"); dv.setUint32(40, f32.length * 2, true);
  for (let i = 0; i < f32.length; i++) dv.setInt16(44 + i * 2, Math.max(-1, Math.min(1, f32[i])) * 32767, true);
  return b;
}
