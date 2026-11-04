<!-- Purpose: durable autonomous continuation request, remaining task queue, and scheduling limits; Created: 2026-10-11. -->
# 自主續作 checkpoint — 尚未全部完成

用戶2026-10-11要求「繼續做，做完全部的項目任務，額度不夠就等，額度夠了，自動做任務」。保留本機自主執行與不購買credits／不用reset券偏好，不commit/push/delete/外部訊息。這不是全部完成的收尾，也不取消既有attempt／source／驗收條件。

## 已實際完成

README已修正過時的「下一步T12／存讀檔與多人尚未驗收」，與主表同步T12/T13限定DONE、T14 PARTIAL及T15–T18 TODO，保留驗收邊界與最新交接。修正「沒有排程」為歷史已有0ad-t14每5小時，但目前狀態／移轉未驗證。README修改前byte保存於work/t14-autonomous-continuation/prior-state/README.md。

前批T14隔離storage/helper/parser/runner wiring與live gap評估已DONE；不重做candidate、syntheticproof或已消耗runtime/offlineattempt。新批沒有產品code、engine、HTTP、SQLite或新proof/tests。

## 剩餘依賴與下一動作

| 項目 | 實際狀態 | 下一必要工作／條件 |
| --- | --- | --- |
| T14 live integration | NOT RUN；隔離接線DONE | 真live producer/context/完整evidence/output整合，需先有必要且不同的runtime問題及契約；不能另名重跑delta/dense/count或full offline。準備詳見t14-live-integration-gap-assessment.md；新engine仍須具體授權、samples/seed/fixture/camera/時長/比較/gates/停止/retry、獨立reviews/source-lock/另callguard |
| T14 overhead／性能與尾活動 | NOT RUN／原有效FAIL保留 | 同條件對照或可驗證修復目標尚未成立；不能以synthetic接線、單一profiled run推定改善；原SQLitecause Insufficient data無法追回 |
| T15 擴充與發行規格 | TODO；依T09/T11–T14 | 若納入本次範圍，先固定既有兩時代可交付內容，整理本機安裝、實際分發清單、署名／來源、已知問題與驗收。名稱／擴充時代／文明尚未定稿，不猜發行目標，不publish，不把T14 PARTIAL改DONE |
| T16 專用攻擊檢查 | TODO；規格見T09第4節 | 若納入本次範圍，先固定隔離海戰沙盒與官方R28來源，implement入口封閉／每次發射重查及完整武器矩陣；兩seed實際HP／事件重播與受影響回歸。不得只擋GUI/CanAttack，不改M2/T07共享元件，不先進C++ |
| T17 潛艇切片 | TODO；依T16 | T16後才做2秒浮潛、深度安全、自動60m偵測、撤銷鎖定、commands/GUI，再掛回存讀檔／多人／效能。原T08探針不是產品元件 |
| T18 精確彈道／停機位 | TODO；依T09 | 若納入本次範圍，先分拆飛行命中與停機預約／排序／避碰契約；沿Mod-first，未取得原生限制與回歸證據前不改C++ |

主表T00–T13各自限定DONE，不為「全部」重做。T14的正式勝負NOT RUN指混合交戰診斷，不否認先前T06與限定完整局已有勝负證據。

目前已提出一次範圍澄清：全部是T14剩餘項目，或亦納入T15–T18。尚未收到回答；暫維持目前T14邊界，不自行把後續潛艇／彈道納入產品。回答後按上述依賴續作，不需每一步再詢問。

## 自動接續的實際限制

已搜尋automation_update／thread工具，但此chat未提供。以原生UI讀Codex也被平台拒絕：`Computer Use is not allowed to use the app 'com.openai.codex' for safety reasons.` 沒有繞過或重試此限制，也沒有改寫本機app資料、另建排程／背景process。因而不能讀回或更新0ad-t14；歷史ACTIVE／每5小時與前chat移轉僅是交接記錄，不當作已驗證現在狀態。

額度恢復後自動執行只能由實際可用且已設定的排程／新訊息喚醒，不能由此chat在工具缺席時保證。若之後提供automation工具，先讀回既有0ad-t14，確認target/prompt後更新同一排程，保留每5小時；只在有意義進展／完成／失敗／必要使用者決策時通知，狀態不變安靜。不要建立重複排程。額度不足保留此checkpoint，不買credits/reset券。

## 恢復入口

真正repo：/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad。讀最新progress/plan/journal及SESSION-HANDOFF-2026-10-11-T14-LIVE-INTEGRATION-GAPS.md、AUTONOMOUS-CONTINUATION-2026-10-11.md與work/t14-autonomous-continuation結果；核Git/來源與source drift再開始。README這次狀態修正不是新engine驗收。前批29seal與舊7207seal仍保留；tracking替代沿原交接不變。
