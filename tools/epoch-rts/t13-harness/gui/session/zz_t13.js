// Purpose: Native save/load test driver; no gameplay decisions. Created: 2026-09-27.
// SPDX-License-Identifier: GPL-2.0-or-later
var t13Saved = new Set();
var t13CommandSent = false;
var t13NetworkFinishedAt = null;
function t13Emit(kind, value)
{
    const data = JSON.stringify(value), size = 1200;
    for (let offset = 0; offset < data.length; offset += size)
        print('EPOCH_T13_FRAME ' + JSON.stringify({kind, index: offset / size,
            total: Math.ceil(data.length / size), data: data.slice(offset, offset + size)}) + '\n');
}
var t13OriginalInit = init;
init = function(data)
{
    t13OriginalInit(data);
    const mode = Engine.ConfigDB_GetValue('user', 't13.mode');
    if (mode == 'load')
        t13Emit('loaded', Engine.GuiInterfaceCall('T13Snapshot'));
    if (mode == 'save' || mode == 'load')
        Engine.SetSimRate(20);
};
var t13OriginalTick = onTick;
onTick = function()
{
    t13OriginalTick();
    if (!g_Settings || !g_SimState)
        return;
    const mode = Engine.ConfigDB_GetValue('user', 't13.mode');
    const time = g_SimState.timeElapsed;
    if (mode == 'network')
    {
        if (!t13CommandSent && time >= 3000)
        {
            const player = Engine.GetPlayerID();
            const snapshot = Engine.GuiInterfaceCall('T13Snapshot');
            const entity = snapshot.players.find(p => p.id == player)?.entities.find(e => e.template == 'units/epoch_rts/spearman');
            if (entity)
            {
                const command = {type: 'stance', entities: [entity.id], name: 'standground', t13: true};
                Engine.PostNetworkCommand(command);
                t13Emit('sent', {player, command});
                t13CommandSent = true;
            }
        }
        if (Engine.GuiInterfaceCall('T13NetworkDone') && t13NetworkFinishedAt === null)
            t13NetworkFinishedAt = Date.now();
        // Both have consumed final before shutdown. Keep the client alive while
        // the server closes, so the server cannot send to an already closed peer.
        const closeDelay = g_IsController ? 3000 : 10000;
        if (t13NetworkFinishedAt !== null && Date.now() - t13NetworkFinishedAt > closeDelay)
            Engine.Exit();
    }
    if (mode == 'save')
        for (const threshold of [120000, 480000, 700000])
            if (time >= threshold && !t13Saved.has(threshold))
            {
                t13Saved.add(threshold);
                const snapshot = Engine.GuiInterfaceCall('T13Snapshot');
                t13Emit('saved-' + threshold, snapshot);
                const prefix = Engine.ConfigDB_GetValue('user', 't13.prefix');
                Engine.SaveGame(prefix + '-' + threshold, 'T13 isolated validation', getSavedGameData());
            }
    if ((mode == 'save' || mode == 'load') && g_SimState.players.slice(1).some(p => p.state == 'won'))
    {
        t13Emit('final', Engine.GuiInterfaceCall('T13Snapshot'));
        Engine.Exit();
    }
};
