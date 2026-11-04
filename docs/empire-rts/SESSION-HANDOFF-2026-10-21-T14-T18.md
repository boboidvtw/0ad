<!-- Purpose: Recoverable T14–T18 local continuation. Created: 2026-10-21. -->
# T14–T18 最新交接

真正 repo：/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad。先讀 work/t14-t18-resume-20261021/current-state.json，再讀本文件與前一版 2026-10-20 交接、AUTONOMOUS-EXECUTION-T14-T18-2026-10-11.md。HEAD 726a3aefcae830f605de438cd13192cc6330414e，既有 dirty work 有意保留，無 commit/push/delete/C++/外部操作。原 heartbeat 的 GUI NOTRUN 狀態已過時，以此 checkpoint 與實檔為準。



## 2026-10-21 來源切片審查與事件契約更正

最新交接：[SESSION-HANDOFF-2026-10-21-T14-T18.md](SESSION-HANDOFF-2026-10-21-T14-T18.md)；結構 checkpoint：work/t14-t18-resume-20261021/current-state.json。Queue prefix 8bfea、typed graph 3e866、fixture base 6b13、archive container 2474 均取得各自 current CODE＋language/API 來源審查核可；來源模型 PASS 不代表原生存檔／零 Advance／roundtrip／視覺驗收。Admission audit 4a08 為 conditional，完整實際 producer/noProxy closure OPEN。

Scenario 首個 freeze 7aa9 因遺漏 registry 要求的 UnitAIStateChanged、UnitAIOrderDataChanged，CODE correction 9b986 與 JS/API 均 BLOCK 1 MEDIUM；原 CODE APPROVE 已撤回並原樣保留，禁止當 current approval。作者正在獨立 event-coverage-amendment 目錄統一六類真事件契約；先取得新契約雙審，再改實作與必要 regression。既有四個 DONE 切片不重跑。Save engine/copy/lock/guard/attempt 尚未建立或執行。

OwnerGUI42 已耗用 FAIL、seed7 STOP、1141-file seal a3466、原 stdout.raw 零 bytes 與 backup 不符均保留，不修原 raw、不重試；T14 PARTIAL、SQLite 原因 Insufficient data。T15–T18 整體未完成。此次 tracking 原版本保存於 work/t14-t18-resume-20261021/before-current-state/manifest.json；所有既有限制與每五小時同一排程保留。

四切片 current manifests 分別為 work/t17-save-queue-prefix-preparation/review-fix/source-for-review.json、work/t17-save-typed-graph-preparation/review-fix/manifest.json、work/t17-save-fixture-base-preparation/manifest.json、work/t17-save-archive-preparation/review-fix/source-for-review.json。各原 BLOCK/RED/FAIL 與 before mapping 皆保留。不得把 prefix [] 或 codec VALID/container framing PASS 當 native 全狀態等值。

作者 /root/save_api_feasibility 僅負責 event-coverage-amendment 新契約，CODE /root/driver_code_review、JS/API /root/fixture_js_review 可接完整獨立審查；原 Scenario source 尚未因 amendment 修改。新契約應保留六類健康／ownership／destroy／stance／UnitAI state／UnitAI order 事件，未知 payload 與未證 producer ref 在反射前 BLOCK，不能以 shape 或 hash label 自證 Proxy-free。外部 quarantine identity 不代表完整持久 opaque payload 證明。完整40 roots、prefix exact equality、600/6x90/30/80、42then7/retry0/raw gates 不變。

後續：新契約雙審 → 六類 source/regression/current dual review → 實際 producer/admission/getter/command/GUI/metadata/host 全鏈實作與 source reviews → 完整 original/copy/runtime/profile inventory/locks → 獨立 fresh guard → 僅新有界 save campaign。不得依 source pass 直接 engine。T16/T18與最終 T15 新特性 package 的未完驗收仍保留，未完成不得報 DONE。

T14 storage6/parser8/runner8/dense/count/delta/completed offline pipeline、P144/382/T15reader51/package159 等 DONE 不重跑。protocol42、K344/GUI272/T17445 與 ownerGUI42 均正式耗用 FAIL，舊 seed7 STOP 不變；原 raw、partialDB、190 slowframes、seal/prior-state chains 全留。額度失敗時存 checkpoint 等既有排程，換 session 不重設額度，無 credits/reset/付費/繞限制。


## 2026-10-21 使用者要求新 session：最新轉移狀態

最新 machine authority：work/t14-t18-session-transfer-20261021/current-state.json。事件六 family 澄清 manifest7de79b9ce8e7883299379f7bc710fdda2278e16b5e0c6fdf7c80cf377cbd03de 已完成兩份完整契約審查：CODE9d3b7bae1eb9c0b63e0a99e8ab49fd99dd378752edc4f31566b55695493d1ab3、JS/API27cec28baee654713f4ee727349c66b5d52ebacf4e3acfb832eab012d93722cf，均 APPROVE_DESIGN_ONLY；CODE1LOW 為 SPEC.md FSM.SwitchToState 筆誤，實際 FSM.prototype.SwitchToNextState，JSON來源義務正確，凍結檔不回寫。7aa source 仍 BLOCK，尚未改成六 family，下一步新source/regressions/current完整雙審；不是 native gate 清除。

Root新增 raw capture source WIP：tools/epoch-rts/t17_save_raw_capture.py、test-t17-save-raw-capture.py；契約與證據 work/t17-save-raw-capture-preparation/，source-wip.json SHA98db3f758f882f25ed0aa5887ac5a762cca7d233debca5a5e2c1d96194756261。10個初步 normal host-file tests PASS，import RED保留，所有案例檔不刪。未完成：nonempty postclose pre-read條件應改為完整前置核對，close/read-error契約測試、optimized/compile、新freeze及CODE+Python完整審查；不得整合或報DONE。已請 /root/driver_code_review 只讀審查，報告將存同目錄 code-review-wip.*；新session先讀實檔，不與作者並行改來源。此元件非engine／drain／原始FAIL根因修復，原raw完全未動。

新session需先寫 child-readback.json 核實repo/HEAD/index/上述hash/已耗用FAIL/目前WIP，再把同一0ad-t14每五小時 heartbeat改指新chat；保留其他排程欄位與通知意圖，無duplicate、不reset。讀回之前不把舊session當仍有產品寫入工作。整體仍PARTIAL，所有舊FAIL/STOP/seal/無外部操作限制保持。
