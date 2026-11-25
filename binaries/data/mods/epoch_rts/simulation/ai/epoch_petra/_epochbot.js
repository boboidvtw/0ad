// Purpose: Instance-scoped R28 Petra compatibility for Epoch. Created: 2026-09-22.
// SPDX-License-Identifier: GPL-2.0-or-later
import * as filters from "simulation/ai/common-api/filters.js";
import { PetraBot } from "simulation/ai/petra/_petrabot.js";

export function EpochPetraBot(settings)
{
    PetraBot.call(this, settings);
}
EpochPetraBot.prototype = Object.create(PetraBot.prototype);

EpochPetraBot.prototype.CustomInit = function(gameState)
{
    if (gameState.getPlayerCiv() != 'epoch')
        throw new Error('Epoch Petra requires the epoch civilization');
    // Override only this AI's GameState, leaving public Petra and other players intact.
    gameState.applyCiv = function(name)
    {
        return name.replace(/\{civ\}/g, 'epoch_rts');
    };
    // The CC offers only the next age (supersedes chain). Petra needs an ordered phase chain,
    // including the automatically researched first age (globalscripts/EpochAges.js). Ages after
    // the game's End Age are disabled, so the chain stops there. Building requirements (Storehouse,
    // Field, Barracks, Forge, Stable, SiegeWorkshop) are met by Petra's generic phase-up builder.
    const disabled = gameState.playerData?.disabledTechnologies || {};
    const lastAge = g_EpochAges.findIndex(age => disabled[age.tech]);
    gameState.phases = g_EpochAges.slice(0, lastAge == -1 ? undefined : lastAge).map(age => ({
        name: age.tech,
        requirements: GetTechnologyBasicDataHelper(gameState.getTemplate(age.tech)._template, 'epoch').reqs
    }));
    // Offensive armies start in Iron Age, or in the End Age when the game ends before Iron Age.
    const attackPhase = Math.min(EpochAgeIndex('iron'), gameState.phases.length - 1) + 1;
    PetraBot.prototype.CustomInit.call(this, gameState);
    const manager = this.HQ.attackManager;
    const upstreamUpdate = manager.update;
    manager.update = function(state, queues, events)
    {
        // Bounded doctrine: defense remains active until the attack phase.
        if (state.currentPhase() < attackPhase)
            return;
        upstreamUpdate.call(this, state, queues, events);
        for (const plans of Object.values(this.upcomingAttacks))
            for (const plan of plans)
            {
                if (plan.epochClasses || !plan.unitStat.MeleeInfantry)
                    continue;
                // This civ has combat-only melee infantry and slingers, no cavalry,
                // citizen-soldier workers, champions or siege. Reuse Petra plans
                // with actual M2 classes instead of changing simulation identities.
                for (const collection of Object.values(plan.unit))
                    collection.unregister();
                plan.unitStat = {
                    MeleeInfantry: {...plan.unitStat.MeleeInfantry, classes: ['Infantry+Swordsman']},
                    RangedInfantry: {...plan.unitStat.RangedInfantry, classes: ['Infantry+Slinger']}
                };
                plan.unit = {};
                plan.buildOrders = [];
                for (const [category, spec] of Object.entries(plan.unitStat))
                {
                    const units = plan.unitCollection.filter(filters.byClasses(spec.classes));
                    units.registerUpdates();
                    plan.unit[category] = units;
                    if (plan.canBuildUnits)
                        plan.buildOrders.push([0, spec.classes, units, spec, category]);
                }
                plan.epochClasses = true;
            }
    };
};
