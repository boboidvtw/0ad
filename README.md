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
- **T04 DONE**：採集、建造、訓練與退款／人口限制已驗收；T05 研究與畫面驗收完成，下一步 T06 作戰與完整對局。兩時代玩法、正式美術及多人測試尚未完成。
- **T05 DONE**：[研究功能與驗收證據](docs/empire-rts/evidence/t05-validation.md)。兩 seed 各 77 項研究與 183 項經濟回歸通過；已確認解鎖單位、鍛造研究及三類繁中不足提示。
- [T04 經濟原型驗收](docs/empire-rts/evidence/t04-validation.md)：兩 seed 各 177 項引擎檢查、GUI 操作及 M1 回歸通過。
- [開始執行與重現測試](docs/empire-rts/baseline.md) · [驗收證據](docs/empire-rts/evidence/m1-validation.md) · [暫用素材](docs/empire-rts/assets.md)

注意：本 Mod 鎖定官方 **0.28.0** runtime；repo 原有較早引擎程式保留，尚未建置驗證。請搭配官方 R28 自帶的 public Mod，勿混用 repo 的舊 public 資料。

正式遊戲名稱尚未決定；「跨時代 RTS」是工作名稱，並非官方《Empire Earth》重製版。沒有預設採用其原始模型、圖像、音樂或其他遊戲資產。

## 維護方式

開始工作先讀計畫與進度；完成一項工作後，在同一批變更中更新任務狀態、實際驗證證據及工作紀錄。未驗證的功能不能標記 DONE。沒有排程或背景服務，文件不會自行更新。

本 README 是 Fork 的新入口；原始 README、上游署名及授權文件仍保留。
