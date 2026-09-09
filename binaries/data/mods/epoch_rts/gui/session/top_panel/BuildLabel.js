// Derived from Wildfire Games R28 BuildLabel.js, GPL-2.0-or-later.
// Purpose: Display epoch age and research status. Created: 2026-09-08.
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
        const iron = state.researchedTechs.has("phase_epoch_iron");
        this.ageLabel.caption = translate(iron ? "Iron Age" : "Bronze Age");
        const tech = iron ? "epoch_forged_weapons" : "phase_epoch_iron";
        const queued = state.researchQueued.get(tech);
        if (state.researchedTechs.has(tech))
            this.statusLabel.caption = translate("Forged Weapons completed");
        else if (queued)
            this.statusLabel.caption = queued.started ?
                sprintf(translate("Researching: %(percent)s%%"), { "percent": Math.floor(100 * (1 - queued.timeRemaining / queued.timeTotal)) }) :
                translate("Research queued");
        else if (!(state.classCounts[iron ? "Forge" : "Barracks"] > 0))
            this.statusLabel.caption = translate(iron ? "Build a Forge to research weapons" : "Requires a completed Barracks");
        else if (state.resourceCounts.food < (iron ? 100 : 400) || state.resourceCounts.metal < 100 || !iron && state.resourceCounts.wood < 200)
            this.statusLabel.caption = translate("Insufficient resources for research");
        else
            this.statusLabel.caption = translate(iron ? "Forged Weapons available" : "Iron Age research available");
    }
}

BuildLabel.prototype.SizePlayer = "50%+44 0 100%-283 100%";

BuildLabel.prototype.SizeObserver = "202 0 85%-279 100%";
