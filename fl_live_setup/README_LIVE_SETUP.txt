SCHRAUBI RFT LAB - FL STUDIO LIVE SETUP
========================================

WHAT IT DOES
- Runs inside FL Studio's official MIDI scripting system.
- Has a project guard: it only edits a project when the expected V3 channel names are present.
- Automatic action: names Mixer tracks 1-32 and links the 24 working channels to Mixer 1-24.
- It does NOT automatically create bus sends, so opening another project cannot unexpectedly change its signal flow.

INSTALL (WINDOWS)
1. Double-click INSTALL_WINDOWS.bat.
2. Restart FL Studio, or reload MIDI scripts.
3. Open Options > MIDI Settings.
4. On a MIDI input you use, choose Controller type: SCHRAUBI RFT Lab Setup (user).
5. Open SCHRAUBI_RFT_SAMPLE_LAB_V3.flp.

Because the script does not handle normal MIDI note messages, FL Studio can continue to process unhandled MIDI data normally.

OPTIONAL BUS HELPERS
Open View > Script output > Interpreter while this script is selected and call:

ApplyCore()
    Re-apply names + channel-to-mixer links.

WireStemAB()
    Routes mixer 2/3/4/5 through BUS STEM SUM (25). Source track stays direct.
    For A/B, mute either SOURCE REF or BUS STEM SUM.

RestoreStemDirect()
    Returns stem tracks 2/3/4/5 directly to Master.

WireKickLab()
    Routes KICK RAW/CLEAN/TOP/BODY (9/10/11/12) through BUS KICK LAB (27).

RestoreKickDirect()
    Returns those four kick tracks directly to Master.

NEXT DEVELOPMENT PASS
Once this live setup is confirmed in FL Studio 25, the next safe step is a saved FL-native template containing the actual stock plugin slots:
- Edison cut station
- Wave Candy analyzer
- Parametric EQ 2 / Fruity Balance A/B helpers
- ESX mono/stereo print paths

We deliberately do not binary-forge effect-slot chunks into the FLP: the V2 screenshot proved the current base opens correctly, so V3 keeps that stable base and uses FL Studio's own API for live mixer mutations.
