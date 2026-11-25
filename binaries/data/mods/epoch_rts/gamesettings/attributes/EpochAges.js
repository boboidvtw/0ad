// Purpose: Epoch RTS start/end age game setting (Empire Earth style epoch range). Created: 2026-11-25.
// SPDX-License-Identifier: GPL-2.0-or-later
// Keys come from globalscripts/EpochAges.js. A map may preset them with EpochStartAge / EpochEndAge
// in its JSON settings. Only players of the epoch civilization are affected.
GameSettings.prototype.Attributes.EpochAges = class EpochAges extends GameSetting
{
	init()
	{
		this.start = g_EpochDefaultStartAge;
		this.end = g_EpochDefaultEndAge;
		this.settings.map.watch(() => this.onMapChange(), ["map"]);
	}

	toInitAttributes(attribs)
	{
		attribs.settings.EpochStartAge = this.start;
		attribs.settings.EpochEndAge = this.end;
	}

	fromInitAttributes(attribs)
	{
		this.setRange(this.getLegacySetting(attribs, "EpochStartAge") || this.start,
			this.getLegacySetting(attribs, "EpochEndAge") || this.end);
	}

	onMapChange()
	{
		this.setRange(this.getMapSetting("EpochStartAge") || g_EpochDefaultStartAge,
			this.getMapSetting("EpochEndAge") || g_EpochDefaultEndAge);
	}

	setStart(key)
	{
		this.setRange(key, this.end);
	}

	setEnd(key)
	{
		this.setRange(this.start, key);
	}

	/** Unknown keys fall back to the defaults; the end age is never before the start age. */
	setRange(start, end)
	{
		const startIndex = EpochAgeIndex(start) == -1 ? EpochAgeIndex(g_EpochDefaultStartAge) : EpochAgeIndex(start);
		const endIndex = EpochAgeIndex(end) == -1 ? EpochAgeIndex(g_EpochDefaultEndAge) : EpochAgeIndex(end);
		this.start = g_EpochAges[startIndex].key;
		this.end = g_EpochAges[Math.max(startIndex, endIndex)].key;
	}
};
