// Purpose: R28 combat/boundary fixtures and command-only standard match. Created: 2026-09-10.
// SPDX-License-Identifier: GPL-2.0-or-later
// Only fixture modes add entities/resources or apply direct damage. Full uses normal commands.
Trigger.prototype.T6Check = function(id, actual, expected)
{
    const stable = x => x && typeof x == 'object' ? (Array.isArray(x) ? x.map(stable) : Object.fromEntries(Object.keys(x).sort().map(k=>[k,stable(x[k])]))) : x;
    const passed = JSON.stringify(stable(actual)) == JSON.stringify(stable(expected));
    this.t6.checks.push(JSON.parse(JSON.stringify({id,actual,expected,passed})));
    if (!passed) throw new Error(id+': '+JSON.stringify(actual)+' != '+JSON.stringify(expected));
};
Trigger.prototype.T6Finish = function(error)
{
    if (this.t6.finished) return;
    this.t6.finished = true;
    const result='EPOCH_TEST_RESULT '+JSON.stringify({passed:!error,checks:this.t6.checks,failure:error?String(error):null,mode:this.t6Mode,events:this.t6.events,steps:this.t6.steps,seconds:Engine.QueryInterface(SYSTEM_ENTITY,IID_Timer).GetTime()/1000});
    for(let i=0;i<result.length;i+=4096) print(result.slice(i,i+4096));
};
Trigger.prototype.T6Won = function(m) { if(this.t6)this.t6.events.push({event:'won',player:m.playerId,time:Engine.QueryInterface(SYSTEM_ENTITY,IID_Timer).GetTime()}); };
Trigger.prototype.T6Defeated = function(m) { if(this.t6){this.t6.events.push({event:'defeated',player:m.playerId,time:Engine.QueryInterface(SYSTEM_ENTITY,IID_Timer).GetTime()});if(this.t6Mode=='full')this.T6FullTick();} };
Trigger.prototype.T6Start = function()
{
    this.t6={checks:[],events:[],steps:[]};
    try {
        const Q=(e,i)=>Engine.QueryInterface(e,i), owned=p=>Q(SYSTEM_ENTITY,IID_RangeManager).GetEntitiesByPlayer(p), tm=Q(SYSTEM_ENTITY,IID_TemplateManager);
        this.t6.centres=[1,2].map(p=>owned(p).find(e=>tm.GetCurrentTemplateName(e)=='structures/epoch_rts/civil_centre'));
        this.T6Check('baseline.conquest',this.conquestQueries.map(q=>q.classFilter),['ConquestCritical+!Foundation']);
        for(const p of [1,2]) {
            this.T6Check('opening.resources.'+p,QueryPlayerIDInterface(p).GetResourceCounts(),{food:300,wood:250,stone:100,metal:0});
            this.T6Check('opening.population.'+p,[QueryPlayerIDInterface(p).GetPopulationCount(),QueryPlayerIDInterface(p).GetPopulationLimit(),QueryPlayerIDInterface(p).GetMaxPopulation()],[8,20,100]);
            this.T6Check('opening.age.'+p,[QueryPlayerIDInterface(p,IID_TechnologyManager).IsTechnologyResearched('phase_epoch_bronze'),QueryPlayerIDInterface(p,IID_TechnologyManager).IsTechnologyResearched('phase_epoch_iron')],[true,false]);
            this.T6Check('opening.entities.'+p,owned(p).filter(e=>Q(e,IID_Position)).length,9);
            this.T6Check('opening.critical.'+p,owned(p).filter(e=>Q(e,IID_Identity)?.HasClass('ConquestCritical')),[this.t6.centres[p-1]]);
        }
        if(this.t6Mode=='full'){this.t6.enemyWorkers=owned(2).filter(e=>tm.GetCurrentTemplateName(e)=='units/epoch_rts/pioneer');this.T6FullStart();return;}
        for(const p of [1,2]) ProcessCommand(p,{type:'stance',entities:owned(p).filter(e=>Q(e,IID_UnitAI)),name:'standground'});
        if(this.t6Mode=='combat'){this.T6Combat();return;}
        const add=(name,p,x,z)=>{const e=Engine.AddEntity(name);Q(e,IID_Position).JumpTo(x,z);Q(e,IID_Ownership).SetOwner(p);return e;};
        this.t6.house=add('structures/epoch_rts/house',2,400,400);
        this.t6.worker=owned(2).find(e=>tm.GetCurrentTemplateName(e)=='units/epoch_rts/pioneer');
        if(this.t6Mode=='research') {
            add('structures/epoch_rts/barracks',1,360,360);
            QueryPlayerIDInterface(1).SetResourceCounts({food:400,wood:200,stone:0,metal:100});
            ProcessCommand(1,{type:'research',entity:this.t6.centres[0],template:'phase_epoch_iron'});
            this.T6Check('research.paid',QueryPlayerIDInterface(1).GetResourceCounts(),{food:0,wood:0,stone:0,metal:0});
            this.T6Check('research.queued',Q(this.t6.centres[0],IID_ProductionQueue).GetQueue().length,1);
            this.DoAfterDelay(59000,'T6Kill',{});
        } else this.T6Kill();
    }catch(e){this.T6Finish(e);}
};
Trigger.prototype.T6Kill = function()
{
    try {
        const Q=(e,i)=>Engine.QueryInterface(e,i),mode=this.t6Mode;
        if(mode=='research'){this.T6Check('research.pending',QueryPlayerIDInterface(1,IID_TechnologyManager).IsTechnologyResearched('phase_epoch_iron'),false);this.T6Check('research.positiveProgress',QueryPlayerIDInterface(1,IID_TechnologyManager).GetQueuedResearch().get('phase_epoch_iron').timeRemaining<60000,true);this.T6Check('research.started',QueryPlayerIDInterface(1,IID_TechnologyManager).GetQueuedResearch().get('phase_epoch_iron').started,true);}
        const order=mode=='double12'?[1,2]:mode=='double21'?[2,1]:[mode=='victory'?2:1];
        if(mode=='resign')ProcessCommand(1,{type:'resign'});
        else for(const p of order){this.t6.events.push({event:'lethal',player:p,time:Q(SYSTEM_ENTITY,IID_Timer).GetTime()});Q(this.t6.centres[p-1],IID_Health).Reduce(10000);}
        Engine.FlushDestroyedEntities();
        this.T6BoundaryResult();
    }catch(e){this.T6Finish(e);}
};
Trigger.prototype.T6BoundaryResult = function()
{
    try {
        const Q=(e,i)=>Engine.QueryInterface(e,i),mode=this.t6Mode;
        const winner=mode=='victory'||mode=='double21'?1:2;
        this.T6Check('boundary.states',[1,2].map(p=>QueryPlayerIDInterface(p).GetState()),[1,2].map(p=>p==winner?'won':'defeated'));
        this.T6Check('boundary.singleWin',this.t6.events.filter(e=>e.event=='won').length,1);
        this.T6Check('boundary.singleDefeat',this.t6.events.filter(e=>e.event=='defeated').length,1);
        if(mode.startsWith('double'))this.T6Check('boundary.bothCentresDestroyed',this.t6.centres.map(e=>!!Q(e,IID_Health)),[false,false]);
        if(mode=='victory')this.T6Check('boundary.survivors',[this.t6.house,this.t6.worker].map(e=>Q(e,IID_Health).GetHitpoints()>0),[true,true]);
        if(mode=='research'){
            this.T6Check('research.noCompletion',QueryPlayerIDInterface(1,IID_TechnologyManager).IsTechnologyResearched('phase_epoch_iron'),false);
            this.T6Check('research.queueCleared',QueryPlayerIDInterface(1,IID_TechnologyManager).GetQueuedResearch().size,0);
            this.T6Check('research.refund',QueryPlayerIDInterface(1).GetResourceCounts(),{food:400,wood:200,stone:0,metal:100});
        }
        this.T6Finish();
    }catch(e){this.T6Finish(e);}
};
Trigger.prototype.T6Combat = function()
{
    const Q=(e,i)=>Engine.QueryInterface(e,i);
    this.t6.fighters=[];
    for(const [name,hp] of [['civil_centre',1000],['house',300],['storehouse',400],['barracks',600],['field',200],['forge',500]]){
        const e=Engine.AddEntity('structures/epoch_rts/'+name);
        this.T6Check(name+'.HP',Q(e,IID_Health).GetMaxHitpoints(),hp);
        this.T6Check(name+'.resistance',Q(e,IID_Resistance).GetEffectiveResistanceAgainst('Damage').Damage,{Hack:5,Pierce:8,Crush:5});
        this.T6Check(name+'.noAttack',!!Q(e,IID_Attack),false);
        Engine.DestroyEntity(e);
    }
    Engine.FlushDestroyedEntities();
    const rows=[['pioneer',40,2,0,0,0],['spearman',100,6,1,2,0],['slinger',60,4,0,1,0],['iron_swordsman',140,10,2,3,0]];
    for(let j=0;j<rows.length;j++){
        const [name,hp,dmg,h,p,c]=rows[j],type=name=='slinger'?'Ranged':'Melee';
        const e=Engine.AddEntity('units/epoch_rts/'+name),target=Engine.AddEntity('structures/epoch_rts/house');
        Q(e,IID_Position).JumpTo(320+j*35,380);Q(e,IID_Ownership).SetOwner(1);
        Q(target,IID_Position).JumpTo(320+j*35,390);Q(target,IID_Ownership).SetOwner(2);
        const a=Q(e,IID_Attack);
        this.T6Check(name+'.HP',Q(e,IID_Health).GetMaxHitpoints(),hp);
        this.T6Check(name+'.damage',a.GetAttackEffectsData(type).Damage,{Hack:type=='Melee'?dmg:0,Pierce:type=='Ranged'?dmg:0,Crush:0});
        this.T6Check(name+'.timers',a.GetTimers(type),{prepare:500,repeat:type=='Ranged'?1500:1000});
        this.T6Check(name+'.range',a.GetRange(type),{min:0,max:type=='Ranged'?40:3});
        this.T6Check(name+'.resistance',Q(e,IID_Resistance).GetEffectiveResistanceAgainst('Damage').Damage,{Hack:h,Pierce:p,Crush:c});
        this.T6Check(name+'.types',a.GetAttackTypes(),[type]);
        this.T6Check(name+'.noPromotion',!!Q(e,IID_Promotion),false);
        this.T6Check(name+'.noBonus',!!a.template[type].Bonuses,false);
        this.T6Check(name+'.noSplash',!!a.GetSplashData(type),false);
        this.T6Check(name+'.canAttackBuilding',a.CanAttack(target,[type]),true);
        this.T6Check(name+'.buildingResistance',Q(target,IID_Resistance).GetEffectiveResistanceAgainst('Damage').Damage,{Hack:5,Pierce:8,Crush:5});
        ProcessCommand(1,{type:'attack',entities:[e],target,allowCapture:false,queued:false});
        this.t6.fighters.push({name,e,target,dmg,type});
    }
    this.DoAfterDelay(12000,'T6CombatResult',{});
};
Trigger.prototype.T6CombatResult = function()
{
    try{
        for(const f of this.t6.fighters){
            const health=Engine.QueryInterface(f.target,IID_Health),loss=300-health.GetHitpoints(),perHit=f.dmg*Math.pow(0.9,f.type=='Ranged'?8:5);
            this.T6Check(f.name+'.realHit',loss>0,true);
            this.T6Check(f.name+'.damageFormula',Math.abs(loss/perHit-Math.round(loss/perHit))<0.00001,true);
            this.t6.steps.push({unit:f.name,loss,perHit,hits:Math.round(loss/perHit)});
        }
        this.T6Finish();
    }catch(e){this.T6Finish(e);}
};
Trigger.prototype.T6FullStart = function()
{
    this.t6.phase=0;this.t6.ticks=0;this.t6.jobs={};this.t6.constructAttempt=0;
    this.T6FullTick();
};
Trigger.prototype.T6FullTick = function()
{
    if(this.t6.finished)return;
    try{
        const t=this.t6,Q=(e,i)=>Engine.QueryInterface(e,i),rm=Q(SYSTEM_ENTITY,IID_RangeManager),tm=Q(SYSTEM_ENTITY,IID_TemplateManager),owned=p=>rm.GetEntitiesByPlayer(p),name=e=>tm.GetCurrentTemplateName(e),find=s=>owned(1).find(e=>name(e)=='structures/epoch_rts/'+s),units=s=>owned(1).filter(e=>name(e)=='units/epoch_rts/'+s),manager=QueryPlayerIDInterface(1,IID_TechnologyManager),r=QueryPlayerIDInterface(1).GetResourceCounts(),centre=t.centres[0],pos=Q(centre,IID_Position).GetPosition2D();
        const log=step=>{t.steps.push({step,seconds:Q(SYSTEM_ENTITY,IID_Timer).GetTime()/1000,resources:{...r}});print('EPOCH_T06_STEP '+JSON.stringify(t.steps[t.steps.length-1]));};
        if(++t.ticks>3600)throw new Error('Full match timeout phase '+t.phase+' resources '+JSON.stringify(r));
        if(QueryPlayerIDInterface(1).GetState()=='defeated')throw new Error('Full player defeated');
        const workers=units('pioneer');
        // Economy controller only issues normal player commands, chooses nearest known local supply.
        workers.forEach((e,i)=>{
            if(Q(e,IID_UnitAI).GetCurrentState().includes('REPAIR')||Q(e,IID_UnitAI).GetCurrentState().includes('BUILD'))return;
            const type=i<3?'food':i<6?'metal':i<9?'wood':r.stone<100?'stone':'food';
            const a=Q(e,IID_UnitAI),idle=a.IsIdle();
            if(t.jobs[e]==type&&!idle)return;
            const supplies=owned(0).filter(s=>{const rs=Q(s,IID_ResourceSupply);return rs&&rs.GetType().generic==type&&rs.GetCurrentAmount()>0&&Q(s,IID_Position)?.IsInWorld();}).sort((a,b)=>Q(a,IID_Position).GetPosition2D().distanceTo(pos)-Q(b,IID_Position).GetPosition2D().distanceTo(pos));
            if(supplies.length){ProcessCommand(1,{type:'gather',entities:[e],target:supplies[0],queued:false});t.jobs[e]=type;}
        });
        const train=(building,unit)=>ProcessCommand(1,{type:'train',entities:[building],template:'units/epoch_rts/'+unit,count:1});
        const build=(kind)=>{
            if(owned(1).some(e=>name(e)=='foundation|structures/epoch_rts/'+kind))return;
            const k=t.constructAttempt++,angle=k*2.39996,rad=55+Math.floor(k/12)*12;
            ProcessCommand(1,{type:'construct',entities:[workers[workers.length-1]],template:'structures/epoch_rts/'+kind,x:pos.x+Math.cos(angle)*rad,z:pos.y+Math.sin(angle)*rad,angle:0,autorepair:true,autocontinue:false,queued:false});
        };
        if(t.phase==0){log('standard-opening');ProcessCommand(2,{type:'stance',entities:owned(2).filter(e=>Q(e,IID_UnitAI)),name:'standground'});t.phase=1;}
        if(t.phase==1){
            if(workers.length<12&&r.food>=50&&!Q(centre,IID_ProductionQueue).GetQueue().length)train(centre,'pioneer');
            if(!find('barracks')&&r.wood>=150&&r.stone>=50)build('barracks');
            if(workers.length>=12&&find('barracks')){log('gather-build-barracks-workers');t.phase=2;}
        }
        else if(t.phase==2){
            const b=find('barracks');if(!units('slinger').length&&r.food>=40&&r.wood>=40&&!Q(b,IID_ProductionQueue).GetQueue().length)train(b,'slinger');
            if(units('slinger').length&&r.food>=400&&r.wood>=200&&r.metal>=100){ProcessCommand(1,{type:'research',entity:centre,template:'phase_epoch_iron'});log('iron-paid');t.phase=3;}
        }
        else if(t.phase==3&&manager.IsTechnologyResearched('phase_epoch_iron')){log('iron-complete');t.phase=4;}
        else if(t.phase==4){if(!find('forge')&&r.wood>=150&&r.stone>=100)build('forge');if(find('forge')){log('forge-built');t.phase=5;}}
        else if(t.phase==5&&r.food>=100&&r.metal>=100){ProcessCommand(1,{type:'research',entity:find('forge'),template:'epoch_forged_weapons'});log('weapons-paid');t.phase=6;}
        else if(t.phase==6&&manager.IsTechnologyResearched('epoch_forged_weapons')){log('weapons-complete');t.phase=7;}
        else if(t.phase==7){
            if(!find('house')&&r.wood>=50)build('house');
            const b=find('barracks');if(units('iron_swordsman').length<6&&r.food>=80&&r.metal>=40&&!Q(b,IID_ProductionQueue).GetQueue().length)train(b,'iron_swordsman');
            if(units('iron_swordsman').length>=6){log('army-trained');const dest=Q(t.centres[1],IID_Position).GetPosition2D();ProcessCommand(1,{type:'attack-walk',entities:[...units('iron_swordsman'),...units('spearman'),...units('slinger')],x:dest.x,z:dest.y,targetClasses:{attack:['Unit','Structure']},allowCapture:false,queued:false});t.phase=8;}
        }
        else if(t.phase==8&&QueryPlayerIDInterface(1).GetState()=='won'){
            log('victory');this.T6Check('full.enemyCentreDead',Q(t.centres[1],IID_Health)?.GetHitpoints()||0,0);t.steps.push({step:'enemy-workers-alive-at-victory',count:t.enemyWorkers.filter(e=>Q(e,IID_Health)?.GetHitpoints()>0).length});this.T6Check('full.states',[1,2].map(p=>QueryPlayerIDInterface(p).GetState()),['won','defeated']);this.T6Check('full.technologies',[manager.IsTechnologyResearched('phase_epoch_iron'),manager.IsTechnologyResearched('epoch_forged_weapons')],[true,true]);this.T6Check('full.singleWin',t.events.filter(e=>e.event=='won').length,1);this.T6Finish();return;
        }
        this.DoAfterDelay(1000,'T6FullTick',{});
    }catch(e){this.T6Finish(e);}
};
{
    const t=Engine.QueryInterface(SYSTEM_ENTITY,IID_Trigger);
    t.RegisterTrigger('OnPlayerWon','T6Won',{enabled:true});
    t.RegisterTrigger('OnPlayerDefeated','T6Defeated',{enabled:true});
    t.DoAfterDelay(1000,'T6Start',{});
}
