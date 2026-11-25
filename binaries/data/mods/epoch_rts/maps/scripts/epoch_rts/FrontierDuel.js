// Purpose: Fixed T04 duel opening, only on this map and only on new games. Created: 2026-09-07.
// SPDX-License-Identifier: GPL-2.0-or-later
Trigger.prototype.EpochDuelInit = function()
{
	for (const player of [1, 2])
	{
		QueryPlayerIDInterface(player).SetResourceCounts({ "food": 300, "wood": 250, "stone": 100, "metal": 0 });
		QueryPlayerIDInterface(player).SetMaxPopulation(100);
		QueryPlayerIDInterface(player, IID_Diplomacy).SetEnemy(3 - player);
	}
	print("EPOCH_DUEL_INIT " + JSON.stringify({ "players": 2, "resources": [300, 250, 100, 0], "maxPopulation": 100 }));
};
Engine.QueryInterface(SYSTEM_ENTITY, IID_Trigger).RegisterTrigger("OnInitGame", "EpochDuelInit", { "enabled": true });

// M7.3: one-page opening guide in R28's tutorial panel (Ctrl+P toggles it).
// English msgids are translated through l10n/zh_TW.epoch.po. Created: 2026-11-24.
Trigger.prototype.EpochDuelIntro = function()
{
	const instructions = [
		"Goal: destroy every enemy unit and building. The AI attacks after it reaches Iron Age.",
		"1. Select Pioneers and right-click trees, berries, stone or metal to gather.",
		"2. Population starts at 20. Each House adds 10 (50 wood). Keep building Houses.",
		"3. Build a Barracks (150 wood, 50 stone) to train Spearmen and Slingers.",
		"4. With a completed Barracks, research Iron Age at the Civic Center (400 food, 200 wood, 100 metal).",
		"5. Iron Age unlocks Iron Swordsmen and the Forge. Research Forged Weapons at the Forge.",
		"6. Keep advancing at the Civic Center: Dark Age needs a Forge, Middle Ages a Stable, Renaissance a Siege Workshop. Each age costs more."
	];
	const cmpGUIInterface = Engine.QueryInterface(SYSTEM_ENTITY, IID_GuiInterface);
	cmpGUIInterface.PushNotification({
		"type": "tutorial",
		"players": [1],
		// Separate "\n" items keep each msgid identical to its po entry.
		"instructions": instructions.flatMap((item, i) => i ? ["\n", item] : [item])
	});
	// Replaces the panel footer. Literal key name: R28 zh_TW mislabels the P key in hotkey captions.
	cmpGUIInterface.PushNotification({
		"type": "tutorial",
		"players": [1],
		"warning": "Press Ctrl+P to hide or show this guide."
	});
	print("EPOCH_DUEL_INTRO " + JSON.stringify({ "lines": instructions.length }));
};
Engine.QueryInterface(SYSTEM_ENTITY, IID_Trigger).RegisterTrigger("OnInitGame", "EpochDuelIntro", { "enabled": true });

// Age ladder timeline in the engine log, so AI and player age-ups are observable in smoke runs.
// Created: 2026-11-25.
Trigger.prototype.EpochAgeLog = function(data)
{
	if (!data.tech.startsWith("phase_epoch_"))
		return;
	const seconds = Engine.QueryInterface(SYSTEM_ENTITY, IID_Timer).GetTime() / 1000;
	print("EPOCH_AGE " + JSON.stringify({ "player": data.player, "tech": data.tech, "seconds": seconds }) + "\n");
};
Engine.QueryInterface(SYSTEM_ENTITY, IID_Trigger).RegisterTrigger("OnResearchFinished", "EpochAgeLog", { "enabled": true });
