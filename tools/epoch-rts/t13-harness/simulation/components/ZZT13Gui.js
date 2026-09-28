// Purpose: Expose only a read-only test snapshot in the opt-in harness. Created: 2026-09-27.
// SPDX-License-Identifier: GPL-2.0-or-later
GuiInterface.prototype.exposedFunctions.T13Snapshot = 1;
GuiInterface.prototype.T13Snapshot = function() { return T13Snapshot(); };
GuiInterface.prototype.exposedFunctions.T13NetworkDone = 1;
GuiInterface.prototype.T13NetworkDone = function() {
    return !!Engine.QueryInterface(SYSTEM_ENTITY, IID_Trigger).t13NetworkDone;
};
