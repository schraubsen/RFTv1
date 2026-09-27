#pragma once

#include <cstdint>

namespace electribe {

// Korg SysEx frame: F0 42 3n <model-id> <function> ... F7  (n = MIDI channel)
//
// TODO: verifizieren. Die konkreten Model-IDs fuer ESX-1 und EMX-1 stehen in
// Korgs "ESX1midiimp.txt" bzw. der MIDI-Implementation-Chart im Handbuch-
// Anhang. Sie werden hier absichtlich NICHT aus dem Gedaechtnis behauptet -
// siehe electribe-dev Skill-Regel. Solange keine bestaetigte Quelle vorliegt,
// bleiben diese Konstanten unbelegt (-1) statt einen falschen Wert zu raten.
constexpr int MODEL_ID_ESX1_TODO_VERIFY = -1;
constexpr int MODEL_ID_EMX1_TODO_VERIFY = -1;

constexpr uint8_t KORG_MANUFACTURER_ID = 0x42;

} // namespace electribe
