// Purpose: Fixed static-asset inspection ground. Created: 2026-09-21.
// SPDX-License-Identifier: GPL-2.0-or-later
Engine.LoadLibrary("rmgen");
Engine.LoadLibrary("rmgen-common");
export function* generateMap(settings)
{
    globalThis.g_Map = new RandomMap(3,"medit_grass_field_a");
    setSkySet("cirrus");
    setSunRotation(Math.PI/4);setSunElevation(Math.PI/4);
    g_Camera.Position={x:340,y:100,z:185};g_Camera.Declination=0.6;
    yield 100;return g_Map;
}
