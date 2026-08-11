from __future__ import annotations

import os
import shutil
import wave
from pathlib import Path

from fl_studio_mcp.routes.pyflp_route import load_samples

BPM = 166.0
PROJECT_NAME = "SCHRAUBI_STEM_LAB"


def make_silence(path: Path, seconds: float = 0.25, sample_rate: int = 44100) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames = int(seconds * sample_rate)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(b"\x00\x00\x00\x00" * frames)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    dist = repo_root / "dist"
    project_dir = dist / PROJECT_NAME
    audio_dir = project_dir / "Audio"

    if dist.exists():
        shutil.rmtree(dist)
    audio_dir.mkdir(parents=True, exist_ok=True)

    lanes = [
        ("00_SOURCE_MASTER.wav", "00 SOURCE MASTER - DROP TRACK HERE"),
        ("01_STEM_DRUMS.wav", "01 STEM - DRUMS"),
        ("02_STEM_BASS.wav", "02 STEM - BASS"),
        ("03_STEM_INSTRUMENTS.wav", "03 STEM - INSTRUMENTS"),
        ("04_STEM_VOCALS.wav", "04 STEM - VOCALS"),
        ("05_KICK_CUTS.wav", "05 CUTS - KICKS"),
        ("06_SNARE_CUTS.wav", "06 CUTS - SNARES"),
        ("07_HAT_PERC_CUTS.wav", "07 CUTS - HATS PERC"),
        ("08_MELO_ACID_CUTS.wav", "08 CUTS - MELO ACID"),
        ("09_VOCAL_FX_CUTS.wav", "09 CUTS - VOCAL FX"),
        ("10_ESX_READY.wav", "10 EXPORT - ESX READY"),
    ]

    for filename, _ in lanes:
        make_silence(audio_dir / filename)

    # Change working directory so FLP stores portable relative paths like Audio/foo.wav.
    os.chdir(project_dir)

    samples = [
        {"path": f"Audio/{filename}", "name": name}
        for filename, name in lanes
    ]

    comments = (
        "SCHRAUBI STEM / SAMPLE EXTRACTION LAB\n\n"
        "1) Delete/replace the silent SOURCE MASTER placeholder with the old set/track.\n"
        "2) In FL Studio: right-click the source Audio Clip > Extract stems from sample.\n"
        "3) Put DRUMS / BASS / INSTRUMENTS / VOCALS on the matching lanes.\n"
        "4) Hunt clean transients and musical fragments; copy them to KICK/SNARE/HAT/MELO/VOCAL lanes.\n"
        "5) Keep the transient; trim bleed; short fades; remove DC/clicks; do not over-denoise.\n"
        "6) Export final ESX one-shots as mono/stereo WAV as needed, then convert to the ESX target format.\n\n"
        "Target: oldschool Tekk / Hardtekk / RFT-style extraction without leaving melody buried in the kick."
    )

    flp_path = project_dir / f"{PROJECT_NAME}.flp"
    info = load_samples(
        str(flp_path),
        samples,
        title="SCHRAUBI Stem / Sample Extraction Lab",
        tempo=BPM,
        artists="Schraubi",
        genre="Tekk / Hardtekk",
        comments=comments,
        arrange=True,
        stagger_bars=0,
    )

    readme = project_dir / "START_HERE.txt"
    readme.write_text(
        "SCHRAUBI STEM / SAMPLE EXTRACTION LAB\n"
        "===================================\n\n"
        "FLP: SCHRAUBI_STEM_LAB.flp\n"
        "Tempo: 166 BPM\n\n"
        "Workflow:\n"
        "- Open the FLP.\n"
        "- Drag your source track/set into the Playlist and remove the silent placeholder.\n"
        "- Right-click source clip -> Extract stems from sample.\n"
        "- Route the four stems into the prepared lanes.\n"
        "- Cut kick/snare/hat-perc/melo-acid/vocal-FX candidates.\n"
        "- Export only the best clean one-shots to your ESX sample bank.\n\n"
        "Note: the Audio/*.wav files are tiny silent placeholders so the FLP opens with portable relative references.\n",
        encoding="utf-8",
    )

    # Keep both the loose project folder and an easy-to-download ZIP.
    os.chdir(repo_root)
    shutil.make_archive(str(dist / PROJECT_NAME), "zip", root_dir=project_dir)

    print(info)
    print(f"Built: {flp_path}")
    print(f"Built: {dist / (PROJECT_NAME + '.zip')}")


if __name__ == "__main__":
    main()
