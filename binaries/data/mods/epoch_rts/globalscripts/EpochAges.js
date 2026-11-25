// Purpose: Ordered Epoch RTS age ladder shared by simulation, GUI, game setup and AI. Created: 2026-11-25.
// SPDX-License-Identifier: GPL-2.0-or-later
// Modeled on Empire Earth's 15 epochs, plus this mod's existing Iron Age (16 in total).
// - key: short id used by the EpochStartAge / EpochEndAge game settings.
// - building: completed entity class the age requires (absent for stat-only later ages).
// - cancel: notification msgid when that building is lost before research starts.
// Names and messages are English msgids translated through l10n/zh_TW.epoch.po.
var g_EpochAges = Object.freeze([
	{ "key": "prehistoric", "tech": "phase_epoch_prehistoric", "name": "Prehistoric Age" },
	{ "key": "stone", "tech": "phase_epoch_stone", "name": "Stone Age", "building": "Storehouse", "buildingName": "Storehouse",
		"cancel": "Stone Age research cancelled: a completed Storehouse is required. Resources refunded." },
	{ "key": "copper", "tech": "phase_epoch_copper", "name": "Copper Age", "building": "Barracks", "buildingName": "Barracks",
		"cancel": "Copper Age research cancelled: a completed Barracks is required. Resources refunded." },
	{ "key": "bronze", "tech": "phase_epoch_bronze", "name": "Bronze Age", "building": "Field", "buildingName": "Field",
		"cancel": "Bronze Age research cancelled: a completed Field is required. Resources refunded." },
	{ "key": "iron", "tech": "phase_epoch_iron", "name": "Iron Age", "building": "Barracks", "buildingName": "Barracks",
		"cancel": "Iron Age research cancelled: a completed Barracks is required. Resources refunded." },
	{ "key": "dark", "tech": "phase_epoch_dark", "name": "Dark Age", "building": "Forge", "buildingName": "Forge",
		"cancel": "Dark Age research cancelled: a completed Forge is required. Resources refunded." },
	{ "key": "medieval", "tech": "phase_epoch_medieval", "name": "Middle Ages", "building": "Stable", "buildingName": "Stable",
		"cancel": "Middle Ages research cancelled: a completed Stable is required. Resources refunded." },
	{ "key": "renaissance", "tech": "phase_epoch_renaissance", "name": "Renaissance", "building": "SiegeWorkshop", "buildingName": "Siege Workshop",
		"cancel": "Renaissance research cancelled: a completed Siege Workshop is required. Resources refunded." },
	{ "key": "imperial", "tech": "phase_epoch_imperial", "name": "Imperial Age" },
	{ "key": "industrial", "tech": "phase_epoch_industrial", "name": "Industrial Age" },
	{ "key": "atomic_ww1", "tech": "phase_epoch_atomic_ww1", "name": "Atomic Age – WWI" },
	{ "key": "atomic_ww2", "tech": "phase_epoch_atomic_ww2", "name": "Atomic Age – WWII" },
	{ "key": "atomic_modern", "tech": "phase_epoch_atomic_modern", "name": "Atomic Age – Modern" },
	{ "key": "digital", "tech": "phase_epoch_digital", "name": "Digital Age" },
	{ "key": "nano", "tech": "phase_epoch_nano", "name": "Nano Age" },
	{ "key": "space", "tech": "phase_epoch_space", "name": "Space Age" }
].map(age => Object.freeze(age)));

// Default game setting values: a normal match starts in Bronze Age and may reach every age.
var g_EpochDefaultStartAge = "bronze";
var g_EpochDefaultEndAge = "space";

function EpochAgeIndex(key)
{
	return g_EpochAges.findIndex(age => age.key == key);
}
