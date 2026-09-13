// Purpose: Actual R28 native-flight probe and isolated air acceptance. Created: 2026-09-13.
// SPDX-License-Identifier: GPL-2.0-or-later
Trigger.prototype.T7Check = function(id,actual,expected)
{
    const passed=JSON.stringify(actual)==JSON.stringify(expected);
    this.t7.checks.push(JSON.parse(JSON.stringify({id,actual,expected,passed})));
    if(!passed)throw new Error(id+': '+JSON.stringify(actual)+' != '+JSON.stringify(expected));
};
Trigger.prototype.T7Finish = function(error)
{
    if(this.t7.finished)return;
    this.t7.finished=true;
    const result='EPOCH_TEST_RESULT '+JSON.stringify({mode:this.t7Mode,passed:!error,checks:this.t7.checks,failure:error?String(error):null,observations:this.t7.observations});
    for(let i=0;i<result.length;i+=4096)print(result.slice(i,i+4096));
};
Trigger.prototype.T7Start = function()
{
    this.t7={checks:[],observations:[]};
    try {
        if(this.t7Mode=='demo'){this.T7Demo();return;}
        if(this.t7Mode!='probe'){this.T7Setup();return;}
        const e=Engine.AddEntity('units/plane');
        Engine.QueryInterface(e,IID_Position).JumpTo(300,300);
        Engine.QueryInterface(e,IID_Ownership).SetOwner(1);
        this.t7.native=e;
        ProcessCommand(1,{type:'walk',entities:[e],x:450,z:450,queued:false});
        this.DoAfterDelay(10000,'T7Probe',{});
    }catch(e){this.T7Finish(e);}
};
Trigger.prototype.T7Probe = function()
{
    try {
        const e=this.t7.native,m=Engine.QueryInterface(e,IID_UnitMotion),p=Engine.QueryInterface(e,IID_Position).GetPosition();
        this.T7Check('native.airborne',!m.onGround,true);
        this.T7Check('native.height',p.y>20,true);
        m.StopMoving();const first=m.landing;m.StopMoving();const second=m.landing;
        this.t7.observations.push({id:'native.repeatStop',first,second});
        m.StopMoving();m.MoveToTargetRange(this.t7.native,0,10);
        this.t7.observations.push({id:'native.moveTargetWhileLanding',landing:m.landing});
        this.T7Finish();
    }catch(e){this.T7Finish(e);}
};
Engine.QueryInterface(SYSTEM_ENTITY,IID_Trigger).DoAfterDelay(1000,'T7Start',{});
Trigger.prototype.T7Add = function(name,x,z,owner=1)
{
    const e=Engine.AddEntity(name);
    Engine.QueryInterface(e,IID_Position).JumpTo(x,z);
    Engine.QueryInterface(e,IID_Ownership).SetOwner(owner);
    return e;
};
Trigger.prototype.T7Setup = function()
{
    this.t7.airfield=this.T7Add('structures/epoch_rts/airfield',300,300);
    this.t7.enemyField=this.T7Add('structures/epoch_rts/airfield',530,430,2);
    this.t7.target=this.T7Add('structures/epoch_rts/house',480,350,2);
    QueryPlayerIDInterface(1).SetResourceCounts({food:1000,wood:1000,stone:1000,metal:1000});
    Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager).SetLosRevealAll(1,true);
    ProcessCommand(1,{type:'train',entities:[this.t7.airfield],template:'units/epoch_rts/aircraft',count:1});
    this.T7Check('F01.woodPaid',QueryPlayerIDInterface(1).GetResourceCounts().wood,800);
    this.T7Check('F01.metalPaid',QueryPlayerIDInterface(1).GetResourceCounts().metal,900);
    this.T7Check('F01.queued',Engine.QueryInterface(this.t7.airfield,IID_ProductionQueue).GetQueue().length,1);
    this.DoAfterDelay(21000,'T7Trained',{});
};
Trigger.prototype.T7Trained = function()
{
    try {
        const entities=Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager).GetEntitiesByPlayer(1).filter(e=>Engine.QueryInterface(e,IID_EpochAircraft));
        this.T7Check('F01.singleAircraft',entities.length,1);
        this.t7.plane=entities[0];
        this.T7Check('F01.grounded',Engine.QueryInterface(this.t7.plane,IID_UnitMotion).onGround,true);
        this.T7Check('F01.HP',Engine.QueryInterface(this.t7.plane,IID_Health).GetHitpoints(),200);
        ProcessCommand(1,{type:'walk',entities:[this.t7.plane],x:430,z:340,queued:false});
        this.DoAfterDelay(10000,'T7Airborne',{});
    }catch(e){this.T7Finish(e);}
};
Trigger.prototype.T7Airborne = function()
{
    try {
        const e=this.t7.plane,m=Engine.QueryInterface(e,IID_UnitMotion),p=Engine.QueryInterface(e,IID_Position).GetPosition();
        this.T7Check('F02.airborne',m.onGround,false);
        const position=Engine.QueryInterface(e,IID_Position),turnMs=Engine.QueryInterface(SYSTEM_ENTITY,IID_Timer).GetLatestTurnLength();
        const expected=position.GetPosition2D().distanceTo(position.GetPreviousPosition2D())*1000/turnMs;
        this.T7Check('F02.predictionSeconds',Math.abs(m.EstimateFuturePosition(1).distanceTo(position.GetPosition2D())-expected)<0.001,true);
        this.T7Check('F02.altitude',Math.round(p.y-Engine.QueryInterface(SYSTEM_ENTITY,IID_Terrain).GetGroundLevel(p.x,p.z)),25);
        const before=m.targetX;
        ProcessCommand(2,{type:'walk',entities:[e],x:100,z:100,queued:false});
        this.T7Check('F04.enemyCannotMove',m.targetX,before);
        ProcessCommand(1,{type:'epoch-air-return',entities:[e],target:this.t7.enemyField});
        this.T7Check('F04.enemyAirfieldRejected',Engine.QueryInterface(e,IID_EpochAircraft).GetStatus().order,'move');
        ProcessCommand(1,{type:'attack',entities:[e],target:this.t7.target,queued:false});
        this.T7Check('F05.groundAccepted',Engine.QueryInterface(e,IID_EpochAircraft).GetStatus().order,'attack');
        const other=this.T7Add('units/epoch_rts/aircraft',470,370,2);this.t7.other=other;
        this.T7Check('F05.airRejected',Engine.QueryInterface(e,IID_Attack).CanAttack(other,['Ranged']),false);
        this.T7Check('F05.friendRejected',Engine.QueryInterface(e,IID_Attack).CanAttack(this.t7.airfield,['Ranged']),false);
        this.DoAfterDelay(16000,'T7AttackResult',{});
    }catch(e){this.T7Finish(e);}
};
Trigger.prototype.T7AttackResult = function()
{
    try {
        this.T7Check('F05.groundDamage',Engine.QueryInterface(this.t7.target,IID_Health).GetHitpoints()<300,true);
        ProcessCommand(1,{type:'stop',entities:[this.t7.plane],queued:false});
        ProcessCommand(1,{type:'stop',entities:[this.t7.plane],queued:false});
        this.T7Check('F06.repeatStop',Engine.QueryInterface(this.t7.plane,IID_EpochAircraft).GetStatus().order,'return');
        this.t7.polls=0;this.DoAfterDelay(1000,'T7LandingPoll',{});
    }catch(e){this.T7Finish(e);}
};
Trigger.prototype.T7LandingPoll = function()
{
    try {
        const e=this.t7.plane,m=Engine.QueryInterface(e,IID_UnitMotion);
        if(++this.t7.polls>90)throw new Error('Landing timeout '+JSON.stringify(Engine.QueryInterface(e,IID_EpochAircraft).GetStatus()));
        if(!m.onGround||m.GetCurrentSpeed()!=0||m.IsMoveRequested()){this.DoAfterDelay(1000,'T7LandingPoll',{});return;}
        const distance=Engine.QueryInterface(e,IID_Position).GetPosition2D().distanceTo(Engine.QueryInterface(this.t7.airfield,IID_Position).GetPosition2D());
        this.t7.observations.push({id:'F03.landingDistance',distance});
        this.T7Check('F03.withinAirfield',distance<=90,true);
        ProcessCommand(1,{type:'walk',entities:[e],x:10000,z:-10000,queued:false});
        this.DoAfterDelay(10000,'T7Boundary',{});
    }catch(e){this.T7Finish(e);}
};
Trigger.prototype.T7Boundary = function()
{
    try {
        const e=this.t7.plane,m=Engine.QueryInterface(e,IID_UnitMotion),p=Engine.QueryInterface(e,IID_Position).GetPosition2D(),size=Engine.QueryInterface(SYSTEM_ENTITY,IID_Terrain).GetMapSize(),half=size/2;
        this.T7Check('F03.relaunch',m.onGround,false);
        this.T7Check('F06.boundary',Math.hypot(p.x-half,p.y-half)<=half-12,true);
        ProcessCommand(1,{type:'stop',entities:[e],queued:false});
        Engine.DestroyEntity(this.t7.airfield);Engine.FlushDestroyedEntities();
        this.DoAfterDelay(15000,'T7MissingAirfield',{});
    }catch(e){this.T7Finish(e);}
};
Trigger.prototype.T7MissingAirfield = function()
{
    try {
        const e=this.t7.plane,m=Engine.QueryInterface(e,IID_UnitMotion);
        this.T7Check('F04.destroyedFieldLands',m.onGround&&m.GetCurrentSpeed()==0,true);
        this.T7Check('F04.noFriendlyField',Engine.QueryInterface(e,IID_EpochAircraft).FindAirfield(),INVALID_ENTITY);
        ProcessCommand(1,{type:'walk',entities:[e],x:410,z:410,queued:false});
        this.DoAfterDelay(15000,'T7AntiAir',{});
    }catch(e){this.T7Finish(e);}
};
Trigger.prototype.T7AntiAir = function()
{
    try {
        const p=Engine.QueryInterface(this.t7.plane,IID_Position).GetPosition2D();
        this.t7.aa=this.T7Add('structures/epoch_rts/anti_air',p.x+30,p.y,2);
        const a=Engine.QueryInterface(this.t7.aa,IID_Attack);
        this.T7Check('F05.aaAir',a.CanAttack(this.t7.plane,['Ranged']),true);
        const ground=Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager).GetEntitiesByPlayer(1).find(e=>Engine.QueryInterface(e,IID_Identity)?.HasClass('CivCentre'));
        this.T7Check('F05.groundFixtureValid',!!Engine.QueryInterface(ground,IID_Health),true);
        this.T7Check('F05.aaGround',a.CanAttack(ground,['Ranged']),false);
        this.T7Check('F05.aaFriendly',a.CanAttack(this.t7.other,['Ranged']),false);
        this.t7.hp=Engine.QueryInterface(this.t7.plane,IID_Health).GetHitpoints();
        this.DoAfterDelay(10000,'T7End',{});
    }catch(e){this.T7Finish(e);}
};
Trigger.prototype.T7End = function()
{
    try {
        const b=Engine.QueryInterface(this.t7.aa,IID_BuildingAI);this.t7.observations.push({id:'aa-diagnostic',targets:b.targetUnits,round:b.currentRound,arrows:b.arrowsLeft,timer:b.timer,plane:Engine.QueryInterface(this.t7.plane,IID_Position)?.GetPosition(),aa:Engine.QueryInterface(this.t7.aa,IID_Position).GetPosition()});
        const hp=Engine.QueryInterface(this.t7.plane,IID_Health)?.GetHitpoints()||0;
        this.t7.observations.push({id:'F05.aaDamage',before:this.t7.hp,after:hp});
        this.T7Check('F05.aaHit',hp<this.t7.hp,true);
        this.T7Edges();
    }catch(e){this.T7Finish(e);}
};

// Regression cases for taxi-stop, moving targets and airfield ownership changes.
Trigger.prototype.T7Edges = function()
{
    this.t7.fieldA=this.T7Add('structures/epoch_rts/airfield',300,300);
    this.t7.edgePlane=this.T7Add('units/epoch_rts/aircraft',360,300);
    const e=this.t7.edgePlane,a=Engine.QueryInterface(e,IID_EpochAircraft),m=Engine.QueryInterface(e,IID_UnitMotion);
    ProcessCommand(1,{type:'walk',entities:[e],x:450,z:400,queued:false});
    ProcessCommand(1,{type:'stop',entities:[e],queued:false});
    this.T7Check('F03.taxiStopCancelsMovement',m.IsMoveRequested(),false);
    this.T7Check('F06.nonfiniteMoveRejected',a.Move(NaN,Infinity),false);
    ProcessCommand(1,{type:'walk',entities:[e],x:450,z:400,queued:false});
    this.DoAfterDelay(400,'T7TaxiStop',{});
};
Trigger.prototype.T7TaxiStop = function()
{
    try {
        const e=this.t7.edgePlane,m=Engine.QueryInterface(e,IID_UnitMotion);
        this.T7Check('F03.taxiMoving',m.onGround&&m.GetCurrentSpeed()>0,true);
        ProcessCommand(1,{type:'stop',entities:[e],queued:false});
        this.DoAfterDelay(1000,'T7TaxiStopped',{});
    }catch(e){this.T7Finish(e);}
};
Trigger.prototype.T7TaxiStopped = function()
{
    try {this.T7MovingSetup();}catch(e){this.T7Finish(e);}
};
Trigger.prototype.T7MovingSetup = function()
{
    const e=this.t7.edgePlane,m=Engine.QueryInterface(e,IID_UnitMotion);
    this.T7Check('F03.taxiBraked',m.onGround&&m.GetCurrentSpeed()==0&&!m.IsMoveRequested(),true);
    ProcessCommand(1,{type:'walk',entities:[e],x:460,z:400,queued:false});
    ProcessCommand(1,{type:'walk',entities:[e],x:420,z:350,queued:false});
    this.T7Check('F02.latestMoveWins',m.targetX,420);
    this.t7.moving=this.T7Add('units/epoch_rts/pioneer',440,360,2);
    this.t7.initialTarget=Engine.QueryInterface(this.t7.moving,IID_Position).GetPosition2D();
    ProcessCommand(2,{type:'walk',entities:[this.t7.moving],x:520,z:440,queued:false});
    ProcessCommand(1,{type:'attack',entities:[e],target:this.t7.moving,queued:false});
    this.DoAfterDelay(2000,'T7Tracking',{});
};
Trigger.prototype.T7Tracking = function()
{
    try {
        const e=this.t7.edgePlane,m=Engine.QueryInterface(e,IID_UnitMotion),p=Engine.QueryInterface(this.t7.moving,IID_Position).GetPosition2D();
        this.T7Check('F05.targetMoved',p.distanceTo(this.t7.initialTarget)>1,true);
        this.T7Check('F05.tracksMovingTarget',Math.hypot(m.targetX-p.x,m.targetZ-p.y)<4,true);
        ProcessCommand(1,{type:'stop',entities:[e],queued:false});
        this.t7.fieldB=this.T7Add('structures/epoch_rts/airfield',420,300);
        Engine.QueryInterface(this.t7.fieldA,IID_Ownership).SetOwner(2);
        this.DoAfterDelay(1000,'T7Rerouted',{});
    }catch(e){this.T7Finish(e);}
};
Trigger.prototype.T7Rerouted = function()
{
    try {
        const e=this.t7.edgePlane,a=Engine.QueryInterface(e,IID_EpochAircraft);
        this.T7Check('F04.capturedFieldReroutes',a.GetStatus().airfield,this.t7.fieldB);
        this.t7.edgePolls=0;
        this.DoAfterDelay(1000,'T7EdgeLanding',{});
    }catch(e){this.T7Finish(e);}
};
Trigger.prototype.T7EdgeLanding = function()
{
    try {
        const e=this.t7.edgePlane,m=Engine.QueryInterface(e,IID_UnitMotion);
        if(++this.t7.edgePolls>90)throw new Error('Replacement airfield landing timeout');
        if(!m.onGround||m.GetCurrentSpeed()!=0||m.IsMoveRequested()){this.DoAfterDelay(1000,'T7EdgeLanding',{});return;}
        const d=Engine.QueryInterface(e,IID_Position).GetPosition2D().distanceTo(Engine.QueryInterface(this.t7.fieldB,IID_Position).GetPosition2D());
        this.T7Check('F04.replacementLanding',d<=90,true);
        for(let i=0;i<10;++i)ProcessCommand(1,{type:'stop',entities:[e],queued:false});
        this.T7Check('F06.groundedRepeatedStop',m.onGround&&!m.IsMoveRequested()&&m.GetCurrentSpeed()==0,true);
        this.T7Finish();
    }catch(e){this.T7Finish(e);}
};

// Interactive demo: only fixture setup is automated; GUI acceptance is recorded separately.
Trigger.prototype.T7Demo = function()
{
    this.t7.airfield=this.T7Add('structures/epoch_rts/airfield',300,300);
    this.t7.plane=this.T7Add('units/epoch_rts/aircraft',335,310);
    this.t7.target=this.T7Add('structures/epoch_rts/house',420,350,2);
    this.t7.aa=this.T7Add('structures/epoch_rts/anti_air',500,410,2);
    Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager).SetLosRevealAll(1,true);
    this.T7Check('demo.fixturesOnly',!!Engine.QueryInterface(this.t7.plane,IID_EpochAircraft),true);
    this.T7Finish();
};
