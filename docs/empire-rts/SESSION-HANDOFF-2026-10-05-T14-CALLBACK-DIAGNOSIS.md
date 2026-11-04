<!-- Purpose: resume bounded offline Timer/search/destruction diagnosis. Created: 2026-10-05. -->
# 2026-10-05 T14 Timer子區段／Destroy離線交接

Repo：`/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`。HEAD仍 `726a3aefcae830f605de438cd13192cc6330414e`，index空，T14未commit。先核實際Git、官方R28、progress／來源與遺留engine／runner／HTTP，不能只依本摘要。無commit／push／刪檔／背景／排程；主Mod／AI／C++／武器／玩法／正式parser不改。

優先讀本文件、progress／plan／journal、[事前離線契約](t14-callback-diagnosis.md)、[validation](evidence/t14-callback-diagnosis-validation.md)、[results](evidence/t14-callback-diagnosis-results.json)、[離線來源鎖](evidence/t14-callback-diagnosis-source-manifest.json)，以及[231現行產品來源](evidence/t14-fine-profile-source-manifest.json)。再讀[最新runtime交接](SESSION-HANDOFF-2026-10-05-T14-FINE-PROFILE.md)與fine／sim／mixed／battle等證據，舊manifest全保留。

## 本輪限定結果

本輪新增runtime **0**、產品修改 **0**；只重讀有效fine場 `work/t14-performance/20261005T020409961988Z-fine-profile-42` 的16main query、1003完整frame／1004markers／92strict sim update。主helper存work，獨立標準庫直接raw重建不import正式parser／helper，正常／-O核算PASS，code review APPROVE；來源路徑限定PASS。原mixed **FAIL**、整體T14 **PARTIAL**保留，根因 **Insufficient data**、改善／overhead／新方法scope **NOT RUN**。

| 同一帶擾動樣本／92parent | Timer | simulation直接Flush |
| --- | ---: | ---: |
| parent wall總ms | 1567.569985 | 720.373002 |
| 直接子聯集ms | 1021.468966 | 638.391114 |
| 未覆蓋wall ms | 546.101019 | 81.981888 |
| 搜尋label count | 3137 | 2085 |
| 搜尋label聯集ms | 998.873025 | 630.590073 |

全部strict FindWalkAndFightTargets label **5223**：上述5222外，另1在MotionMgr_PostMove（frame613／0.330999ms），沒有marker外call。不同parent分類不是不同樣本；nested inclusive不加總，未覆蓋wall不命名callback／scan／CPU-exclusive／wait／GC／GPU。

最慢Flush frame818／turn66 **52.053999ms**，152個搜尋label聯集 **45.812013ms**、直接variation0.581916ms、總直接子46.393929ms、未覆蓋5.660070ms。GUI14.313194→14.402370秒、outer sim75.681ms；上游Timer18.460001ms与前批四Death0.272998／Corpse0.243998ms不能相加或歸為完整清理原因。最慢Timer frame976／turn81 **46.872ms**，98搜尋label聯集29.558990ms、子聯集30.119959ms、未覆蓋16.752041ms；同turn Flush6.074998ms。全92逐例／後代ancestry／18慢parent／29慢GUI／最大cases保留在 `work/t14-callback-diagnosis/decomposition.json`。

## 來源與重要限制

`work/t14-callback-diagnosis/source-reference`有112檔來源／證據hash、實際public.zip全83頂層JS handler inventory、两unit父／mixin component集合与官方固定v0.28.0 commit `a2cae4d69f816e9e9d7eecb6bf88f762afc0c90d` 的native provenance。不能用local HEAD當官方來源。

搜尋label在UnitAI.js兩site：1090附近包含搜尋方法及條件式FSM SetNextState(MEMBER)，2288附近只包方法（FinishOrder／判斷在scope外）。方法還有未profile的callsite；同名label沒有entity／state／site attrs。現有數字表示**已標記區段**，不是純native查詢、全部方法call或確定callback／caller。既有scope缺try/finally，但本場原trace平衡與無errors已核，不無證據稱壞資料。

6個明確JS OnDestroy definitions（UnitAI、Pack、TriggerPoint、BuildingAI、GarrisonHolder、Gate）；無既有JS Deinit或OnGlobalDestroy。初始兩單位靜態enabled component只匹配UnitAI.OnDestroy，仍有native/global/dynamic handlers與後來corpse，不等於runtime handler完整清單。添加人工Deinit會增加新生命周期呼叫，本輪不做。

UnitMotion Deinit空、Destroy只unregister；StopMoving／RangeManager.DestroyActiveQuery不直接呼叫搜尋，因此不能指定這些捷徑。Ownership Deinit空，Destroy才SetOwner(INVALID_PLAYER)→同步OwnershipChanged local/global/dynamic dispatch；有reentrant路徑可能，但未證實搜尋caller。UnitAI只有local OnOwnershipChanged，轉INVALID不進其有条件FSM重設；其他global listeners未知。僅包UnitAI.OnDestroy不是完整覆蓋，亦不能由source路徑直接判根因。

## 前批狀態與保留

現行231來源（舊220全未改）／fine場measured124不變。本輪641份既有raw／evidence／profiles、前批76evidence lock、T13 129及42raw資料夾核對；收尾 `work/t14-callback-diagnosis/closeout.json`、read-source manifest、獨立audit／review及新source manifest保存。HEAD／index／官方runtime／engine／runner／HTTP退出在收尾重核。獨立stdout兩份也保留。

前批fine單場取證限定PASS、無FAIL／retry；GUI105.116412秒／sim101.2、5653intervals／22snap／106timings、65慢幀／max92.815918ms全保留，末P1Slinger133／P2零、loss167／300、正式statesactive、endless耗盡不是勝利。帶擾動全局与第一窗性能投影未達，第二窗mixedactivity不足，不被診斷取證PASS覆蓋。camera／設定相符，visual_verified:false。70 Death／Corpse call涵蓋到20秒marker，15.045390秒快照loss41是較早區間，非帳差29。

原mixed no-profiler FAIL、profiler首場工具錯誤PARTIAL、不限FPS／200重複性FAIL、soak camera首FAIL、準備repeatability attempt FAIL、late／flight輸出FAIL保留。前批唯一profiler工具retry已用完，不盲目第三場。單士兵battle、600移動30分鐘、雙AI單seed、固定防守seed42／7與事前3同條件完整局仍各自限定PASS，不當完整遊戲性能。雙AI損失分類差11未知；cap60不是頻率根因證明。飛行／AA／strike只片段，潛艇缺hidden／自動偵測等前置，不擴功能。

## 下一步

最小新觀測候選：隔離wrapper **既有UnitAI.FindWalkAndFightTargets方法**，保留原函式this／arguments／return／throw與descriptor、不改handler／timer／FSM／玩法，只加固定scope及entity／current-state attributes，沿原Timer／Flush／motion ancestry識別哪些方法call／state出現在清理期間。這能區分方法與舊label，但仍未必識別觸發訊息或全部native清理成本；不要事先稱根因已證。

先寫新的单一變因、樣本／非配對對照／擾動、MapSeed／AISeed、初始與實際unit／weapon／HP／owner、畫面／camera、時長／活動／全局与局部gate／比較／stop／真FAIL／工具retry契約；完成mock／相關回歸／獨立審查／來源鎖定才量測。不要先包全部callbacks或加人工Deinit，不改C++／AI／武器、不擴矩陣、不重做T05–T13。新觀測runtime目前NOT RUN。

熱頻率／GPU、overhead因果、修復改善、正式勝負、混合性能／重複性、AI戰鬥長壓、雙AI跨seed／重複性、多人跨硬體、精確空戰／返航／停機位、潛艇前置仍未驗收。持續更新progress／plan／journal／新證據與交接，保留所有局部FAIL／慢幀／raw；不commit／push／刪檔／背景／排程。
