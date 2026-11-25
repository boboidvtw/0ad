// Purpose: Real-engine fixtures for the 16-age epoch ladder; loaded only by its validation maps. Created: 2026-11-25.
// SPDX-License-Identifier: GPL-2.0-or-later
// Guards against: an age that skips its building gate or charge, completes early, unlocks the
// wrong content or bonus, shows out of order at the Civic Center, keeps a refund-less cancellation,
// or ignores the EpochStartAge / EpochEndAge game settings.
// Two maps load this script: the default range (Bronze start, Space end) and an early range
// (Prehistoric start, Renaissance end) preset in the map JSON. Fixtures set resources and advance
// queues directly (one ProgressTimeout = one second).
Trigger.prototype.EpochCheck = function(id, actual, expected)
{
	const normalize = value => value && typeof value == "object" ?
		(Array.isArray(value) ? value.map(normalize) : Object.fromEntries(Object.keys(value).sort().map(key => [key, normalize(value[key])]))) : value;
	const passed = JSON.stringify(normalize(actual)) === JSON.stringify(normalize(expected));
	this.epochResults.push({ "id": id, "actual": actual, "expected": expected, "passed": passed });
	if (!passed)
		throw new Error(id + ": " + JSON.stringify(actual) + " != " + JSON.stringify(expected));
};
Trigger.prototype.EpochFinish = function(exception)
{
	const result = "EPOCH_TEST_RESULT " + JSON.stringify({
		"passed": !exception && this.epochResults.every(result => result.passed),
		"kind": "real-engine age ladder fixtures",
		"checks": this.epochResults, "failure": exception ? String(exception) : null
	});
	for (let offset = 0; offset < result.length; offset += 4096)
		print(result.slice(offset, offset + 4096));
};
Trigger.prototype.EpochRun = function()
{
	this.epochResults = [];
	try
	{
		const fx = this.EpochFixtures();
		if (InitAttributes.settings.EpochStartAge == "prehistoric")
			this.EpochEarlyRange(fx);
		else
			this.EpochDefaultRange(fx);
		this.EpochFinish();
	}
	catch (e) { this.EpochFinish(e); }
};
Trigger.prototype.EpochFixtures = function()
{
	const Q = (e, iid) => Engine.QueryInterface(e, iid);
	const tm = Q(SYSTEM_ENTITY, IID_TemplateManager);
	const owned = p => Q(SYSTEM_ENTITY, IID_RangeManager).GetEntitiesByPlayer(p);
	const find = (p, name) => owned(p).find(e => tm.GetCurrentTemplateName(e) == name);
	const centre = find(1, "structures/epoch_rts/civil_centre");
	const queue = Q(centre, IID_ProductionQueue);
	const player = QueryPlayerIDInterface(1);
	const fx = {
		Q, tm, owned, find, centre, queue, player,
		"check": this.EpochCheck.bind(this),
		"manager": QueryPlayerIDInterface(1, IID_TechnologyManager),
		"zero": { "food": 0, "wood": 0, "stone": 0, "metal": 0 },
		// Copy: GetResourceCounts returns the live object, which would rewrite recorded evidence.
		"money": () => ({ ...player.GetResourceCounts() }),
		"fund": cost => player.SetResourceCounts({ "food": 0, "wood": 0, "stone": 0, "metal": 0, ...cost }),
		"add": (name, x, z) => { const e = Engine.AddEntity(name); Q(e, IID_Position).JumpTo(x, z); Q(e, IID_Ownership).SetOwner(1); return e; },
		"destroy": e => { Q(e, IID_Position)?.MoveOutOfWorld(); Engine.DestroyEntity(e); Engine.FlushDestroyedEntities(); },
		"research": tech => ProcessCommand(1, { "type": "research", "entity": centre, "template": tech }),
		"tick": n => { for (let i = 0; i < n; ++i) queue.ProgressTimeout(null, 0); },
		"offered": () => Q(centre, IID_Researcher).GetTechnologiesList().filter(Boolean),
		"round": value => Math.round(value * 1000) / 1000
	};
	return fx;
};
/**
 * Research one age through every gate. `age` holds its expected values from docs/empire-rts/age-ladder.md;
 * `next` is the following age (or undefined) for the out-of-order check.
 */
Trigger.prototype.EpochStepAge = function(fx, age, next, x)
{
	const { check, manager, queue, money, fund, add, destroy, research, tick, offered, zero } = fx;
	const id = age.tech.replace("phase_epoch_", "");
	const cost = { ...zero, ...age.cost };
	check("L01.offeredOnlyNext." + id, offered(), [age.tech]);
	if (next)
	{
		// A later age with its building present is still rejected before this age.
		const later = next.building && add("structures/epoch_rts/" + next.building, x, 420);
		fund(next.cost);
		const stock = money();
		research(next.tech);
		check("L02.outOfOrderRejected." + id, [queue.GetQueue().length, money()], [0, stock]);
		if (later)
			destroy(later);
	}
	let building;
	if (age.building)
	{
		fund(age.cost);
		research(age.tech);
		check("L03.needsBuilding." + id, [queue.GetQueue().length, money()], [0, cost]);
		const foundation = add("foundation|structures/epoch_rts/" + age.building, x, 360);
		research(age.tech);
		check("L03.foundationNotEnough." + id, queue.GetQueue().length, 0);
		destroy(foundation);
		building = add("structures/epoch_rts/" + age.building, x, 360);
	}
	for (const type of Object.keys(age.cost))
	{
		const poor = { ...cost, [type]: cost[type] - 1 };
		fx.player.SetResourceCounts(poor);
		research(age.tech);
		check("L04.poor." + id + "." + type, [queue.GetQueue().length, money()], [0, poor]);
	}
	if (building)
	{
		// Pre-start loss of the building cancels with a full refund and a translated notice.
		fund({ ...age.cost, "food": cost.food + 50 });
		ProcessCommand(1, { "type": "train", "entities": [fx.centre], "template": "units/epoch_rts/pioneer", "count": 1 });
		research(age.tech);
		check("L05.paid." + id, money(), zero);
		destroy(building);
		tick(16);
		check("L05.preStartLossCancels." + id, [queue.GetQueue().length, manager.IsTechnologyResearched(age.tech), money()], [0, false, cost]);
		const message = Researcher.prototype.EpochAgeCancelMessages[age.tech];
		check("L05.notice." + id, fx.Q(SYSTEM_ENTITY, IID_GuiInterface).GetTimeNotifications(1).some(n => n.message == message && n.translateMessage), true);
		add("structures/epoch_rts/" + age.building, x, 360);
	}
	// Full timed research: not done one second early, done on time, content unlocked.
	fund(age.cost);
	research(age.tech);
	check("L06.charged." + id, money(), zero);
	const unlocks = age.unlocks || [];
	check("L06.lockedDuring." + id, unlocks.map(name => manager.CanProduce(name)), unlocks.map(() => false));
	tick(age.seconds - 1);
	check("L06.notEarly." + id, manager.IsTechnologyResearched(age.tech), false);
	tick(1);
	check("L06.completeOnTime." + id, manager.IsTechnologyResearched(age.tech), true);
	check("L06.unlocked." + id, unlocks.map(name => manager.CanProduce(name)), unlocks.map(() => true));
};
Trigger.prototype.EpochDefaultRange = function(fx)
{
	const { Q, check, manager, find } = fx;
	const disabled = QueryPlayerIDInterface(1).GetDisabledTechnologies();
	check("L00.startAge", ["prehistoric", "stone", "copper", "bronze", "iron"].map(k => manager.IsTechnologyResearched("phase_epoch_" + k)),
		[true, true, true, true, false]);
	check("L00.noDisabledAges", g_EpochAges.filter(age => disabled[age.tech]).length, 0);
	check("L00.noStartAgeNotices", Q(SYSTEM_ENTITY, IID_GuiInterface).notifications.filter(n => n.type == "phase").length, 0);
	check("L00.bronzeContent", ["structures/epoch_rts/field", "structures/epoch_rts/barracks", "units/epoch_rts/slinger", "units/epoch_rts/spearman"]
		.map(name => manager.CanProduce(name)), [true, true, true, true]);

	const spear = find(1, "units/epoch_rts/spearman");
	const worker = find(1, "units/epoch_rts/pioneer");
	const hp = e => fx.round(Q(e, IID_Health).GetMaxHitpoints());
	const hack = () => fx.round(Q(spear, IID_Attack).GetAttackEffectsData("Melee").Damage.Hack);
	// Bonus checks use independently computed values (base x listed multipliers).
	const ladder = [
		{ "tech": "phase_epoch_iron", "building": "barracks", "cost": { "food": 400, "wood": 200, "metal": 100 }, "seconds": 60,
			"unlocks": ["units/epoch_rts/iron_swordsman", "structures/epoch_rts/forge"] },
		{ "tech": "phase_epoch_dark", "building": "forge", "cost": { "food": 600, "wood": 300, "metal": 200 }, "seconds": 75,
			"unlocks": ["structures/epoch_rts/stable", "units/epoch_rts/horseman"] },
		{ "tech": "phase_epoch_medieval", "building": "stable", "cost": { "food": 800, "wood": 400, "stone": 200, "metal": 300 }, "seconds": 90,
			"unlocks": ["structures/epoch_rts/siege_workshop", "units/epoch_rts/battering_ram", "units/epoch_rts/knight"] },
		{ "tech": "phase_epoch_renaissance", "building": "siege_workshop", "cost": { "food": 1000, "wood": 500, "stone": 300, "metal": 500 }, "seconds": 105,
			"unlocks": ["units/epoch_rts/bombard_packed"] },
		{ "tech": "phase_epoch_imperial", "cost": { "food": 1200, "wood": 600, "stone": 400, "metal": 600 }, "seconds": 120,
			"bonus": () => hp(spear), "expected": 110 },
		{ "tech": "phase_epoch_industrial", "cost": { "food": 1400, "wood": 700, "stone": 500, "metal": 700 }, "seconds": 120,
			"bonus": () => fx.round(Q(worker, IID_ResourceGatherer).GetGatherRates()["wood.tree"]), "expected": 0.805 },
		{ "tech": "phase_epoch_atomic_ww1", "cost": { "food": 1600, "wood": 800, "stone": 600, "metal": 800 }, "seconds": 120,
			"bonus": hack, "expected": 6.6 },
		{ "tech": "phase_epoch_atomic_ww2", "cost": { "food": 1800, "wood": 900, "stone": 700, "metal": 900 }, "seconds": 120,
			"bonus": () => hp(fx.centre), "expected": 2400 },
		{ "tech": "phase_epoch_atomic_modern", "cost": { "food": 2000, "wood": 1000, "stone": 800, "metal": 1000 }, "seconds": 120,
			"bonus": () => fx.round(Q(spear, IID_UnitMotion).GetWalkSpeed()), "expected": 8.8 },
		{ "tech": "phase_epoch_digital", "cost": { "food": 2200, "wood": 1100, "stone": 900, "metal": 1100 }, "seconds": 120,
			"bonus": () => fx.round(Q(worker, IID_Cost).GetBuildTime()), "expected": 13.5 },
		{ "tech": "phase_epoch_nano", "cost": { "food": 2400, "wood": 1200, "stone": 1000, "metal": 1200 }, "seconds": 120,
			"bonus": () => hp(spear), "expected": 121 },
		{ "tech": "phase_epoch_space", "cost": { "food": 2600, "wood": 1300, "stone": 1100, "metal": 1300 }, "seconds": 120,
			"bonus": hack, "expected": 7.26 }
	];
	let x = 300;
	ladder.forEach((age, i) => {
		const id = age.tech.replace("phase_epoch_", "");
		const before = age.bonus && age.bonus();
		this.EpochStepAge(fx, age, ladder[i + 1], x);
		if (age.bonus)
			check("L06.bonus." + id, [before == age.expected, age.bonus()], [false, age.expected]);
		x += 40;
	});
	check("L07.noAgeAfterLast", fx.offered(), []);
	check("L07.noPublicPhases", ["phase_town", "phase_city"].map(tech => manager.IsTechnologyResearched(tech)), [false, false]);
	this.EpochNewContent(fx);
};
Trigger.prototype.EpochEarlyRange = function(fx)
{
	const { check, manager } = fx;
	const disabled = QueryPlayerIDInterface(1).GetDisabledTechnologies();
	check("L10.startAge", [1, 2].map(p => ["prehistoric", "stone", "bronze"].map(k =>
		QueryPlayerIDInterface(p, IID_TechnologyManager).IsTechnologyResearched("phase_epoch_" + k))), [[true, false, false], [true, false, false]]);
	check("L10.endAgeDisablesLater", g_EpochAges.map(age => !!disabled[age.tech]), g_EpochAges.map((age, i) => i > EpochAgeIndex("renaissance")));
	check("L10.prehistoricContent", ["structures/epoch_rts/house", "structures/epoch_rts/storehouse", "structures/epoch_rts/field",
		"structures/epoch_rts/barracks", "units/epoch_rts/slinger", "units/epoch_rts/spearman"].map(name => manager.CanProduce(name)),
		[true, true, true, false, false, false]);
	const ladder = [
		{ "tech": "phase_epoch_stone", "building": "storehouse", "cost": { "food": 100, "wood": 50 }, "seconds": 30,
			"unlocks": ["structures/epoch_rts/barracks", "units/epoch_rts/slinger"] },
		{ "tech": "phase_epoch_copper", "building": "barracks", "cost": { "food": 200, "wood": 100 }, "seconds": 40,
			"unlocks": ["units/epoch_rts/spearman"] },
		{ "tech": "phase_epoch_bronze", "building": "field", "cost": { "food": 300, "wood": 150, "stone": 50 }, "seconds": 50 },
		{ "tech": "phase_epoch_iron", "building": "barracks", "cost": { "food": 400, "wood": 200, "metal": 100 }, "seconds": 60 }
	];
	let x = 300;
	ladder.slice(0, 3).forEach((age, i) => { this.EpochStepAge(fx, age, ladder[i + 1], x); x += 40; });
	// Fixture: grant Iron to Renaissance directly; the default map times them.
	for (const key of ["iron", "dark", "medieval", "renaissance"])
		manager.ResearchTechnology("phase_epoch_" + key);
	check("L11.nothingAfterEndAge", fx.offered(), []);
	fx.fund({ "food": 5000, "wood": 5000, "stone": 5000, "metal": 5000 });
	const stock = fx.money();
	fx.research("phase_epoch_imperial");
	check("L11.endAgeResearchRejected", [fx.queue.GetQueue().length, fx.money(), manager.IsTechnologyResearched("phase_epoch_imperial")], [0, stock, false]);
};
Trigger.prototype.EpochNewContent = function(fx)
{
	const { Q, check, tm, owned, add, player } = fx;
	// Costs and stats from the age table; trained at the right building.
	for (const [name, hp, seconds, cost, pop] of [
		["units/epoch_rts/horseman", 160, 30, [100, 0, 0, 40], 1],
		["units/epoch_rts/knight", 260, 40, [150, 0, 0, 100], 1],
		["units/epoch_rts/battering_ram", 400, 45, [0, 300, 0, 100], 3],
		["units/epoch_rts/bombard_packed", 300, 50, [0, 250, 100, 200], 3]])
	{
		const t = tm.GetTemplate(name);
		check("L08.template." + name, [+t.Health.Max, +t.Cost.BuildTime, ["food", "wood", "stone", "metal"].map(r => +t.Cost.Resources[r]), +t.Cost.Population],
			[hp, seconds, cost, pop]);
		check("L08.noLeak." + name, !!(t.Auras || t.Promotion || t.Looter || t.Builder || t.ResourceGatherer || t.Garrisonable || t.Attack?.Capture || t.Attack?.Slaughter), false);
	}
	for (const [name, hp, seconds, wood, stone] of [["stable", 600, 50, 200, 50], ["siege_workshop", 700, 60, 300, 100]])
	{
		const t = tm.GetTemplate("structures/epoch_rts/" + name);
		check("L08.building." + name, [+t.Health.Max, +t.Cost.BuildTime, +t.Cost.Resources.wood, +t.Cost.Resources.stone], [hp, seconds, wood, stone]);
		check("L08.noLeakBuilding." + name, !!(t.Attack || t.Capturable || t.GarrisonHolder || t.TerritoryDecay || t.Auras || t.Looter || t.Researcher), false);
	}
	check("L08.bombardPacks", [tm.GetTemplate("units/epoch_rts/bombard_packed").Pack.Entity, tm.GetTemplate("units/epoch_rts/bombard_unpacked").Pack.Entity],
		["units/epoch_rts/bombard_unpacked", "units/epoch_rts/bombard_packed"]);
	check("L08.pioneerBuilds", ["stable", "siege_workshop"].map(name => tm.GetTemplate("units/epoch_rts/pioneer").Builder.Entities._string.includes("structures/epoch_rts/" + name)), [true, true]);
	const stable = add("structures/epoch_rts/stable", 260, 440);
	const workshop = add("structures/epoch_rts/siege_workshop", 330, 460);
	// Digital Age (researched above) trains units 10% faster: 30/40/45/50 s become 27/36/40.5/45 s.
	for (const [building, name, seconds] of [[stable, "units/epoch_rts/horseman", 27], [stable, "units/epoch_rts/knight", 36],
		[workshop, "units/epoch_rts/battering_ram", 41], [workshop, "units/epoch_rts/bombard_packed", 45]])
	{
		player.SetResourceCounts({ "food": 1000, "wood": 1000, "stone": 1000, "metal": 1000 });
		const before = owned(1).filter(e => tm.GetCurrentTemplateName(e) == name).length;
		ProcessCommand(1, { "type": "train", "entities": [building], "template": name, "count": 1 });
		const bq = Q(building, IID_ProductionQueue);
		for (let i = 0; i < seconds - 1; ++i) bq.ProgressTimeout(null, 0);
		check("L09.notEarly." + name, bq.GetQueue().length, 1);
		bq.ProgressTimeout(null, 0);
		check("L09.trained." + name, owned(1).filter(e => tm.GetCurrentTemplateName(e) == name).length, before + 1);
	}
};
Engine.QueryInterface(SYSTEM_ENTITY, IID_Trigger).DoAfterDelay(1, "EpochRun", {});
