<!-- Purpose: Latest T14 offline mixed FAIL diagnosis and pending profiler checkpoint. Created: 2026-10-04. -->
# T14 mixed 離線診斷接續交接 — 2026-10-04

Repo `/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`，HEAD仍`726a3aefcae830f605de438cd13192cc6330414e`、index空。T13限定DONE，T14 **PARTIAL**，全部T14未commit/push。現行產品來源仍[evidence/t14-mixed-source-manifest.json](evidence/t14-mixed-source-manifest.json)的209檔，無新產品工具/主Mod/AI/C++修改。先核實際Git/progress/變更/官方R28/來源/遺留程序，不只依交接。

## 本回合已完成（無新runtime）

[離線方法](t14-mixed-diagnosis.md)、[驗證報告](evidence/t14-mixed-diagnosis-validation.md)、[全部結果/22 bins/64慢幀/快照對齊](evidence/t14-mixed-diagnosis-results.json)、[時間軸圖](evidence/t14-mixed-diagnosis-timeline.png)。**離線正確性PASS，根因仍Insufficient data，原mixed性能及後段活動FAIL不改。**

- 直接raw重組2253chunks/5667frames/105042.83203125ms/22snapshots/106 timing samples。64個>50ms全保留，最後index2593 start50.892270020/end50.959812988秒、67.54296875ms；包含原開局/最大95.558837891ms。
- 5秒bins只作診斷：0–5秒2個、5–45秒60個、45–55秒2個、55秒以後0。15–20秒bin最多12個。按frame結束時刻分配，跨界幀不切割；不另做bins性能PASS或取代原60秒/尾窗。
- GUI timestamp/interval在snapshot之前，成本進入**下一筆**間隔。20個中間snapshot後幀全部≤17.972167969ms、0個>50ms，不支持直接歸因這64慢幀是每5秒snapshot同步阻塞；不證明observer零成本、無GC/缓存/等待吸收或負载交互。
- 初始snapshot在timer前、末snapshot/JSON輸出在最后now後，两者沒有可觀察incoming/following interval，沒有填0，也沒有刪原開局幀。
- 第1窗累積wall−sim3.805966064秒、末4.242832031秒；後窗新增.436865967秒。後段局部ratio改善不代表整體追回落後。sample sim有200ms量化，短相鄰ratio不套用正式分鐘門檻。
- 活動合計ATTACKING峰398於wall30.041063秒、存活466；P2近戰首次0於50.066756秒。活動/存活/死亡/慢幀共同分布不證明近戰/Projectile/pathfinding/藝術/死亡處理是根因。
- 封存R28 main.cpp順序GUI→simulation→render→LimitFPS；GUI now-to-now不等同native frame CPU。GetMicroseconds=JS_Now epoch；OS只有runner launch monotonic elapsed，無GUI epoch起點/OS bracket。107.160634−105.042832=2.117802秒包含startup/export/polling，不是GUI anchor/observer cost。
- CPU中位55.85%/RSS峰442.625MiB是整程序低頻含載入/收尾，不可精確對齊慢幀或GUI5秒bins；熱/頻率/GPU/逐frame sim/per-region/observer-exclusive耗時未量測。

獨立code-reviewer未import正式parser/helper，直接raw核算全部關鍵數字/phase/原兩窗口FAIL PASS、無實質findings；work/t14-mixed-diagnosis/independent-offline-review.json。另一explorer只讀核clock/call order/ring/API，observability-review.json；profiler文件限定審查PASS并補attribute/terminal marker精度說明，profile-contract-review.json。這次確實有不同代理的只讀複查；**不追溯把上一mixed量測的主代理分離核算改稱独立代理**。

443份既有raw/evidence/profiles hash、39 raw資料夾/T13 129/主Mod集合/現行209保留；10份read-source-manifest.json封存本次讀到的來源hash（不是新runtime manifest）。helper scripts與audit保留work/t14-mixed-diagnosis；首檢preflight.json、末檢closeout-audit.json。沒有重新跑原121 Python/runtime矩陣，僅離線helper/reviewer/JSON/圖/鏈結與hash核對。

## 新profiler契約：待執行、NOT RUN

[t14-mixed-profile.md](t14-mixed-profile.md)已寫，**未啟動或實作新profile入口**。下一次若續做：

1. 先核官方R28 GUI `ProfileStart/Stop/Attribute` binding能在main profiler2留下可識別region/sequence；public UnitAI simulation呼叫不證明GUI/profiler2。官方source讀取未取得可驗C++（不可用/回HTML），沒有拿current HEAD或HTML當R28證據；目前此binding **NOT VERIFIED**。未達前置不得起engine；不要用遊戲試跑碰運氣。
2. 來源確立後再準備隔離opt-in工具，原mixed入口仍拒絕profiler、原harness/parser/CLI語義不改。若API根本不能建立native marker，先修訂為有界相關診斷，精確clock alignment明列NOT RUN，不臨場自行放寬。
3. 原fixture/兵種HP/武器/布局/seed/1×/cap60/render/camera/endless/两正常命令與原最多120秒或首次耗盡stop不改；**唯一新增觀測處置profiling/marker/GET**有擾動，不是paired causal experiment。主要tracesim0→GUI20秒是資料目標，不縮短原game stop、不稱完整遊戲性能驗收。
4. CPU profiler只127.0.0.1動態port/GPU off、只GET overview/query、不download；約每1秒捕捉，上限24 main+2 overview/每JSON32MiB/总512MiB/timeout2秒。4MiB ring可能覆寫，launch60單GET或15/30/45/60 sparse GET不能保證sim0；實際缺口PARTIAL，不造補完整。
5. 固定region label＋attribute序列（僅已證binding）；epoch-before/after在native enter/leave内，kind4 attribute自身無timestamp，橋接用外圍native區間而非精確offset。GUI20 terminal marker/最後完整frame結尾必須在末GET，不能按runner elapsed20秒停取。
6. 先mock/負例/普通與-O/JS/CLI拒絕/39歷史raw精確重解析、審查与source/contract lock，再1場正式診斷。需完整region/frame/clock/source/activity、sim0起點，資料valid PASS和根因推論分開；profiler樣本不用原no-profiler性能gate，inclusive nested不可加總或當GPU。
7. 真實不足/FAIL不重跑；只有具體工具錯誤封存/修正/重審重鎖後至多1retry，同錯停止。結尾核engine/runner/HTTP退出、根profiles/歷史hash保留；無背景/排程/commit/push/刪檔。

## 原mixed與先前驗收仍保留

完整mixed交接：[SESSION-HANDOFF-2026-10-04-T14-MIXED.md](SESSION-HANDOFF-2026-10-04-T14-MIXED.md)。單場有效資料、限定FAIL、無工具錯誤/retry：初始600，每席150T11 EpochMelee＋150Slinger/HP24000、sim0/cap60/noAI/endless，wall105.042832/sim100.8、5667幀；全局p95 25.472168 PASS/p99 52.647217 FAIL/simwall.959608553 PASS。第一窗60.005966秒p95 35.623047/p99 64.110107/simwall.936573539三項FAIL、活動PASS；第二窗45.036866秒性能PASS但P2近戰已0而混合活動FAIL。兩窗≥30全受gate，不能事後改短或救FAIL。

末P1近戰0/Slinger133、P2全0，官方Unit loss167/300，逐ID/HP/owner/template/native lastAttacked讀回一致。兩席正式active/endless，不是正式勝利；正式混合勝負NOT RUN。原raw work/t14-performance/20261004T092355508923Z-mixed-42。

更早[單兵種交接](SESSION-HANDOFF-2026-10-04-T14.md)與[10-03交接](SESSION-HANDOFF-2026-10-03-T14.md)保留：同種600 battle限定PASS、固定防守map42/map7各PASS、3場map42/AI42同條件重複性PASS、雙AI單seed限定PASS、600地面往返30分鐘性能/活動/RSS工程容差PASS，經濟/late/flight/AA/strike各片段PASS。原不限FPS/200重複性/late legacy/flight輸出/soak相機/誤啟attempt FAIL不變；cap60支持本機落後緩解，不證明頻率平滑唯一根因。

T14仍PARTIAL，mixed已測FAIL而非NOT RUN。AI/戰鬥長壓、雙AI跨seed/重複性、定量熱/頻率、多人跨硬體、正式混合勝負、精確空戰/返航/停機位、潛艇仍NOT RUN；潛艇缺自動偵測/hidden gate，不能為效能擴功能。不重做T05–T13、不無故重跑舊矩陣、不改AI/C++/主Mod/未完成特殊機制；持續更新progress/plan/journal/evidence/新交接。

收尾engine/runner退出、HEAD/index/來源/證據保留核對；無commit/push/刪檔/背景任務或排程。下次仍核現場。
