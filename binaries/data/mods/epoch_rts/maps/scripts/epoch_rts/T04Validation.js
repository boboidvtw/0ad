// Purpose: Real-engine T04 integration fixtures; loaded only by the validation map. Created: 2026-09-07.
// SPDX-License-Identifier: GPL-2.0-or-later
// Fixtures may set resources, entities and work time; the final walking/gathering/building
// section uses normal commands and the real simulation clock. This is not a full match test.
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
		"kind": "real-engine integration fixtures and timed command flows",
		"checks": this.epochResults, "failure": exception ? String(exception) : null
	});
    // Engine print truncates large messages. Emit bounded chunks on the same stream.
    for (let offset = 0; offset < result.length; offset += 4096)
        print(result.slice(offset, offset + 4096));
};
Trigger.prototype.EpochRun = function()
{
	try { this.EpochFixtures(); }
	catch (exception) { this.EpochFinish(exception); }
};
Trigger.prototype.EpochFixtures = function()
{
	this.epochResults = [];
	const Q = (ent, iid) => Engine.QueryInterface(ent, iid);
	const tm = Q(SYSTEM_ENTITY, IID_TemplateManager);
	const entities = player => Q(SYSTEM_ENTITY, IID_RangeManager).GetEntitiesByPlayer(player);
	const find = (player, name) => entities(player).filter(ent => tm.GetCurrentTemplateName(ent) == name);
	const player = QueryPlayerIDInterface(1);
	const money = () => player.GetResourceCounts();
	const fund = (food = 10000, wood = 10000, stone = 10000, metal = 10000) => player.SetResourceCounts({ food, wood, stone, metal });
	const destroy = ent => { Q(ent, IID_Position)?.MoveOutOfWorld(); Engine.DestroyEntity(ent); Engine.FlushDestroyedEntities(); };
	const add = (name, x, z, owner = 1) => {
		const ent = Engine.AddEntity(name);
		Q(ent, IID_Position).JumpTo(x, z);
		Q(ent, IID_Ownership).SetOwner(owner);
		return ent;
	};
	for (const p of [1, 2])
	{
		this.EpochCheck("E01.start." + p, [find(p, "structures/epoch_rts/civil_centre").length, find(p, "units/epoch_rts/pioneer").length, find(p, "units/epoch_rts/spearman").length], [1, 6, 2]);
		this.EpochCheck("E01.resources." + p, QueryPlayerIDInterface(p).GetResourceCounts(), { "food": 300, "wood": 250, "stone": 100, "metal": 0 });
		this.EpochCheck("E01.population." + p, [QueryPlayerIDInterface(p).GetPopulationCount(), QueryPlayerIDInterface(p).GetPopulationLimit(), QueryPlayerIDInterface(p).GetMaxPopulation()], [8, 20, 100]);
		this.EpochCheck("E01.phase." + p, [QueryPlayerIDInterface(p, IID_TechnologyManager).IsTechnologyResearched("phase_epoch_bronze"), QueryPlayerIDInterface(p, IID_TechnologyManager).IsTechnologyResearched("phase_epoch_iron")], [true, false]);
	}
	this.worker = find(1, "units/epoch_rts/pioneer")[0];
	this.centre = find(1, "structures/epoch_rts/civil_centre")[0];
	const worker = this.worker;
	const centre = this.centre;
const centrePos = Q(centre, IID_Position).GetPosition2D();
	ProcessCommand(1, { "type": "delete-entities", "entities": [centre] });
	Engine.FlushDestroyedEntities();
	this.EpochCheck("E11.centreUndeletable", !!Q(centre, IID_Health), true);
	for (const p of [1, 2])
	{
		const base = Q(find(p, "structures/epoch_rts/civil_centre")[0], IID_Position).GetPosition2D();
		const counts = {};
		for (const ent of entities(0))
		{
			const pos = Q(ent, IID_Position)?.GetPosition2D();
			const supply = Q(ent, IID_ResourceSupply);
			if (!pos || !supply || Math.hypot(pos.x - base.x, pos.y - base.y) > 160)
				continue;
			const type = supply.GetType().generic;
			counts[type] = (counts[type] || 0) + 1;
		}
		this.EpochCheck("E02.resources." + p, [counts.wood >= 30, counts.food >= 5, counts.stone >= 1, counts.metal >= 1], [true, true, true, true]);
	}
	this.EpochCheck("E11.builderWhitelist", Q(worker, IID_Builder).GetEntitiesList(), ["house", "storehouse", "barracks", "field", "forge"].map(id => "structures/epoch_rts/" + id));
	for (const [id, hp, seconds, cost, speed] of [
		["pioneer", 40, 15, [50, 0, 0, 0], 9], ["spearman", 100, 20, [60, 20, 0, 0], 8],
		["slinger", 60, 25, [40, 40, 0, 0], 9], ["iron_swordsman", 140, 30, [80, 0, 0, 40], 9]])
	{
		const t = tm.GetTemplate("units/epoch_rts/" + id);
		this.EpochCheck("E07.template." + id, [+t.Health.Max, +t.Cost.BuildTime, ["food", "wood", "stone", "metal"].map(r => +t.Cost.Resources[r]), +t.UnitMotion.WalkSpeed], [hp, seconds, cost, speed]);
		this.EpochCheck("E11.noLeakedUnit." + id, !!(t.Auras || t.Promotion || t.Looter || t.Attack.Capture || t.Attack.Slaughter || (id != "pioneer" && (t.Builder || t.ResourceGatherer))), false);
		this.EpochCheck("E11.noCriticalUnit." + id, GetIdentityClasses(t.Identity).includes("ConquestCritical"), false);
	}
	for (const [id, hp, seconds, w, s] of [["house", 300, 25, 50, 0], ["storehouse", 400, 30, 100, 0], ["barracks", 600, 50, 150, 50], ["field", 200, 30, 60, 0], ["forge", 500, 50, 150, 100], ["civil_centre", 1000, 50, 0, 0]])
	{
		const t = tm.GetTemplate("structures/epoch_rts/" + id);
		this.EpochCheck("E04.template." + id, [+t.Health.Max, +t.Cost.BuildTime, +t.Cost.Resources.wood, +t.Cost.Resources.stone], [hp, seconds, w, s]);
		this.EpochCheck("E11.noLeakedBuilding." + id, !!(t.Attack || t.Capturable || t.GarrisonHolder || t.TerritoryDecay || t.Auras || t.Looter), false);
		this.EpochCheck("E11.researchWhitelist." + id, t.Researcher?.Technologies?._string || "", id == "civil_centre" ? "phase_epoch_iron" : id == "forge" ? "epoch_forged_weapons" : "");
        this.EpochCheck("E11.critical." + id, GetIdentityClasses(t.Identity).includes("ConquestCritical"), id == "civil_centre");
	}
	this.EpochCheck("E03.rates", Q(worker, IID_ResourceGatherer).GetGatherRates(), { "food.fruit": 1, "food.grain": 0.5, "wood.tree": 0.7, "stone.rock": 0.35, "metal.ore": 0.35 });
	const store = add("structures/epoch_rts/storehouse", 330, 340);
	for (const target of [centre, store])
		for (const type of ["food", "wood", "stone", "metal"])
		{
			fund(0, 0, 0, 0);
			const gatherer = Q(worker, IID_ResourceGatherer);
			this.EpochCheck("E03.capacity." + target + type, gatherer.GetCapacity(type), 10);
			gatherer.GiveResources([{ "type": type, "amount": 10 }]);
			this.EpochCheck("E03.carryNotStock." + target + type, money()[type], 0);
			gatherer.CommitResources(target);
			this.EpochCheck("E03.deposit." + target + type, money()[type], 10);
		}
	destroy(store);
	// Inspect real construction commands, including rejected commands that must not pay.
	Q(SYSTEM_ENTITY, IID_RangeManager).ExploreMap(1);
	const build = (id, x = 360, z = 350, builder = worker) => {
		const before = new Set(entities(1));
		ProcessCommand(1, { "type": "construct", "entities": [builder], "template": "structures/epoch_rts/" + id, "x": x, "z": z, "angle": 0, "autorepair": false, "queued": false });
		Engine.FlushDestroyedEntities();
		return entities(1).find(ent => !before.has(ent) && Q(ent, IID_Foundation));
	};
	for (const [id, w, s] of [["house", 50, 0], ["storehouse", 100, 0], ["barracks", 150, 50], ["field", 60, 0]])
	{
		fund(0, w - 1, s, 0);
		this.EpochCheck("E06.buildPoor." + id, !!build(id), false);
		this.EpochCheck("E06.buildPoorUncharged." + id, money().wood, w - 1);
		fund(0, w, s, 0);
		const foundation = build(id);
		this.EpochCheck("E06.buildExact." + id, !!foundation, true);
		this.EpochCheck("E06.buildPaid." + id, [money().wood, money().stone], [0, 0]);
		this.EpochCheck("E04.foundationNoPopulation." + id, player.GetPopulationLimit(), 20);
		destroy(foundation);
		this.EpochCheck("E09.unstartedRefund." + id, [money().wood, money().stone], [w, s]);
	}
	fund();
	for (const id of ["civil_centre", "forge"])
	{
		const before = JSON.stringify(money());
		this.EpochCheck("E11.illegalConstruction." + id, !!build(id), false);
		this.EpochCheck("E11.illegalUncharged." + id, JSON.stringify(money()), before);
	}

	const enemy = Q(find(2, "structures/epoch_rts/civil_centre")[0], IID_Position).GetPosition2D();
	for (const [label, x, z, builder] of [
		["overlapBuilding", centrePos.x, centrePos.y, worker],
		["enemyTerritory", enemy.x + 60, enemy.y + 60, worker],
		["militaryBuilder", 360, 350, find(1, "units/epoch_rts/spearman")[0]],
		["overlapUnit", Q(worker, IID_Position).GetPosition2D().x, Q(worker, IID_Position).GetPosition2D().y, worker]])
	{
		const before = JSON.stringify(money());
		this.EpochCheck("E04.reject." + label, !!build("house", x, z, builder), false);
		this.EpochCheck("E04.rejectUncharged." + label, JSON.stringify(money()), before);
	}
	fund(0, 150, 49, 0);
	this.EpochCheck("E06.barracksMissingStone", !!build("barracks"), false);
	this.EpochCheck("E06.barracksMissingStoneUncharged", [money().wood, money().stone], [150, 49]);
	for (const lethal of [false, true])
	{
		fund(0, 150, 50, 0);
		const foundation = build("barracks");
		const f = Q(foundation, IID_Foundation);
		f.AddBuilder(worker);
		Q(foundation, IID_Health).SetHitpoints(240);
		f.Build(worker, 0); // Commit and remember precisely 40% highest progress.
		this.EpochCheck("E09.progress." + lethal, f.maxProgress, 0.4);
		Q(foundation, IID_Health).Reduce(100);
		if (lethal) { Q(foundation, IID_Health).Kill(); Engine.FlushDestroyedEntities(); }
		else destroy(foundation);
		this.EpochCheck("E09.highestProgressRefund." + lethal, [money().wood, money().stone], [90, 30]);
	}
	const barracks = add("structures/epoch_rts/barracks", 360, 350);
	this.EpochCheck("E11.trainerWhitelist", Q(barracks, IID_Trainer).GetEntitiesList(), ["spearman", "slinger", "iron_swordsman"].map(id => "units/epoch_rts/" + id));
	for (const [id, place, f, w, secs] of [["pioneer", centre, 50, 0, 15], ["spearman", barracks, 60, 20, 20], ["slinger", barracks, 40, 40, 25]])
	{
		const queue = Q(place, IID_ProductionQueue);
		const command = { "type": "train", "entities": [place], "template": "units/epoch_rts/" + id, "count": 1 };
		fund(f - 1, w, 0, 0); ProcessCommand(1, command);
		this.EpochCheck("E06.trainPoor." + id, [queue.GetQueue().length, money().food], [0, f - 1]);

		if (w)
		{
			fund(f, w - 1, 0, 0); ProcessCommand(1, command);
			this.EpochCheck("E06.trainMissingWood." + id, [queue.GetQueue().length, money().wood], [0, w - 1]);
		}
		fund(f, w, 0, 0); ProcessCommand(1, command);
		this.EpochCheck("E07.queuePaid." + id, [queue.GetQueue().length, money().food, money().wood], [1, 0, 0]);
		queue.ResetQueue();
		this.EpochCheck("E07.cancelQueued." + id, [money().food, money().wood, player.GetPopulationCount()], [f, w, 8]);
		ProcessCommand(1, command); queue.ProgressTimeout(null, 0);
		this.EpochCheck("E07.reserved." + id, player.GetPopulationCount(), 9);
		queue.ResetQueue();
		this.EpochCheck("E07.cancelStarted." + id, [money().food, money().wood, player.GetPopulationCount()], [f, w, 8]);
		ProcessCommand(1, command);
		const original = new Set(entities(1));
		for (let second = 0; second < secs - 1; ++second) queue.ProgressTimeout(null, 0);
		this.EpochCheck("E07.notEarly." + id, entities(1).filter(ent => !original.has(ent)).length, 0);
		queue.ProgressTimeout(null, 0);
		const spawned = entities(1).filter(ent => !original.has(ent));
		this.EpochCheck("E07.completed." + id, [queue.GetQueue().length, spawned.length, player.GetPopulationCount()], [0, 1, 9]);
		destroy(spawned[0]);
	}
	fund();
	const tq = Q(barracks, IID_ProductionQueue);
	const train = (count = 1) => ProcessCommand(1, { "type": "train", "entities": [barracks], "template": "units/epoch_rts/spearman", count });
	player.SetMaxPopulation(8); train(); tq.ProgressTimeout(null, 0);
	this.EpochCheck("E08.fullWait", [player.GetPopulationCount(), tq.GetQueue().length], [8, 1]);
	player.SetMaxPopulation(100);
	const house = add("structures/epoch_rts/house", 320, 360);
	this.EpochCheck("E08.houseCapacity", player.GetPopulationLimit(), 30);
	tq.ProgressTimeout(null, 0);
	this.EpochCheck("E08.resumeReservation", player.GetPopulationCount(), 9);
	// Reserve remaining free population as another trainer would, then lose capacity.
	player.TryReservePopulationSlots(21); destroy(house);
	this.EpochCheck("E08.overCap", [player.GetPopulationCount(), player.GetPopulationLimit()], [30, 20]);
	const original = new Set(entities(1));
	for (let i = 0; i < 20; ++i) tq.ProgressTimeout(null, 0);
	this.EpochCheck("E08.reservedFinishesOverCap", entities(1).filter(ent => !original.has(ent)).length, 1);
	for (const ent of entities(1).filter(ent => !original.has(ent))) destroy(ent);
	player.UnReservePopulationSlots(21);
	player.SetMaxPopulation(100);
	const houses = Array.from({ length: 9 }, (_, i) => add("structures/epoch_rts/house", 290 + i * 17, 290));
	this.EpochCheck("E08.hardCap", player.GetPopulationLimit(), 100);
	for (const ent of houses) destroy(ent);

	// Two independent trainers compete for one remaining slot.
	const secondBarracks = add("structures/epoch_rts/barracks", 410, 350);
	const secondQueue = Q(secondBarracks, IID_ProductionQueue);
	player.SetMaxPopulation(9); fund(); train();
	ProcessCommand(1, { "type": "train", "entities": [secondBarracks], "template": "units/epoch_rts/spearman", "count": 1 });
	tq.ProgressTimeout(null, 0); secondQueue.ProgressTimeout(null, 0);
	this.EpochCheck("E10.competingReservations", player.GetPopulationCount(), 9);
	tq.ResetQueue(); secondQueue.ProgressTimeout(null, 0);
	this.EpochCheck("E10.competingResume", player.GetPopulationCount(), 9);
	secondQueue.ResetQueue(); destroy(secondBarracks); player.SetMaxPopulation(100);
	// Fill actual native footprint spawn points with equal-sized blockers.
	const probe = Engine.AddEntity("units/epoch_rts/spearman");
	const blockers = [];
	for (let i = 0; i < 256; ++i)
	{
		const pos = Q(barracks, IID_Footprint).PickSpawnPoint(probe);
		if (pos.y < 0) break;
		blockers.push(add("units/epoch_rts/spearman", pos.x, pos.z, 0));
	}
	this.EpochCheck("E10.spawnBlockedFixture", Q(barracks, IID_Footprint).PickSpawnPoint(probe).y < 0, true);
	fund(120, 40, 0, 0); train(2);
	for (let i = 0; i < 40; ++i) tq.ProgressTimeout(null, 0);
	this.EpochCheck("E10.blockedNoSpawn", [tq.GetQueue().length, player.GetPopulationCount(), money().food], [1, 10, 0]);
	const beforePartial = new Set(entities(1));
	destroy(blockers.shift()); tq.ProgressTimeout(null, 0);
	const partial = entities(1).filter(ent => !beforePartial.has(ent));
	this.EpochCheck("E10.partialBatchSpawn", partial.length, 1);
	tq.ResetQueue();
	this.EpochCheck("E10.partialBatchRefund", [money().food, money().wood, player.GetPopulationCount()], [60, 20, 9]);
	destroy(partial[0]);
	for (const ent of blockers) destroy(ent);
	destroy(probe);
	fund(120, 40, 0, 0); train(2); tq.ProgressTimeout(null, 0); tq.ResetQueue();
	this.EpochCheck("E10.batchCancel", [money().food, money().wood, player.GetPopulationCount()], [120, 40, 8]);
	train(2); tq.ProgressTimeout(null, 0); destroy(barracks);
	this.EpochCheck("E09.trainerDestroyed", [money().food, money().wood, player.GetPopulationCount()], [120, 40, 8]);
	const field = add("structures/epoch_rts/field", 360, 350);
	const supply = Q(field, IID_ResourceSupply);
	const workers = find(1, "units/epoch_rts/pioneer");
	this.EpochCheck("E05.gathererSlots", workers.map(ent => supply.AddGatherer(ent)), [true, true, true, true, true, false]);
	this.EpochCheck("E05.noDiminishing", supply.GetDiminishingReturns(), 1);
	supply.TakeResources(100000);
	this.EpochCheck("E05.infiniteFood", supply.GetCurrentAmount() == Infinity, true);
	for (const ent of workers) supply.RemoveGatherer(ent);
	destroy(field);
	// Real command flow: walking and harvesting each resource on the actual map.
	fund(300, 250, 100, 0);
	this.epochJobs = ["food", "wood", "stone", "metal"];
	this.epochJobIndex = 0;
	this.epochGatherPlayer = 1;
	this.epochFirstWorker = this.worker;
	this.EpochStartGather();
};
Trigger.prototype.EpochStartGather = function()
{
	const Q = (ent, iid) => Engine.QueryInterface(ent, iid);
	const type = this.epochJobs[this.epochJobIndex];
	const pos = Q(this.worker, IID_Position).GetPosition2D();
	const targets = Q(SYSTEM_ENTITY, IID_RangeManager).GetEntitiesByPlayer(0).filter(ent => Q(ent, IID_ResourceSupply)?.GetType().generic == type);
	targets.sort((a, b) => {
		const pa = Q(a, IID_Position).GetPosition2D(), pb = Q(b, IID_Position).GetPosition2D();
		return Math.hypot(pa.x - pos.x, pa.y - pos.y) - Math.hypot(pb.x - pos.x, pb.y - pos.y);
	});
	this.epochStockBefore = QueryPlayerIDInterface(this.epochGatherPlayer).GetResourceCounts()[type];
	this.epochWait = 0;
	this.epochSawCarried = false;
	ProcessCommand(this.epochGatherPlayer, { "type": "gather", "entities": [this.worker], "target": targets[0], "queued": false });
	this.DoAfterDelay(1000, "EpochPollGather", {});
};
Trigger.prototype.EpochPollGather = function()
{
	try
	{
		const type = this.epochJobs[this.epochJobIndex];
		const stock = QueryPlayerIDInterface(this.epochGatherPlayer).GetResourceCounts()[type];
		const gatherer = Engine.QueryInterface(this.worker, IID_ResourceGatherer);
		if (gatherer.IsCarrying(type) && stock == this.epochStockBefore)
			this.epochSawCarried = true;
		if (stock > this.epochStockBefore)
		{
			this.EpochCheck("E03.timedCarrying." + this.epochGatherPlayer + "." + type, this.epochSawCarried, true);
			this.EpochCheck("E03.timedDeposit." + this.epochGatherPlayer + "." + type, stock - this.epochStockBefore, 10);
			ProcessCommand(this.epochGatherPlayer, { "type": "stop", "entities": [this.worker], "queued": false });
			gatherer.DropResources();
			if (++this.epochJobIndex < this.epochJobs.length)
				this.EpochStartGather();
			else if (this.epochGatherPlayer == 1)
			{
				this.epochGatherPlayer = 2;
				this.epochJobIndex = 0;
				this.worker = Engine.QueryInterface(SYSTEM_ENTITY, IID_RangeManager).GetEntitiesByPlayer(2).find(ent => Engine.QueryInterface(ent, IID_ResourceGatherer));
				this.EpochStartGather();
			}
			else
			{
				this.worker = this.epochFirstWorker;
				this.epochGatherPlayer = 1;
				this.EpochTimedBuild();
			}
			return;
		}
		if (++this.epochWait > 180)
			throw new Error("Timed gather/deposit timeout: " + type + "; state=" + Engine.QueryInterface(this.worker, IID_UnitAI).GetCurrentState());
		this.DoAfterDelay(1000, "EpochPollGather", {});
	}
	catch (exception) { this.EpochFinish(exception); }
};

Trigger.prototype.EpochTimedBuild = function()
{
	QueryPlayerIDInterface(1).SetResourceCounts({ "food": 1000, "wood": 1000, "stone": 1000, "metal": 0 });
	const pos = Engine.QueryInterface(this.centre, IID_Position).GetPosition2D();
	this.epochConstructionPoint = { "x": pos.x - 75, "z": pos.y + 65 };
	this.epochBuilds = ["house", "storehouse", "barracks", "field"];
	this.epochBuildIndex = 0;
	this.EpochIssueBuild();
};
Trigger.prototype.EpochIssueBuild = function()
{
	this.epochWait = 0;
	ProcessCommand(1, { "type": "construct", "entities": [this.worker],
		"template": "structures/epoch_rts/" + this.epochBuilds[this.epochBuildIndex],
		...this.epochConstructionPoint, "angle": 0, "autorepair": true, "autocontinue": false, "queued": false });
	this.DoAfterDelay(1000, "EpochPollBuild", {});
};
Trigger.prototype.EpochPollBuild = function()
{
	try
	{
		const tm = Engine.QueryInterface(SYSTEM_ENTITY, IID_TemplateManager);
		const owned = Engine.QueryInterface(SYSTEM_ENTITY, IID_RangeManager).GetEntitiesByPlayer(1);
		const id = this.epochBuilds[this.epochBuildIndex];
		const ent = owned.find(e => tm.GetCurrentTemplateName(e) == "structures/epoch_rts/" + id);
		if (ent)
		{
			const health = Engine.QueryInterface(ent, IID_Health);
			this.EpochCheck("E04.timedConstruction." + id, health.GetHitpoints(), health.GetMaxHitpoints());
			if (id == "house") this.EpochCheck("E04.timedHouseBonus", QueryPlayerIDInterface(1).GetPopulationLimit(), 30);
			ProcessCommand(this.epochGatherPlayer, { "type": "stop", "entities": [this.worker], "queued": false });
			if (id == "field")
			{
				this.epochRepairEntity = ent;
				this.epochRepairStock = JSON.stringify(QueryPlayerIDInterface(1).GetResourceCounts());
				health.Reduce(100);
				this.epochWait = 0;
				ProcessCommand(1, { "type": "repair", "entities": [this.worker], "target": ent, "autocontinue": false, "queued": false });
				this.DoAfterDelay(1000, "EpochPollRepair", {});
				return;
			}
			const before = JSON.stringify(QueryPlayerIDInterface(1).GetResourceCounts());
			ProcessCommand(1, { "type": "delete-entities", "entities": [ent] });
			Engine.FlushDestroyedEntities();
			this.EpochCheck("E09.completedNoRefund." + id, JSON.stringify(QueryPlayerIDInterface(1).GetResourceCounts()), before);
			// The construction site becomes available after rubble (nonblocking) appears.
			++this.epochBuildIndex;
			ProcessCommand(1, { "type": "walk", "entities": [this.worker], "x": this.epochConstructionPoint.x - 35, "z": this.epochConstructionPoint.z + 35, "queued": false });
			this.DoAfterDelay(10000, "EpochIssueBuild", {});
			return;
		}
		if (++this.epochWait > 180) throw new Error("Timed build timeout: " + id);
		this.DoAfterDelay(1000, "EpochPollBuild", {});
	}
	catch (exception) { this.EpochFinish(exception); }
};
Trigger.prototype.EpochPollRepair = function()
{
	try
	{
		const health = Engine.QueryInterface(this.epochRepairEntity, IID_Health);
		if (health.GetHitpoints() == health.GetMaxHitpoints())
		{
			this.EpochCheck("E12.timedRepairHP", health.GetHitpoints(), 200);
			this.EpochCheck("E12.repairNoCharge", JSON.stringify(QueryPlayerIDInterface(1).GetResourceCounts()), this.epochRepairStock);
			ProcessCommand(1, { "type": "stop", "entities": [this.worker], "queued": false });
			const tm = Engine.QueryInterface(SYSTEM_ENTITY, IID_TemplateManager);
			const enemyCentre = Engine.QueryInterface(SYSTEM_ENTITY, IID_RangeManager).GetEntitiesByPlayer(2).find(ent => tm.GetCurrentTemplateName(ent) == "structures/epoch_rts/civil_centre");
			const pos = Engine.QueryInterface(enemyCentre, IID_Position).GetPosition2D();
			this.epochWalkTarget = { "x": pos.x + 85, "z": pos.y + 85 };
			this.epochWait = 0;
			ProcessCommand(1, { "type": "walk", "entities": [this.worker], ...this.epochWalkTarget, "queued": false });
			this.DoAfterDelay(1000, "EpochPollWalk", {});
			return;
		}
		if (++this.epochWait > 100) throw new Error("Timed repair timeout");
		this.DoAfterDelay(1000, "EpochPollRepair", {});
	}
	catch (exception) { this.EpochFinish(exception); }
};
Trigger.prototype.EpochPollWalk = function()
{
	try
	{
		const pos = Engine.QueryInterface(this.worker, IID_Position).GetPosition2D();
		if (Math.hypot(pos.x - this.epochWalkTarget.x, pos.y - this.epochWalkTarget.z) < 4)
		{
			this.EpochCheck("E02.walkBetweenBases", true, true);
			this.EpochFinish();
			return;
		}
		if (++this.epochWait > 180) throw new Error("Walk between bases timed out");
		this.DoAfterDelay(1000, "EpochPollWalk", {});
	}
	catch (exception) { this.EpochFinish(exception); }
};
Engine.QueryInterface(SYSTEM_ENTITY, IID_Trigger).DoAfterDelay(1, "EpochRun", {});
