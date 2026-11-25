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
    // including the automatically researched starting age. Each age's building requirement
    // (Barracks, Forge, Stable, SiegeWorkshop) is met by Petra's generic phase-up builder.
    gameState.phases = ['phase_epoch_bronze', 'phase_epoch_iron', 'phase_epoch_dark',
        'phase_epoch_medieval', 'phase_epoch_renaissance'].map(name => ({
        name,
        requirements: GetTechnologyBasicDataHelper(gameState.getTemplate(name)._template, 'epoch').reqs
    }));
    PetraBot.prototype.CustomInit.call(this, gameState);
    const manager = this.HQ.attackManager;
    const upstreamUpdate = manager.update;
    manager.update = function(state, queues, events)
    {
        // Bounded doctrine: defense remains active, offensive armies start in Iron Age.
        if (state.currentPhase() < 2)
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
