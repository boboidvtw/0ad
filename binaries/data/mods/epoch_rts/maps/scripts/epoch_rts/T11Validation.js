// Purpose: Isolated art-only M2 inheritance and action probes. Created: 2026-09-21.
// SPDX-License-Identifier: GPL-2.0-or-later
Trigger.prototype.T11Check=function(id,actual,expected)
{
    this.t11.checks.push({id,actual,expected,passed:JSON.stringify(actual)==JSON.stringify(expected)});
};
Trigger.prototype.T11Finish=function(error)
{
    const result='EPOCH_TEST_RESULT '+JSON.stringify({mode:'validation',passed:!error&&this.t11.checks.every(c=>c.passed),failure:error?String(error):null,checks:this.t11.checks,observations:this.t11.observations});
    for(let i=0;i<result.length;i+=4096)print(result.slice(i,i+4096));
};
Trigger.prototype.T11Add=function(name,x,z,owner)
{
    const e=Engine.AddEntity(name);Engine.QueryInterface(e,IID_Position).JumpTo(x,z);
    Engine.QueryInterface(e,IID_Ownership).SetOwner(owner);return e;
};
Trigger.prototype.T11Start=function()
{
    print('T11_STAGE Start');
    this.t11={checks:[],observations:[]};
    try {
        Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager).SetLosRevealAll(1,true);
        const tm=Engine.QueryInterface(SYSTEM_ENTITY,IID_TemplateManager);
        for(const [kind,child,parent] of [['units','worker','pioneer'],['units','soldier','spearman'],['structures','house','house']])
        {
            const current=tm.GetTemplate(kind+'/epoch_rts/t11_'+child),original=tm.GetTemplate(kind+'/epoch_rts/'+parent);
            for(const key of Object.keys(original).filter(k=>k!='VisualActor'&&k!='Identity'&&!(child=='worker'&&k=='Builder')&&!k.startsWith('@')))
                this.T11Check(child+'.inherited.'+key,current[key],original[key]);
            for(const key of Object.keys(original.Identity).filter(k=>k!='Icon'))
                this.T11Check(child+'.identity.'+key,current.Identity[key],original.Identity[key]);
            if(child=='worker')
            {
                this.T11Check('worker.builderRate',current.Builder.Rate,original.Builder.Rate);
                this.T11Check('worker.builderArtRemap',current.Builder.Entities._string,original.Builder.Entities._string.replace('structures/epoch_rts/house','structures/epoch_rts/t11_house'));
            }
            this.T11Check(child+'.icon',current.Identity.Icon,'epoch_rts/t11_'+child+'.png');
            this.T11Check(child+'.actor',current.VisualActor.Actor,(kind=='units'?'units':'structures')+'/epoch_rts/t11_'+child+'.xml');
        }
        this.t11.house=this.T11Add('structures/epoch_rts/t11_house',320,310,1);
        this.t11.redHouse=this.T11Add('structures/epoch_rts/t11_house',348,310,2);
        this.t11.worker=this.T11Add('units/epoch_rts/t11_worker',304,284,1);
        this.t11.soldier=this.T11Add('units/epoch_rts/t11_soldier',328,282,1);
        this.t11.redWorker=this.T11Add('units/epoch_rts/t11_worker',351,283,2);
        this.t11.redSoldier=this.T11Add('units/epoch_rts/t11_soldier',358,283,2);
        this.t11.tree=this.T11Add('gaia/tree/aleppo_pine',295,298,0);
        this.t11.observations.push({id:'fixture',entities:Object.fromEntries(Object.entries(this.t11).filter(([k,v])=>typeof v=='number'))});
        for(const e of [this.t11.soldier,this.t11.redSoldier])Engine.QueryInterface(e,IID_UnitAI).SwitchToStance('standground');
        ProcessCommand(1,{type:'walk',entities:[this.t11.worker],x:308,z:298,queued:false});
        ProcessCommand(1,{type:'walk',entities:[this.t11.soldier],x:336,z:284,queued:false});
        this.DoAfterDelay(9000,'T11Gather',{});
    }catch(e){this.T11Finish(e);}
};
Trigger.prototype.T11Gather=function()
{
    print('T11_STAGE Gather');
    try {
        const p=Engine.QueryInterface(this.t11.worker,IID_Position).GetPosition2D();
        this.T11Check('worker.walk',Math.hypot(p.x-308,p.y-298)<2,true);
        this.t11.initialWood=Engine.QueryInterface(this.t11.tree,IID_ResourceSupply).GetCurrentAmount();
        ProcessCommand(1,{type:'gather',entities:[this.t11.worker],target:this.t11.tree,queued:false});
        this.DoAfterDelay(22000,'T11Repair',{});
    }catch(e){this.T11Finish(e);}
};
Trigger.prototype.T11Repair=function()
{
    print('T11_STAGE Repair');
    try {
        const wood=Engine.QueryInterface(this.t11.tree,IID_ResourceSupply).GetCurrentAmount();
        this.T11Check('worker.gather',wood<this.t11.initialWood,true);
        this.t11.observations.push({id:'gather',woodBefore:this.t11.initialWood,woodAfter:wood,state:Engine.QueryInterface(this.t11.worker,IID_UnitAI).GetCurrentState()});
        Engine.QueryInterface(this.t11.house,IID_Health).Reduce(80);
        ProcessCommand(1,{type:'repair',entities:[this.t11.worker],target:this.t11.house,autocontinue:false,queued:false});
        this.DoAfterDelay(25000,'T11Build',{});
    }catch(e){this.T11Finish(e);}
};
Trigger.prototype.T11Build=function()
{
    print('T11_STAGE Build');
    try {
        const hp=Engine.QueryInterface(this.t11.house,IID_Health).GetHitpoints();
        this.T11Check('worker.repair',hp>220,true);
        this.t11.observations.push({id:'repair',hp,state:Engine.QueryInterface(this.t11.worker,IID_UnitAI).GetCurrentState()});
        this.t11.woodBeforeBuild=QueryPlayerIDInterface(1).GetResourceCounts().wood;
        ProcessCommand(1,{type:'construct',entities:[this.t11.worker],template:'structures/epoch_rts/t11_house',x:310,z:276,angle:0,autorepair:true,autocontinue:false,queued:false});
        this.DoAfterDelay(10000,'T11Building',{});
        this.DoAfterDelay(40000,'T11Built',{});
    }catch(e){this.T11Finish(e);}
};
Trigger.prototype.T11Building=function()
{
    try {
        const state=Engine.QueryInterface(this.t11.worker,IID_UnitAI).GetCurrentState();
        this.T11Check('worker.buildingState',state.includes('REPAIRING'),true);
        this.t11.observations.push({id:'building',state});
    }catch(e){this.T11Finish(e);}
};
Trigger.prototype.T11Built=function()
{
    try {
        const tm=Engine.QueryInterface(SYSTEM_ENTITY,IID_TemplateManager);
        const houses=Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager).GetEntitiesByPlayer(1).filter(e=>tm.GetCurrentTemplateName(e)=='structures/epoch_rts/t11_house');
        this.T11Check('worker.constructedHouse',houses.length,2);
        this.T11Check('worker.constructionWoodCost',this.t11.woodBeforeBuild-QueryPlayerIDInterface(1).GetResourceCounts().wood,50);
        this.t11.observations.push({id:'construction',houses,woodCost:this.t11.woodBeforeBuild-QueryPlayerIDInterface(1).GetResourceCounts().wood});
        this.T11Attack();
    }catch(e){this.T11Finish(e);}
};
Trigger.prototype.T11Attack=function()
{
    print('T11_STAGE Attack');
    try {
        // A stationary art dummy uses ordinary M2 health; no attack or damage overrides.
        ProcessCommand(1,{type:'attack',entities:[this.t11.soldier],target:this.t11.redHouse,queued:false});
        this.DoAfterDelay(22000,'T11Death',{});
    }catch(e){this.T11Finish(e);}
};
Trigger.prototype.T11Death=function()
{
    print('T11_STAGE Death');
    try {
        const hp=Engine.QueryInterface(this.t11.redHouse,IID_Health).GetHitpoints();
        this.T11Check('soldier.attack',hp<300,true);
        this.t11.observations.push({id:'attack',hp,state:Engine.QueryInterface(this.t11.soldier,IID_UnitAI).GetCurrentState()});
        ProcessCommand(1,{type:'stop',entities:[this.t11.soldier],queued:false});
        Engine.QueryInterface(this.t11.redWorker,IID_Health).Kill();
        Engine.QueryInterface(this.t11.redSoldier,IID_Health).Kill();
        this.DoAfterDelay(3000,'T11End',{});
    }catch(e){this.T11Finish(e);}
};
Trigger.prototype.T11End=function()
{
    print('T11_STAGE End');
    try {
        this.T11Check('worker.deadEntityRemoved',!!Engine.QueryInterface(this.t11.redWorker,IID_Health),false);
        this.T11Check('soldier.deadEntityRemoved',!!Engine.QueryInterface(this.t11.redSoldier,IID_Health),false);
        this.T11Check('worker.alive',Engine.QueryInterface(this.t11.worker,IID_Health).GetHitpoints(),40);
        this.T11Finish();
    }catch(e){this.T11Finish(e);}
};
Engine.QueryInterface(SYSTEM_ENTITY,IID_Trigger).DoAfterDelay(5000,'T11Start',{});
