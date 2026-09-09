// Purpose: Enforce the epoch builder whitelist and prerequisites before any payment. Created: 2026-09-07.
// SPDX-License-Identifier: GPL-2.0-or-later
{
	const upstreamConstruct = g_Commands.construct;
	g_Commands.construct = function(player, cmd, data)
	{
		if (QueryPlayerIDInterface(player, IID_Identity)?.GetCiv() != "epoch")
			return upstreamConstruct(player, cmd, data);

		// R28 construction does not enforce Builder/Entities, and its failed
		// technology check does not return before payment. Reject both here.
		const builders = data.entities.filter(ent =>
			Engine.QueryInterface(ent, IID_Builder)?.GetEntitiesList().includes(cmd.template));
		if (!builders.length || !QueryPlayerIDInterface(player, IID_TechnologyManager).CanProduce(cmd.template))
		{
			Engine.QueryInterface(SYSTEM_ENTITY, IID_GuiInterface).PushNotification({
				"type": "text", "players": [player],
				"message": "Cannot build: select a suitable worker and meet the age requirements.",
				"translateMessage": true
			});
			return;
		}

		// Preview uses the native oriented footprint to detect construction-blocking
		// units. Do not change Unit obstruction flags (R28 fixes those in its schema).
		const preview = Engine.AddEntity("preview|" + cmd.template);
		if (preview == INVALID_ENTITY)
		    return;
		const position = Engine.QueryInterface(preview, IID_Position);
		position.JumpTo(cmd.x, cmd.z);
		position.SetYRotation(cmd.angle);
		const occupied = Engine.QueryInterface(preview, IID_Obstruction).GetEntitiesBlockingConstruction().length > 0;
		position.MoveOutOfWorld();
		Engine.DestroyEntity(preview);
		if (occupied)
		{
		    Engine.QueryInterface(SYSTEM_ENTITY, IID_GuiInterface).PushNotification({
		        "type": "text", "players": [player], "message": "Units occupy the building site. Move them away first.", "translateMessage": true
		    });
		    return;
		}
		return upstreamConstruct(player, { ...cmd, "entities": builders }, { ...data, "entities": builders });
	};
}

// R28 single-entity research commands bypass FilterEntityList. Scope validation
// to epoch games, including cancellation, before touching another player's queue.
{
    for (const type of ["research", "stop-production"])
    {
        const upstream = g_Commands[type];
        g_Commands[type] = function(player, cmd, data)
        {
            if (QueryPlayerIDInterface(player, IID_Identity)?.GetCiv() != "epoch")
                return upstream(player, cmd, data);
            if (Engine.QueryInterface(cmd.entity, IID_Ownership)?.GetOwner() != player)
                return;
            if (type == "research" &&
                (Engine.QueryInterface(cmd.entity, IID_Foundation) ||
                 !Engine.QueryInterface(cmd.entity, IID_Researcher)?.GetTechnologiesList().includes(cmd.template)))
                return;
            return upstream(player, cmd, data);
        };
    }
}
