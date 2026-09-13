// Purpose: Route only aircraft commands; preserve all non-aircraft commands. Created: 2026-09-13.
// SPDX-License-Identifier: GPL-2.0-or-later
{
    for(const type of ['walk','attack','stop']) {
        const upstream=g_Commands[type];
        g_Commands[type]=function(player,cmd,data) {
            const ordinary=[];
            for(const entity of data.entities) {
                const aircraft=Engine.QueryInterface(entity,IID_EpochAircraft);
                if(!aircraft){ordinary.push(entity);continue;}
                if(Engine.QueryInterface(entity,IID_Ownership)?.GetOwner()!=player)continue;
                if(type=='walk')aircraft.Move(cmd.x,cmd.z);
                else if(type=='attack')aircraft.AttackGround(cmd.target);
                else aircraft.Return();
            }
            if(ordinary.length)return upstream(player,{...cmd,entities:ordinary},{...data,entities:ordinary});
        };
    }
    g_Commands['epoch-air-return']=function(player,cmd,data) {
        for(const entity of data.entities)
            if(Engine.QueryInterface(entity,IID_Ownership)?.GetOwner()==player)
                Engine.QueryInterface(entity,IID_EpochAircraft)?.Return(cmd.target);
    };
}
