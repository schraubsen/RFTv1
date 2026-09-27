#!/usr/bin/env python3
"""Multishotifier - baut aus einem Ordner voller .wav-Samples eine einzige
multishot.wav, die man per Start-Position-Knob (0..127) auf dem Korg
Electribe SX/MX ansteuert. Reine Python-Stdlib (wave + audioop), kein SoX
nötig.

Funktionsprinzip: alle Samples werden auf dieselbe Länge (das längste Sample)
gepolstert, optional normalisiert, jeweils mit einer kurzen Stille-Lücke
versehen (damit Autoslice auf der Hardware saubere Grenzen erkennt) und zu
einer Datei aneinandergehängt. Slot Nr. i (0-basiert) entspricht direkt dem
Start-Position-Knob-Wert i - das Mapping ist nur exakt, wenn alle Slots gleich
lang sind, weshalb das Padding zwingend ist.

Annahme: Ausgabeformat ist 16-bit linear PCM (gängiger Sampler-Standard).
Das ist eine Werkzeug-Voreinstellung, keine verifizierte ESX/EMX-Spezifikation.
"""

import argparse
import audioop
import json
import sys
import wave
from pathlib import Path

TARGET_SAMPWIDTH = 2  # 16-bit, siehe Modul-Docstring
MAX_SLOTS = 128  # Anzahl Start-Position-Werte auf ESX/EMX (0..127)


def find_wavs(input_dir: Path) -> list[Path]:
    return sorted(p for p in input_dir.rglob("*.wav") if p.is_file())


def read_wav(path: Path) -> tuple[int, int, int, bytes]:
    with wave.open(str(path), "rb") as wf:
        framerate = wf.getframerate()
        sampwidth = wf.getsampwidth()
        nchannels = wf.getnchannels()
        frames = wf.readframes(wf.getnframes())
    return framerate, sampwidth, nchannels, frames


def convert_channels(frames: bytes, width: int, in_ch: int, out_ch: int) -> bytes:
    if in_ch == out_ch:
        return frames
    if in_ch == 2 and out_ch == 1:
        return audioop.tomono(frames, width, 0.5, 0.5)
    if in_ch == 1 and out_ch == 2:
        return audioop.tostereo(frames, width, 1.0, 1.0)
    raise ValueError(f"unsupported channel conversion {in_ch} -> {out_ch}")


def convert_sample(frames: bytes, framerate: int, sampwidth: int, nchannels: int,
                    out_rate: int, out_channels: int) -> bytes:
    frames = audioop.lin2lin(frames, sampwidth, TARGET_SAMPWIDTH)
    frames = convert_channels(frames, TARGET_SAMPWIDTH, nchannels, out_channels)
    if framerate != out_rate:
        frames, _ = audioop.ratecv(frames, TARGET_SAMPWIDTH, out_channels, framerate, out_rate, None)
    return frames


def normalize(frames: bytes, width: int, target_ratio: float = 0.97) -> bytes:
    peak = audioop.max(frames, width)
    if peak <= 0:
        return frames
    full_scale = 2 ** (width * 8 - 1) - 1
    factor = (full_scale * target_ratio) / peak
    return audioop.mul(frames, width, factor)


def pad_frame_count(frames: bytes, width: int, channels: int) -> int:
    return len(frames) // (width * channels)


def pad_to_length(frames: bytes, width: int, channels: int, target_frames: int, mode: str) -> bytes:
    current_frames = pad_frame_count(frames, width, channels)
    missing = target_frames - current_frames
    if missing <= 0:
        return frames
    missing_bytes = missing * width * channels
    if mode == "reversed":
        reversed_frames = audioop.reverse(frames, width)
        pad = (reversed_frames * ((missing_bytes // len(reversed_frames)) + 1))[:missing_bytes] if reversed_frames else b"\x00" * missing_bytes
    else:
        pad = b"\x00" * missing_bytes
    return frames + pad


def write_wav(path: Path, framerate: int, sampwidth: int, nchannels: int, frames: bytes) -> None:
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(nchannels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)
        wf.writeframes(frames)


def build(input_dir: Path, output_path: Path, max_shots: int, pad_mode: str,
          gap_ms: float, normalize_shots: bool, out_rate: int | None,
          out_channels: int | None) -> list[dict]:
    wavs = find_wavs(input_dir)
    if not wavs:
        raise SystemExit(f"keine .wav-Dateien in {input_dir} gefunden")
    if len(wavs) > max_shots:
        print(f"warnung: {len(wavs)} samples gefunden, nur die ersten {max_shots} werden verwendet",
              file=sys.stderr)
        wavs = wavs[:max_shots]

    loaded = [read_wav(p) for p in wavs]
    if out_rate is None:
        out_rate = loaded[0][0]
    if out_channels is None:
        out_channels = loaded[0][2]

    converted = [
        convert_sample(frames, rate, width, ch, out_rate, out_channels)
        for rate, width, ch, frames in loaded
    ]
    if normalize_shots:
        converted = [normalize(f, TARGET_SAMPWIDTH) for f in converted]

    slot_frames = max(pad_frame_count(f, TARGET_SAMPWIDTH, out_channels) for f in converted)
    gap_frames = int(out_rate * gap_ms / 1000)
    slot_frames_with_gap = slot_frames + gap_frames

    manifest = []
    output_chunks = []
    for index, (path, frames) in enumerate(zip(wavs, converted)):
        padded = pad_to_length(frames, TARGET_SAMPWIDTH, out_channels, slot_frames_with_gap, pad_mode)
        output_chunks.append(padded)
        manifest.append({
            "index": index,
            "start_position_knob": index,
            "file": str(path),
            "offset_frames": index * slot_frames_with_gap,
            "offset_ms": round(index * slot_frames_with_gap / out_rate * 1000, 1),
        })

    write_wav(output_path, out_rate, TARGET_SAMPWIDTH, out_channels, b"".join(output_chunks))
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_dir", type=Path, help="Ordner mit .wav-Samples (rekursiv durchsucht)")
    parser.add_argument("output", type=Path, help="Ziel-Datei, z.B. multishot.wav")
    parser.add_argument("--max-shots", type=int, default=MAX_SLOTS,
                         help=f"maximale Anzahl Slots (default {MAX_SLOTS}, ESX/EMX-Limit)")
    parser.add_argument("--pad", choices=["silence", "reversed"], default="silence",
                         help="Auffüllung kürzerer Samples: Stille oder gespiegeltes Sample")
    parser.add_argument("--gap-ms", type=float, default=10.0,
                         help="Stille-Lücke nach jedem Shot in ms, hilft Hardware-Autoslice (default 10)")
    parser.add_argument("--no-normalize", action="store_true", help="Peak-Normalisierung deaktivieren")
    parser.add_argument("--rate", type=int, default=None, help="Ziel-Samplerate (default: Rate des ersten Samples)")
    parser.add_argument("--mono", action="store_true", help="Ausgabe auf 1 Kanal mischen")
    parser.add_argument("--stereo", action="store_true", help="Ausgabe auf 2 Kanäle erweitern")
    parser.add_argument("--manifest", type=Path, default=None,
                         help="Pfad für die JSON-Manifest-Ausgabe (default: <output>.json)")
    args = parser.parse_args()

    if args.mono and args.stereo:
        parser.error("--mono und --stereo schließen sich aus")
    out_channels = 1 if args.mono else (2 if args.stereo else None)

    manifest = build(
        args.input_dir, args.output, args.max_shots, args.pad, args.gap_ms,
        not args.no_normalize, args.rate, out_channels,
    )

    manifest_path = args.manifest or args.output.with_suffix(".json")
    manifest_path.write_text(json.dumps(manifest, indent=2))

    print(f"{len(manifest)} shots -> {args.output}")
    print(f"manifest -> {manifest_path}")
    print("\nStart-Position-Knob-Werte:")
    for entry in manifest:
        print(f"  {entry['start_position_knob']:3d}  {Path(entry['file']).name}")


if __name__ == "__main__":
    main()
