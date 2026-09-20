// Purpose: Isolated native R28 submarine feasibility measurements. Created: 2026-09-20.
// SPDX-License-Identifier: GPL-2.0-or-later
Trigger.prototype.T8Check = function(id, actual, expected)
{
    const passed = JSON.stringify(actual) == JSON.stringify(expected);
    this.t8.checks.push({id, actual, expected, passed});
};
Trigger.prototype.T8Finish = function(error)
{
    const passed = !error && this.t8.checks.length > 0 && this.t8.checks.every(c => c.passed);
    const result = 'EPOCH_TEST_RESULT ' + JSON.stringify({mode:this.t8Visual ? 'visual' : 'probe', passed, checks:this.t8.checks,
        failure:error ? String(error) : null, observations:this.t8.observations});
    for (let i=0; i<result.length; i+=4096) print(result.slice(i,i+4096));
};
Trigger.prototype.T8Add = function(template,x,z,owner)
{
    const e=Engine.AddEntity(template);
    Engine.QueryInterface(e,IID_Position).JumpTo(x,z);
    Engine.QueryInterface(e,IID_Ownership).SetOwner(owner);
    Engine.QueryInterface(e,IID_UnitAI).SwitchToStance("none"); // Freeze autonomous reactions, keep normal commanded motion.
    return e;
};
Trigger.prototype.T8Start = function()
{
    this.t8={checks:[],observations:[]};
    try {
        if (this.t8Visual) { this.T8VisualStart(); return; }
        this.t8.ship=this.T8Add('units/epoch_rts/t08_native_ship',280,300,1);
        this.t8.sub=this.T8Add('units/epoch_rts/t08_sub_probe',330,300,2);
        this.t8.detector=this.T8Add('units/epoch_rts/t08_native_ship',180,300,1);
        const p=Engine.QueryInterface(this.t8.sub,IID_Position);
        const rm=Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager);
        const methods = obj => {const a=[];for(let k in obj)if(typeof obj[k]=='function')a.push(k);return a.sort();};
        this.t8.observations.push({id:'native.bindings',position:methods(p),rangeManager:methods(rm)});
        this.DoAfterDelay(1000,'T8Sample',{});
    }catch(e){this.T8Finish(e);}
};
Trigger.prototype.T8Sample = function()
{
    try {
        const p=Engine.QueryInterface(this.t8.sub,IID_Position), pos=p.GetPosition();
        const w=Engine.QueryInterface(SYSTEM_ENTITY,IID_WaterManager).GetWaterLevel(pos.x,pos.z);
        const rm=Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager);
        this.t8.observations.push({id:'native.initial',position:pos,water:w,enemyVisibility:rm.GetLosVisibility(this.t8.sub,1)});
        this.T8Check('S02.floatDepth4',Math.abs(pos.y-(w-4))<0.01,true);
        this.T8Check('S03.depthAloneVisible',rm.GetLosVisibility(this.t8.sub,1),'visible');
        this.T8Check('S02.waterDepth12',Math.round(w-Engine.QueryInterface(SYSTEM_ENTITY,IID_Terrain).GetGroundLevel(pos.x,pos.z)),12);
        this.t8.water=w;
        p.SetHeightFixed(w);
        this.T8Check('S02.surfaceFixed',Math.abs(p.GetPosition().y-w)<0.01,true);
        p.SetHeightFixed(w-4);
        this.T8Check('S02.submergeFixed',Math.abs(p.GetPosition().y-(w-4))<0.01,true);
        const v=Engine.QueryInterface(this.t8.sub,IID_Visibility);
        v.submerged=true;v.detector=this.t8.detector;v.Activate();
        rm.RequestVisibilityUpdate(this.t8.sub);
        this.DoAfterDelay(1000,'T8Hidden',{});
    }catch(e){this.T8Finish(e);}
};
Engine.QueryInterface(SYSTEM_ENTITY,IID_Trigger).DoAfterDelay(1000,'T8Start',{});
Trigger.prototype.T8Visibility = function(id, expected)
{
    const rm=Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager);
    this.t8.observations.push({id,position:Engine.QueryInterface(this.t8.sub,IID_Position).GetPosition(),hp:this.T8HP()});
    this.T8Check(id+'.enemy',rm.GetLosVisibility(this.t8.sub,1),expected);
    this.T8Check(id+'.owner',rm.GetLosVisibility(this.t8.sub,2),'visible');
};
Trigger.prototype.T8HP = function() {return Engine.QueryInterface(this.t8.sub,IID_Health).GetHitpoints();};
Trigger.prototype.T8Refresh = function()
{
    Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager).RequestVisibilityUpdate(this.t8.sub);
};
Trigger.prototype.T8Hidden = function()
{
    try {
        this.T8Visibility('S03.scriptedHidden','hidden');
        this.T8Check('S03.canAttackNotLoS',Engine.QueryInterface(this.t8.ship,IID_Attack).CanAttack(this.t8.sub,['Ranged']),true);
        this.T8Check('S03.unitAISeesHidden',Engine.QueryInterface(this.t8.ship,IID_UnitAI).CheckTargetVisible(this.t8.sub),false);
        this.t8.hp=this.T8HP();
        ProcessCommand(1,{type:'attack',entities:[this.t8.ship],target:this.t8.sub,queued:false});
        this.DoAfterDelay(3000,'T8HiddenOrder',{});
    }catch(e){this.T8Finish(e);}
};
Trigger.prototype.T8HiddenOrder = function()
{
    try {
        this.t8.observations.push({id:'hidden.newAttackOrder',before:this.t8.hp,after:this.T8HP(),state:Engine.QueryInterface(this.t8.ship,IID_UnitAI).GetCurrentState()});
        this.T8Check('S04.hiddenOrderStillDamages.nativeLimitation',this.T8HP()<this.t8.hp,true);
        ProcessCommand(1,{type:'stop',entities:[this.t8.ship],queued:false});
        Engine.QueryInterface(this.t8.detector,IID_Position).JumpTo(390,300);
        this.T8Refresh();this.DoAfterDelay(1000,'T8Detected',{});
    }catch(e){this.T8Finish(e);}
};
Trigger.prototype.T8Detected = function()
{
    try {
        this.T8Visibility('S04.detectorAt60','visible');
        this.t8.hp=this.T8HP();
        ProcessCommand(1,{type:'attack',entities:[this.t8.ship],target:this.t8.sub,queued:false});
        this.DoAfterDelay(3000,'T8Attacking',{});
    }catch(e){this.T8Finish(e);}
};
Trigger.prototype.T8Attacking = function()
{
    try {
        this.T8Check('S04.visibleAttackDamage',this.T8HP()<this.t8.hp,true);
        this.t8.observations.push({id:'detected.attack',before:this.t8.hp,after:this.T8HP()});
        Engine.QueryInterface(this.t8.detector,IID_Position).JumpTo(391,300);
        this.T8Refresh();this.DoAfterDelay(1000,'T8Lost',{});
    }catch(e){this.T8Finish(e);}
};
Trigger.prototype.T8Lost = function()
{
    try {
        this.T8Visibility('S04.detectorAt61','hidden');
        this.t8.hp=this.T8HP();
        this.DoAfterDelay(3000,'T8LostDamage',{});
    }catch(e){this.T8Finish(e);}
};
Trigger.prototype.T8LostDamage = function()
{
    try {
        this.t8.observations.push({id:'lostDetection.ongoingAttack',before:this.t8.hp,after:this.T8HP(),state:Engine.QueryInterface(this.t8.ship,IID_UnitAI).GetCurrentState()});
        this.T8Check('S04.lostDetectionStillDamages.nativeLimitation',this.T8HP()<this.t8.hp,true);
        ProcessCommand(1,{type:'stop',entities:[this.t8.ship],queued:false});
        const hp=this.T8HP();
        Engine.QueryInterface(this.t8.ship,IID_Attack).PerformAttack('Ranged',this.t8.sub);
        this.T8Check('S04.directAttackBypassesHidden',this.T8HP()<hp,true);
        const detector=Engine.QueryInterface(this.t8.detector,IID_Position);
        detector.JumpTo(360,300);
        Engine.QueryInterface(this.t8.detector,IID_Ownership).SetOwner(2);
        this.T8Refresh();this.DoAfterDelay(1000,'T8Transferred',{});
    }catch(e){this.T8Finish(e);}
};
Trigger.prototype.T8Transferred = function()
{
    try {
        this.T8Visibility('S04.enemyOwnedDetector','hidden');
        Engine.QueryInterface(this.t8.detector,IID_Ownership).SetOwner(1);
        this.T8Refresh();this.DoAfterDelay(1000,'T8Restored',{});
    }catch(e){this.T8Finish(e);}
};
Trigger.prototype.T8Restored = function()
{
    try {
        this.T8Visibility('S04.detectorRestored','visible');
        Engine.DestroyEntity(this.t8.detector);Engine.FlushDestroyedEntities();
        this.T8Refresh();this.DoAfterDelay(1000,'T8Destroyed',{});
    }catch(e){this.T8Finish(e);}
};
Trigger.prototype.T8Destroyed = function()
{
    try {
        this.T8Visibility('S04.detectorDestroyed','hidden');
        Engine.QueryInterface(this.t8.sub,IID_Visibility).submerged=false;
        Engine.QueryInterface(this.t8.sub,IID_Position).SetHeightFixed(this.t8.water);
        this.T8Refresh();this.DoAfterDelay(1000,'T8Surfaced',{});
    }catch(e){this.T8Finish(e);}
};
Trigger.prototype.T8Surfaced = function()
{
    try {
        this.T8Visibility('S03.surfacedNoDetector','visible');
        const land=this.T8Add('units/epoch_rts/pioneer',570,300,2);
        const friendly=this.T8Add('units/epoch_rts/t08_native_ship',250,380,1);
        const attack=Engine.QueryInterface(this.t8.ship,IID_Attack);
        this.T8Check('S04.restrictedLand',attack.CanAttack(land,['Ranged']),false);
        this.T8Check('S04.restrictedFriendly',attack.CanAttack(friendly,['Ranged']),false);
        Engine.QueryInterface(this.t8.sub,IID_Position).SetHeightFixed(this.t8.water-4);
        ProcessCommand(2,{type:'walk',entities:[this.t8.sub],x:450,z:300,queued:false});
        this.DoAfterDelay(15000,'T8Moved',{});
    }catch(e){this.T8Finish(e);}
};
Trigger.prototype.T8Moved = function()
{
    try {
        const pos=Engine.QueryInterface(this.t8.sub,IID_Position).GetPosition();
        this.t8.observations.push({id:'submerged.move',position:pos});
        this.T8Check('S02.underwaterMove',pos.x>420,true);
        this.T8Check('S02.depthAfterMove',Math.abs(pos.y-(this.t8.water-4))<0.01,true);
        ProcessCommand(2,{type:'walk',entities:[this.t8.sub],x:600,z:300,queued:false});
        this.DoAfterDelay(20000,'T8LandBoundary',{});
    }catch(e){this.T8Finish(e);}
};
Trigger.prototype.T8LandBoundary = function()
{
    try {
        const pos=Engine.QueryInterface(this.t8.sub,IID_Position).GetPosition();
        this.t8.observations.push({id:'ship.landBoundary',position:pos});
        this.T8Check('S02.noLandCrossing',pos.x<520,true);
        this.T8Finish();
    }catch(e){this.T8Finish(e);}
};
// Separate GUI sequence: no combat, four 30-second stages. API checks do not certify rendering.
Trigger.prototype.T8VisualStart = function()
{
    this.t8.ship=this.T8Add('units/epoch_rts/t08_native_ship',280,300,1);
    this.t8.sub=this.T8Add('units/epoch_rts/t08_sub_probe',330,300,2);
    this.t8.detector=this.T8Add('units/epoch_rts/t08_native_ship',210,300,1);
    const v=Engine.QueryInterface(this.t8.sub,IID_Visibility);
    v.detector=this.t8.detector;v.Activate();
    Engine.QueryInterface(this.t8.sub,IID_Position).SetHeightFixed(20);
    this.t8.phase=0;
    this.DoAfterDelay(1000,'T8VisualStage',{});
};
Trigger.prototype.T8VisualStage = function()
{
    try {
        const stages=['surface','hidden','detected','resurfaced'];
        const expected=this.t8.phase==1?'hidden':'visible';
        this.T8Visibility('GUI.'+stages[this.t8.phase],expected);
        print('EPOCH_T08_VISUAL '+JSON.stringify({stage:stages[this.t8.phase],entity:this.t8.sub,position:Engine.QueryInterface(this.t8.sub,IID_Position).GetPosition(),visibility:Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager).GetLosVisibility(this.t8.sub,1)}));
        if(this.t8.phase==3){this.T8Finish();return;}
        this.DoAfterDelay(30000,'T8VisualNext',{});
    }catch(e){this.T8Finish(e);}
};
Trigger.prototype.T8VisualNext = function()
{
    try {
        ++this.t8.phase;
        if(this.t8.phase==1) {
            Engine.QueryInterface(this.t8.sub,IID_Position).SetHeightFixed(16);
            Engine.QueryInterface(this.t8.sub,IID_Visibility).submerged=true;
        }
        if(this.t8.phase==2)Engine.QueryInterface(this.t8.detector,IID_Position).JumpTo(370,300);
        if(this.t8.phase==3) {
            Engine.QueryInterface(this.t8.sub,IID_Visibility).submerged=false;
            Engine.QueryInterface(this.t8.sub,IID_Position).SetHeightFixed(20);
        }
        this.T8Refresh();this.DoAfterDelay(1000,'T8VisualStage',{});
    }catch(e){this.T8Finish(e);}
};
