// Purpose: Reproducible UI research fixture; not a standard opening. Created: 2026-09-08.
// SPDX-License-Identifier: GPL-2.0-or-later
Trigger.prototype.EpochResearchDemo = function()
{
    QueryPlayerIDInterface(1).SetResourceCounts({food:1000,wood:1000,stone:1000,metal:1000});
    const tm=Engine.QueryInterface(SYSTEM_ENTITY,IID_TemplateManager);
    const centre=Engine.QueryInterface(SYSTEM_ENTITY,IID_RangeManager).GetEntitiesByPlayer(1).find(e=>tm.GetCurrentTemplateName(e)=="structures/epoch_rts/civil_centre");
    const pos=Engine.QueryInterface(centre,IID_Position).GetPosition2D();
    const barracks=Engine.AddEntity("structures/epoch_rts/barracks");
    Engine.QueryInterface(barracks,IID_Position).JumpTo(pos.x-65,pos.y+55);
    Engine.QueryInterface(barracks,IID_Ownership).SetOwner(1);
};
Engine.QueryInterface(SYSTEM_ENTITY,IID_Trigger).DoAfterDelay(1,"EpochResearchDemo",{});
