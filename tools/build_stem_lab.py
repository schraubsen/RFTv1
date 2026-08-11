from __future__ import annotations

import csv
import json
import os
import shutil
import wave
from pathlib import Path

from fl_studio_mcp.routes.pyflp_route import load_samples

BPM = 166.0
PROJECT_NAME = "SCHRAUBI_RFT_SAMPLE_LAB_V2"
BAR_SECONDS = 4.0 * 60.0 / BPM


def make_silence(
    path: Path,
    *,
    seconds: float = BAR_SECONDS,
    sample_rate: int = 44100,
    channels: int = 2,
) -> None:
    """Create a portable silent placeholder that is long enough to see in Playlist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    frames = int(seconds * sample_rate)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(2)  # 16-bit PCM
        wav.setframerate(sample_rate)
        wav.writeframes(b"\x00\x00" * channels * frames)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    dist = repo_root / "dist"
    project_dir = dist / PROJECT_NAME

    if dist.exists():
        shutil.rmtree(dist)
    project_dir.mkdir(parents=True, exist_ok=True)

    # The lane order is the actual workflow: source -> stems -> extraction -> cleanup -> ESX export.
    lanes = [
        ("Audio/00_Source/00_SOURCE_ORIGINAL.wav", "00 SOURCE - ORIGINAL", 2, "source"),
        ("Audio/01_Stems/01_STEM_DRUMS.wav", "01 STEM - DRUMS", 2, "stem"),
        ("Audio/01_Stems/02_STEM_BASS.wav", "02 STEM - BASS", 2, "stem"),
        ("Audio/01_Stems/03_STEM_INSTRUMENTS.wav", "03 STEM - INSTRUMENTS", 2, "stem"),
        ("Audio/01_Stems/04_STEM_VOCALS.wav", "04 STEM - VOCALS", 2, "stem"),
        ("Audio/02_Check/05_STEM_SUM_CHECK.wav", "05 CHECK - STEM SUM VS SOURCE", 2, "check"),
        ("Audio/02_Check/06_AB_REFERENCE.wav", "06 CHECK - A B REFERENCE", 2, "check"),
        ("Audio/03_Candidates/07_DRUM_CANDIDATES.wav", "07 CANDIDATES - DRUM TRANSIENTS", 2, "candidate"),
        ("Audio/03_Candidates/08_KICK_RAW.wav", "08 KICK - RAW", 2, "candidate"),
        ("Audio/04_Clean/09_KICK_CLEAN.wav", "09 KICK - CLEAN", 2, "clean"),
        ("Audio/04_Clean/10_KICK_TOP.wav", "10 KICK - TOP TRANSIENT", 2, "clean"),
        ("Audio/04_Clean/11_KICK_BODY.wav", "11 KICK - BODY TAIL", 2, "clean"),
        ("Audio/03_Candidates/12_SNARE_RAW.wav", "12 SNARE - RAW", 2, "candidate"),
        ("Audio/04_Clean/13_SNARE_CLEAN.wav", "13 SNARE - CLEAN", 2, "clean"),
        ("Audio/04_Clean/14_HATS_PERC.wav", "14 HATS PERC - CLEAN", 2, "clean"),
        ("Audio/04_Clean/15_BASS_ONESHOTS.wav", "15 BASS - ONESHOTS", 2, "clean"),
        ("Audio/04_Clean/16_MELO_ACID.wav", "16 MELO ACID - CUTS", 2, "clean"),
        ("Audio/04_Clean/17_VOCAL_FX.wav", "17 VOCAL FX - CUTS", 2, "clean"),
        ("Audio/05_Loops/18_LOOP_1BAR.wav", "18 LOOPS - 1 BAR", 2, "loop"),
        ("Audio/05_Loops/19_LOOP_2BAR.wav", "19 LOOPS - 2 BAR", 2, "loop"),
        ("Audio/05_Loops/20_LOOP_4BAR.wav", "20 LOOPS - 4 BAR", 2, "loop"),
        ("Audio/06_Rejects/21_REJECT_BLEED.wav", "21 REJECT - BLEED ARTIFACTS", 2, "reject"),
        ("Audio/07_ESX_Export/22_ESX_MONO_READY.wav", "22 EXPORT - ESX MONO READY", 1, "export"),
        ("Audio/07_ESX_Export/23_ESX_STEREO_READY.wav", "23 EXPORT - ESX STEREO READY", 2, "export"),
    ]

    for relpath, _name, channels, _stage in lanes:
        make_silence(project_dir / relpath, channels=channels)

    # Make practical target folders even before the first real sample is cut.
    for folder in [
        "Exports/ESX_MONO",
        "Exports/ESX_STEREO",
        "Exports/LOOPS",
        "Reference",
        "Notes",
    ]:
        (project_dir / folder).mkdir(parents=True, exist_ok=True)

    os.chdir(project_dir)
    samples = [{"path": relpath, "name": name} for relpath, name, _channels, _stage in lanes]

    comments = (
        "SCHRAUBI RFT SAMPLE EXTRACTION LAB V2\n\n"
        "WORKFLOW\n"
        "00: Replace SOURCE placeholder with the old set/track.\n"
        "01-04: FL Studio > Extract stems from sample: Drums / Bass / Instruments / Vocals.\n"
        "05-06: Compare stem sum and A/B against the source before cutting.\n"
        "07-17: Find candidates, then separate RAW from CLEAN. Keep transient and character.\n"
        "18-20: Keep useful 1/2/4-bar loops separate from one-shots.\n"
        "21: Put contaminated or artifact-heavy cuts here instead of deleting them immediately.\n"
        "22-23: Final ESX-ready exports only.\n\n"
        "KICK RULE: if melody/bass is audible in the raw kick, do not just EQ harder. Try a better hit, "
        "use the drum stem, shorten/rebuild the tail, or split TOP/BODY. Preserve attack.\n"
        "TARGET: oldschool Tekk / Hardtekk / RFT character with cleaner separation and predictable ESX transfer."
    )

    flp_path = project_dir / f"{PROJECT_NAME}.flp"
    info = load_samples(
        str(flp_path),
        samples,
        title="SCHRAUBI RFT Sample Extraction Lab V2",
        tempo=BPM,
        artists="Schraubi",
        genre="Tekk / Hardtekk / RFT sample extraction",
        comments=comments,
        arrange=True,
        stagger_bars=0,
    )

    # Fail the CI build if the generated FLP is structurally incomplete.
    expected_channels = len(lanes)
    if int(info.get("channel_count", -1)) != expected_channels:
        raise RuntimeError(f"FLP validation failed: expected {expected_channels} channels, got {info.get('channel_count')}")
    if abs(float(info.get("tempo", 0.0)) - BPM) > 0.01:
        raise RuntimeError(f"FLP validation failed: expected {BPM} BPM, got {info.get('tempo')}")

    readme = project_dir / "START_HERE.txt"
    readme.write_text(
        "SCHRAUBI RFT SAMPLE EXTRACTION LAB V2\n"
        "=====================================\n\n"
        "1. Open SCHRAUBI_RFT_SAMPLE_LAB_V2.flp.\n"
        "2. Replace 00 SOURCE - ORIGINAL with your real recording.\n"
        "3. Right-click the source Audio Clip -> Extract stems from sample.\n"
        "4. Put Drums/Bass/Instruments/Vocals onto lanes 01-04.\n"
        "5. A/B the stems against the source before you cut anything.\n"
        "6. RAW lanes are for promising hits. CLEAN lanes are only for edited candidates.\n"
        "7. If a kick contains melody: prefer another transient or the Drum stem before aggressive cleanup.\n"
        "8. Use TOP/BODY lanes when rebuilding a contaminated kick.\n"
        "9. Put failures in REJECT/BLEED; they can still be useful as FX or texture.\n"
        "10. Only final approved files go to ESX MONO/STEREO READY.\n\n"
        "Recommended ESX transfer format: WAV, standard PCM, 16-bit, 44.1 kHz. "
        "The ESX-1 can import a wider range, but 44.1 kHz matches its native sampling frequency.\n",
        encoding="utf-8",
    )

    (project_dir / "ESX_EXPORT_SETTINGS.txt").write_text(
        "ESX-1 EXPORT / TRANSFER TARGET\n"
        "==============================\n\n"
        "Recommended working target:\n"
        "- WAV\n"
        "- Standard PCM\n"
        "- 16-bit\n"
        "- 44,100 Hz\n"
        "- Mono for kicks, snares, most hats/percs/bass where stereo is not essential\n"
        "- Stereo only when the stereo image is musically important\n\n"
        "Korg manual facts:\n"
        "- WAV import/export: standard PCM, mono or stereo, 8/16-bit.\n"
        "- Supported WAV sampling rate: 11,025 to 96,000 Hz.\n"
        "- If rate is not 44,100 Hz, ESX adjusts sample Tune during loading for correct pitch.\n"
        "- ESX-1 native sampling frequency: 44.1 kHz.\n\n"
        "Source: KORG ESX-1 Owner's Manual, pages 88 and 99 (PDF page indexing may differ).\n",
        encoding="utf-8",
    )

    (project_dir / "CUT_QUALITY_CHECKLIST.txt").write_text(
        "SAMPLE QUALITY CHECK - A / B / C\n"
        "==============================\n\n"
        "A = clean enough to use directly; transient intact; minimal musical bleed; no click/DC issue.\n"
        "B = useful after light cleanup; small bleed acceptable if it adds character.\n"
        "C = obvious melody/bass/vocal contamination, stem artifact, hollow transient, or bad tail.\n\n"
        "KICK CLEANUP ORDER\n"
        "1. Choose a better hit first.\n"
        "2. Compare source vs Drum stem.\n"
        "3. Trim at zero crossing / add tiny fades.\n"
        "4. Shorten or rebuild contaminated tail.\n"
        "5. Split TOP and BODY if useful.\n"
        "6. EQ only what is actually wrong.\n"
        "7. Re-A/B at matched loudness.\n"
        "8. Export only when the hit still punches at low monitoring level.\n",
        encoding="utf-8",
    )

    with (project_dir / "LANE_MANIFEST.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["lane", "name", "path", "channels", "stage"])
        for lane_no, (relpath, name, channels, stage) in enumerate(lanes):
            writer.writerow([lane_no, name, relpath, channels, stage])

    (project_dir / "VALIDATION.json").write_text(json.dumps(info, indent=2), encoding="utf-8")

    os.chdir(repo_root)
    # Loose FLP for one-click download + complete portable project ZIP.
    shutil.copy2(flp_path, dist / f"{PROJECT_NAME}.flp")
    shutil.make_archive(str(dist / PROJECT_NAME), "zip", root_dir=project_dir)

    print(json.dumps(info, indent=2))
    print(f"Built: {dist / (PROJECT_NAME + '.flp')}")
    print(f"Built: {dist / (PROJECT_NAME + '.zip')}")


if __name__ == "__main__":
    main()
