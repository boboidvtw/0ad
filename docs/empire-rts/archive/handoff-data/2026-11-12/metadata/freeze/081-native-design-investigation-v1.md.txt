<!-- Purpose: bounded R07 source investigation of native metadata controls and host preSave causality. Created: 2026-11-06 Asia/Taipei. -->
# R07 native metadata controls：GUI preSave 獨立 capture 有來源候選；完整 provenance／整合仍 OPEN

本調查完成於既有 task／settings，只有 read/hash／靜態文字推理與本報告落盤。**不是完整三方 DESIGN review，不准入任何 metadata 實作或 native case。十一項義務全部 OPEN，關閉數 0。** 先前 usage-limit interruption 不抹除；本子任務可見上下文沒有原始 error bytes，僅承接根端所報中斷，不重建錯誤內容、不另開 actor 或換設定。

本報告所有相對路徑以實際 repo `/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad` 為根。以下縮寫只縮短引用，沒有新 authority：

- `P` = `work/t17-save-metadata-expected-controls-preparation/source-plan-v1`
- `N` = `P/primaryrefs/source`
- `O` = `P/primaryrefs/official-public`
- `G` = `tools/epoch-rts/t17-save-harness/gui/t17_save/session_transaction.js`
- `T` = `work/t17-save-network-preparation/save-source-design-20261018/typed-root-fix/SPEC.md`
- `A` = `work/t17-save-session-transaction-preparation/prearm-deadline-amendment-v2/SPEC.md`
- `X` = `docs/empire-rts/METADATA-CONTROLS-CROSSWALK-2026-11-05.md`
- `S` = `P/context/work/t17-save-allocation-consumer-integration-preparation/native-loader-closure/primaryrefs/source/simulation2/scripting/JSInterface_Simulation.cpp`

## 已知結論與不可混淆的契約層級

1. 真正現有 native getter 機制存在：GetEngineInfo、GuiInterfaceCall('GetInitAttributes')、GetPlayerID、camera 六值。它們能成為新的 source-owned capture 設計材料，但現有 G 沒有 EngineInfo／full InitAttributes expected-controls producer。沒有執行 getter，未量得任何 runtime 值。
2. **原 sealed metadata source-plan**要求獨立、preSave precommitted controls，另要求 host immutable raw／commit／readback 順序證據（P/HOST-API-DRAFT.md:8–12、26；P/FUTURE-SCHEDULE-ABSENCE.md:12）。HOST-API:10 精確文字為「Control需在該Save之前由source因果鏈建立，host commit/readback與接收順序需要實作證明」。FUTURE:12 為「origin每Save之前control independentlyprecommitted」。**兩處沒有逐字要求 host disk commit/readback 必須先於 Save**；不能把並列的host evidence要求自行移進Save前時序。
3. **R06 derived crosswalk**文字「同PID與host commit/readback在Save之前」（X:33）比上述 sealed source-plan更強。R06不能自行加新原契約門檻。本子任務早期以其較強文字判定總BLOCK的解讀，經根端問題澄清後明確撤回；原 progress-v1保留歷史，不覆寫成假裝一開始已正確。根端可保原preimage修正derived crosswalk；這是原文對齊，並非暗中放寬原契約。
4. **較早 typed-root-fix R5**寫的是 Save 後 request／host archive verification／final ACK（T:191、195、197）。不能倒稱舊 base wire 已有 metadata preSave host commit。它目前恰缺這條因果通道。
5. `GUI genuine source capture/immutable encode → Save → host receive/persist/readback → host Materialize expected → actual metadata read/compare` **可成為原sealed source-plan的可審來源設計候選**。它不證host在Save前落盤，也不滿足X:33較強字面，但不因此違反原HOST-API:10。必證capture確實執行於Save之前、control未再變、host未先讀actual反填，且完整source/caller/realm/PID/phase/producer/clone/serialization閉合。freeze/encode/hash本身不給provenance。此候選仍須新設計核可、後續source與R08實際因果證據，未實作或准入。

## getter 候選比較及 exact producer

| 候選 | 來源與用途 | 在本案仍缺甚麼 |
| --- | --- | --- |
| Engine.GetEngineInfo() | N/ps/scripting/JSInterface_Mod.cpp:113–129 直接用 engine_version 與 g_Mods.GetEnabledModsData，deep freeze 結果；:35–42、56–63 轉出完整四欄 mod/name/version/ignoreInCompatibilityChecks；N/ps/Mod.cpp:184–203 保 enabled order，僅排 mod/user，沒有 compatibility filter。Save 用相同 native symbol/producer（N/ps/SavedGame.cpp:83–96）。 | 真正 guarded binary/build/profile／五 mod selection/order/完整 records，source API 未被替換、同 PID/GUI realm/caller/phase 的 raw capture 與 host precommit。Freeze 本身不是 provenance。不可從 package version 或 AreModsPlayCompatible 猜值。 |
| Engine.GuiInterfaceCall('GetInitAttributes') | O/simulation/components/GuiInterface.js:202–205 回完整 InitAttributes，:2066 expose；:2128–2133 按 exposed method dispatch。S:46–64 從當前 g_Game simulation 呼叫 ScriptCall(viewedPlayer)，並 clone result 回 GUI。N/simulation2/Simulation2.cpp:843–859 先 LoadMapSettings、freeze attrs、SetGlobal，之後 startup／trigger scripts；Save :83 讀 simulation.GetInitAttributes。 | 這是 JS simulation getter 經 native bridge／clone，不能改標為 C++ 專用 getter或 authenticated principal。完整 startup writer／global binding／prototype／method hooks／clone closure，固定 base 所有 key、未知 key 拒絕，capture 位置與 host precommit仍 OPEN。 |
| Replay start raw | N/ps/Replay.cpp:71–88 寫完整本次 attrs；:76、79–82 覆寫 timestamp/version/mods。 | :88 只有 newline，:91–101 才於 Turn flush。Freshload L0 不能等可見性、warmturn、flush、第二 Save 或延長五秒；不能以 origin replay start 代本次 load。此候選不適合當已保證可得的 immediate-load control。 |
| Native GetPlayerID | N/ps/scripting/JSInterface_Game.cpp:62–68 讀 g_Game 的 ID，Save :94 亦讀此 ID。G:49–50 的 ReadSaveContext 正好區分實 ID 與 nativeQueryCaller。 | literal 1 是 expected；真 capture 前後 returned 值與 source/case/PID/phase 的原始因果證據仍缺。payload.player／viewplayer／nativeQueryCaller 皆不能代替。 |
| Native camera getters | N/graphics/scripting/JSInterface_GameView.cpp:76–114／N/graphics/GameView.cpp:317–329／N/graphics/CameraController.cpp:418–432；Save :102–115 用相同 CGameView getter。 | 有相同 source 路徑，不等已證完整 Save 中無 mutation、JSON rawlineage 或 load fixed roundtrip。實際六值未量測。 |

**GetInitAttributes 比 replay disk visibility 更直接**：它可在 session FIRST native pause、upstream restore、第一次 L0 附近作候選 readonly capture，不需要推進 turn 才能讀到 Replay 在本次 startup 已寫入的 attrs。這只是機制與候選位置判斷，不是允許新增 getter／改順序的 implementation approval，更不解決 host precommit。不能先把完整 getter clone 當 expected 再從 actual 學未知 key；必先以 immutable plan 核完整 base/settings/binding、Replay 三個已知轉換、獨立 EngineInfo，未知 writer/key 必 BLOCK。

Origin：G:84 initialAttrs 有 top-level script 與七 settings；N/ps/scripting/JSInterface_Game.cpp:39–54 clone 到 sim；N/ps/Game.cpp:382–387 先 Replay 再 RegisterInit／:219 SetInitAttributes。Load：N/ps/scripting/JSInterface_SavedGame.cpp:91–115 原 archive 是載入資料，建立 CGame(true)、clone attrs、restore player，再 StartGame；Replay 仍重新寫三欄。故每 freshload 必取自己的 exact nested timestamp。只有最外 metadata.time 走獨立 epoch interval；不從原 archive timestamp 推定本次值，兩次值碰巧相同亦非錯誤。

## Camera LOW 的精確修正範圍

既有 JS review `ccc2ef605452c2748626eb7305a72de5dc976636f0042d1b96395101b62315fe` 的 LOW `JS-DESIGN-LOW-001` 保留。此新報告明確採 **GetValue()**，不採 GetSmoothedValue()；不改 sealed P/FIELD-MATRIX.md:33。

精確路徑：JS nominal setter → entity_pos_t (`N/simulation2/helpers/Position.h:36` = CFixed_15_16) → fixed conversion（N/maths/Fixed.h:151–164）→ ToFloat（:170–174，可能 lossy）→ CCameraController.SetValue 與 FocusHeight／SetupCamera（N/graphics/CameraController.cpp:434–449）→ **GetValue() float**（:418–432）→ ToJSVal<float> 使用 JS::NumberValue（N/scriptinterface/ScriptConversions.cpp:194–197）／zoom NumberValue（JSInterface_GameView.cpp:91）→ JSON number。

mapping 必保 `position.x/y/z → PosX/Y/Z`、`rotation.x/y → RotX/Y`、`zoom → Zoom`。不由 nominal 0.6 重算、不 epsilon、不 rounding、不投影。Save 先 SerializeState（SavedGame.cpp:79–81），才讀 attrs／mods／principal／camera（:83–120）；因此同期純 readonly 與 serializer／prototype／callback 無 mutation 義務不能用「同一 S／paused」替代。G:177 cameraSame 與 :178 再驗只是部分邊界，並不是 native transitive closure 全證。

Load 官方 restore 再走 fixed setter（O/gui/session/session.js:591–607），G:263 只在 origin 設 nominal camera，load 讀 restore 後 fresh getters。必保 verified-origin controls lineage，但不能保證兩次 fixed/float 轉換仍 exact；不能以 roundtrip actual metadata 自填新的 expected。

## 較強 host-before-Save 解讀的具體矛盾；不誤升原契約總 BLOCK

目前 G 的 source order 是：

`permitFor → pause/or firstLoad already paused → context/A or first L0 → SAVE_CALL raw → cameraSame → unique SaveGame → B/L1 → request WriteJSON/readback → REQUEST_READY → return → later pollAck`。

精確引用 G:167–184、186–198。`SAVE_CALL` 是 :176 發的 stdout 記錄，並不是 host callback；:177 下一步即 Save。`emit` 只 print（G:22），沒有 host commit-return fence。Host 同時讀 stdout 或 watcher 理論上可能搶先，但沒有 source causal relation保證完成，不能拿「通常夠快」當 precommit。

Origin 的 arm intent 在 checkpoint−200 lattice 寫出（G:151–156），host t_arm／permit可早於 Pause（A:20）；但原 intent 的 exact keys 是 planned identity/window，沒有當次完整 native metadata controls，也沒有後來 A 至 Save 的 camera/groups/writer closure。把 controls 偷放 arm intent／permit、raw identity、boot 或 context 都是 wire/source guard 新變更。靜態 plan／description 可早準備，不等於動態完整 controls 已 capture/host commit。

Freshload 更嚴格：host reserve t_arm／permit **在 Popen 前**（A:22），當時該新 process 尚未產生 timestamp／camera／getter values。GUI wrapped init 第一個 native action必 SetPaused（G:284–289），upstream init/restore之後 initialize取得 first L0（G:260–265），立刻在同 callback 呼 transaction，唯一 Save不先 yield。不能在 prelaunch permit裡偽放此後才產生的 fresh values，也不能把 source-owned producer label 當時間反轉證據。

若要在該 callback 中取得 host 已完成 commit/readback 的回覆，只可能需要現不存在的 synchronous host fence，或將 GUI Save 拆成等 host 的後續步驟。前者無既有 API／禁止 C++，後者新增等待／state/protocol／VFS watcher visibility 成本；兩者均不是目前允許的小改。單次 fail-fast FileExists 讀「可能已存在」的 token亦新增 token/channel，且不能保證本次 capture 的 commit 已先完成；失敗保持 BLOCK，不可靠競態取得保證。

原 A:26–32 的 `D=t_arm+5,000,000,000ns` 不變：load 剩餘 guards、Popen、startup、Pause/L0/Save/L1、archive gates、final ACK與 GUI_ACK_VERIFIED 都在 D內。A:28 明列不可移後 t_arm／warmup／略 guard／retry。時間足夠與否未量測，**Insufficient data**；即使假設有餘裕，新增等待仍需 prospective amendment，不能因不加五秒就自動合法。

以上只說明 **若另要求host-before-Save barrier**，原callback及現有wire沒有它；不能把這件事直接升成原sealed source-plan不可能。原契約可用真正GUI preSave capture作事前control、host postSave但preActualRead完成持久化的設計候選。其runtime五秒與完整closure仍Insufficient data，不能以候選存在先實作或假定通過。

## 最小仍可進行的 source-only 範圍

目前可細化以下 **不執行的最小來源候選設計**，不用新增等待、Save、turn、flush、bootkey、VFS path、context key或C++：

1. Prepare在launch前於host固定immutable case/phase/checkpoint/ordinal、description literal、完整預期runtime/mod/source identity、base init/settings與十emptygroups；PID只在實際Popen後以host ledger綁定，不偽填launch前未知PID。Load ancestry只用已獨立驗證的origin controls，archive仍只是載入資料。
2. 保G wrapped init FIRST native pause、upstream restore及first graph L0。於transaction原L0/A取得之後、唯一Save之前，由封閉source-owned caller真正讀GetEngineInfo、GetPlayerID前後、完整GetInitAttributes native bridge及camera六值；既有ReadSaveContext仍exact六keys。只增加readonly capture，不取代L0、不觸發sim advance。每個getter及transitive callback的purity、hooks/prototypes與nativeclone需另審，不能以readonly名字假定。
3. 對capture核全部固定base/settings/binding、version/mod controls、literal principal1、十emptygroups與所有未知key。只對新建data-only snapshot完整encode/freeze並存external lexical closure；不freeze native live object／g_Groups等改變產品行為，不掛simulation/InitAttributes/groups/Timer/component或metadata。完整body、phase/checkpoint/ordinal及單調source sequence在Save前固定，禁止Save後補getter或重建expected。Freeze只是immutability，provenance仍由source/caller/realm實際執行證據支持。
4. 以既有stdout raw transcript通道輸出完整control raw，再立即原唯一Save/B或L1/request，不等host接收／commit。沒有聲稱print flush。新增record framing/body及byte cap必先有明確source設計與fresh reviews；本報告未建立已部署record，也不把新JSON自標native。若固定raw schema實際禁止新record，須先列prospective amendment，不能偷偷變wire。
5. Host可以Save後才收到buffered capture，但必先保原receivedbackup、按實際path/PID/sequence/source/case/phase核原raw、持久化與完整readback、Bind/Materialize獨立expected，**再開讀／解析actual archive metadata**。raw missing/late/截斷、body/順序不符、closure未知或deadline到即BLOCK/FAIL，無metadata fallback或第二Save。Archive已由Save產生不等host已讀metadata；兩種時序必分開記錄。
6. 原五秒D、prelaunch t_arm、outer deadlines/freshguard/原件持久化不變，capture/encode/hostpersist吃同budget；成本未量測，不能聲稱可達成。Source sequence需以真callback控制流與guardedsource支持，單靠JSON的beforeSave字串不能證body執行。

來源圖仍需補startup/mutator/serializer／groups input closure與getter exact mapping，保持原六key context／ACK／wire／boot。**有可審的最小source方案，尚沒有已核可且滿足全部admission gates的producer實作範圍**；理由是完整closure、source/caller/body/raw causal evidence及設計核可尚缺，不是必須發明hostpreSavefence。不得先寫stub或以JSONreceipt升格authority。

若未來提出preSave capture VFS paths／host token或precommit ACK、bootkeys／arm request或permit fields、GUI等待／yield state、host synchronous fence或固定wire/schema/cap變更，必另列 **PROSPECTIVE_UNAPPROVED_AMENDMENT**。既有stdout新capture record也要先有exact framing/size/source-review設計，若改變固定raw規範則進amendment；不能藉不改context迴避。GUI causal capture＋hostpostSave/preActualRead持久化本身不是原HOST-API:10語意變更，不能誤列為必須放寬原契約。未選定或部署任何protocol改動。

## 十一義務全部保留

| 義務 | 本調查新增的定位；仍 OPEN 的原因 |
| --- | --- |
| ENGINE_INFO_RUNTIME | 同 native version/mod producer 已定位；binary/runtime／五 mods真選擇、order、四欄、真 capture／commit未執行。 |
| PRINCIPAL_CAPTURE | native ID 與 viewcaller已分明；前後 returned receipt／PID/phase/host lineage未實作。 |
| FULL_INITATTRS_PRODUCER | GetInitAttributes native bridge候選明確；完整 startup/map/settings/trigger/global writer closure未閉。 |
| LOAD_NESTED_TIMESTAMP | fresh Replay rewrite已定位；本次 fresh native capture／host precommit未成立。 |
| REPLAY_START_AVAILABILITY | flush缺口保留；getter候選可繞 disk dependency的設計，不是已關閉的 runtime可得性。 |
| CAMERA_CONTROL | GetValue float/JSON／fixed/load restore mapping明列；值、nonmutation／rawlineage／commit未驗。 |
| GROUPS_INPUT_CLOSURE | O/selection.js:41–45、529–534、589 建十組；session.js:584–607 get/restore；human/hotkey/update/prototype/toJSON/clone/mutator完整閉合未做。 |
| STATIC_DESCRIPTION_HOST_FACTORY | G:177 literal與 immutable case derivation可確定；factory/once caller/raw／commit未實作。 |
| PRECOMMIT_TRANSPORT | G同callback Save先於request；新GUI genuinepreSavecapture／hostpostSave-preActualRead持久化為可審候選，未部署／未有body/raw實證，仍OPEN。較強host-before-Save解讀無既有fence，不當作原契約新增gate。 |
| FUTURE_SCHEDULE_ABSENCE | 全值相等不能證absence。完整 producer/mutator/clone/serializer＋graph/queue/native證據未閉；合法 gameplay Timer不得刪。 |
| FULL_NATIVE_PIPELINE | host/current runtime/source/profile locks/fullguards／budget／actual Save/load/raw/archives/queue0/40roots皆 NOT_RUN，不能升格。 |

## 閱讀 coverage 與核對限制

完整讀取：X 1–47；P/{CONTRACT.md 1–6, FIELD-MATRIX.md 1–37, HOST-API-DRAFT.md 1–28, FUTURE-SCHEDULE-ABSENCE.md 1–15, OPEN-obligations.json 1–67, manifest.json 1–255}；A 1–40；T 1–227；既有 JS review.md 1–16 與 review.json 1–759。舊 review 的 48/48 MATCH是舊審查事實，本調查未重作其獨立 48 artifact audit。

G：已讀全部 functional text 1–4、7–297（含 PREARM line8）；巨型內嵌 WIRE line5未完整逐欄審查，line6分隔未另聲稱 schema closure。這不足以做完整 source implementation／wire review，卻足以定位 transaction source order。GUI current SHA 實算 `ec8c8a23d79b7f6e4fce11230b4a6f25a5c89861d2518a3a3de0b3522408e885`；舊 JS review.json 實算 `ccc2ef605452c2748626eb7305a72de5dc976636f0042d1b96395101b62315fe`。

完整 primary files讀取：N/ps/scripting/{JSInterface_Mod.cpp,JSInterface_SavedGame.cpp}及 S。其他 primary只讀上述指定範圍：SavedGame 55–135、Replay65–108、CameraController418–452、JSInterface_GameView70–160、Game205–223/380–400、Simulation2 835–862、Mod184–205、JSInterface_Game35–80、ScriptConversions.cpp180–204、Position.h28–40、Fixed.h145–180、O/session.js580–610、O/selection.js40–48/525–535/585–590、O/GuiInterface.js198–208/2058–2070/2128–2140。GameView317–329以逐行 rg結果讀到 getter forwarding，未冒稱整檔閱讀。

根端的74bindings／1,324,660bytes context snapshot為調查輸入；本子任務實算 context-manifest SHA `f3ca2c1e38538f8a80921f7fa1c53898004231e4fac0b10e949a43ada649c02a`，只讀其前100行 mapping，不宣稱自己完整讀／逐檔 hash全部74bindings。P manifest SHA實算17eb3663…；A SHA bbde20a000d4e3e5bdaed90073c1a9d3a886048d3e9602d46af3ed665c93410e；T SHA ccaf88f75461745a82d4aba67622d38cb30cf94b522d02d025ff70fac142903b。

未讀／未閉：完整 startup／map generation／settings writer、GetInitAttributes hook/global replacement／native clone所有 transitives、groups hotkeys/input/update/prototype/toJSON完整 closure、Save SerializeState所有 callback、完整 hostrunner/watch/VFS transport／74 context全面current-match audit。這些不得用本調查的 BLOCK定位假裝已正式審查通過。

只有 native-progress-v1.json、本 MD及同名 JSON由本 actor新增。所有 code/producer／test/model/helper／import/compile/Popen/engine/resource probe/guard/attempt/copyruntime/network/commit/push/delete 都未執行。原 fault guard afb3339b／STOP／三 formal cases NOT_RUN／24 consumed helpers及其他 dirty work維持原義，不重跑不升格。
