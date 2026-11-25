// Derived from Wildfire Games R28 BuildLabel.js, GPL-2.0-or-later.
// Purpose: Display epoch age and research status. Created: 2026-09-08; age ladder 2026-11-25.
/**
 * This class displays the version information in the top panel.
 */
class BuildLabel
{
	constructor(playerViewControl)
	{
		this.viewPlayer = Engine.GetGUIObjectByName("viewPlayer");
		this.buildLabel = Engine.GetGUIObjectByName("buildLabel");
        this.ageLabel = Engine.GetGUIObjectByName("epochAgeLabel");
        this.statusLabel = Engine.GetGUIObjectByName("buildTimeLabel");
        this.originalAge = this.ageLabel.caption;
        registerSimulationUpdateHandler(this.updateEpochAge.bind(this));

		Engine.GetGUIObjectByName("buildTimeLabel").caption = getBuildString();

		playerViewControl.registerViewedPlayerChangeHandler(this.onViewedPlayerChanged.bind(this));
	}

	onViewedPlayerChanged()
	{
		const isPlayer = g_ViewedPlayer > 0;
		this.buildLabel.hidden = isPlayer && !this.viewPlayer.hidden;
		this.buildLabel.size = isPlayer ? this.SizePlayer : this.SizeObserver;
        this.updateEpochAge();
	}
    updateEpochAge()
    {
        const state = g_SimState?.players[g_ViewedPlayer];
        if (!state || state.civ != "epoch")
        {
            this.ageLabel.caption = this.originalAge;
            this.statusLabel.caption = getBuildString();
            return;
        }
        // Highest researched age (table in globalscripts/EpochAges.js).
        let current = 0;
        g_EpochAges.forEach((age, i) => {
            if (state.researchedTechs.has(age.tech))
                current = i;
        });
        this.ageLabel.caption = translate(g_EpochAges[current].name);
        // The game's End Age disables every later age.
        const next = g_EpochAges[current + 1] && !state.disabledTechnologies?.[g_EpochAges[current + 1].tech] ?
            g_EpochAges[current + 1] : undefined;
        if (!next)
        {
            this.statusLabel.caption = translate("Final age reached");
            return;
        }
        const queued = state.researchQueued.get(next.tech);
        const ageName = translate(next.name);
        if (queued)
            this.statusLabel.caption = queued.started ?
                sprintf(translate("Researching: %(percent)s%%"), { "percent": Math.floor(100 * (1 - queued.timeRemaining / queued.timeTotal)) }) :
                translate("Research queued");
        else if (next.building && !(state.classCounts[next.building] > 0))
            this.statusLabel.caption = sprintf(translate("%(age)s needs a completed %(building)s"),
                { "age": ageName, "building": translate(next.buildingName) });
        else if (!this.canAfford(state, next.tech))
            this.statusLabel.caption = translate("Insufficient resources for research");
        else
            this.statusLabel.caption = sprintf(translate("%(age)s research available"), { "age": ageName });
    }

    canAfford(state, tech)
    {
        const cost = GetTechnologyData(tech, "epoch")?.cost || {};
        return Object.keys(cost).every(type => type == "time" || (state.resourceCounts[type] || 0) >= cost[type]);
    }
}

BuildLabel.prototype.SizePlayer = "50%+44 0 100%-283 100%";

BuildLabel.prototype.SizeObserver = "202 0 85%-279 100%";
