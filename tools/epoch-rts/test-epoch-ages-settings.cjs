// Purpose: Test the Epoch start/end age game setting and setup dropdowns with mocked R28 APIs. Created: 2026-11-25.
// SPDX-License-Identifier: GPL-2.0-or-later
// Guards against: an end age before the start age, unknown keys leaking into InitAttributes,
// map presets being ignored, and dropdowns that do not reach the setting or the layout.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const mod = path.join(__dirname, '../../binaries/data/mods/epoch_rts');
const load = (context, file) => vm.runInContext(fs.readFileSync(path.join(mod, file), 'utf8'), context);

class Observable {
    constructor() { this.watchers = []; }
    watch(callback, props) { this.watchers.push({callback, props}); }
}
class GameSetting extends Observable {
    constructor(settings) { super(); this.settings = settings; }
    getLegacySetting(attribs, name) { return attribs?.settings?.[name]; }
    getMapSetting(name) { return this.settings.map.data?.settings?.[name]; }
}
function GameSettings() {}
GameSettings.prototype.Attributes = {};
const context = {Observable, GameSetting, GameSettings};
vm.createContext(context);
load(context, 'globalscripts/EpochAges.js');
load(context, 'gamesettings/attributes/EpochAges.js');

const map = {data: undefined, watch() {}};
const setting = new GameSettings.prototype.Attributes.EpochAges({map});
setting.init();
assert.deepEqual([setting.start, setting.end], ['bronze', 'space'], 'default range');
setting.setStart('industrial');
setting.setEnd('copper');
assert.deepEqual([setting.start, setting.end], ['industrial', 'industrial'], 'end never before start');
setting.setRange('not-an-age', 'also-not');
assert.deepEqual([setting.start, setting.end], ['bronze', 'space'], 'unknown keys fall back to defaults');
map.data = {settings: {EpochStartAge: 'prehistoric', EpochEndAge: 'renaissance'}};
setting.onMapChange();
assert.deepEqual([setting.start, setting.end], ['prehistoric', 'renaissance'], 'map preset');
const attribs = {settings: {}};
setting.toInitAttributes(attribs);
assert.deepEqual(attribs.settings, {EpochStartAge: 'prehistoric', EpochEndAge: 'renaissance'});
setting.fromInitAttributes({settings: {EpochStartAge: 'dark'}});
assert.deepEqual([setting.start, setting.end], ['dark', 'renaissance'], 'partial saved settings keep the other value');

// Dropdowns: list every age, show the setting, write through the setter, join the Player tab.
class GameSettingControlDropdown {
    constructor() { this.dropdown = {}; this.gameSettingsController = {sent: 0, setNetworkInitAttributes() { ++this.sent; }}; }
    setSelectedValue(value) { this.selected = value; }
}
const layout = [{settings: ['MapType']}, {settings: ['PlayerCount', 'StartingResources', 'Cheats']}];
const gui = {GameSettingControlDropdown, GameSettingControls: {}, g_GameSettingsLayout: layout,
    g_GameSettings: {epochAges: setting}, translate: text => text};
vm.createContext(gui);
load(gui, 'globalscripts/EpochAges.js');
load(gui, 'gui/gamesetup/Pages/GameSetupPage/GameSettings/Single/Dropdowns/EpochAges.js');
assert.deepEqual(layout[1].settings.slice(-2), ['EpochStartAge', 'EpochEndAge']);
const start = new gui.GameSettingControls.EpochStartAge();
const end = new gui.GameSettingControls.EpochEndAge();
assert.equal(start.dropdown.list.length, 16);
assert.equal(start.dropdown.list[0], 'Prehistoric Age');
assert.equal(start.dropdown.list[15], 'Space Age');
assert.deepEqual([start.selected, end.selected], ['dark', 'renaissance']);
start.onSelectionChange(start.dropdown.list_data.indexOf('stone'));
end.onSelectionChange(end.dropdown.list_data.indexOf('iron'));
assert.deepEqual([setting.start, setting.end], ['stone', 'iron']);
assert.equal(start.gameSettingsController.sent + end.gameSettingsController.sent, 2, 'network sync after each change');
console.log('PASS: default range, clamping, unknown keys, map preset, init attributes, dropdown list/setter/layout; mocked API, not the setup page');
