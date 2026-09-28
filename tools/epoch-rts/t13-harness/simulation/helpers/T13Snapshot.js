// Purpose: Read-only deterministic T13 state snapshot. Created: 2026-09-27.
// SPDX-License-Identifier: GPL-2.0-or-later
function T13Snapshot()
{
    const query = (ent, iid) => Engine.QueryInterface(ent, iid);
    const range = query(SYSTEM_ENTITY, IID_RangeManager);
    const tm = query(SYSTEM_ENTITY, IID_TemplateManager);
    const players = [1, 2].map(id => {
        const p = QueryPlayerIDInterface(id);
        const tech = QueryPlayerIDInterface(id, IID_TechnologyManager);
        return {id, resources: p.GetResourceCounts(), population: [p.GetPopulationCount(), p.GetPopulationLimit(), p.GetMaxPopulation()],
            state: p.GetState(), researched: Array.from(tech.GetResearchedTechs()).sort(), queuedResearch: Array.from(tech.GetQueuedResearch().keys()).sort().map(name => ({name, info: tech.GetBasicInfo(name)})),
            statistics: QueryPlayerIDInterface(id, IID_StatisticsTracker).GetStatistics(),
            entities: range.GetEntitiesByPlayer(id).sort((a, b) => a-b).map(ent => {
                const position = query(ent, IID_Position), ai = query(ent, IID_UnitAI);
                const health = query(ent, IID_Health), queue = query(ent, IID_ProductionQueue);
                const foundation = query(ent, IID_Foundation), gatherer = query(ent, IID_ResourceGatherer);
                return {id: ent, template: tm.GetCurrentTemplateName(ent),
                    position: position?.IsInWorld() ? position.GetPosition() : null,
                    rotation: position?.GetRotation(), hp: health?.GetHitpoints(),
                    state: ai?.GetCurrentState(), orders: ai?.GetOrders(),
                    queue: queue?.GetQueue(), foundation: foundation?.GetBuildPercentage(),
                    carrying: gatherer?.GetCarryingStatus()};
            })};
    });
    return {time: query(SYSTEM_ENTITY, IID_Timer).GetTime(), players};
}
Engine.RegisterGlobal('T13Snapshot', T13Snapshot);
