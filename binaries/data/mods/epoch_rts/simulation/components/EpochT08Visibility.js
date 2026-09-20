// Purpose: T08 opt-in visibility API experiment, not a production controller. Created: 2026-09-20.
// SPDX-License-Identifier: GPL-2.0-or-later
function EpochT08Visibility() {}
EpochT08Visibility.prototype.Schema = "<empty/>";
EpochT08Visibility.prototype.Init = function() { this.submerged = false; this.detector = INVALID_ENTITY; this.active = false; };
EpochT08Visibility.prototype.IsActivated = function() { return this.active; };
EpochT08Visibility.prototype.GetRetainInFog = function() { return false; };
EpochT08Visibility.prototype.GetAlwaysVisible = function() { return false; };
EpochT08Visibility.prototype.GetVisibility = function(player, isVisible, isExplored)
{
    const owner = Engine.QueryInterface(this.entity, IID_Ownership).GetOwner();
    if (player == owner) return 2;
    if (!isVisible) return 0;
    if (!this.submerged) return 2;
    const detectorPos = Engine.QueryInterface(this.detector, IID_Position);
    const detectorOwner = Engine.QueryInterface(this.detector, IID_Ownership);
    const health = Engine.QueryInterface(this.detector, IID_Health);
    const position = Engine.QueryInterface(this.entity, IID_Position);
    return detectorPos && detectorPos.IsInWorld() && detectorOwner && detectorOwner.GetOwner() == player &&
        health && health.GetHitpoints() > 0 && position.GetPosition2D().distanceTo(detectorPos.GetPosition2D()) <= 60 ? 2 : 0;
};
EpochT08Visibility.prototype.Activate = function()
{
    this.active = true;
    Engine.QueryInterface(SYSTEM_ENTITY, IID_RangeManager).ActivateScriptedVisibility(this.entity, true);
};
Engine.RegisterComponentType(IID_Visibility, "EpochT08Visibility", EpochT08Visibility);
