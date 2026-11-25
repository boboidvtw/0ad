// Purpose: Test instance isolation and collection lifecycle of the T12 adapter. Created: 2026-09-26.
// SPDX-License-Identifier: GPL-2.0-or-later
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
let updates = 0;
function upstreamUpdate() { ++updates; }
function PetraBot() {
    this.HQ = {attackManager: {update: upstreamUpdate, upcomingAttacks: {Attack: []}}};
}
PetraBot.prototype.CustomInit = function() {};
const context = {PetraBot, filters: {byClasses: classes => classes},
    GetTechnologyBasicDataHelper: template => ({reqs: template.requirements})};
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(__dirname,
    '../../binaries/data/mods/epoch_rts/globalscripts/EpochAges.js'), 'utf8'), context);
const source = fs.readFileSync(path.join(__dirname,
    '../../binaries/data/mods/epoch_rts/simulation/ai/epoch_petra/_epochbot.js'), 'utf8');
vm.runInContext(source.replace(/^import .*;\n/gm, '').replace('export function', 'function'), context);
function state(civ, disabledTechnologies = {}) {
    return {playerData: {disabledTechnologies}, getPlayerCiv: () => civ, applyCiv: name => name.replace('{civ}', civ),
        getTemplate: name => ({_template: {requirements: [name]}}), currentPhase: () => 1};
}
const other = new PetraBot(), otherState = state('athen');
const bot = new context.EpochPetraBot({}), gs = state('epoch');
assert.throws(() => bot.CustomInit(otherState), /epoch civilization/);
bot.CustomInit(gs);
assert.equal(gs.applyCiv('structures/{civ}/civil_centre'), 'structures/epoch_rts/civil_centre');
assert.equal(otherState.applyCiv('structures/{civ}/civil_centre'), 'structures/athen/civil_centre');
assert.equal(other.HQ.attackManager.update, upstreamUpdate);
const allAges = ['prehistoric', 'stone', 'copper', 'bronze', 'iron', 'dark', 'medieval', 'renaissance',
    'imperial', 'industrial', 'atomic_ww1', 'atomic_ww2', 'atomic_modern', 'digital', 'nano', 'space'].map(k => 'phase_epoch_' + k);
assert.equal(JSON.stringify(gs.phases.map(p => p.name)), JSON.stringify(allAges));
assert.equal(gs.phases[4].requirements[0], 'phase_epoch_iron');
assert.equal(gs.phases[15].requirements[0], 'phase_epoch_space');
// An End Age of Copper disables Bronze onward; the chain stops and attacks start in the End Age.
const capped = new context.EpochPetraBot({}), cappedState = state('epoch', {phase_epoch_bronze: true, phase_epoch_iron: true});
capped.CustomInit(cappedState);
assert.equal(JSON.stringify(cappedState.phases.map(p => p.name)), JSON.stringify(allAges.slice(0, 3)));
capped.HQ.attackManager.upcomingAttacks = {};
cappedState.currentPhase = () => 2;
const cappedUpstream = updates;
capped.HQ.attackManager.update(cappedState, {}, {});
assert.equal(updates, cappedUpstream, 'Stone must not attack when the End Age is Copper');
cappedState.currentPhase = () => 3;
capped.HQ.attackManager.update(cappedState, {}, {});
assert.equal(updates, cappedUpstream + 1, 'End Age Copper attacks from Copper');
updates = cappedUpstream;
const manager = bot.HQ.attackManager;
manager.update(gs, {}, {});
gs.currentPhase = () => 4;
manager.update(gs, {}, {});
assert.equal(updates, 0, 'Bronze must not update offensive manager');
let unregistered = 0, registered = 0;
function plan(canBuildUnits) {
    return {canBuildUnits, unitStat: {MeleeInfantry: {minSize: 6}, RangedInfantry: {minSize: 6}, Hero: {}},
        unit: {a: {unregister() { ++unregistered; }}, b: {unregister() { ++unregistered; }}},
        unitCollection: {filter(classes) {
            return {classes, registerUpdates() { ++registered; }};
        }}, buildOrders: [['stale']]};
}
const training = plan(true), noTraining = plan(false), raid = {unitStat: {FastMoving: {}}};
manager.upcomingAttacks.Attack.push(training, noTraining, raid);
gs.currentPhase = () => 5;
manager.update(gs, {}, {});
assert.equal(updates, 1);
assert.equal(unregistered, 4);
assert.equal(registered, 4);
assert.equal(training.buildOrders.length, 2);
assert.equal(noTraining.buildOrders.length, 0);
assert.equal(training.buildOrders[0][2], training.unit.MeleeInfantry);
assert.equal(training.buildOrders[0][3], training.unitStat.MeleeInfantry);
assert.equal(training.unitStat.MeleeInfantry.classes[0], 'Infantry+Swordsman');
assert.equal(training.unitStat.RangedInfantry.classes[0], 'Infantry+Slinger');
assert.equal(training.unitStat.Hero, undefined);
assert.equal(raid.epochClasses, undefined);
manager.update(gs, {}, {});
assert.equal(updates, 2);
assert.equal(unregistered, 4, 'Re-adaptation must not unregister active collections');
assert.equal(registered, 4);
assert.equal(other.HQ.attackManager.update, upstreamUpdate);
console.log('PASS: instance isolation, phase mapping, Bronze gate, collection lifecycle, build orders, idempotence; mocked API, not engine acceptance');
