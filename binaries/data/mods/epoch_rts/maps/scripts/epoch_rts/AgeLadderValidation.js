// Purpose: Real-engine fixtures for the five-age epoch ladder; loaded only by its validation map. Created: 2026-11-25.
// SPDX-License-Identifier: GPL-2.0-or-later
// Guards against: an age that skips its building gate or charge, completes early, unlocks the
// wrong content, shows out of order at the Civic Center, or keeps a refund-less cancellation.
// Fixtures set resources and advance queues directly (one ProgressTimeout = one second).
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
	try { this.EpochAgeLadder(); this.EpochFinish(); }
	catch (e) { this.EpochFinish(e); }
};
Trigger.prototype.EpochAgeLadder = function()
{
	const Q = (e, iid) => Engine.QueryInterface(e, iid);
	const check = this.EpochCheck.bind(this);
	const tm = Q(SYSTEM_ENTITY, IID_TemplateManager);
	const owned = p => Q(SYSTEM_ENTITY, IID_RangeManager).GetEntitiesByPlayer(p);
	const find = (p, name) => owned(p).find(e => tm.GetCurrentTemplateName(e) == name);
	const centre = find(1, "structures/epoch_rts/civil_centre");
	const queue = Q(centre, IID_ProductionQueue);
	const player = QueryPlayerIDInterface(1);
	const manager = QueryPlayerIDInterface(1, IID_TechnologyManager);
	// Copy: GetResourceCounts returns the live object, which would rewrite recorded evidence.
	const money = () => ({ ...player.GetResourceCounts() });
	const fund = cost => player.SetResourceCounts({ "food": 0, "wood": 0, "stone": 0, "metal": 0, ...cost });
	const add = (name, x, z) => { const e = Engine.AddEntity(name); Q(e, IID_Position).JumpTo(x, z); Q(e, IID_Ownership).SetOwner(1); return e; };
	const destroy = e => { Q(e, IID_Position)?.MoveOutOfWorld(); Engine.DestroyEntity(e); Engine.FlushDestroyedEntities(); };
	const research = tech => ProcessCommand(1, { "type": "research", "entity": centre, "template": tech });
	const tick = n => { for (let i = 0; i < n; ++i) queue.ProgressTimeout(null, 0); };
	const offered = () => Q(centre, IID_Researcher).GetTechnologiesList().filter(Boolean);
	const zero = { "food": 0, "wood": 0, "stone": 0, "metal": 0 };

	// Expected values come from the age table in docs/empire-rts/age-ladder.md.
	const ladder = [
		{ "tech": "phase_epoch_iron", "building": "barracks", "cost": { "food": 400, "wood": 200, "metal": 100 }, "seconds": 60,
			"unlocks": ["units/epoch_rts/iron_swordsman", "structures/epoch_rts/forge"] },
		{ "tech": "phase_epoch_dark", "building": "forge", "cost": { "food": 600, "wood": 300, "metal": 200 }, "seconds": 75,
			"unlocks": ["structures/epoch_rts/stable", "units/epoch_rts/horseman"] },
		{ "tech": "phase_epoch_medieval", "building": "stable", "cost": { "food": 800, "wood": 400, "stone": 200, "metal": 300 }, "seconds": 90,
			"unlocks": ["structures/epoch_rts/siege_workshop", "units/epoch_rts/battering_ram", "units/epoch_rts/knight"] },
		{ "tech": "phase_epoch_renaissance", "building": "siege_workshop", "cost": { "food": 1000, "wood": 500, "stone": 300, "metal": 500 }, "seconds": 105,
			"unlocks": ["units/epoch_rts/bombard_packed"] }
	];
	check("L00.startAge", [manager.IsTechnologyResearched("phase_epoch_bronze"), manager.IsTechnologyResearched("phase_epoch_iron")], [true, false]);
	check("L00.allLockedAtStart", ladder.flatMap(age => age.unlocks).map(name => manager.CanProduce(name)), ladder.flatMap(age => age.unlocks).map(() => false));
	let x = 300;
	ladder.forEach((age, i) => {
		const id = age.tech.replace("phase_epoch_", "");
		const cost = { ...zero, ...age.cost };
		check("L01.offeredOnlyNext." + id, offered(), [age.tech]);
		if (ladder[i + 1])
		{
			// A later age with its building present is still rejected before this age.
			const later = add("structures/epoch_rts/" + ladder[i + 1].building, x, 420);
			fund(ladder[i + 1].cost);
			const stock = money();
			research(ladder[i + 1].tech);
			check("L02.outOfOrderRejected." + id, [queue.GetQueue().length, money()], [0, stock]);
			destroy(later);
		}
		fund(age.cost);
		research(age.tech);
		check("L03.needsBuilding." + id, [queue.GetQueue().length, money()], [0, cost]);
		const foundation = add("foundation|structures/epoch_rts/" + age.building, x, 360);
		research(age.tech);
		check("L03.foundationNotEnough." + id, queue.GetQueue().length, 0);
		destroy(foundation);
		const building = add("structures/epoch_rts/" + age.building, x, 360);
		for (const type of Object.keys(age.cost))
		{
			const poor = { ...cost, [type]: cost[type] - 1 };
			player.SetResourceCounts(poor);
			research(age.tech);
			check("L04.poor." + id + "." + type, [queue.GetQueue().length, money()], [0, poor]);
		}
		// Pre-start loss of the building cancels with a full refund and a translated notice.
		fund({ ...age.cost, "food": cost.food + 50 });
		ProcessCommand(1, { "type": "train", "entities": [centre], "template": "units/epoch_rts/pioneer", "count": 1 });
		research(age.tech);
		check("L05.paid." + id, money(), zero);
		destroy(building);
		tick(16);
		check("L05.preStartLossCancels." + id, [queue.GetQueue().length, manager.IsTechnologyResearched(age.tech), money()], [0, false, cost]);
		const message = Researcher.prototype.EpochAgeCancelMessages[age.tech];
		check("L05.notice." + id, Q(SYSTEM_ENTITY, IID_GuiInterface).GetTimeNotifications(1).some(n => n.message == message && n.translateMessage), true);
		// Full timed research: not done one second early, done on time, content unlocked.
		add("structures/epoch_rts/" + age.building, x, 360);
		research(age.tech);
		check("L06.charged." + id, money(), zero);
		check("L06.lockedDuring." + id, age.unlocks.map(name => manager.CanProduce(name)), age.unlocks.map(() => false));
		tick(age.seconds - 1);
		check("L06.notEarly." + id, manager.IsTechnologyResearched(age.tech), false);
		tick(1);
		check("L06.completeOnTime." + id, manager.IsTechnologyResearched(age.tech), true);
		check("L06.unlocked." + id, age.unlocks.map(name => manager.CanProduce(name)), age.unlocks.map(() => true));
		x += 40;
	});
	check("L07.noAgeAfterLast", offered(), []);
	check("L07.noPublicPhases", ["phase_town", "phase_city"].map(tech => manager.IsTechnologyResearched(tech)), [false, false]);

	// New content: costs and stats from the age table; trained at the right building.
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
	for (const [building, name, seconds] of [[stable, "units/epoch_rts/horseman", 30], [stable, "units/epoch_rts/knight", 40],
		[workshop, "units/epoch_rts/battering_ram", 45], [workshop, "units/epoch_rts/bombard_packed", 50]])
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
