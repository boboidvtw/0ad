<!-- Purpose: 本 Fork 的專案入口；Created: 2026-09-06. -->
# 跨時代 RTS 改造計畫

本 Fork 計畫以 **0 A.D. / Pyrogenesis 為基礎，製作受《Empire Earth》（世紀爭霸）跨時代玩法啟發的原創 RTS 全面改造 Mod（Total Conversion）**。目前第一階段已建立 Mod、測試地圖與自訂單位，引擎測試、實際畫面、選取／移動與正常退出驗收均已通過。T04 已加入青銅經濟與生產，T05 鐵器研究、鍛造科技與繁中 HUD 已完成引擎及畫面驗收；上游既有功能不代表改造功能已完成。

開發原則：先做 Mod 與小型可玩原型，驗證海陸空特殊機制；只有在證據顯示 Mod 層無法滿足需求時，才局部修改引擎。美術先以暫用素材驗證，再替換成輪廓清楚、略帶風格化的原創 3D 資產。

## 從這裡開始

| 文件 | 用途 |
| --- | --- |
| [開發計畫](docs/empire-rts/plan.md) | 目標、範圍、技術決策、里程碑與驗收條件 |
| [兩時代玩法規格](docs/empire-rts/m2-rules.md) | 青銅→鐵器規則、數值與解鎖條件 |
| [M2 驗收清單](docs/empire-rts/m2-acceptance.md) | 經濟、升級、戰鬥與整局測試要求 |
| [美術規格與資產清單](docs/empire-rts/art-direction.md) | 視覺方向、製作流程、第一批資產與授權紀錄 |
| [進度追蹤](docs/empire-rts/progress.md) | 現況、任務狀態、依賴、證據與下一步；進度的唯一主表 |
| [決策與工作紀錄](docs/empire-rts/journal.md) | 為何這樣做、每次變更與驗證、恢復工作所需資訊 |
| [原始 0 A.D. README](README.txt) | 上游介紹、建置與使用資訊 |
| [原始授權說明](LICENSE.txt) | 程式、素材及第三方檔案的授權分類 |

## 目前位置

- **M1 DONE**：官方 R28 macOS ARM64 基線已驗證；`epoch_rts` Mod 與 Frontier 01 測試地圖已建立。
- 已通過：seed 42、7 引擎測試、Pioneer 實際畫面／選取／移動與正常退出，最終日誌 0 錯誤／0 警告。
- **M2 DONE**：兩時代最小流程完成；T06 兩 seed 戰鬥、勝負邊界與標準資源脚本整局通過，見 [T06 證據](docs/empire-rts/evidence/t06-validation.md)。T07 飛行原型、T08 潛艇調查、T09 架構決策、T10 靜態匯入與 T11 原創低面數美術切片已完成各自限定驗收；完整潛艇、精確飛行彈道及全套美術尚未完成，維持 R28 與 Mod、暫不改 C++。
- **T12、T13 限定 DONE**：[T12 AI](docs/empire-rts/evidence/t12-validation.md)限兩 seed 對固定防守；[T13 存讀檔與多人](docs/empire-rts/evidence/t13-validation.md)限已驗收存檔與本機 loopback，不代表通用 AI、任意存檔相容或跨機多人完成。
- **T14 PARTIAL**：已有多項限定效能與完整局證據，但原不限 FPS、重複性及混合交戰 FAIL 仍保留。隔離 storage parser／runner 接線已完成；真實 live integration、量化 observer overhead 與安全玩法修復尚未驗收。以 [進度主表](docs/empire-rts/progress.md)及 [2026-11-05 整體評估與計劃](docs/empire-rts/PROJECT-ASSESSMENT-2026-11-05.md)為準，不以 synthetic proof 取代 runtime 驗收。
- **T15–T18 PARTIAL**：已有本機封包、元件／來源切片及精確彈道非圖像有界驗收；GUI、停機位、完整潛艇、存讀檔／network等必要驗收未完成，原正式FAIL與STOP保留。
- **任務盤點：19項（T00–T18）中14項限定DONE、5項未完成**。五項剩餘工作拆成18個計劃工作包，見[整體評估](docs/empire-rts/PROJECT-ASSESSMENT-2026-11-05.md)；不代表遊戲完成百分比。SOURCE-v2三方正式來源核可已完成，原readiness過期STOP／guard待決策，三正式案例仍NOT_RUN。
- **T05 DONE**：[研究功能與驗收證據](docs/empire-rts/evidence/t05-validation.md)。兩 seed 各 77 項研究與 183 項經濟回歸通過；已確認解鎖單位、鍛造研究及三類繁中不足提示。
- [T04 經濟原型驗收](docs/empire-rts/evidence/t04-validation.md)：兩 seed 各 177 項引擎檢查、GUI 操作及 M1 回歸通過。
- [開始執行與重現測試](docs/empire-rts/baseline.md) · [驗收證據](docs/empire-rts/evidence/m1-validation.md) · [暫用素材](docs/empire-rts/assets.md)

注意：本 Mod 鎖定官方 **0.28.0** runtime；repo 原有較早引擎程式保留，尚未建置驗證。請搭配官方 R28 自帶的 public Mod，勿混用 repo 的舊 public 資料。

正式遊戲名稱尚未決定；「跨時代 RTS」是工作名稱，並非官方《Empire Earth》重製版。沒有預設採用其原始模型、圖像、音樂或其他遊戲資產。

## 維護方式

開始工作先讀計畫與進度；完成一項工作後，在同一批變更中更新任務狀態、實際驗證證據及工作紀錄。未驗證的功能不能標記 DONE。既有 `0ad-t14` 每 5 小時排程的 Nov2 移轉結果與後續 heartbeat 已記錄在交接中；本次收工未修改或新建排程，不保證額度恢復後立即啟動。文件仍须由實際執行的工作更新，不會因排程存在而自動標記任務完成。

本 README 是 Fork 的新入口；原始 README、上游署名及授權文件仍保留。

## 2026-11-12 最新接續 checkpoint

[交接與完整文字證據](docs/empire-rts/handoff-data/2026-11-12/README.md)：30項交接／170項設計完整性檢查MATCH；根端歷次合計閱讀71/85，本次本人24完整／1部分，歸屬分開。三方正式DESIGN報告仍缺，metadata實作未准入；11技術義務OPEN、guard待決策、三正式案例NOT_RUN。整體仍PARTIAL。

## 2026-11-05 最新評估與資料

[成果評估與剩餘計劃](docs/empire-rts/PROJECT-ASSESSMENT-2026-11-05.md) · [接續工作](docs/empire-rts/reference_t14_t18_next_steps.md) · [本次文字證據包](docs/empire-rts/handoff-data/2026-11-05/README.md)。此節取代下方歷史快照的當時NEXT；三SOURCE核可不等於native／GUI／official驗收。

## 2026-11-04 歷史交接快照 / Historical handoff snapshot

以下保留當時狀態；Python報告目前已完成，以Nov5評估為準。

[收工說明](docs/empire-rts/SESSION-CLOSEOUT-2026-11-04-T14-T18.md) · [下一步](docs/empire-rts/reference_t14_t18_next_steps.md) · [交接資料與逐檔SHA](docs/empire-rts/handoff-data/2026-11-04/README.md)。CODE、JS/API僅SOURCE核可；Python正式報告待完成，三正式案例NOT RUN，整體T14–T18仍PARTIAL。原始work/raw/seals與其他未提交工作保留本機；本快照不是完整可執行發行包。

CODE and JS/API approve the exact frozen source only. The Python final report is pending; all three formal cases remain NOT RUN. This scoped handoff exports text evidence and data, with three runtime binaries identified but kept local. It is not a game release or full-machine backup; retain the original working directory and follow the continuation checklist.
