// Purpose: Static house import fixture and inherited M2/path checks. Created: 2026-09-21.
// SPDX-License-Identifier: GPL-2.0-or-later
Trigger.prototype.T10Check=function(id,actual,expected)
{
    this.t10.checks.push({id,actual,expected,passed:JSON.stringify(actual)==JSON.stringify(expected)});
};
Trigger.prototype.T10Finish=function(error)
{
    const result='EPOCH_TEST_RESULT '+JSON.stringify({mode:'validation',passed:!error&&this.t10.checks.every(c=>c.passed),failure:error?String(error):null,checks:this.t10.checks,observations:this.t10.observations});
    for(let i=0;i<result.length;i+=4096)print(result.slice(i,i+4096));
};
Trigger.prototype.T10Add=function(name,x,z,owner)
{
    const e=Engine.AddEntity(name);Engine.QueryInterface(e,IID_Position).JumpTo(x,z);
    Engine.QueryInterface(e,IID_Ownership).SetOwner(owner);return e;
};
Trigger.prototype.T10Start=function()
{
    this.t10={checks:[],observations:[],path:[]};
    try {
        Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager).SetLosRevealAll(1,true);
        this.t10.blue=this.T10Add('structures/epoch_rts/t10_house',320,300,1);
        this.t10.red=this.T10Add('structures/epoch_rts/t10_house',350,300,2);
        this.t10.reference=this.T10Add('structures/epoch_rts/house',390,300,1);
        this.t10.worker=this.T10Add('units/epoch_rts/pioneer',290,300,1);
        const tm=Engine.QueryInterface(SYSTEM_ENTITY,IID_TemplateManager);
        const imported=tm.GetTemplate('structures/epoch_rts/t10_house'),original=tm.GetTemplate('structures/epoch_rts/house');
        for(const key of ['Cost','Health','Footprint','Obstruction','Population','BuildRestrictions'])
            this.T10Check('asset.inherited.'+key,imported[key],original[key]);
        this.T10Check('asset.newActor',imported.VisualActor.Actor,'structures/epoch_rts/t10_house.xml');
        this.T10Check('asset.HP',Engine.QueryInterface(this.t10.blue,IID_Health).GetHitpoints(),300);
        const p=Engine.QueryInterface(this.t10.blue,IID_Position).GetPosition();
        const ground=Engine.QueryInterface(SYSTEM_ENTITY,IID_Terrain).GetGroundLevel(p.x,p.z);
        this.T10Check('asset.grounded',Math.abs(p.y-ground)<0.01,true);
        this.T10Check('asset.playerOwners',[Engine.QueryInterface(this.t10.blue,IID_Ownership).GetOwner(),Engine.QueryInterface(this.t10.red,IID_Ownership).GetOwner()],[1,2]);
        this.t10.observations.push({id:'asset.fixture',position:p,ground,footprint:imported.Footprint,obstruction:imported.Obstruction,entities:{blue:this.t10.blue,red:this.t10.red,reference:this.t10.reference,worker:this.t10.worker}});
        // Normal command across the sample's footprint; the worker must detour.
        ProcessCommand(1,{type:'walk',entities:[this.t10.worker],x:338,z:300,queued:false});
        this.DoAfterDelay(200,'T10Path',{});
    }catch(e){this.T10Finish(e);}
};
Trigger.prototype.T10Path=function()
{
    try {
        const p=Engine.QueryInterface(this.t10.worker,IID_Position).GetPosition2D();
        this.t10.path.push({x:p.x,z:p.y});
        if(this.t10.path.length<100){this.DoAfterDelay(200,'T10Path',{});return;}
        this.T10Check('asset.workerReached',Math.hypot(p.x-338,p.y-300)<5,true);
        this.T10Check('asset.workerDetour',this.t10.path.some(v=>Math.abs(v.z-300)>5),true);
        this.T10Check('asset.sampleStillHealthy',Engine.QueryInterface(this.t10.blue,IID_Health).GetHitpoints(),300);
        this.t10.observations.push({id:'asset.workerPath',samples:this.t10.path});
        this.T10Finish();
    }catch(e){this.T10Finish(e);}
};
Engine.QueryInterface(SYSTEM_ENTITY,IID_Trigger).DoAfterDelay(1000,'T10Start',{});
