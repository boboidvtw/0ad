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
