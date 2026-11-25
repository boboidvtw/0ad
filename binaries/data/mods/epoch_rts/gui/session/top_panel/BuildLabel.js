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
        // Highest researched age; the starting Bronze Age is researched automatically.
        let current = 0;
        for (let i = 0; i < this.EpochAges.length; ++i)
            if (state.researchedTechs.has(this.EpochAges[i].tech))
                current = i;
        this.ageLabel.caption = translate(this.EpochAges[current].name);
        const next = this.EpochAges[current + 1];
        // After the last age, the Iron Age Forge upgrade is the remaining research goal.
        const tech = next ? next.tech : "epoch_forged_weapons";
        const queued = state.researchQueued.get(tech);
        if (state.researchedTechs.has(tech))
            this.statusLabel.caption = translate("All ages reached");
        else if (queued)
            this.statusLabel.caption = queued.started ?
                sprintf(translate("Researching: %(percent)s%%"), { "percent": Math.floor(100 * (1 - queued.timeRemaining / queued.timeTotal)) }) :
                translate("Research queued");
        else if (!(state.classCounts[next ? next.building : "Forge"] > 0))
            this.statusLabel.caption = translate(next ? next.missing : "Build a Forge to research weapons");
        else if (!this.canAfford(state, tech))
            this.statusLabel.caption = translate("Insufficient resources for research");
        else
            this.statusLabel.caption = translate(next ? next.available : "Forged Weapons available");
    }

    canAfford(state, tech)
    {
        const cost = GetTechnologyData(tech, "epoch")?.cost || {};
        return Object.keys(cost).every(type => type == "time" || (state.resourceCounts[type] || 0) >= cost[type]);
    }
}

// Ordered epoch ladder; "building" is the completed class each next age requires.
BuildLabel.prototype.EpochAges = [
    { "tech": "phase_epoch_bronze", "name": "Bronze Age" },
    { "tech": "phase_epoch_iron", "name": "Iron Age", "building": "Barracks",
        "missing": "Requires a completed Barracks", "available": "Iron Age research available" },
    { "tech": "phase_epoch_dark", "name": "Dark Age", "building": "Forge",
        "missing": "Requires a completed Forge", "available": "Dark Age research available" },
    { "tech": "phase_epoch_medieval", "name": "Middle Ages", "building": "Stable",
        "missing": "Requires a completed Stable", "available": "Middle Ages research available" },
    { "tech": "phase_epoch_renaissance", "name": "Renaissance", "building": "SiegeWorkshop",
        "missing": "Requires a completed Siege Workshop", "available": "Renaissance research available" }
];

BuildLabel.prototype.SizePlayer = "50%+44 0 100%-283 100%";

BuildLabel.prototype.SizeObserver = "202 0 85%-279 100%";
