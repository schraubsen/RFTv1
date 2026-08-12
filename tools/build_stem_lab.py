from __future__ import annotations

import csv
import json
import os
import shutil
import wave
from pathlib import Path

import pyflp
from fl_studio_mcp.routes.pyflp_route import load_samples

BPM = 166.0
PROJECT_NAME = "SCHRAUBI_RFT_SAMPLE_LAB_V3"
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

    # Playlist/channel order = source -> stems -> checks -> extraction -> cleanup -> ESX export.
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

    # V3: every Audio Clip is hard-routed to its own mixer insert (1..24).
    # Inserts 25..32 are reserved as the bus layout for the next live-FL pass.
    mixer_names = {
        1: "SOURCE REF",
        2: "STEM DRUMS",
        3: "STEM BASS",
        4: "STEM INSTR",
        5: "STEM VOCALS",
        6: "STEM SUM CHECK",
        7: "A B REFERENCE",
        8: "DRUM CANDIDATES",
        9: "KICK RAW",
        10: "KICK CLEAN",
        11: "KICK TOP",
        12: "KICK BODY",
        13: "SNARE RAW",
        14: "SNARE CLEAN",
        15: "HATS PERC",
        16: "BASS ONESHOTS",
        17: "MELO ACID",
        18: "VOCAL FX",
        19: "LOOP 1 BAR",
        20: "LOOP 2 BAR",
        21: "LOOP 4 BAR",
        22: "REJECT BLEED",
        23: "ESX MONO READY",
        24: "ESX STEREO READY",
        25: "BUS STEM SUM",
        26: "BUS A-B MONITOR",
        27: "BUS KICK LAB",
        28: "BUS CUT STATION",
        29: "BUS ANALYZER",
        30: "BUS ESX MONO",
        31: "BUS ESX STEREO",
        32: "BUS PREMASTER CHECK",
    }

    for relpath, _name, channels, _stage in lanes:
        make_silence(project_dir / relpath, channels=channels)

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
        "SCHRAUBI RFT SAMPLE EXTRACTION LAB V3\n\n"
        "V3 CHANGE: all 24 working Audio Clips are routed to Mixer Inserts 1-24. "
        "Mixer Inserts 25-32 are reserved for STEM SUM / A-B / KICK LAB / CUT STATION / ANALYZER / ESX EXPORT buses.\n\n"
        "00: Replace SOURCE placeholder with the old set/track.\n"
        "01-04: Extract stems: Drums / Bass / Instruments / Vocals.\n"
        "05-06: Compare stem sum and A/B against the source before cutting.\n"
        "07-17: Candidates -> RAW -> CLEAN. Preserve transient and character.\n"
        "18-20: Useful 1/2/4-bar loops.\n"
        "21: Reject/bleed/artifact parking lane.\n"
        "22-23: Final ESX-ready material only.\n\n"
        "KICK RULE: if melody/bass remains in a kick, choose another hit or Drum stem first; "
        "then shorten/rebuild the tail or split TOP/BODY. Do not destroy the transient with aggressive cleanup."
    )

    flp_path = project_dir / f"{PROJECT_NAME}.flp"
    base_info = load_samples(
        str(flp_path),
        samples,
        title="SCHRAUBI RFT Sample Extraction Lab V3",
        tempo=BPM,
        artists="Schraubi",
        genre="Tekk / Hardtekk / RFT sample extraction",
        comments=comments,
        arrange=True,
        stagger_bars=0,
    )

    # ------------------------------------------------------------------
    # V3 pass: real Channel Rack -> Mixer routing.
    # PyFLP exposes Sampler.insert as FL's ChannelID.RoutedTo value.
    # This is deterministic and survives save/re-open in FL.
    # ------------------------------------------------------------------
    project = pyflp.parse(flp_path)
    channels = list(project.channels)
    if len(channels) != len(lanes):
        raise RuntimeError(f"Expected {len(lanes)} channels before routing, got {len(channels)}")

    route_before = []
    for idx, channel in enumerate(channels):
        target_insert = idx + 1
        route_before.append(getattr(channel, "insert", None))
        channel.insert = target_insert

    # Rename mixer inserts where the template exposes a writable name event.
    # FL can omit explicit InsertID.Name events for default tracks, so failures are recorded
    # instead of corrupting the FLP. Channel routing itself is mandatory and validated below.
    mixer_name_results: dict[str, dict[str, object]] = {}
    for insert_no, desired_name in mixer_names.items():
        try:
            insert = project.mixer[insert_no]
            old_name = insert.name
            insert.name = desired_name
            mixer_name_results[str(insert_no)] = {
                "ok": True,
                "old": old_name,
                "new": insert.name,
            }
        except Exception as exc:  # explicit audit trail; not a silent guess
            mixer_name_results[str(insert_no)] = {
                "ok": False,
                "desired": desired_name,
                "error": f"{type(exc).__name__}: {exc}",
            }

    pyflp.save(project, flp_path)

    # Re-open and verify every audio channel landed on the intended insert.
    routed = pyflp.parse(flp_path)
    routed_channels = list(routed.channels)
    route_after = [getattr(channel, "insert", None) for channel in routed_channels]
    expected_routes = list(range(1, len(lanes) + 1))
    if route_after != expected_routes:
        raise RuntimeError(
            "FLP mixer-routing validation failed: "
            f"expected {expected_routes}, got {route_after}"
        )

    validation = {
        "project": PROJECT_NAME,
        "tempo": float(routed.tempo),
        "expected_channel_count": len(lanes),
        "actual_channel_count": len(routed_channels),
        "route_before": route_before,
        "route_after": route_after,
        "mixer_insert_names": mixer_name_results,
        "base_builder_info": base_info,
    }

    if abs(float(routed.tempo) - BPM) > 0.01:
        raise RuntimeError(f"Expected {BPM} BPM, got {routed.tempo}")

    (project_dir / "START_HERE.txt").write_text(
        "SCHRAUBI RFT SAMPLE EXTRACTION LAB V3\n"
        "=====================================\n\n"
        "WHAT IS NEW IN V3\n"
        "- Playlist/Channel Rack work lanes remain 00-23.\n"
        "- Every lane is now routed to its own Mixer Insert 1-24.\n"
        "- Inserts 25-32 are the planned bus area. See MIXER_ROUTING_MAP.csv.\n"
        "- A stock-plugin wiring blueprint is included for the live FL pass.\n\n"
        "FIRST USE\n"
        "1. Open SCHRAUBI_RFT_SAMPLE_LAB_V3.flp.\n"
        "2. Confirm SOURCE is on Mixer 1, DRUMS on 2, BASS on 3 ... ESX STEREO READY on 24.\n"
        "3. Replace SOURCE placeholder with your real recording.\n"
        "4. Extract Drums/Bass/Instruments/Vocals and place them on 01-04.\n"
        "5. A/B before cleanup; do not process the reference path.\n"
        "6. Use RAW -> CLEAN -> ESX READY as the approval chain.\n\n"
        "IMPORTANT: effect-slot creation and send-bus wiring are intentionally NOT forged offline. "
        "Those are added in a live-FL/FL-saved-template pass so we do not corrupt a known-good FL25 project.\n",
        encoding="utf-8",
    )

    with (project_dir / "LANE_MANIFEST.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["lane", "playlist_name", "audio_path", "channels", "stage", "mixer_insert"])
        for lane_no, (relpath, name, channels_count, stage) in enumerate(lanes):
            writer.writerow([lane_no, name, relpath, channels_count, stage, lane_no + 1])

    with (project_dir / "MIXER_ROUTING_MAP.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["mixer_insert", "target_name", "purpose", "automatic_in_v3"])
        purposes = {
            25: "Sum/monitor the four stem mixer tracks after manual send wiring",
            26: "Matched-level source vs stem-sum A/B monitor",
            27: "Kick RAW/CLEAN/TOP/BODY comparison and rebuild station",
            28: "Edison cut/edit station for approved candidates",
            29: "Wave Candy / metering monitor bus",
            30: "Mono ESX print path",
            31: "Stereo ESX print path",
            32: "Final safety/pre-master check; no loudness chasing",
        }
        for insert_no in range(1, 33):
            purpose = purposes.get(insert_no, f"Direct lane mixer for Playlist lane {insert_no - 1:02d}")
            automatic = "YES - channel routed" if insert_no <= 24 else "RESERVED - wire sends in FL"
            writer.writerow([insert_no, mixer_names[insert_no], purpose, automatic])

    (project_dir / "V3_STOCK_PLUGIN_BLUEPRINT.txt").write_text(
        "V3 STOCK-PLUGIN / BUS BLUEPRINT\n"
        "================================\n\n"
        "DO NOT PROCESS THE SOURCE REFERENCE. Gain-match only when A/B testing.\n\n"
        "25 BUS STEM SUM\n"
        "- Route Mixer 2/3/4/5 here as sends or a bus in FL.\n"
        "- No coloration. Use Fruity Balance only if level matching is needed.\n\n"
        "26 BUS A-B MONITOR\n"
        "- Compare SOURCE REF against STEM SUM at matched loudness.\n"
        "- One path active at a time. No limiter/clipper.\n\n"
        "27 BUS KICK LAB\n"
        "- Feed KICK RAW / CLEAN / TOP / BODY as needed.\n"
        "- Suggested stock tools: Parametric EQ 2 -> Fruity Balance.\n"
        "- Use Edison for surgical edits rather than stacking destructive EQ.\n\n"
        "28 BUS CUT STATION\n"
        "- Edison first for trim, zero-cross/fades and region work.\n"
        "- Parametric EQ 2 only for specific contamination.\n"
        "- Fruity Balance for matched-level A/B.\n\n"
        "29 BUS ANALYZER\n"
        "- Wave Candy: spectrum + peak/oscilloscope as needed.\n"
        "- Monitoring only; do not render through analyzer processing.\n\n"
        "30 BUS ESX MONO\n"
        "- Final mono-approved one-shots. Export WAV PCM 16-bit / 44.1 kHz.\n"
        "- Keep headroom; do not normalize every sample blindly.\n\n"
        "31 BUS ESX STEREO\n"
        "- Only material whose stereo field is musically useful.\n"
        "- Export WAV PCM 16-bit / 44.1 kHz.\n\n"
        "32 BUS PREMASTER CHECK\n"
        "- Safety comparison only. No loudness-maximizing chain.\n",
        encoding="utf-8",
    )

    (project_dir / "CUT_QUALITY_CHECKLIST.txt").write_text(
        "SAMPLE QUALITY CHECK - A / B / C\n"
        "==============================\n\n"
        "A = usable directly: transient intact, minimal musical bleed, no click/DC problem.\n"
        "B = useful after light cleanup; minor bleed is acceptable when it adds character.\n"
        "C = obvious melody/bass/vocal contamination, stem artifact, hollow transient or bad tail.\n\n"
        "KICK CLEANUP ORDER\n"
        "1. Choose a better hit first.\n"
        "2. Compare Source vs Drum stem.\n"
        "3. Trim at a sensible zero crossing / add tiny fades.\n"
        "4. Shorten or rebuild a contaminated tail.\n"
        "5. Split TOP and BODY when useful.\n"
        "6. EQ only what is actually wrong.\n"
        "7. Re-A/B at matched loudness.\n"
        "8. Approve only if the hit still punches at low monitoring level.\n",
        encoding="utf-8",
    )

    (project_dir / "ESX_EXPORT_SETTINGS.txt").write_text(
        "ESX-1 EXPORT / TRANSFER TARGET\n"
        "==============================\n\n"
        "Recommended working target:\n"
        "- WAV / standard PCM\n"
        "- 16-bit\n"
        "- 44,100 Hz\n"
        "- Mono for kicks/snares/most hats-percs/bass when stereo is not essential\n"
        "- Stereo only when stereo information matters musically\n\n"
        "Do not normalize by habit. Match samples by perceived role and leave transient headroom.\n",
        encoding="utf-8",
    )

    (project_dir / "VALIDATION.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")

    os.chdir(repo_root)
    shutil.copy2(flp_path, dist / f"{PROJECT_NAME}.flp")
    shutil.make_archive(str(dist / PROJECT_NAME), "zip", root_dir=project_dir)

    print(json.dumps(validation, indent=2))
    print(f"Built: {dist / (PROJECT_NAME + '.flp')}")
    print(f"Built: {dist / (PROJECT_NAME + '.zip')}")


if __name__ == "__main__":
    main()
