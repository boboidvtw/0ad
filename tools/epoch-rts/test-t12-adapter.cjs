// Purpose: Test instance isolation and collection lifecycle of the T12 adapter. Created: 2026-09-26.
// SPDX-License-Identifier: GPL-2.0-or-later
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
let updates = 0;
function upstreamUpdate() { ++updates; }
function PetraBot() {
    this.HQ = {attackManager: {update: upstreamUpdate, upcomingAttacks: {Attack: []}},
        researchManager: {Config: {Economy: {popPhase2: 38, workPhase3: 65, workPhase4: 80}, priorities: {majorTech: 200}}}};
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
// Petra's thresholds follow the age's place on the ladder, not its index in the chain: a Bronze
// start must reach Iron at popPhase2, as the two-age game did, instead of waiting for workPhase4.
function phaseQueues() {
    const plans = [];
    const queue = (queued = false) => ({hasQueuedUnits: () => queued, addPlan: p => plans.push(p)});
    return {plans, queues: {majorTech: queue(), civilCentre: queue(), wonder: queue()}};
}
function phaseState(current, population, workers) {
    return {...gs, currentPhase: () => current, getPhaseName: i => gs.phases[i - 1]?.name, hasResearchers: () => true,
        ai: {HQ: {getAccountedPopulation: () => population, getAccountedWorkers: () => workers},
            queueManager: {changePriority() {}}, Config: {priorities: {majorTech: 200}}}};
}
context.ResearchPlan = function(state, name) { this.name = name; };
const research = bot.HQ.researchManager;
const nextAge = (current, population, workers) => {
    const {plans, queues} = phaseQueues();
    const s = phaseState(current, population, workers);
    s.ai.HQ.phasing = 0;
    research.checkPhase(s, queues);
    return plans[0]?.name;
};
assert.equal(nextAge(4, 37, 37), undefined, 'Iron waits for popPhase2');
assert.equal(nextAge(4, 38, 30), 'phase_epoch_iron', 'Bronze start: Iron at popPhase2, not workPhase4');
assert.equal(nextAge(1, 38, 30), 'phase_epoch_stone', 'Prehistoric start: Stone at popPhase2');
assert.equal(nextAge(5, 90, 65), undefined, 'Dark Age waits for more than workPhase3 workers');
assert.equal(nextAge(5, 90, 66), 'phase_epoch_dark');
assert.equal(nextAge(6, 90, 80), undefined, 'Middle Ages and later wait for workPhase4');
assert.equal(nextAge(6, 90, 81), 'phase_epoch_medieval');
assert.equal(nextAge(16, 200, 200), undefined, 'no age after Space');
// Petra's Attack queue has priority 90 and majorTech 700, so ages after Iron Age kept the attack
// army from training and AI games ran past 20 minutes. Those ages now queue below the army.
const priorityFor = (current, population, workers) => {
    const {queues} = phaseQueues();
    const s = phaseState(current, population, workers);
    let set;
    s.ai.queueManager.changePriority = (queue, value) => { set = [queue, value]; };
    research.checkPhase(s, queues);
    return set;
};
assert.deepEqual(priorityFor(4, 38, 30), ['majorTech', 200], 'Iron Age keeps the configured priority');
assert.deepEqual(priorityFor(5, 90, 66), ['majorTech', 50], 'Dark Age queues below the Attack queue (90)');
assert.deepEqual(priorityFor(12, 90, 81), ['majorTech', 50], 'later ages too');
console.log('PASS: instance isolation, phase mapping, Bronze gate, ladder-based phase thresholds, collection lifecycle, build orders, idempotence; mocked API, not engine acceptance');
