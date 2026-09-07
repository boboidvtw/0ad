// Copyright (C) 2026 Epoch RTS contributors. SPDX-License-Identifier: GPL-2.0-or-later
// Purpose: T04 economy map using public rmgen and temporary assets. Created: 2026-09-06.
Engine.LoadLibrary("rmgen");
Engine.LoadLibrary("rmgen-common");

export function* generateMap(mapSettings)
{
	if (getNumPlayers() != 2 || mapSettings.Size != 192 || mapSettings.Nomad ||
		getCivCode(1) != "epoch" || getCivCode(2) != "epoch")
		throw new Error("Frontier Duel requires two epoch players, size 192 and Nomad disabled.");

	globalThis.g_Map = new RandomMap(3, "medit_grass_field_a");
	const playerClass = g_Map.createTileClass();
	const resourceClass = g_Map.createTileClass();
	const placement = playerPlacementCircle(fractionToTiles(0.28), 0);

	placePlayerBases({
		"PlayerPlacement": placement,
		"PlayerTileClass": playerClass,
		"BaseResourceClass": resourceClass,
		"Walls": false,
		"CityPatch": {
			"outerTerrain": "medit_city_tile",
			"innerTerrain": "medit_city_tile"
		},
		"Berries": { "template": "gaia/fruit/berry_01" },
		"Mines": {
			"types": [
				{ "template": "gaia/ore/mediterranean_large" },
				{ "template": "gaia/rock/mediterranean_large" }
			]
		},
		"Trees": { "template": "gaia/tree/aleppo_pine", "count": 30 }
	});
	yield 50;


	setSkySet("cirrus");
	setSunRotation(Math.PI / 4);
	setSunElevation(Math.PI / 4);
	g_Map.log("Epoch RTS T04: Duel ready; players=2; workers=12; spearmen=4;");
	yield 100;
	return g_Map;
}
