# name=SCHRAUBI RFT Lab Setup

"""FL Studio 25 live setup helper for SCHRAUBI RFT Sample Extraction Lab V3.

Safety design:
- OnInit only changes anything when the expected SCHRAUBI project channel names are detected.
- Automatic pass only renames mixer tracks and links channels 00..23 to inserts 1..24.
- Optional bus-routing helpers are NOT run automatically.

The functions WireStemAB(), RestoreStemDirect(), WireKickLab(), RestoreKickDirect()
can be called from FL Studio's Script Output > Interpreter when needed.
"""

import channels
import mixer
import ui

EXPECTED = {
    0: "00 SOURCE - ORIGINAL",
    1: "01 STEM - DRUMS",
    2: "02 STEM - BASS",
    3: "03 STEM - INSTRUMENTS",
    4: "04 STEM - VOCALS",
    8: "08 KICK - RAW",
    22: "22 EXPORT - ESX MONO READY",
    23: "23 EXPORT - ESX STEREO READY",
}

MIXER_NAMES = {
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


def _matches_project():
    try:
        if channels.channelCount() < 24:
            return False
        for index, expected_name in EXPECTED.items():
            if channels.getChannelName(index) != expected_name:
                return False
        return True
    except Exception:
        return False


def _notify(text):
    try:
        ui.setHintMsg(text)
    except Exception:
        pass
    print(text)


def ApplyCore():
    """Safe core setup: name mixer 1..32 and link channels 00..23 -> mixer 1..24."""
    if not _matches_project():
        _notify("SCHRAUBI RFT Lab: project guard did not match - no changes made")
        return False

    for track, name in MIXER_NAMES.items():
        mixer.setTrackName(track, name)

    for channel_index in range(24):
        mixer.linkChannelToTrack(channel_index, channel_index + 1, 0)

    mixer.afterRoutingChanged()
    _notify("SCHRAUBI RFT Lab: mixer names + direct routing 1-24 applied")
    return True


def WireStemAB():
    """Route the four stems through BUS STEM SUM (25). Source stays direct for A/B muting."""
    if not ApplyCore():
        return False

    # Stems 2..5 no longer go directly to Master; they feed track 25 instead.
    for track in (2, 3, 4, 5):
        mixer.setRouteTo(track, 0, 0, False)
        mixer.setRouteTo(track, 25, 1, False)
        try:
            mixer.setRouteToLevel(track, 25, 1.0)
        except Exception:
            pass

    mixer.setRouteTo(25, 0, 1, False)
    mixer.afterRoutingChanged()
    _notify("SCHRAUBI RFT Lab: stems 2-5 -> BUS STEM SUM 25. Mute SOURCE or bus 25 for A/B")
    return True


def RestoreStemDirect():
    """Restore stems 2..5 directly to Master and remove their send to bus 25."""
    if not _matches_project():
        _notify("SCHRAUBI RFT Lab: project guard did not match - no changes made")
        return False

    for track in (2, 3, 4, 5):
        mixer.setRouteTo(track, 25, 0, False)
        mixer.setRouteTo(track, 0, 1, False)
    mixer.afterRoutingChanged()
    _notify("SCHRAUBI RFT Lab: stem tracks restored direct to Master")
    return True


def WireKickLab():
    """Route KICK RAW/CLEAN/TOP/BODY (9..12) through BUS KICK LAB (27)."""
    if not ApplyCore():
        return False

    for track in (9, 10, 11, 12):
        mixer.setRouteTo(track, 0, 0, False)
        mixer.setRouteTo(track, 27, 1, False)
        try:
            mixer.setRouteToLevel(track, 27, 1.0)
        except Exception:
            pass

    mixer.setRouteTo(27, 0, 1, False)
    mixer.afterRoutingChanged()
    _notify("SCHRAUBI RFT Lab: kick tracks 9-12 -> BUS KICK LAB 27")
    return True


def RestoreKickDirect():
    """Restore KICK RAW/CLEAN/TOP/BODY directly to Master."""
    if not _matches_project():
        _notify("SCHRAUBI RFT Lab: project guard did not match - no changes made")
        return False

    for track in (9, 10, 11, 12):
        mixer.setRouteTo(track, 27, 0, False)
        mixer.setRouteTo(track, 0, 1, False)
    mixer.afterRoutingChanged()
    _notify("SCHRAUBI RFT Lab: kick tracks restored direct to Master")
    return True


def OnInit():
    # Project guard prevents this script from renaming/routing unrelated FL projects.
    if _matches_project():
        ApplyCore()
    else:
        _notify("SCHRAUBI RFT Lab loaded; waiting for matching V3 project")
