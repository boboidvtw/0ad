// Derived from Wildfire Games 0.28.0 MiniMapPanel.js, GPL-2.0-or-later.
// Purpose: Use an existing temporary minimap frame for epoch. Created: 2026-09-07.
/**
 * This class is concerned with managing the different elements of the minimap panel.
 */
class MiniMapPanel
{
	constructor(playerViewControl, diplomacyColors, idleWorkerClasses)
	{
		this.diplomacyColorsButton = new MiniMapDiplomacyColorsButton(diplomacyColors);
		this.idleWorkerButton = new MiniMapIdleWorkerButton(playerViewControl, idleWorkerClasses);
		this.flareButton = new MiniMapFlareButton(playerViewControl);
		this.miniMap = new MiniMap();
		playerViewControl.registerViewedPlayerChangeHandler(this.rebuild.bind(this));
		registerHotkeyChangeHandler(this.rebuild.bind(this));
	}

	flare(target, playerID)
	{
		return this.miniMap.flare(target, playerID);
	}

	isMouseOverMiniMap()
	{
		return this.miniMap.isMouseOverMiniMap();
	}

	rebuild()
	{
		this.setCivBackgroundTexture();
	}

	setCivBackgroundTexture()
	{
		let playerCiv = g_ViewedPlayer > 0 ? g_Players[g_ViewedPlayer].civ : "gaia";
		// Temporary R28 art; epoch has no final minimap frame yet.
		if (playerCiv == "epoch")
			playerCiv = "athen";
		const backgroundObject = Engine.GetGUIObjectByName("minimapBackgroundTexture");
		backgroundObject.sprite = `stretched:session/icons/bkg/background_circle_${playerCiv}.png`;
	}
}
