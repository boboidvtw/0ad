// Purpose: T11 original art inspection ground. Created: 2026-09-21.
// SPDX-License-Identifier: GPL-2.0-or-later
Engine.LoadLibrary("rmgen");
Engine.LoadLibrary("rmgen-common");
export function* generateMap(settings)
{
    globalThis.g_Map = new RandomMap(3,"medit_grass_field_a");
    setSkySet("cirrus");
    setSunRotation(Math.PI/4);setSunElevation(Math.PI/4);
    g_Camera.Position={x:330,y:85,z:210};g_Camera.Declination=0.6;
    yield 100;return g_Map;
}
