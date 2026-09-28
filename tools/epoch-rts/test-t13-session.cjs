// Purpose: Cover role-ordered network closeout without changing save/load hooks. Created: 2026-09-28.
// SPDX-License-Identifier: GPL-2.0-or-later
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, 't13-harness/gui/session/zz_t13.js'), 'utf8');
function harness(mode, controller) {
    let now = 0, exits = 0, speed = null;
    const context = {init() {}, onTick() {}, g_IsController: controller, g_Settings: {},
        g_SimState: {timeElapsed: 0, players: [{}, {state: 'active'}, {state: 'active'}]},
        Date: {now: () => now}, print() {},
        Engine: {ConfigDB_GetValue: () => mode, GuiInterfaceCall: () => true,
            SetSimRate: x => { speed = x; }, Exit: () => { ++exits; }}};
    vm.createContext(context); vm.runInContext(source, context);
    return {context, tick: t => { now = t; context.onTick(); }, exits: () => exits, speed: () => speed};
}
const host = harness('network', true), client = harness('network', false);
for (const h of [host, client]) { h.tick(0); h.tick(3000); assert.equal(h.exits(), 0); }
host.tick(3001); client.tick(3001);
assert.equal(host.exits(), 1); assert.equal(client.exits(), 0);
client.tick(10000); assert.equal(client.exits(), 0);
client.tick(10001); assert.equal(client.exits(), 1);
for (const mode of ['save', 'load']) {
    const h = harness(mode, true); h.context.init({}); h.tick(20000);
    assert.equal(h.speed(), 20); assert.equal(h.exits(), 0);
}
console.log('PASS: host closes before client, grace intervals, save/load hooks retain normal acceleration');
