// Purpose: Observe real two-client commands and synchronized states. Created: 2026-09-28.
// SPDX-License-Identifier: GPL-2.0-or-later
Trigger.prototype.T13Emit = function(kind, value)
{
    const data = JSON.stringify(value), size = 1200;
    for (let offset = 0; offset < data.length; offset += size)
        print('EPOCH_T13_FRAME ' + JSON.stringify({kind, index: offset / size,
            total: Math.ceil(data.length / size), data: data.slice(offset, offset + size)}) + '\n');
};
Trigger.prototype.T13Command = function(message)
{
    if (!message.cmd.t13)
        return;
    this.DoAfterDelay(200, 'T13Executed', message);
};
Trigger.prototype.T13Executed = function(message)
{
    const entities = message.cmd.entities.map(entity => ({entity,
        owner: Engine.QueryInterface(entity, IID_Ownership)?.GetOwner(),
        stance: Engine.QueryInterface(entity, IID_UnitAI)?.GetStanceName()}));
    this.T13Emit('command-' + message.player, {player: message.player, command: message.cmd, entities});
};
Trigger.prototype.T13NetworkTick = function()
{
    const time = Engine.QueryInterface(SYSTEM_ENTITY, IID_Timer).GetTime();
    if (this.t6?.finished)
    {
        this.T13Emit('network-final', {snapshot: T13Snapshot(), checks: this.t6.checks,
            events: this.t6.events, steps: this.t6.steps});
        this.t13NetworkDone = true;
        return;
    }
    this.T13Emit('network-' + time, T13Snapshot());
    this.DoAfterDelay(10000, 'T13NetworkTick', {});
};
{
    const trigger = Engine.QueryInterface(SYSTEM_ENTITY, IID_Trigger);
    trigger.RegisterTrigger('OnPlayerCommand', 'T13Command', {enabled: true});
    trigger.DoAfterDelay(10000, 'T13NetworkTick', {});
}
