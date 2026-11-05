<!-- Purpose: six non-time fields exact producer/getter/precommit matrix. Created: 2026-10-26. -->
# 六欄位來源計畫：可確定 source chain；expected-controls 實作／runtime 全 OPEN

唯一 comparator是85f93c30ba9484b2cce4129e0ec930b7f85449ef7d5e363da94ae8814a4b4d30所核 t17_save_metadata.validate_metadata(actual_raw, expected_without_time_raw, earliest_epoch,latest_epoch)。Actual頂層exact7keys；expected exact6keys，只有最外層time由獨立wallclock interval驗，其餘完整值含nested timestamp、未知key、全部mods、gui/camera逐值比較。Status只MATCH_METADATA_VALUES_ONLY，沒有認證expected來源或future schedule absence。此scope不修改comparator，不重跑其DONE tests。

以下原生source行號指primaryrefs/source/；GUI current source ec8c8a23d79b7f6e4fce11230b4a6f25a5c89861d2518a3a3de0b3522408e885，map-script-fix06a9已另雙核source-only。Plan/current source結論均不等actualengine測量。

| 欄位 | 真正 metadata producer | 獨立 expected 候選／預承諾順序 | 已知 vs OPEN |
|---|---|---|---|
| engine_version | SavedGame.cpp91–96使用native engine_version symbol | 先鎖實際binary/profile，再source-owned Engine.GetEngineInfo()完整control（JSInterface_Mod.cpp113–131用同symbol），先於Save/actualmetadata讀取；與預承諾runtime/build identity核對 | Getter機制可得；本次實際getter、編譯常數值／版本映射、caller/realm/raw/control provenance未固定。不能用package版本猜engine_version。OPEN |
| playerID | SavedGame.cpp94直接g_Game->GetPlayerID | Plan固定literal1；Save前後真Engine.GetPlayerID native讀回（JSInterface_Game.cpp64ff），完整returned receipt後restore1；不得拿nativeQueryCaller或payload.player替代 | 現GUI本身有principal邊界檢查，但host獨立capture/phase/runtime closure未實作。OPEN |
| mods | SavedGame.cpp84–85：g_Mods.GetEnabledModsData→ToJSVal | Plan先固定五mod預期order/四欄records；GetEngineInfo同nativegetter可獨立核對並在Save前封存，來源為實際ModData／精確mod.json與native選擇鏈 | Mod.cpp184–203依enabled順序，排除internal mod/user，並不按ignoreInCompatibilityChecks剔除。每筆完整{mod,name,version,ignoreInCompatibilityChecks}（JSInterface_Mod.cpp35–42）。實際五mod選擇／版本／bool與useroverride/profile還OPEN，不把static candidate當runtime |
| initAttributes | SavedGame.cpp83 simulation.GetInitAttributes() | 靜態base由已核GUI initialAttrs+immutable boot independently建立，含top-level script。再明確處理Replay新增3key；候選官方native GetInitAttributes完整getter或本次preSave replay start raw，必先驗完整producer/realm/phase/來源，不從metadata取expected | GUI literal不是最終fullattrs。Replay.cpp71–90在origin與load重寫timestamp/engine_version/mods；nested timestamp必exact保留。所有其餘setup/script writer不變性及capture尚OPEN |
| gui | 官方getSavedGameData返回groups；JSInterface_SavedGame.cpp44–49先structuredclone；SavedGame.cpp98–119讀clone、用nativecamera六值覆加camera | Plan源碼固定10emptygroups；獨立nativecamera gettercontrol在Save前建立，full exact{groups,camera}對比；load需已獨立驗過origin controls的lineage及fresh getter，不能採roundtrip metadata自建expected | Groups建構／restore/update來源可讀。未證實際沒有human/controlgroup mutation、constructor/prototype/serialization effects；camera bit/quantization與load roundtrip純度／實際controls OPEN |
| description | GUItransaction177：'T17 save '+phase+' '+checkpoint；nativeSave接原wstring SavedGame.cpp120 | host以預承諾phase(origin/load)+五checkpoint literal直接derive exact string，與exactcase/ordinal相綁，不讀metadata.description | 靜態完整producer可確定。實際一次Save呼叫參數／nativecaller/raw phase綁定未執行；尚無hostcontrolfactory。OPEN |

## Origin／load 完整callorder

Origin：GUI ReadBoot/StartFromBoot用source-owned init literal（mapType/map/**script:'epoch_t17_save_six.js'**/settings，binding內campaign/source/seed）→JSI_Game.StartGame39–55 newCGame(defaultscripts)→clone attrs到simulation→CGame.StartGame382–388先ReplayLogger.StartGame→Replay.cpp71–90原地覆加timestamp/engine_version/mods→RegisterInit→SetInitAttributes/Game.cpp219→map/player/settings startup→Simulation2.LoadMapSettings843–859 freeze attrs並SetGlobal InitAttributes→GUI原init／origin-only nominalcamera setter／independentgetter CAMERA_READBACK→固定transaction Pause/A→SaveGame(getSavedGameData())→structuredclone GUI→SavedGames::Save先native top-time、SerializeState，再取fullinit/mod/player、GUIclone+nativecamera、description→native stringify/archive。Exact metadata getter讀取順序不可假定都在Serialize之前。

Load：獨立驗證origin archive及其expected metadata control→host prelaunch只複製已驗origin原bytes（本計畫未執行copy）→JSI_SavedGame.StartSavedGame78–115讀archive metadata→newCGame(true)/defaultscripts→clone原metadata attrs到sim→恢復native playerID→CGame.StartGame仍呼ReplayLogger，**新load timestamp/nativeengine/mods覆寫原attrs三key**→RegisterInit/Deserialize及原startup→session FIRSTnativePause→官方restoreSavedGameData從已驗original GUI還原camera/groups→NEWtransaction不再重設nominalcamera／首次gettercontrol、L0→唯一roundtripSave/L1。Settings/profilebinding可保持原值，但不能把全部load attrs當origin完整同值。

因此：expected origin五次Save可共享同次native startup控制；每個freshload有自己的startup控制。Origin與load timestamps可能碰巧相等或不同，不強迫相等／不同，更不刪nestedtimestamp。Comparator只排metadata最外time，initAttributes.timestamp是完整值之一。Host對nestedtimestamp必由獨立startup source輸出取得精確數值，不能只給寬interval後填實際metadata值。

## Independent init-controls 候選與可得性

官方simulation/components/GuiInterface.js202–205 GetInitAttributes直接return InitAttributes，2066列exposedFunctions。NativeJSI_Simulation.GuiInterfaceCall46–64在simulation realm以actualviewplayer ScriptCall，再crosscompartment clone回GUI；GetPlayerID前後／原readonly方法／realm/source/nativeclone delivery仍需完整callerproof。本次既有GUI**沒有**產生完整initattrs capture或EngineInfo capture。GetInitAttributes機制存在≠已有vouched expected producer。

Replay.cpp88的commands.txt start行是Save之前的獨立producer輸出，含完整當次attrs；但StartGame只寫'\n'而未flush，Turn93–105才flush。Origin經turn後可能可見；freshload immediateL0/Save不能假設preSave start已flush，不能加warmturn、flush、等待、第二Save、延長同5秒來救可得性。Raw原path/PID/source/startup/phase、完整line/bytes與immutable expectedcontrol在metadata之前的因果順序全部OPEN。不得複製整個任意start JSON作expected而略過固定base/schema/來源變更：staticbase與engine/mod controls仍須獨立核對，unexpected新增futurekey須BLOCK。

## Camera與groups的精確界線

JSI_GameView.SetCameraData147–155的六參數是entity_pos_t（Position.h36=Cfixed_15_16），ToFloat進CGameView.SetCamera；Fixed.h151–177有rounding與lossy float轉換。CCameraController434–451 SetValue後FocusHeight/SetupCameraMatrix，getter418–432回smoothed native float狀態。GetCameraPosition105–114/GetCameraRotation76–84/GetCameraZoom87–92回與SavedGames.cpp102–115相同CGameView getter值／float promotion。可採getter值作**獨立於archive metadata**的preSavecontrol；不可用JS字面0.6代替原生實際RotX，也不能假定setter nominal xyz等於最後getter。

GUI metadata camera exactkeys PosX/PosY/PosZ/RotX/RotY/Zoom；gettermapping為position.x/y/z,rotation.x/y,zoom。來源序列／nativeSerialize中途無camera mutation與controls transport/raw/timing須關閉。Native metadata使用JSON.stringify數值語意；不可自行round/epsilon/normalize來通過comparator。load官方restoreSavedGameData593–597會再用SetCameraData(savedcamera)，這是原restore，不是NEWtransaction重設nominalcamera；fixed/float重轉後是否exact需獨立getter與原verified origincontrol lineage，未量測就OPEN，不能從新roundtrip metadata取camera當expected。

selection.js42–46 EntityGroups初始化 own groups={}、ents={}；529–534 EntityGroupsContainer建立10個，589 g_Groups建立container。官方session.js584–589只返回groups:g_Groups.groups；restore602–605原樣還原groups/ents，updateGroups會更新現有groups。Source plan可預承諾10×{groups:{},ents:{}}，但實際全程無group assignment/hotkey/human/nativeeffect、原metadata JSON serialization不得額外加futurekey仍需guard。不能把actual非空group投影成empty；任何unexpected完整值應FAIL/BLOCK。
