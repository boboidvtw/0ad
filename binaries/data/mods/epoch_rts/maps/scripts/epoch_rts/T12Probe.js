// Purpose: Read-only AI behavior observations for T12 probes. Created: 2026-09-22.
// SPDX-License-Identifier: GPL-2.0-or-later
Trigger.prototype.T12ProbeSample = function()
{
    try
    {
        const tm = Engine.QueryInterface(SYSTEM_ENTITY, IID_TemplateManager);
        const sample = {time: Engine.QueryInterface(SYSTEM_ENTITY, IID_Timer).GetTime(), players: []};
        for (const id of [1, 2])
        {
            const player = QueryPlayerIDInterface(id);
            const entities = Engine.QueryInterface(SYSTEM_ENTITY, IID_RangeManager).GetEntitiesByPlayer(id);
            const types = {}, states = {};
            for (const ent of entities)
            {
                const type = tm.GetCurrentTemplateName(ent);
                types[type] = (types[type] || 0) + 1;
                const ai = Engine.QueryInterface(ent, IID_UnitAI);
                if (ai)
                {
                    const state = ai.GetCurrentState();
                    states[state] = (states[state] || 0) + 1;
                }
            }
            sample.players.push({id, ai: player.IsAI(), state: player.GetState(),
                resources: player.GetResourceCounts(), types, states,
                researched: Array.from(QueryPlayerIDInterface(id, IID_TechnologyManager).GetResearchedTechs()),
                statistics: QueryPlayerIDInterface(id, IID_StatisticsTracker).GetStatistics()});
        }
        print('EPOCH_T12_SAMPLE ' + JSON.stringify(sample));
        if (sample.time < 1800000)
            this.DoAfterDelay(10000, 'T12ProbeSample', {});
        else
            print('EPOCH_T12_PROBE_COMPLETE');
    }
    catch (e)
    {
        error('T12 probe failed: ' + e + '\n' + e.stack);
    }
};
Engine.QueryInterface(SYSTEM_ENTITY, IID_Trigger).DoAfterDelay(1000, 'T12ProbeSample', {});
