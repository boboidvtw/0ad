// Purpose: Isolated deep-water R28 API probe map. Created: 2026-09-20.
// SPDX-License-Identifier: GPL-2.0-or-later
Engine.LoadLibrary("rmgen");
Engine.LoadLibrary("rmgen-common");
export function* generateMap(settings)
{
    globalThis.g_Map = new RandomMap(-12, "medit_sand_wet");
    setWaterHeight(20); // R28 rmgen exports terrain with SEA_LEVEL +20.
    setWaterType("ocean");
    setSkySet("cirrus");
    g_Camera.Position = {x:325,y:120,z:150};
    g_Camera.Declination = 0.6;
    // Land strip provides an actual native ship pathability boundary.
    for (let x = 130; x < settings.Size; ++x)
        for (let z = 0; z < settings.Size; ++z)
            g_Map.setHeight(new Vector2D(x,z), 4);
    yield 100;
    return g_Map;
}
