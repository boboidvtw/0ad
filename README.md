<!-- Purpose: 本 Fork 的專案入口；Created: 2026-09-06；2026-11-15 依重設計畫改寫。 -->
# 跨時代 RTS 改造計畫

以 0 A.D. / Pyrogenesis 為基礎，製作受《Empire Earth》（世紀爭霸）跨時代玩法啟發的**原創** RTS 全面改造 Mod（Total Conversion）。Mod 位於 `binaries/data/mods/epoch_rts/`，鎖定官方 **0.28.0（R28）** runtime。

## 目前位置（2026-11-15）

- **能玩的部分**：一個文明、青銅→鐵器兩時代，採集、建造、訓練、研究、作戰到分出勝負都能跑完整局；有繁中 HUD、限定範圍的 Petra AI 對手、存讀檔與本機雙端連線。
- **原型**：飛機、機場、防空、精確彈道、潛艇可行性調查、原創低面數美術樣板。
- **T14–T18**：已依[重設計畫](docs/empire-rts/RESET-PLAN-2026-11-15.md)凍結正式核可流程。成果保留，未通過的項目改記為已知限制。
- **下一步**：M7「可分享的試玩版 v0.4」。現況與待辦以 [STATUS.md](docs/empire-rts/STATUS.md) 為準。

## 從這裡開始

| 文件 | 用途 |
| --- | --- |
| [STATUS](docs/empire-rts/STATUS.md) | 現況與下一步（最先讀這份） |
| [重設計畫](docs/empire-rts/RESET-PLAN-2026-11-15.md) | 工作規則、完成定義、M7／M8 路線 |
| [定案紀錄](docs/empire-rts/decisions.md) | 長期有效的決策 |
| [開發計畫](docs/empire-rts/plan.md) | 目標、範圍、技術決策、里程碑 |
| [兩時代玩法規格](docs/empire-rts/m2-rules.md) | 青銅→鐵器規則、數值與解鎖條件 |
| [進度主表](docs/empire-rts/progress.md) | T00–T18 任務狀態與證據 |
| [工作紀錄](docs/empire-rts/journal.md) | 歷次變更與驗證 |
| [執行與重現測試](docs/empire-rts/baseline.md) | R28 安裝、啟動、smoke test |
| [美術規格](docs/empire-rts/art-direction.md) · [暫用素材](docs/empire-rts/assets.md) | 視覺方向、素材來源與授權 |
| [封存](docs/empire-rts/archive/README.md) | 2026-09-13～11-15 的交接檔與 T14–T18 證據包 |
| [原始 0 A.D. README](README.txt) · [原始授權說明](LICENSE.txt) | 上游介紹、建置、授權 |

## 注意

- 請搭配官方 R28 內建的 `public` Mod，不要混用本 repo 裡較舊的 `public` 資料；repo 裡的舊版 C++ 原始碼沒有建置驗證過。
- 「跨時代 RTS」是工作名稱，不是官方《Empire Earth》重製版，也不使用原作的模型、圖像、音樂或其他資產。
- GitHub 上的 `0ad/0ad` 鏡像從 2024-08 起停止更新，上游已經搬到 Wildfire Games 的 Gitea。

## 維護方式

照[重設計畫第 3 節](docs/empire-rts/RESET-PLAN-2026-11-15.md#3-新的工作規則取代-t14t18-期間累積的流程)的完成定義工作。做完一件事，就在同一個 commit 更新 `STATUS.md` 一行；不再新增 session 交接檔。
