// Purpose: Reproduce replacement of Trigger during native load. Created: 2026-09-28.
// SPDX-License-Identifier: GPL-2.0-or-later
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
function Trigger() {}
Trigger.prototype.RegisterTrigger = function() {};
Trigger.prototype.DoAfterDelay = function() {};
let active = new Trigger();
const beforeLoad = active;
let food = 300, calls = 0;
const original = () => { ++calls; food -= 50; return 'native-result'; };
const context = {Trigger, SYSTEM_ENTITY: 0, IID_Trigger: 'trigger', IID_TechnologyManager: 'tech',
    Engine: {QueryInterface: () => active}, print() {},
    QueryPlayerIDInterface: (id, iid) => iid == 'tech' ? {IsTechnologyResearched: () => true} : {GetResourceCounts: () => ({food, wood: 0, stone: 0, metal: 0})},
    g_Commands: {construct: original, train: original, research: original}};
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(__dirname, '../../binaries/data/mods/epoch_rts/maps/scripts/epoch_rts/T12Validation.js'), 'utf8'), context);
function initialize(t) {
    t.t12 = {payments: []};
    t.T12Entities = () => [1];
    t.T12Name = () => 'structures/epoch_rts/barracks';
    t.T12Time = () => 480000;
}
initialize(beforeLoad);
active = new Trigger();
initialize(active);
assert.equal(context.g_Commands.train(2, {template: 'units/epoch_rts/iron_swordsman'}, {}), 'native-result');
assert.equal(calls, 1);
assert.equal(beforeLoad.t12.payments.length, 0, 'Stale pre-load Trigger must remain untouched');
assert.equal(active.t12.payments.length, 1, 'Payment must reach restored Trigger');
assert.equal(active.t12.payments[0].cost.food, 50);
assert.equal(active.t12.payments[0].template, 'units/epoch_rts/iron_swordsman');
context.g_Commands.train(1, {template: 'other'}, {});
assert.equal(calls, 2);
assert.equal(active.t12.payments.length, 1, 'Other players are not observed');
active = new Trigger();
context.g_Commands.research(2, {template: 'other'}, {});
assert.equal(calls, 3, 'Pre-init command still delegates');
console.log('PASS: restored Trigger payment capture, untouched stale instance, normal command delegation; mocked lifecycle');
