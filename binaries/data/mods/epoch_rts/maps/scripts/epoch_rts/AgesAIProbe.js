// Purpose: AI age-ladder probe for epoch_ages_ai_probe: log player 2 economy every 60 sim seconds. Created: 2026-11-25.
// Used to diagnose AI stalls (the Prehistoric food deadlock was found this way); not a pass/fail test.
// SPDX-License-Identifier: GPL-2.0-or-later
Trigger.prototype.EpochAIProbe = function()
{
	const cmp = QueryPlayerIDInterface(2);
	const tm = Engine.QueryInterface(SYSTEM_ENTITY, IID_TemplateManager);
	const names = {};
	for (const e of Engine.QueryInterface(SYSTEM_ENTITY, IID_RangeManager).GetEntitiesByPlayer(2))
	{
		const n = tm.GetCurrentTemplateName(e).replace(/^.*\//, "");
		names[n] = (names[n] || 0) + 1;
	}
	const tech = QueryPlayerIDInterface(2, IID_TechnologyManager);
	print("EPOCH_AI_PROBE " + JSON.stringify({ "t": Engine.QueryInterface(SYSTEM_ENTITY, IID_Timer).GetTime() / 1000,
		"pop": cmp.GetPopulationCount(), "popMax": cmp.GetPopulationLimit(), "res": cmp.GetResourceCounts(), names,
		"queued": [...tech.GetQueuedResearch().keys()] }) + "\n");
	this.DoAfterDelay(60000, "EpochAIProbe", {});
};
Engine.QueryInterface(SYSTEM_ENTITY, IID_Trigger).DoAfterDelay(1000, "EpochAIProbe", {});
