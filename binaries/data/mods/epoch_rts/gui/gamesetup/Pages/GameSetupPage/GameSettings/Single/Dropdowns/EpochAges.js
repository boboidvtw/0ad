// Purpose: Game setup dropdowns for the Epoch RTS start and end age. Created: 2026-11-25.
// SPDX-License-Identifier: GPL-2.0-or-later
class EpochAgeDropdown extends GameSettingControlDropdown
{
	constructor(...args)
	{
		super(...args);
		this.dropdown.list = g_EpochAges.map(age => translate(age.name));
		this.dropdown.list_data = g_EpochAges.map(age => age.key);
		g_GameSettings.epochAges.watch(() => this.render(), ["start", "end"]);
		this.render();
	}

	onLoad()
	{
		this.render();
	}

	render()
	{
		this.setSelectedValue(g_GameSettings.epochAges[this.Property]);
	}

	onSelectionChange(itemIdx)
	{
		g_GameSettings.epochAges[this.Setter](this.dropdown.list_data[itemIdx]);
		this.gameSettingsController.setNetworkInitAttributes();
	}
}

GameSettingControls.EpochStartAge = class EpochStartAge extends EpochAgeDropdown {};
GameSettingControls.EpochStartAge.prototype.Property = "start";
GameSettingControls.EpochStartAge.prototype.Setter = "setStart";
GameSettingControls.EpochStartAge.prototype.TitleCaption = translate("Start Age");
GameSettingControls.EpochStartAge.prototype.Tooltip =
	translate("Epoch RTS: the age every Frontier Union player starts in. Earlier ages are granted at once.");

GameSettingControls.EpochEndAge = class EpochEndAge extends EpochAgeDropdown {};
GameSettingControls.EpochEndAge.prototype.Property = "end";
GameSettingControls.EpochEndAge.prototype.Setter = "setEnd";
GameSettingControls.EpochEndAge.prototype.TitleCaption = translate("End Age");
GameSettingControls.EpochEndAge.prototype.Tooltip =
	translate("Epoch RTS: the last age Frontier Union players can research.");

// g_GameSettingsLayout is defined in GameSettings/, loaded before this Dropdowns/ directory.
g_GameSettingsLayout.find(tab => tab.settings.includes("StartingResources")).settings.push("EpochStartAge", "EpochEndAge");
