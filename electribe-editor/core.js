// electribe core: kein DOM, läuft im Browser und in Node.
export const MODEL_ID = { ESX1: null, EMX1: null }; // TODO: verifizieren (ESX1midiimp.txt)

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
export function parseSchema(text) {
  const fields = [];
  text.split(/\r?\n/).forEach((raw, i) => {
    const line = raw.trim();
    if (!line || line[0] === "#") return;
    const [spec, label = ""] = line.split(";");
    const t = spec.trim().split(/\s+/);
    if (t[0] !== "field" || t.length < 4) throw new Error(`Schema Zeile ${i + 1}: ungültig`);
    let off = t[2], verified = false;
    if (off[0] === "!") { verified = true; off = off.slice(1); }
    const offset = Number(off);
    if (!Number.isInteger(offset) || offset < 0) throw new Error(`Schema Zeile ${i + 1}: Offset`);
    const type = t[3];
    if (!["u8", "u16le", "u16be", "ascii"].includes(type)) throw new Error(`Schema Zeile ${i + 1}: Typ ${type}`);
    const rest = t.slice(4).map(Number);
    const f = { id: t[1], offset, verified, type, label: label.trim() || t[1] };
    if (type === "ascii") { f.len = rest[0]; if (!f.len) throw new Error(`Schema Zeile ${i + 1}: len`); }
    else { f.min = rest[0]; f.max = rest[1]; }
    fields.push(f);
  });
  return fields;
}
const size = f => (f.type === "u8" ? 1 : f.type === "ascii" ? f.len : 2);
export function readField(buf, f) {
  if (f.offset + size(f) > buf.length) return null;
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  switch (f.type) {
    case "u8": return buf[f.offset];
    case "u16le": return dv.getUint16(f.offset, true);
    case "u16be": return dv.getUint16(f.offset, false);
    case "ascii": return String.fromCharCode(...buf.subarray(f.offset, f.offset + f.len)).replace(/\0+$/, "");
  }
}
export function writeField(buf, f, v) {
  if (f.offset + size(f) > buf.length) throw new Error("Offset außerhalb der Datei");
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  if (f.type === "ascii") {
    for (let i = 0; i < f.len; i++) buf[f.offset + i] = i < v.length ? v.charCodeAt(i) & 0x7f : 0;
    return;
  }
  v = Number(v);
  if (!Number.isFinite(v)) throw new Error("Zahl erwartet");
  if (f.min != null && v < f.min) v = f.min;
  if (f.max != null && v > f.max) v = f.max;
  if (f.type === "u8") buf[f.offset] = v & 255;
  else dv.setUint16(f.offset, v & 0xffff, f.type === "u16le");
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
