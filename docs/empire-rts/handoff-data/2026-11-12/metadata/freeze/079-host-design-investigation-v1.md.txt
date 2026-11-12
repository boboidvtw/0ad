<!-- Purpose: bounded R07 host-side prospective design investigation; no implementation or formal approval. Date: 2026-11-06 Asia/Taipei. -->
# R07 host 來源調查 v1

**修正後結論：PROSPECTIVE_SOURCE_DESIGN_CANDIDATE_OPEN，尚無 implementation/runtime 准入。** 原 HOST-API-DRAFT:10 明訂 controls 必在 Save 前由 source 因果鏈建立，沒有明文規定 host durable commit 必在 Save 前完成。R06 crosswalk 的較強文字不能自行新增 gate。因此「GUI 先 capture → 同 callback 唯一 Save → host 先持久化 controls/固定 expected → 才讀 actual metadata」有可繼續設計的候選路線；不必先假定新增 wait/兩向 barrier。詳見末段「根端 challenge 後修正」。以下初步 BLOCK 推論與引文完整保留為調查歷程，不作最終 normative 結論。

此文件是 delegated investigation，**不是原作者、CODE/Python/JS 三方正式 DESIGN review，也不是 implementation 准入**。十一技術義務關閉 0；source/runtime/native 均未升級。74-binding context manifest 為 `f3ca2c1e38538f8a80921f7fa1c53898004231e4fac0b10e949a43ada649c02a`。本 task 讀了 manifest 全文，不聲稱獨立重驗其74 bindings或完成74份內容審查；完整讀／部分讀／未讀清單見同名 JSON。

## 原權威原文與實際衝突

下列引文僅摘錄既有權威，不替換原作者或簽署核可：

- `source-plan-v1/HOST-API-DRAFT.md:10`：「Control需在該Save之前由source因果鏈建立，host commit/readback與接收順序需要實作證明；bufferedstdout/replay不可假定及時。」同檔:4 明確排除任意 JSON、opaque identity、frozen class、hash/label 自證來源；:12 未閉合前不能 Materialize。
- `prearm-deadline-amendment-v2/SPEC.md:22`：「Host在Popen以前reserve t_arm並發permit。」同段要求 session init 首 native pause、upstream init 後第一完整 L0 直接唯一 roundtrip Save/L1。
- 同 SPEC:26：「D=t_arm+5,000,000,000ns」；permit IO、load startup、全部 Save/archive/metadata/ACK 都吃同一 D；:28 不移後 t_arm、不 warmup、不多 engine attempt/archive/load/retry。
- `typed-root-fix/SPEC.md:197`：「session prehook首動作SetPaused→upstreaminit→pureL0→首次唯一roundtripSave→pureL1→request」。原 ACK 在 Save、archive 與完整 native gates 之後，不能提前借作 controls commit ACK（同檔:191–195）。

實際 source：`session_transaction.js:284–289` 首 native action pause、upstream init、同 callback 呼 initialize；:263 native camera getter及 CAMERA_READBACK；:264 first graph、:265 立刻 transaction；:167–177 驗 permit/paused/S/L0 後直接 `Engine.SaveGame(...)`；:178–184 Save 後才 request/REQUEST_READY，:186–198 才跨 tick 等 final ACK。因此在 stdout 新加一筆 getter raw 也只建立 producer-before-Save，**不能因 print 已返回而推出 host 已 durable commit/readback-before-Save**。目前 host helper :598–601 對非 GUI_ACK_VERIFIED 的 frame 直接返回，:717–721 明寫沒有 durable pipe reader/full host runner。

load permit 的原始 bytes 在 `t17_save_prearm.py:444–497` 由 prelaunch boot/arm plan 建立，:467 固定 D，:469–472 固定 permit；它沒有此後 native startup controls 的 SHA。把之後 controls 塞入原 permit 會破壞 immutable bytes；把原 permit 解讀成這些尚未存在資料的 commit 證明會倒置因果。final ACK 是 Save 後 archive 決策，不能作 Save 前 receipt。

## 最小有用的 prospective host API 邊界

以下是待獨立審查的設計要求，沒有新 class/JSON/runtime API，也沒有執行任何 helper。

| 階段 | 唯一可用 authority | 必須拒絕／目前缺口 |
| --- | --- | --- |
| Prepare | 實讀且來源已閉合的 immutable case/phase/checkpoint/ordinal、binary/mod/profile/source inventory、boot factory literal；origin verified controls 的獨立 lineage | 不能把任意 dict 改名 LockedProfile；nonce/sourceSHA 文字不是 source guard；PID 未啟動前只能 pending，不能虛構；actual/archive metadata 不作 expected 輸入 |
| Bind | 實際 launcher/pipe-owner record 綁同一次 process start identity/PID、exact GUI loader/caller source、native clone realm/return path；接收原 bytes、sequence、完整值、preSave commit/readback proof | API 不接 trusted/sourceVouched/verified bool；不接受 caller 自填 PID/realm 代替實際 ownership；目前 full launcher/pipe/control transport 與 closure 未整合 |
| Materialize | 只接受實際內部已閉合的 plan+bound controls，固定六欄 UTF8 bytes；source-owned description factory；全 key/full-value 驗證、未知 writer/key fail closed | 不是 frozen object/hash 就有 authority；不得從 actual metadata 補 timestamp/camera/mods；precommit unresolved 時無成功返回；comparator 結果只能 MATCH_METADATA_VALUES_ONLY |

Prepare 可先固定 literal1、`T17 save <origin|load> <checkpoint>`、完整 GUI base init（含 top-level script）、十 empty groups，以及五 mod 完整順序／四欄候選。實際 binary/version/mod 選擇仍須來源與 native getter交叉證明，不能由 package 版本猜。host description 不接 archive.description；load archive 的 bytes/SHA 只提供資料 ancestry，不是 expected authority。

Bind 必須證明以下實際鏈，而不是在資料 envelope 寫同名字：launcher 的唯一 process/pipe → guard 鎖住的 session XML/include 與 closure → 真 `Engine.GetPlayerID` 前後 → 真 `Engine.GetEngineInfo`、`Engine.GuiInterfaceCall('GetInitAttributes')` 與 camera getters → native caller/realm/clone → 原 raw → host read/full durable commit/post-close readback → GUI 看見相同 commit reference → 唯一 Save。PID reuse 必須靠原 process lifetime/start identity 與管道 ownership排除；這裡未指定不存在的現有 authority。

## Native getter 與欄位控制

- `primaryrefs/source/ps/scripting/JSInterface_Mod.cpp:113–129` GetEngineInfo 使用真 engine_version 與 g_Mods.GetEnabledModsData；SavedGame.cpp:83–96 使用相同 producers，但沒有因此證明當次 caller/profile/runtime。mods 的 enabled order/完整四欄不得投影。
- `context-v1/040-JSInterface_Game.cpp:62–67` GetPlayerID 回真 g_Game principal；`008-JSInterface_Simulation.cpp:58–63` GuiInterfaceCall 跨 compartment clone，ScriptCall 用 GetViewedPlayerID。因此 view caller、request player 或 literal1 都不替代真 principal 前後邊界。
- `024-GuiInterface.js:202–205` GetInitAttributes 回完整 InitAttributes，是比 buffered replay 更有用的候選；但**current session source 沒有這項完整 capture**，caller/realm/native clone/source writers/read-only closure 未證。完整 init 需獨立 fixed base + Replay 本次 timestamp/engine_version/mods，未知 key 不從 observed attrs 學成 expected。fresh load 必須有自己本次 startup timestamp，不能複製 origin 或只用 time interval。
- `038-Replay.cpp:71–88` 寫本次 timestamp/version/mods 與 start line；:91–101 只有 Turn 明確 flush。不能假定 L0 前已可讀 replay，不能等待、flush、warm turn、額外 Save 或延長 D。從 getter取得本次值可以避開 replay-file flush 依賴，但**不解決 host precommit barrier**。
- `027-CameraController.cpp:418–432` 使用 **GetValue()**，不是 GetSmoothedValue。`031-JSInterface_GameView.cpp:76–113` getters → native float/JSON；:147–154 setter先 fixed→float。不得 nominal0.6、epsilon、rounding。`023-session.js:591–607` load restore重新 setter並 restore groups；fresh getter與已核 origin lineage都必要，不能假定精確 roundtrip 同值。
- SavedGame.cpp:79–122 先 SerializeState，後讀 init/mod/player，再 clone GUI與 native camera/description、stringify。控到 preSave getter不等於 Save serialization 期間無 mutation。原 source-plan/FUTURE-SCHEDULE-ABSENCE.md:8–13 完整 producer/mutator/prototype/toJSON/clone/serializer與graph/queue closure仍必要；兩邊同污染會 MATCH，合法 gameplay timers保留。

## 可行性與 amendment 分界

| 路線 | 不改既有契約下結論 |
| --- | --- |
| 只 host factory/static controls | description/base 可以規格化；fresh timestamp與native float不能猜。無完整 controls，BLOCK |
| 只新 print capture，host稍後讀 | 可記 producer raw 的候選；無 host-before-Save 因果屏障。BLOCK |
| 原 prelaunch permit當 controls receipt | controls尚不存在且原 permit immutable；沒有本次 raw binding。拒絕 |
| 等原 final ACK後再建 expected | Save已發生，不符合 host precommit-beforeSave。拒絕 |
| Replay start file | freshload未保證 flush；no wait/turn/extraSave 下不能保證可得。Insufficient data/BLOCK |
| 同 callback 一次檢查新 controls receipt | 若 host剛好已commit可 fail-closed；但需**新 channel/paths/receipt/source guard exceptions與額外驗讀位置**，目前不存在且未核可。不能把排程競賽可成功視為5秒可行性證明 |
| 新 paused tick WAIT_CONTROLS_COMMIT | 可以構成待研究因果barrier，但改 first-L0→Save ordering/no-wait，明確 UNAPPROVED AMENDMENT |
| 新 native synchronous host RPC/hook | 目前沒有 source-proven可用 API；通常需要新 native介面/C++，本任務禁止。不是最小已可行路線 |

**目前無同時保留原 wire/context六keys/ACK、無新 paths/channel、same-callback唯一 Save/no wait、host precommit/readback-beforeSave 的完整可准入設計。** 這不是斷言可用同一5秒的新 amendment 必然失敗；其 scheduling/IO/startup 可行性仍 Insufficient data。任何新 overhead都消耗原 D，不重新開錶，不把 getter/capture移到首 pause之前，不換 L0、不增加 Save/turn/branch/retry。

最小必要下一步是原根端先決定是否願意提出**新的 prospective channel/ordering amendment 設計**，不是實作授權：精確定義 raw producer與host commit receipt 的兩向因果、路徑與metadata/inventory exceptions、一次消耗順序、保存 partial/late 原bytes、同D/outercap、GUI一次讀不到即BLOCK或若需pause tick等待則明列順序變更。若原 no-new-wire/no-wait/同callback限制完全不改，本支線保持 BLOCKED_DESIGN_CURRENT_CONSTRAINTS。不得只降低「host commit beforeSave」成「GUI先print」，或先寫stub/modeltests再稱技術缺口關閉。

## 範圍與保留

原 host source-scope `SCOPE-RATIONALE.md:9–11` 與 completion-source-scope-only.json保留 fullfreeze a32ef348... BLOCK10939/10940及metadata/inode/inventory/runtime缺口。APPROVE_SOURCE_SCOPE_ONLY 不能清掉 full host BLOCK。controller原 SOURCE-v2三核可、guard afb3339b... STOP、三正式case NOT_RUN、24 helpers已耗用與所有舊FAIL/seals不變。

只做文字讀取、選定檔案SHA與新owned文件寫入；無 import/compile/tests/helper/models/producer/Popen/engine/guard/probe/fixture/runtimecopy/network/commit/push/delete。四個當次SHA讀回見JSON。未把48份舊binding或74份context閱讀包當本task全部已讀／重核。此前 quota error由根端原紀錄保留；本task沿同task/settings恢復，未重開角色/換model救quota。

## 根端 challenge 後修正：原義務不等 host 必先落盤

**本節是本報告最終解讀；前述必須 preSave host commit/barrier 的 BLOCK 假說已撤回，原文字保留。** 精確區分三個邊界：

1. HOST-API-DRAFT:10 明文要求的是「Control需在該Save之前由source因果鏈建立」。接續「host commit/readback與接收順序需要實作證明」沒有明文把 host disk commit 的時點也限定到 Save 前。:8 Prepare 先固定 immutable plan；:12 Materialize 只有必要 source/native/caller/phase 義務閉合才可組合 expected；兩者都不明訂 host write-beforeSave。
2. R06 crosswalk「host commit/readback在Save之前」是後續對照的較強 derived wording。它不能單方面改原契約。若要把它升為硬 gate，須另 prospective amendment；不能因這條 derived wording 直接判原設計無解。
3. 原義務仍禁止 actual→expected bootstrap：**capture-beforeSave、host接受完整 controls後固定expected-before-actual-read** 是可審查且不同於 host-durable-beforeSave 的候選。原 source-plan :10 的接收順序/持久化與 buffered raw疑慮仍必證，但不須假定兩向GUI等待。

### 不新增 wait/path/context/ACK 的候選因果鏈

Prospective source 只增一個 source-owned capture/body與既有 emit 的額外 kind（名稱尚待review固定，不在此指定為已核 wire）：

`prelaunch固定靜態plan → 原load prearm/Popen → session首nativePause → upstream init/restore → 真native getters及source-owned完整capture → 私有lexical一次保存immutable primitive encoded record並在原stdout emit → 第一L0 → 同callback唯一Save/L1 → 原request/finalACK → host原raw接收`

Host 的另一條明確順序為：

`實際同process pipe原bytes → 完整frame/原sequence/phase/once與source/realm原件核實 → durable保存完整control原bytes+post-close readback → independent plan/bind validation與immutable expected六欄bytes保存/readback → 才允許actualarchive/metadata consumer讀取metadata bytes → 既有comparator → 原archive/native gates/finalACK/GUIendpoint`

這條鏈並不聲稱 host接收發生在 Save 前。source hash/loader與同callback順序證明 capture-beforeSave；真pipe ownership/source caller證明 raw來源；host source固定 expected-before-actual-read。即使多筆frame在同一chunk到達，也不能假造不同host receive times；原bytes/order完整保留，capture先Save的權威來自已閉合source，不是payload sequence或host時鐘猜測。若只有body自稱「preSave」而無實際source closure，一樣BLOCK。

**原caseRoot/boot/request/ACK/prearm physicalpaths全部可不變，原ReadSaveContext六keys與finalACK完整不變，A/L0→Save→B/L1原順序不變；無跨tick等待、無多turn/flush/額外Save/C++。** 可以把一次startup controls capture置於 upstream init/restore之後、first L0之前；origin startup controls可共享，但每checkpoint的native principal/camera boundary與無mutation義務不能省。fresh load每次重新capture nested timestamp，不把load原metadata作control。不得以第二次graph query替換first L0。

Prepare 只從source-owned staticplan建構；Bind從source-owned pipe parser收到本次native GetEngineInfo、GetPlayerID前後、full GetInitAttributes與精確camera原件；Materialize在host自身pipeline尚未開啟actualmetadata reader時完成。capture encoded string只是保存原件的方法，**不是provenance gate**。getter body必逐字段/fullvalue核固定base與native transformations；不把未知key學入expected。load保存原archive可先於launch，但metadata consumer應有明確source邊界，不能偷從archive讀值建expected。既有獨立originexpected/verifiedcontrol ancestry需真完整來源，不能caller傳自認verified dict。

### 候選仍缺的證據與 amendment 判定

- 既有emit(kind,data)允許多種record，prearm parser :598–601忽略非endpoint的kind；故新增record不必自動改base request/context/ACK schema，也不必新physicalchannel。但這是**新增producer/raw-stage source interface**，不等已核可，須獨立完整prospective設計與fresh source reviews。若原raw-stage allowlist/runner/caps另有exact限制，須明文 additive amendment；尚未讀完全runner/registry，現在不能宣稱無需任何amendment。
- 不能把rawStage塞入現exactReadSaveContext/boot/request/ACK，不能偷偷新增path或挪permit時點。如果後續設計仍需要GUI等待commit receipt、paused tick、改L0/Save順序、新path/channel或nativeRPC，這些均為 **UNAPPROVED AMENDMENT**。本候選不以它們作必要前提。
- host raw持久化/metadata read遮罩、實際producer/source/loader/realm/clone/PID/phase/readonly與full init writer、groups/input/prototype/serializer/Save中途無mutation、futureabsence、original/copy/profile/source/runtime inventory仍OPEN，不能以新JSON證書關閉。host原fullfreeze BLOCK完全保留。
- 全部新增capture/encodedbytes/raw保存/expectedreadback仍吃同D與outercaps；若controls缺失、重複、late、來源unknown、raw過cap或時限不足就FAIL/BLOCK，不能改D或多試。能否在原load5秒完成仍 **Insufficient data / NOT_RUN**。

因此最小必要下一步是把這條候選寫成完整prospective source設計，列exactcapture位置、raw envelope/once/phase/source binding、host parser與durable expected-before-actual-read gate、mutation closure與相容性清單，接受必要完整獨立review；**無須先要求使用者批准放寬no-wait或新增兩向barrier**。本調查本身未實作、未正式核可，十一義務仍OPEN/關閉0。先前host-progress-v1的preSave hostcommit推論是preliminary，由本節與最終JSON顯式修正，不刪去歷程。
