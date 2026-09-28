// Purpose: Observe normal AI decisions and validate bounded T12 play. Created: 2026-09-22.
// SPDX-License-Identifier: GPL-2.0-or-later
Trigger.prototype.T12Time = function()
{
    return Engine.QueryInterface(SYSTEM_ENTITY, IID_Timer).GetTime();
};
Trigger.prototype.T12Entities = function(player)
{
    return Engine.QueryInterface(SYSTEM_ENTITY, IID_RangeManager).GetEntitiesByPlayer(player);
};
Trigger.prototype.T12Name = function(ent)
{
    return Engine.QueryInterface(SYSTEM_ENTITY, IID_TemplateManager).GetCurrentTemplateName(ent);
};
Trigger.prototype.T12Log = function(kind, data)
{
    const event = {time: this.T12Time(), kind, ...data};
    this.t12.events.push(event);
    print('EPOCH_T12_EVENT ' + JSON.stringify(event));
};
Trigger.prototype.T12Init = function()
{
    this.t12 = {events: [], commands: {}, payments: [], finished: false, initial: {}, maxUnits: {},
        gathered: {}, houseCapacity: false, built: [], trained: [], ironFinished: null, centreDamaged: false};
    for (const id of [1, 2])
    {
        const p = QueryPlayerIDInterface(id);
        this.t12.initial[id] = {resources: {...p.GetResourceCounts()},
            population: [p.GetPopulationCount(), p.GetPopulationLimit(), p.GetMaxPopulation()], ai: p.IsAI(),
            rates: Engine.QueryInterface(this.T12Entities(id).find(e => this.T12Name(e) == 'units/epoch_rts/pioneer'), IID_ResourceGatherer).GetGatherRates()};
    }
    const defenders = this.T12Entities(1).filter(e => Engine.QueryInterface(e, IID_UnitAI));
    // Fixture only: the opposing opening force holds its ground and never produces.
    ProcessCommand(1, {type: 'stance', entities: defenders, name: 'standground'});
    this.t12.enemyCentre = this.T12Entities(1).find(e => this.T12Name(e) == 'structures/epoch_rts/civil_centre');
    this.T12Log('opening', this.t12.initial);
    this.DoAfterDelay(1000, 'T12Observe', {});
};
Trigger.prototype.T12Command = function(data)
{
    if (!this.t12 || data.player != 2)
        return;
    const type = data.cmd.type;
    this.t12.commands[type] = (this.t12.commands[type] || 0) + 1;
};
Trigger.prototype.T12Built = function(data)
{
    if (!this.t12 || Engine.QueryInterface(data.building, IID_Ownership)?.GetOwner() != 2)
        return;
    const name = this.T12Name(data.building);
    this.t12.built.push(name);
    const populationLimit = QueryPlayerIDInterface(2).GetPopulationLimit();
    if (name == 'structures/epoch_rts/house' && populationLimit > this.t12.initial[2].population[1])
        this.t12.houseCapacity = true;
    this.T12Log('built', {name, populationLimit});
};
Trigger.prototype.T12Trained = function(data)
{
    if (!this.t12 || data.owner != 2)
        return;
    for (const ent of data.entities)
    {
        const name = this.T12Name(ent);
        this.t12.trained.push(name);
        this.T12Log('trained', {name});
    }
};
Trigger.prototype.T12Research = function(data)
{
    if (!this.t12 || data.player != 2 || data.tech != 'phase_epoch_iron')
        return;
    this.t12.ironFinished = this.T12Time();
    this.T12Log('iron-finished', {});
};
Trigger.prototype.T12Observe = function()
{
    if (!this.t12 || this.t12.finished)
        return;
    const counts = {};
    for (const ent of this.T12Entities(2))
    {
        const name = this.T12Name(ent);
        counts[name] = (counts[name] || 0) + 1;
        this.t12.maxUnits[name] = Math.max(counts[name], this.t12.maxUnits[name] || 0);
    }
    const health = Engine.QueryInterface(this.t12.enemyCentre, IID_Health);
    if (health && health.GetHitpoints() < health.GetMaxHitpoints() && !this.t12.centreDamaged)
    {
        this.t12.centreDamaged = true;
        this.T12Log('enemy-centre-damaged', {hp: health.GetHitpoints()});
    }
    this.t12.gathered = QueryPlayerIDInterface(2, IID_StatisticsTracker).GetStatistics().resourcesGathered;
    if (this.T12Time() >= 1800000)
        this.T12Finish('timeout');
    else
        this.DoAfterDelay(1000, 'T12Observe', {});
};
Trigger.prototype.T12Won = function(data)
{
    if (!this.t12 || this.t12.finished)
        return;
    this.T12Observe();
    this.T12Log('won', {player: data.playerId});
    this.T12Finish('game-ended');
};
Trigger.prototype.T12Finish = function(reason)
{
    if (this.t12.finished)
        return;
    this.t12.finished = true;
    const t = this.t12, checks = [];
    const check = (id, actual, expected) => checks.push({id, actual, expected,
        passed: JSON.stringify(actual) == JSON.stringify(expected)});
    for (const id of [1, 2])
    {
        check('opening.resources.' + id, t.initial[id].resources, {food: 300, wood: 250, stone: 100, metal: 0});
        check('opening.population.' + id, t.initial[id].population, [8, 20, 100]);
        check('opening.ai.' + id, t.initial[id].ai, id == 2);
        for (const [resource, rate] of Object.entries({'food.fruit': 1, 'food.grain': 0.5, 'wood.tree': 0.7, 'stone.rock': 0.35, 'metal.ore': 0.35}))
            check('opening.gatherRate.' + id + '.' + resource, t.initial[id].rates[resource], rate);
    }
    for (const resource of ['food', 'wood', 'metal'])
        check('gather.' + resource, (t.gathered[resource] || 0) > 0, true);
    for (const name of ['house', 'barracks'])
        check('built.' + name, t.built.includes('structures/epoch_rts/' + name), true);
    check('built.house-capacity', t.houseCapacity, true);
    for (const name of ['pioneer', 'iron_swordsman'])
        check('trained.' + name, t.trained.includes('units/epoch_rts/' + name), true);
    const iron = t.payments.find(p => p.type == 'research' && p.template == 'phase_epoch_iron' &&
        p.cost.food == 400 && p.cost.wood == 200 && p.cost.metal == 100);
    check('paid.house', t.payments.some(p => p.template == 'structures/epoch_rts/house' && p.cost.wood == 50), true);
    check('paid.barracks', t.payments.some(p => p.template == 'structures/epoch_rts/barracks' && p.cost.wood == 150 && p.cost.stone == 50), true);
    check('paid.worker', t.payments.some(p => p.template == 'units/epoch_rts/pioneer' && p.cost.food == 50 * p.count), true);
    check('paid.swordsman', t.payments.some(p => p.template == 'units/epoch_rts/iron_swordsman' && p.cost.food == 80 * p.count && p.cost.metal == 40 * p.count), true);
    check('iron.paid', !!iron, true);
    check('iron.finished', t.ironFinished !== null, true);
    check('iron.duration', !!iron && t.ironFinished - iron.time >= 60000, true);
    check('iron.prerequisites', !!iron && iron.bronze && iron.barracks, true);
    check('attack.command', (t.commands.attack || 0) + (t.commands['attack-walk'] || 0) > 0, true);
    check('attack.centre-damaged', t.centreDamaged, true);
    check('winner.ai', QueryPlayerIDInterface(2).GetState(), 'won');
    check('loser.defender', QueryPlayerIDInterface(1).GetState(), 'defeated');
    check('no-cheat-command', t.commands.cheat || 0, 0);
    check('deadline', this.T12Time() <= 1800000, true);
    const result = {mode: 'validation', passed: checks.every(c => c.passed), reason,
        time: this.T12Time(), checks, events: t.events, commands: t.commands,
        ironPayment: iron || null, paymentCount: t.payments.length, gathered: t.gathered, maxUnits: t.maxUnits};
    // Frame short JSON lines: long undelimited native stdout records are truncated.
    const output = JSON.stringify(result), size = 1500;
    for (let offset = 0; offset < output.length; offset += size)
        print('EPOCH_T12_RESULT_CHUNK ' + JSON.stringify({index: offset / size,
            total: Math.ceil(output.length / size), data: output.slice(offset, offset + size)}) + '\n');

};
{
    const trigger = Engine.QueryInterface(SYSTEM_ENTITY, IID_Trigger);
    for (const [event, method] of [['OnInitGame', 'T12Init'], ['OnPlayerCommand', 'T12Command'],
        ['OnStructureBuilt', 'T12Built'], ['OnTrainingFinished', 'T12Trained'],
        ['OnResearchFinished', 'T12Research'], ['OnPlayerWon', 'T12Won']])
        trigger.RegisterTrigger(event, method, {enabled: true});
    // Observe immediate transaction deltas without changing arguments or return values.
    for (const type of ['research', 'train', 'construct'])
    {
        const original = g_Commands[type];
        g_Commands[type] = function(player, cmd, data)
        {
            // Loading replaces component instances; never retain the pre-load Trigger.
            const activeTrigger = Engine.QueryInterface(SYSTEM_ENTITY, IID_Trigger);
            if (player != 2 || !activeTrigger.t12)
                return original(player, cmd, data);
            const p = QueryPlayerIDInterface(player);
            const before = {...p.GetResourceCounts()};
            const bronze = QueryPlayerIDInterface(player, IID_TechnologyManager).IsTechnologyResearched('phase_epoch_bronze');
            const barracks = activeTrigger.T12Entities(player).some(e => activeTrigger.T12Name(e) == 'structures/epoch_rts/barracks');
            const result = original(player, cmd, data);
            const after = p.GetResourceCounts(), cost = {};
            for (const key of ['food', 'wood', 'stone', 'metal'])
                cost[key] = before[key] - after[key];
            if (Object.values(cost).some(value => value > 0))
            {
                const payment = {time: activeTrigger.T12Time(), type, template: cmd.template, count: cmd.count || 1,
                    cost, bronze, barracks};
                activeTrigger.t12.payments.push(payment);
                print('EPOCH_T12_PAYMENT ' + JSON.stringify(payment));
            }
            return result;
        };
    }
}
