// Purpose: Apply the EpochStartAge / EpochEndAge game settings to one epoch player. Created: 2026-11-25.
// SPDX-License-Identifier: GPL-2.0-or-later
// Runs on MT_InitGame (new games only), after PreInitGame auto-research and before the AI reads
// the game state. Ages up to the start age are granted; ages after the end age are disabled.
function EpochAges() {}

EpochAges.prototype.Schema = "<empty/>";

EpochAges.prototype.Init = function()
{
};

/**
 * @param {Object} [settings] - InitAttributes.settings; missing keys use the default range.
 * @return {{start: number, end: number}} indices into g_EpochAges.
 */
EpochAges.prototype.ResolveRange = function(settings)
{
	const index = (key, fallback) => {
		const i = EpochAgeIndex(key);
		return i == -1 ? EpochAgeIndex(fallback) : i;
	};
	const start = index(settings?.EpochStartAge, g_EpochDefaultStartAge);
	return { "start": start, "end": Math.max(start, index(settings?.EpochEndAge, g_EpochDefaultEndAge)) };
};

EpochAges.prototype.OnInitGame = function()
{
	const settings = typeof InitAttributes == "undefined" ? undefined : InitAttributes.settings;
	this.Apply(this.ResolveRange(settings));
};

EpochAges.prototype.Apply = function(range)
{
	const cmpPlayer = Engine.QueryInterface(this.entity, IID_Player);
	const cmpTechnologyManager = Engine.QueryInterface(this.entity, IID_TechnologyManager);
	const granted = [];
	for (const age of g_EpochAges.slice(0, range.start + 1))
		if (!cmpTechnologyManager.IsTechnologyResearched(age.tech))
		{
			cmpTechnologyManager.ResearchTechnology(age.tech);
			granted.push(age.tech);
		}
	// Starting ages are not achievements: drop their "has reached" phase notifications.
	const cmpGuiInterface = Engine.QueryInterface(SYSTEM_ENTITY, IID_GuiInterface);
	cmpGuiInterface.notifications = cmpGuiInterface.notifications.filter(n =>
		!(n.type == "phase" && granted.includes(n.phaseName) && n.players.includes(cmpPlayer.GetPlayerID())));
	for (const age of g_EpochAges.slice(range.end + 1))
		cmpPlayer.AddDisabledTechnology(age.tech);
};

Engine.RegisterComponentType(IID_EpochAges, "EpochAges", EpochAges);
