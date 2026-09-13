// Purpose: Airfield return and ground-attack control for the isolated air prototype. Created: 2026-09-13.
// SPDX-License-Identifier: GPL-2.0-or-later
function EpochAircraft() {}
EpochAircraft.prototype.Schema = '<empty/>';
EpochAircraft.prototype.Init = function()
{
    this.order='ground';
    this.airfield=INVALID_ENTITY;
    this.attackTarget=INVALID_ENTITY;
    this.nextShot=0;
};
EpochAircraft.prototype.IsAirfield = function(entity)
{
    const owner=Engine.QueryInterface(this.entity,IID_Ownership)?.GetOwner();
    return owner>0 && Engine.QueryInterface(entity,IID_Ownership)?.GetOwner()==owner &&
        Engine.QueryInterface(entity,IID_Identity)?.HasClass('EpochAirfield') &&
        !Engine.QueryInterface(entity,IID_Foundation) &&
        Engine.QueryInterface(entity,IID_Health)?.GetHitpoints()>0 &&
        Engine.QueryInterface(entity,IID_Position)?.IsInWorld();
};
EpochAircraft.prototype.FindAirfield = function()
{
    const owner=Engine.QueryInterface(this.entity,IID_Ownership)?.GetOwner();
    if(!(owner>0))return INVALID_ENTITY;
    const pos=Engine.QueryInterface(this.entity,IID_Position).GetPosition2D();
    const entities=Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager).GetEntitiesByPlayer(owner).filter(e=>this.IsAirfield(e));
    entities.sort((a,b)=>{
        const d=Engine.QueryInterface(a,IID_Position).GetPosition2D().distanceTo(pos)-Engine.QueryInterface(b,IID_Position).GetPosition2D().distanceTo(pos);
        return d||a-b;
    });
    return entities[0]||INVALID_ENTITY;
};
EpochAircraft.prototype.Move = function(x,z)
{
    if(!Number.isFinite(x)||!Number.isFinite(z))return false;
    const motion=Engine.QueryInterface(this.entity,IID_UnitMotion);
    if(!motion.MoveToPointRange(x,z,0,15))return false;
    this.order='move';this.airfield=INVALID_ENTITY;this.attackTarget=INVALID_ENTITY;
    return true;
};
EpochAircraft.prototype.AttackGround = function(target)
{
    const attack=Engine.QueryInterface(this.entity,IID_Attack);
    if(!attack?.CanAttack(target,['Ranged']))return false;
    const pos=Engine.QueryInterface(target,IID_Position).GetPosition2D();
    if(!this.Move(pos.x,pos.y))return false;
    this.order='attack';this.attackTarget=target;
    this.nextShot=Math.max(this.nextShot,Engine.QueryInterface(SYSTEM_ENTITY,IID_Timer).GetTime()+attack.GetTimers('Ranged').prepare);
    return true;
};
EpochAircraft.prototype.Return = function(target=INVALID_ENTITY)
{
    if(target!=INVALID_ENTITY&&!this.IsAirfield(target))return false;
    if(this.order=='return' && (target==INVALID_ENTITY||target==this.airfield))return true;
    this.order='return';this.attackTarget=INVALID_ENTITY;
    this.airfield=target!=INVALID_ENTITY?target:this.FindAirfield();
    const motion=Engine.QueryInterface(this.entity,IID_UnitMotion);
    if(this.airfield==INVALID_ENTITY)motion.Land();
    else {
        const p=Engine.QueryInterface(this.airfield,IID_Position).GetPosition2D();
        if(!motion.onGround)motion.MoveToPointRange(p.x,p.y,0,30);
        else if(Engine.QueryInterface(this.entity,IID_Position).GetPosition2D().distanceTo(p)>90)
            motion.MoveToPointRange(p.x,p.y,0,30);
        else motion.Land();
    }
    return true;
};
EpochAircraft.prototype.OnUpdate = function()
{
    const pos=Engine.QueryInterface(this.entity,IID_Position);
    if(!pos?.IsInWorld())return;
    const motion=Engine.QueryInterface(this.entity,IID_UnitMotion);
    if(this.order=='return') {
        if(!this.IsAirfield(this.airfield)) {
            const replacement=this.FindAirfield();
            if(replacement!=this.airfield) {
                this.airfield=replacement;
                if(replacement!=INVALID_ENTITY) {
                    const p=Engine.QueryInterface(replacement,IID_Position).GetPosition2D();
                    motion.MoveToPointRange(p.x,p.y,0,30);
                }
            }
            if(replacement==INVALID_ENTITY)motion.Land();
        }
        if(this.IsAirfield(this.airfield)) {
            const destination=Engine.QueryInterface(this.airfield,IID_Position).GetPosition2D();
            if(pos.GetPosition2D().distanceTo(destination)<45)motion.Land();
        }
        if(motion.onGround&&motion.GetCurrentSpeed()==0&&!motion.IsMoveRequested())this.order='ground';
    }
    if(this.order!='attack')return;
    const attack=Engine.QueryInterface(this.entity,IID_Attack);
    if(!attack.CanAttack(this.attackTarget,['Ranged'])){this.Return();return;}
    const targetPos=Engine.QueryInterface(this.attackTarget,IID_Position).GetPosition2D();
    motion.MoveToPointRange(targetPos.x,targetPos.y,0,15);
    const now=Engine.QueryInterface(SYSTEM_ENTITY,IID_Timer).GetTime();
    if(!motion.onGround&&attack.IsTargetInRange(this.attackTarget,'Ranged')&&now>=this.nextShot) {
        attack.PerformAttack('Ranged',this.attackTarget);
        this.nextShot=now+attack.GetRepeatTime('Ranged');
    }
};
EpochAircraft.prototype.GetStatus = function()
{
    const motion=Engine.QueryInterface(this.entity,IID_UnitMotion);
    return {order:this.order,airfield:this.airfield,attackTarget:this.attackTarget,onGround:motion.onGround,landing:motion.landing,speed:motion.GetCurrentSpeed()};
};
Engine.RegisterComponentType(IID_EpochAircraft,'EpochAircraft',EpochAircraft);
