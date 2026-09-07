<!-- Purpose: 本 Fork 的專案入口；Created: 2026-09-06. -->
# 跨時代 RTS 改造計畫

本 Fork 計畫以 **0 A.D. / Pyrogenesis 為基礎，製作受《Empire Earth》（世紀爭霸）跨時代玩法啟發的原創 RTS 全面改造 Mod（Total Conversion）**。目前第一階段已建立 Mod、測試地圖與自訂單位，真正引擎的無畫面測試通過；畫面與操作驗收待完成。跨時代玩法尚未實作；上游既有功能不代表改造功能已完成。

開發原則：先做 Mod 與小型可玩原型，驗證海陸空特殊機制；只有在證據顯示 Mod 層無法滿足需求時，才局部修改引擎。美術先以暫用素材驗證，再替換成輪廓清楚、略帶風格化的原創 3D 資產。

## 從這裡開始

| 文件 | 用途 |
| --- | --- |
| [開發計畫](docs/empire-rts/plan.md) | 目標、範圍、技術決策、里程碑與驗收條件 |
| [美術規格與資產清單](docs/empire-rts/art-direction.md) | 視覺方向、製作流程、第一批資產與授權紀錄 |
| [進度追蹤](docs/empire-rts/progress.md) | 現況、任務狀態、依賴、證據與下一步；進度的唯一主表 |
| [決策與工作紀錄](docs/empire-rts/journal.md) | 為何這樣做、每次變更與驗證、恢復工作所需資訊 |
| [原始 0 A.D. README](README.txt) | 上游介紹、建置與使用資訊 |
| [原始授權說明](LICENSE.txt) | 程式、素材及第三方檔案的授權分類 |

## 目前位置

- **M1 PARTIAL**：官方 R28 macOS ARM64 基線已驗證；`epoch_rts` Mod 與 Frontier 01 測試地圖已建立。
- 已通過：seed 42、7 的真正引擎生成與模擬測試，未記錄錯誤／警告。
- 待完成：畫面、Pioneer 選取與移動驗收。兩時代玩法、正式美術及多人測試尚未完成。
- [開始執行與重現測試](docs/empire-rts/baseline.md) · [驗收證據](docs/empire-rts/evidence/m1-validation.md) · [暫用素材](docs/empire-rts/assets.md)

注意：本 Mod 鎖定官方 **0.28.0** runtime；repo 原有較早引擎程式保留，尚未建置驗證。請搭配官方 R28 自帶的 public Mod，勿混用 repo 的舊 public 資料。

正式遊戲名稱尚未決定；「跨時代 RTS」是工作名稱，並非官方《Empire Earth》重製版。沒有預設採用其原始模型、圖像、音樂或其他遊戲資產。

## 維護方式

開始工作先讀計畫與進度；完成一項工作後，在同一批變更中更新任務狀態、實際驗證證據及工作紀錄。未驗證的功能不能標記 DONE。沒有排程或背景服務，文件不會自行更新。

本 README 是 Fork 的新入口；原始 README、上游署名及授權文件仍保留。
