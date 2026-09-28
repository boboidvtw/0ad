// Purpose: Start native saved game in a fresh engine process. Created: 2026-09-27.
// SPDX-License-Identifier: GPL-2.0-or-later
function init(data)
{
    if (Engine.ConfigDB_GetValue('user', 't13.mode') != 'load')
        return;
    const name = Engine.ConfigDB_GetValue('user', 't13.load');
    const metadata = Engine.StartSavedGame(name);
    if (!metadata)
        throw new Error('T13 native load failed: ' + name);
    Engine.SwitchGuiPage('page_loading.xml', {attribs: metadata.initAttributes,
        playerAssignments: {local: {name: 'T13 observer', player: metadata.playerID}}, savedGUIData: metadata.gui});
};
