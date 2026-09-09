// Purpose: Real-engine T05 integration fixtures; loaded only by the validation map. Created: 2026-09-07.
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
    this.epochResults = [];
    try { this.EpochResearchFixtures(); }
    catch (e) { this.EpochFinish(e); }
};
Trigger.prototype.EpochResearchFixtures = function()
{
    const Q = (e, iid) => Engine.QueryInterface(e, iid);
    const owned = p => Q(SYSTEM_ENTITY, IID_RangeManager).GetEntitiesByPlayer(p);
    const tm = Q(SYSTEM_ENTITY, IID_TemplateManager);
    const find = (p, name) => owned(p).find(e => tm.GetCurrentTemplateName(e) == name);
    const centre = find(1, "structures/epoch_rts/civil_centre");
    const player = QueryPlayerIDInterface(1);
    const manager = QueryPlayerIDInterface(1, IID_TechnologyManager);
    const queue = Q(centre, IID_ProductionQueue);
    const age = "phase_epoch_iron", weapon = "epoch_forged_weapons";
    const money = () => player.GetResourceCounts();
    const fund = (food=1000,wood=1000,stone=1000,metal=1000) => player.SetResourceCounts({food,wood,stone,metal});
    const add = (name, x=360, z=350, p=1) => {
        const e=Engine.AddEntity(name); Q(e,IID_Position).JumpTo(x,z); Q(e,IID_Ownership).SetOwner(p); return e;
    };
    const destroy = e => { Q(e,IID_Position)?.MoveOutOfWorld(); Engine.DestroyEntity(e); Engine.FlushDestroyedEntities(); };
    const research = (e=centre, tech=age, p=1) => ProcessCommand(p,{type:"research",entity:e,template:tech});
    const check = this.EpochCheck.bind(this);
    const noAge = id => check(id,[queue.GetQueue().length,manager.IsTechnologyResearched(age)],[0,false]);
    const cost = {food:400,wood:200,stone:0,metal:100};
    fund(400,200,0,100); research(); noAge("A01.noBarracks"); check("A01.noCharge",money(),cost);
    const foundation=add("foundation|structures/epoch_rts/barracks");
    research(); noAge("A01.foundationNotEnough"); destroy(foundation);
    let barracks=add("structures/epoch_rts/barracks");
    for (const r of ["food","wood","metal"])
    {
        const poor={...cost,[r]:cost[r]-1}; player.SetResourceCounts(poor);research();noAge("A01.missing."+r);check("A01.uncharged."+r,money(),poor);
    }
    fund(); const before=money();
    research(barracks);check("A01.wrongBuilding",Q(barracks,IID_ProductionQueue).GetQueue().length,0);
    const enemyCentre=find(2,"structures/epoch_rts/civil_centre");research(enemyCentre);check("A01.enemyQueue",Q(enemyCentre,IID_ProductionQueue).GetQueue().length,0);
    research(centre,"phase_town");check("A01.nonWhitelist",queue.GetQueue().length,0);check("A01.illegalUncharged",money(),before);
    const swordCommand={type:"train",entities:[barracks],template:"units/epoch_rts/iron_swordsman",count:1};
    ProcessCommand(1,swordCommand);check("A04.swordLockedBefore",Q(barracks,IID_ProductionQueue).GetQueue().length,0);
    check("A04.forgeLockedBefore",manager.CanProduce("structures/epoch_rts/forge"),false);
    const buildForge = () => ProcessCommand(1,{type:"construct",entities:[find(1,"units/epoch_rts/pioneer")],template:"structures/epoch_rts/forge",x:400,z:400,angle:0,autorepair:false,queued:false});
    let stock=JSON.stringify(money());buildForge();Engine.FlushDestroyedEntities();
    check("A04.forgeCommandBeforeUncharged",JSON.stringify(money()),stock);
    check("A04.forgeCommandBeforeRejected",owned(1).some(e=>tm.GetCurrentTemplateName(e)=="foundation|structures/epoch_rts/forge"),false);
    // Queue behind a worker, then remove the prerequisite before its first work.
    fund(450,200,0,100);ProcessCommand(1,{type:"train",entities:[centre],template:"units/epoch_rts/pioneer",count:1});research();
    check("A02.sharedQueue",queue.GetQueue().length,2);check("A02.paidOnce",money(),{food:0,wood:0,stone:0,metal:0});
    destroy(barracks);
    for(let i=0;i<16;++i) queue.ProgressTimeout(null,0);
    noAge("A02.preStartLossCancels");check("A02.preStartFullRefund",money(),cost);
    check("A02.cancelNotification",Q(SYSTEM_ENTITY,IID_GuiInterface).GetTimeNotifications(1).some(n=>n.message=="Iron Age research cancelled: a completed Barracks is required. Resources refunded."&&n.translateMessage&&n.players.includes(1)),true);
    // Queued and started cancellation both restore the exact full cost.
    barracks=add("structures/epoch_rts/barracks");
    for(const started of [false,true])
    {
        fund(400,200,0,100);research();if(started) for(let i=0;i<10;++i)queue.ProgressTimeout(null,0);
        const id=queue.GetQueue()[0].id;ProcessCommand(2,{type:"stop-production",entity:centre,id});check("A05.enemyCannotCancel."+started,queue.GetQueue().length,1);
        ProcessCommand(1,{type:"stop-production",entity:centre,id});noAge("A05.cancel."+started);check("A05.fullRefund."+started,money(),cost);
    }
    fund();research();check("A05.restartAtZero",manager.GetQueuedResearch().get(age).timeRemaining,60000);queue.ResetQueue();
    // Destruction is a fixture action; it exercises native ownership/queue cleanup.
    const extraCentre=add("structures/epoch_rts/civil_centre",310,300);
    fund(400,200,0,100);research(extraCentre);Q(extraCentre,IID_ProductionQueue).ProgressTimeout(null,0);destroy(extraCentre);
    check("A05.destroyResearchPlaceRefund",money(),cost);check("A05.destroyNoEffect",manager.IsTechnologyResearched(age),false);
    // Real simulation timer: leave the queued age untouched for its full duration.
    fund(1000,1000,1000,1000);research();
    check("A03.ageCost",money(),{food:600,wood:800,stone:1000,metal:900});
    ProcessCommand(1,swordCommand);check("A04.swordLockedDuring",Q(barracks,IID_ProductionQueue).GetQueue().length,0);
    check("A04.forgeLockedDuring",manager.CanProduce("structures/epoch_rts/forge"),false);
    stock=JSON.stringify(money());buildForge();Engine.FlushDestroyedEntities();
    check("A04.forgeCommandDuringUncharged",JSON.stringify(money()),stock);
    check("A04.forgeCommandDuringRejected",owned(1).some(e=>tm.GetCurrentTemplateName(e)=="foundation|structures/epoch_rts/forge"),false);
    this.t05={centre,barracks,age,weapon,oldSpear:find(1,"units/epoch_rts/spearman"),worker:find(1,"units/epoch_rts/pioneer"),beforeUnits:owned(1).filter(e=>Q(e,IID_UnitAI)).length};
    this.DoAfterDelay(2000,"EpochAgeStarted",{});
};
Trigger.prototype.EpochAgeStarted = function()
{
    try {
        const t=this.t05, manager=QueryPlayerIDInterface(1,IID_TechnologyManager);
        this.EpochCheck("A02.started",manager.GetQueuedResearch().get(t.age).started,true);
        Engine.QueryInterface(t.barracks,IID_Position).MoveOutOfWorld();Engine.DestroyEntity(t.barracks);Engine.FlushDestroyedEntities();
        this.DoAfterDelay(56000,"EpochAgeNotEarly",{});
    } catch(e){this.EpochFinish(e);}
};
Trigger.prototype.EpochAgeNotEarly = function()
{
    try {
        this.EpochCheck("A03.notCompleteAt58s",QueryPlayerIDInterface(1,IID_TechnologyManager).IsTechnologyResearched(this.t05.age),false);
        this.DoAfterDelay(3000,"EpochAgeCompleted",{});
    } catch(e){this.EpochFinish(e);}
};
Trigger.prototype.EpochAgeCompleted = function()
{
    try {
        const t=this.t05, Q=(e,iid)=>Engine.QueryInterface(e,iid), manager=QueryPlayerIDInterface(1,IID_TechnologyManager), player=QueryPlayerIDInterface(1);
        const check=this.EpochCheck.bind(this);
        check("A03.completedAt61sAfterBarracksLoss",manager.IsTechnologyResearched(t.age),true);
        check("A03.noExtraResourceCost",player.GetResourceCounts(),{food:600,wood:800,stone:1000,metal:900});
        check("A03.noPublicTownBonus",manager.IsTechnologyResearched("phase_town"),false);
        check("A03.workerHPUnchanged",Q(t.worker,IID_Health).GetMaxHitpoints(),40);
        check("A03.spearHPUnchanged",Q(t.oldSpear,IID_Health).GetMaxHitpoints(),100);
        check("A03.noFreeUnits",Q(SYSTEM_ENTITY,IID_RangeManager).GetEntitiesByPlayer(1).filter(e=>Q(e,IID_UnitAI)).length,t.beforeUnits);
        check("A04.swordUnlocked",manager.CanProduce("units/epoch_rts/iron_swordsman"),true);
        check("A04.forgeUnlocked",manager.CanProduce("structures/epoch_rts/forge"),true);
        const add=(name,x,z)=>{const e=Engine.AddEntity(name);Q(e,IID_Position).JumpTo(x,z);Q(e,IID_Ownership).SetOwner(1);return e;};
        t.barracks=add("structures/epoch_rts/barracks",360,350);
        const bq=Q(t.barracks,IID_ProductionQueue);
        ProcessCommand(1,{type:"train",entities:[t.barracks],template:"units/epoch_rts/iron_swordsman",count:1});
        check("A04.swordPaid",player.GetResourceCounts(),{food:520,wood:800,stone:1000,metal:860});
        for(let i=0;i<29;++i)bq.ProgressTimeout(null,0);check("A04.swordNotEarly",bq.GetQueue().length,1);
        bq.ProgressTimeout(null,0);check("A04.swordComplete30s",bq.GetQueue().length,0);
        const tm=Q(SYSTEM_ENTITY,IID_TemplateManager);t.oldSword=Q(SYSTEM_ENTITY,IID_RangeManager).GetEntitiesByPlayer(1).find(e=>tm.GetCurrentTemplateName(e)=="units/epoch_rts/iron_swordsman");
        t.slinger=add("units/epoch_rts/slinger",450,350);t.forge=add("structures/epoch_rts/forge",320,360);
        const research=()=>ProcessCommand(1,{type:"research",entity:t.forge,template:t.weapon});
        const fund=()=>player.SetResourceCounts({food:100,wood:0,stone:0,metal:100});
        const fq=Q(t.forge,IID_ProductionQueue);
        for(const r of ["food","metal"])
        {
            const poor={food:100,wood:0,stone:0,metal:100,[r]:99};player.SetResourceCounts(poor);research();
            check("A06.poor."+r,fq.GetQueue().length,0);check("A06.poorUncharged."+r,player.GetResourceCounts(),poor);
        }
        for(const started of [false,true])
        {
            fund();research();if(started)fq.ProgressTimeout(null,0);fq.ResetQueue();check("A05.weaponRefund."+started,player.GetResourceCounts(),{food:100,wood:0,stone:0,metal:100});
        }
        fund();research();fq.ProgressTimeout(null,0);Q(t.forge,IID_Position).MoveOutOfWorld();Engine.DestroyEntity(t.forge);Engine.FlushDestroyedEntities();
        check("A05.forgeDestroyedRefund",player.GetResourceCounts(),{food:100,wood:0,stone:0,metal:100});
        check("A05.forgeDestroyedNoEffect",manager.IsTechnologyResearched(t.weapon),false);
        t.forge=add("structures/epoch_rts/forge",320,360);research();
        check("A06.cost",player.GetResourceCounts(),{food:0,wood:0,stone:0,metal:0});
        check("A06.restartZero",manager.GetQueuedResearch().get(t.weapon).timeRemaining,30000);
        check("A06.spearBefore",Q(t.oldSpear,IID_Attack).GetAttackEffectsData("Melee").Damage.Hack,6);
        check("A06.swordBefore",Q(t.oldSword,IID_Attack).GetAttackEffectsData("Melee").Damage.Hack,10);
        this.DoAfterDelay(28000,"EpochWeaponNotEarly",{});
    } catch(e){this.EpochFinish(e);}
};
Trigger.prototype.EpochWeaponNotEarly = function()
{
    try {
        this.EpochCheck("A06.notComplete28s",QueryPlayerIDInterface(1,IID_TechnologyManager).IsTechnologyResearched(this.t05.weapon),false);
        this.DoAfterDelay(3000,"EpochWeaponCompleted",{});
    } catch(e){this.EpochFinish(e);}
};
Trigger.prototype.EpochWeaponCompleted = function()
{
    try {
        const t=this.t05,Q=(e,iid)=>Engine.QueryInterface(e,iid),manager=QueryPlayerIDInterface(1,IID_TechnologyManager),check=this.EpochCheck.bind(this);
        check("A06.completed31s",manager.IsTechnologyResearched(t.weapon),true);
        check("A06.oldSpear",Q(t.oldSpear,IID_Attack).GetAttackEffectsData("Melee").Damage.Hack,8);
        check("A06.oldSword",Q(t.oldSword,IID_Attack).GetAttackEffectsData("Melee").Damage.Hack,12);
        check("A06.slingerUnchanged",Q(t.slinger,IID_Attack).GetAttackEffectsData("Ranged").Damage.Pierce,4);
        check("A06.workerUnchanged",Q(t.worker,IID_ResourceGatherer).GetGatherRates()["wood.tree"],0.7);
        for(const [id,hack] of [["spearman",8],["iron_swordsman",12]])
        {
            const e=Engine.AddEntity("units/epoch_rts/"+id);Q(e,IID_Position).JumpTo(450,400);Q(e,IID_Ownership).SetOwner(1);
            check("A06.new."+id,Q(e,IID_Attack).GetAttackEffectsData("Melee").Damage.Hack,hack);
        }
        for(const e of [t.forge,t.barracks]){Q(e,IID_Position).MoveOutOfWorld();Engine.DestroyEntity(e);}Engine.FlushDestroyedEntities();
        for(const id of ["barracks","forge"]){const e=Engine.AddEntity("structures/epoch_rts/"+id);Q(e,IID_Position).JumpTo(id=="forge"?320:360,350);Q(e,IID_Ownership).SetOwner(1);if(id=="forge")t.forge=e;}
        check("A07.rebuildRetainsTech",[manager.IsTechnologyResearched(t.age),manager.IsTechnologyResearched(t.weapon)],[true,true]);
        QueryPlayerIDInterface(1).SetResourceCounts({food:100,wood:0,stone:0,metal:100});
        ProcessCommand(1,{type:"research",entity:t.forge,template:t.weapon});
        check("A06.repeatDenied",Q(t.forge,IID_ProductionQueue).GetQueue().length,0);
        check("A06.repeatUncharged",QueryPlayerIDInterface(1).GetResourceCounts(),{food:100,wood:0,stone:0,metal:100});
        // A real worker constructs the unlocked Forge; no direct foundation work.
        QueryPlayerIDInterface(1).SetResourceCounts({food:100,wood:150,stone:100,metal:100});
        const pos=Q(t.centre,IID_Position).GetPosition2D();
        ProcessCommand(1,{type:"construct",entities:[t.worker],template:"structures/epoch_rts/forge",x:pos.x-75,z:pos.y+65,angle:0,autorepair:true,autocontinue:false,queued:false});
        check("A04.forgeConstructionPaid",QueryPlayerIDInterface(1).GetResourceCounts(),{food:100,wood:0,stone:0,metal:100});
        const owned=Q(SYSTEM_ENTITY,IID_RangeManager).GetEntitiesByPlayer(1),tm=Q(SYSTEM_ENTITY,IID_TemplateManager);
        check("A04.forgeFoundationCreated",owned.some(e=>tm.GetCurrentTemplateName(e)=="foundation|structures/epoch_rts/forge"),true);
        t.previousForges=owned.filter(e=>tm.GetCurrentTemplateName(e)=="structures/epoch_rts/forge");
        t.buildSeconds=0;
        this.DoAfterDelay(1000,"EpochPollForge",{});
    } catch(e){this.EpochFinish(e);}
};
Trigger.prototype.EpochPollForge = function()
{
    try {
        const t=this.t05,Q=(e,iid)=>Engine.QueryInterface(e,iid),tm=Q(SYSTEM_ENTITY,IID_TemplateManager);
        ++t.buildSeconds;
        const forge=Q(SYSTEM_ENTITY,IID_RangeManager).GetEntitiesByPlayer(1).find(e=>!t.previousForges.includes(e)&&tm.GetCurrentTemplateName(e)=="structures/epoch_rts/forge");
        if(forge)
        {
            this.EpochCheck("A04.realForgeCompletedHP",Q(forge,IID_Health).GetHitpoints(),500);
            this.EpochCheck("A04.realForgeNotBefore50s",t.buildSeconds>=50,true);
            this.EpochCheck("A04.realForgeNoExtraCharge",QueryPlayerIDInterface(1).GetResourceCounts(),{food:100,wood:0,stone:0,metal:100});
            this.EpochFinish();return;
        }
        if(t.buildSeconds>180)throw new Error("Real Forge construction timed out");
        this.DoAfterDelay(1000,"EpochPollForge",{});
    }catch(e){this.EpochFinish(e);}
};
Engine.QueryInterface(SYSTEM_ENTITY,IID_Trigger).DoAfterDelay(1,"EpochRun",{});
