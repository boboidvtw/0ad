// Purpose: Instance-scoped R28 Petra compatibility for Epoch. Created: 2026-09-22.
// SPDX-License-Identifier: GPL-2.0-or-later
import * as filters from "simulation/ai/common-api/filters.js";
import { PetraBot } from "simulation/ai/petra/_petrabot.js";
import { ResearchPlan } from "simulation/ai/petra/queueplanResearch.js";

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
    this.HQ.researchManager.checkPhase = epochCheckPhase;
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

// Petra's own checkPhase picks its threshold by the age's index in the chain (popPhase2 for the
// second age, workPhase3 for the third, workPhase4 after). With 16 ages a Bronze start is already
// the fourth, so Iron Age (and from a Prehistoric start, Copper Age onward) waited for workPhase3/4
// workers instead of popPhase2. Thresholds follow the age's place on the ladder instead: up to
// Iron Age (the old second age) popPhase2, Dark Age workPhase3, later ages workPhase4. Apart from
// that and the priority below, identical to R28 ResearchManager.checkPhase.
const epochIronIndex = EpochAgeIndex('iron');
const epochDarkIndex = EpochAgeIndex('dark');
const epochLateAgePriority = 50;
function epochCheckPhase(gameState, queues)
{
    if (queues.majorTech.hasQueuedUnits() || queues.civilCentre.hasQueuedUnits() || queues.wonder.hasQueuedUnits())
        return;
    const current = gameState.currentPhase();
    const nextPhaseName = gameState.getPhaseName(current + 1);
    if (!nextPhaseName)
        return;
    // The chain starts at Prehistoric Age, so the next age's ladder index equals current.
    const economy = this.Config.Economy, HQ = gameState.ai.HQ;
    const ready = current <= epochIronIndex ? HQ.getAccountedPopulation(gameState) >= economy.popPhase2 :
        current == epochDarkIndex ? HQ.getAccountedWorkers(gameState) > economy.workPhase3 :
            HQ.getAccountedWorkers(gameState) > economy.workPhase4;
    if (!ready || !gameState.hasResearchers(nextPhaseName, true))
        return;
    HQ.phasing = current + 1;
    // Balance: Petra's Attack queue has priority 90 and majorTech 700, so after Iron Age the AI
    // saved for Dark Age to Renaissance while its first army waited, and games vs an idle player
    // ran 20.5-21 minutes (target 10-20). Ages after Iron Age queue below the army instead.
    const priority = current > epochIronIndex ? epochLateAgePriority : gameState.ai.Config.priorities.majorTech;
    gameState.ai.queueManager.changePriority('majorTech', priority);
    queues.majorTech.addPlan(new ResearchPlan(gameState, nextPhaseName, true));
}
