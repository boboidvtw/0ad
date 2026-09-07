// Copyright (C) 2026 Epoch RTS contributors. SPDX-License-Identifier: GPL-2.0-or-later
// Purpose: M1 integration map using public rmgen and temporary assets. Created: 2026-09-06.
Engine.LoadLibrary("rmgen");
Engine.LoadLibrary("rmgen-common");

export function* generateMap(mapSettings)
{
	if (getNumPlayers() != 2 || mapSettings.Size < 128 || mapSettings.Nomad)
		throw new Error("Epoch Frontier requires two players, size >= 128 and Nomad disabled.");

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

	const { playerIDs, playerPosition: positions } = placement;
	for (let i = 0; i < playerIDs.length; ++i)
	{
		// Place the custom unit near its starting civic centre for easy visual verification.
		const position = new Vector2D(positions[i].x + 8, positions[i].y + 8);
		if (!g_Map.placeEntityPassable("units/epoch_rts/pioneer", playerIDs[i], position, 0))
			throw new Error("Epoch Frontier could not place a Pioneer for player " + playerIDs[i]);
	}

	setSkySet("cirrus");
	setSunRotation(Math.PI / 4);
	setSunElevation(Math.PI / 4);
	g_Map.log("Epoch RTS M1: Frontier ready; players=2; pioneers=2; two-era gameplay pending.");
	yield 100;
	return g_Map;
}
