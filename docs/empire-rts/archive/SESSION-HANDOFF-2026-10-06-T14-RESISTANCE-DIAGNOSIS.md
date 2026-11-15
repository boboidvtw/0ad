<!-- Purpose: continuation checkpoint for offline fan-out and method-cost observability decision. Created: 2026-10-06. -->
# T14 Resistance fan-out 離線診斷交接

Repo `/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`。先查實際Git/progress/變更/官方R28/來源與鎖/engine-runner，不只依本交接。HEAD726a3aefcae830f605de438cd13192cc6330414e/index空，T13限定DONE，全部T14未commit，T14仍PARTIAL。

## 本批完成

按[t14-resistance-diagnosis事前離線契約](t14-resistance-diagnosis.md)，只分析前批有效raw `work/t14-performance/20261005T105101310412Z-resistance-profile-42`，新增runtime0／產品修改0。詳[validation](evidence/t14-resistance-diagnosis-validation.md)、[results](evidence/t14-resistance-diagnosis-results.json)；全部ID/turn/entity/labels在`work/t14-resistance-diagnosis/distribution.json`。

- 全1128完整frame／674handler／8196search保留；strict93turn／71invalid-handler／7914search，2148巢狀Flush search/403entity。
- **同handler同entity重複0，同strict turn同entity跨handler重複0**。最大handler target590/turn47為107call/107entity（104Slinger/3Melee）；最大turn66四handler内152call/152entity。沒有本場可供通知去重／合併的重複訊號。
- 巢狀2148皆初始opposite owner：1838Slinger＋310Melee。44turn有search/49無，fan-out平均30.253521／中位24；不是實際attackerSet數或獨立重複樣本。341/403entity跨不同turn再搜尋，最多entity335十五call/十五turn/十五target-handler，不代表同輸入冗餘。
- native ResetActiveQuery/ExecuteQuery label在CPU-profiler2 NOT OBSERVED；來源是舊PROFILE，PROFILE3才含PROFILE2。native query含PerformQuery/lastMatch/stable_sort；JS方法則filter/preferences/order，不是純讀取。缺query label不是零成本。
- strict方法內具名後代仅FindObjectVariation18844call/21.038910ms（Flush6265/8.225810；Timer12577/12.813100；motion2/量化0）。不稱GPU/純query/全部餘額/exclusiveCPU，不將parent-child相加。未核該label具體nativecaller。

一般/-O主directraw完全一致，另一flat-stack獨立stdlib（不import主helper/正式parser）逐handler/turn/entity與label/bounds/union核PASS，6合成一般/-O PASS；來源與最終docs審查記於work review/source-inputs。官方installed Resistance/Attack/UnitAI/FSM逐byte相符，native固定commit a2cae4d69f816e9e9d7eecb6bf88f762afc0c90d與provenance相符。

## 下一個最小工作

**先核方法內成本觀測的Mod層可行性，不直接再跑場。** 目標是找官方native ResetActiveQuery與JS filter/order之間可觀測且保留原語義的邊界。現有資料沒有查詢結果大小、逐操作時間或訂單/target變化，不足選安全修復；不要由無重複直接改去重/合併，也不要把方法wall當純查詢。

Attack.StopAttacking单一reason/targetBefore/callerIIDBefore（保留undefined/absent）仍是不同契約候選NOT RUN，可補精確鏈資訊，不能直接分離query成本／證安全去重。不要只因caller未知自動又跑一場；若確實選新observer，先另立樣本/fixture/控制/seed/camera/全局與每窗gate/比較/停止/retry事前契約，來源/descriptor/loader/this/arguments/return/throw/同步順序回歸、獨立review/source lock/獨立guard通過才量測。不得預掃/複製/清空/重排attackers，不丟未知ID或猜corpse/local/mirage，不同批包全部callbacks。

前場entity288先Death再Timer搜尋再Flush仍未解，不稱全部Timer搜尋為存活者；caller/reason/唯一根因仍Insufficient data。修復效果/overhead/正式勝負NOT RUN。混合/雙AI重複性、AI戰鬥長壓、熱頻率/GPU、多人跨硬體、精確空戰/返航/停機位及潛艇前置仍未驗收。

## 必須保留與收尾

原mixed no-profiler FAIL與所有歷史FAIL不補過。前批Resistance首場`20261005T104832965402Z`的主代理hash前置未阻止launch之流程FAIL已停，22raw/來源/review留存；唯一retry有效PASS，前批attempts2/valid1/retry用完，不能第三次重試。本批沒有新runtime。

產品256／measured128未變，T13 129/674資料/前置809/45raw保留。前批142鎖在本批preflight全match；其progress/plan/journal舊mutable checkpoint在更新前保存到`work/t14-resistance-diagnosis/prior-state`並hash吻合，映射見prior-mutable-checkpoint-map.json。歷史manifest不覆寫，收尾分139未變live與3舊snapshot核對，新鎖另封。實際sources/exit/ports/HEAD/index見本批closeout/evidence-lock。

官方R28 binary SHA531981d016596b0abde110cd239feaed98998c3fdaa837d0fa8d6f75482c81ef、public.zip SHA ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429。engine/runner退出、5ports閉、全部45raw保留。無commit/push/刪profile.txt/profile2.jsonp/work/背景任務/排程。不重做T05–T13，不無故重跑T14矩陣、不改AI/C++/玩法、不擴未完空戰/潛艇。持續更新repo計畫/progress/journal/證據/交接，分PASS/PARTIAL/NOT RUN。
