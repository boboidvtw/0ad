<!-- Purpose: resume bounded offline T14 simulation diagnosis. Created: 2026-10-05. -->
# 2026-10-05 T14 simulation／cleanup交接

Repo：`/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`。HEAD保持`726a3aefcae830f605de438cd13192cc6330414e`，index空，全部T14未commit。先核實際Git、官方R28 runtime、progress／plan／journal、現行來源與遺留engine／runner，不只依交接。

優先讀本文件、[離線契約](t14-sim-diagnosis.md)、[validation](evidence/t14-sim-diagnosis-validation.md)、[results](evidence/t14-sim-diagnosis-results.json)、[離線來源鎖定](evidence/t14-sim-diagnosis-source-manifest.json)。前批[完整profiler交接](SESSION-HANDOFF-2026-10-04-T14-PROFILE.md)、[現行220產品來源](evidence/t14-mixed-profile-source-manifest.json)與原mixed／battle等證據保留，不覆寫歷史manifest。

## 本輪限定成果

只重讀有效profiling場 `work/t14-performance/20261004T103345111872Z-mixed-profile-42` 的17份main query，新增runtime **0**、產品／正式parser／AI／C++／武器变更 **0**。原mixed600 no-profiler **FAIL**、profiler首場工具錯誤 **PARTIAL**、整體T14 **PARTIAL**不改。離線分解／獨立核算／靜態source route各限定PASS，唯一根因 **Insufficient data**，修復／改善 **NOT RUN**。

93個strict-contained sim update／turn0–92、987 marker、986連續完整frame核對。逐turn以直接子region時間聯集核算，p95 parent62.862001ms／union62.790001ms，max parent74.334ms／union74.263003ms。未覆蓋wall p950.276005ms／max3.458997ms，只是未被這組label覆蓋的wall，不是CPU-exclusive、wait、GC、limiter或GPU。

全部93次最長直接子label：Sim - Update67、Sim - Motion Unit9、Flush17。17次>50ms sim update中Flush13／Update4；與前批34個慢GUI interval不同，原34項在新results原樣保留。最慢parent frame794／turn66內Flush51.166001ms，落在GUI14.044→14.130秒，不能算pre-sim0載入，也不能指定哪個entity／component或死亡原因。

1171個strict-contained generic Flush依parent分為frame直接子93、sim update直接子93、sim interpolate直接子985。只有93個是這組simulation直接cleanup。完整逐turn／全部慢parent／粗快照上下文／全部Flush在 `work/t14-sim-diagnosis/decomposition.json`；獨立raw重建在同目錄 `independent-audit.py/json`，不import主要helper或正式parser。聯集浮點算術界線不改raw timestamp；既有來源推導sync精度界線維持。

官方固定v0.28.0 commit `a2cae4d69f816e9e9d7eecb6bf88f762afc0c90d` 的Simulation2／ComponentManager，以及實際安裝public.zip五JS／damage.json來源與hash列於 `work/t14-sim-diagnosis/source-reference`。Update label涵蓋CMessageUpdate廣播全部subscribers，Timer可通往Attack／DelayedDamage／Health；死亡、corpse、統計可能在入Destroy queue前處理，不全歸Flush。Flush包含Destroy handler、Deinit、釋放與map維護，也可能再入queue。現有label沒有逐handler耗時／callback次數／queue長度／entity／component ID，因此路徑支持候選，不能作runtime分攤或因果證明。

## 前批狀態仍有效

原混合600場全局p99／第一窗性能／第二窗混合活動FAIL保留；profiler樣本有marker／GET擾動，只取證PASS。首場parser同步基準工具錯誤後唯一retry已用完，沒有第三場。前批154 Python一般／-O、10JS、8CLI、39歷史raw精確重解析PASS維持歷史，本輪产品未改，未無故重跑。

單士兵battle、600移動30分鐘、雙AI難度3單seed、固定防守seed42／seed7及事前3場同條件重複性皆各自限定PASS；原不限FPS／200重複性、soak camera首場、過早repeatability attempt、late計數／flight輸出等FAIL不改。cap60只支持本機模擬落後緩解，不證頻率平滑唯一根因。雙AI分類損失帳差11原因未定。飛行／AA／strike僅片段；正式勝負、混合性能／重複性、AI戰鬥長壓、雙AI跨seed／重複性、定量熱頻率／GPU、多人跨硬體、精確空戰／返航／停機位及潛艇前置機制均未完成。`visual_verified:false`不改。

## 下一步

先評估既有Mod層**只增加觀測**能否安全提供Update subscriber／Timer callback或死亡路徑的細分邊界，不改AI／武器／HP／死亡玩法，不因缺native queue telemetry而改C++。先在repo說明可觀測與不可觀測範圍、樣本／對照、單一變因與profiling擾動；如值得量測，再完整寫seed／實際單位／ownership／武器／camera／時長／活動／全局與局部gate／比較／stop／FAIL保存及工具retry契約，完成回歸／審查／來源鎖定後才啟動。

不重做T05–T13、不重跑已完成T14矩陣，不擴空戰／潛艇、不事後補門檻稱PASS。限定離線診斷不是完整遊戲性能驗收。保留work／profile.txt／profile2.jsonp、全部失敗與局部慢幀；不commit／push／刪檔／背景工作／排程。

本輪收尾audit在 `work/t14-sim-diagnosis/closeout.json`，逐核現行220／T13 129／608份先前raw與evidence及profiles、41raw資料夾、HEAD／index、engine／runner／HTTP退出。最新progress／plan／journal已更新。下次仍以實際文件與Git重新核對。
