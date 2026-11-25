<!-- Purpose: 專案現況與下一步的唯一入口（≤80 行）；Created: 2026-11-15. -->
# STATUS

更新：2026-11-15（Phase 0、Phase 1 完成）

## 現況

| 範圍 | 狀態 | 一句話 |
|---|---|---|
| M1 Mod 骨架 | DONE | R28 macOS ARM64 可啟動，Frontier 地圖、選取與移動正常 |
| M2 兩時代流程 | DONE | 青銅→鐵器整局：採集、建造、訓練、研究、作戰、勝負 |
| M3 特殊機制 | DONE（原型） | 飛機／機場／防空原型、潛艇調查；維持 R28、不改 C++ |
| M4 美術切片 | DONE（樣板） | 原創低面數工人、長矛兵、房屋與 3 個圖示 |
| M5 AI／存檔／多人 | DONE（限定） | 兩 seed 對固定防守的 AI；存讀檔；本機 loopback 雙端 |
| T14–T18 | 結案 | T14、T18 縮小範圍 DONE；T15–T17 DROPPED；已知限制寫在 [progress](progress.md) 主表 |

## 下一步

| # | 項目 | 狀態 |
|---|---|---|
| P0 | 重設計畫 Phase 0：止血 | DONE（0.1 排程待本人處理、0.5 LFS 暫緩） |
| P1 | Phase 1：progress.md 的 T14–T18 改為 DONE／DROPPED＋已知限制 | DONE |
| M7.1 | `epoch_frontier_duel` 接上 T12 AI，本人玩一局 | DONE（2026-11-16）：`launch-macos.sh duel` 玩家 2 為 `epoch_petra`（難度 3）；`smoke-macos.py --scenario duel-ai` seed 42／7 AI 勝（897／909 秒，無錯誤）；本人實玩一局 1068 秒（約 18 分）由 AI 獲勝，無錯誤 |
| M7.2 | 最小平衡，一局 10–20 分鐘 | DONE（2026-11-24，以真人對 AI 數據結案）：本人 2 局 1068／1094 秒（約 18 分），AI 對不操作玩家 917／935 秒（約 15 分），皆在 10–20 分內；AI 對 AI 偏長（中位數約 29 分）列為已知限制，M7.6 試玩再補真人樣本。過程：基準 AI 局 15 分、本人局 18 分，時長已在範圍內。唯一調整：市中心 HP 1000→2000（原本 AI 軍隊到達後約 18 秒就結束，防守方來不及反應），AI 局變 15.3／15.6 分。另一個觀察：本人局 836 秒前只蓋 1 棟房屋，人口卡在 30，交給 M7.3 開場提示。本人 2 局（參考）：1068、1094 秒，皆 AI 勝。2026-11-24 改用 AI 對 AI 驗收（`duel-batch-macos.py`）：現行數值 3v3 中位數 29–33 分（20 seeds 只有 2 局落在 10–20 分），2v3 24 分、3v2 29 分。試過市中心 HP 1000、市中心穿刺護甲 3、傷害 +50%、鐵器時代降價、採集 +50%，中位數只變動 0–8 分，且多在 8 局樣本的誤差內；鐵器降價在 20 seeds 上 29.0→27.3 分，效果不明確，未採用。判斷：AI 對 AI 的時長主要由 Petra 互守決定，單純調數值改不動。2026-11-24 改 AI 行為（同 20 seeds，3v3）：攻勢直接打市中心 30.3 分；放寬出兵條件（總兵力 70% 或集結 120 秒即出發）＋打市中心 29.5 分；再加鐵器降價、訓練時間 -30% 為 35.7 分，皆未改善，已全部還原。診斷紀錄（seed 13）：第一波約 750–870 秒才出發，攻方常整波耗盡、守方重建，要第 3–4 波才分勝負。 |
| M7.3 | 遊戲內繁中開場說明 | DONE（2026-11-24）：`duel` 開局在 R28 教學面板顯示一頁繁中說明（目標、採集、房屋 +10 人口、兵營、市中心研究鐵器時代的條件與花費、鍛造所），Ctrl+P 可隱藏／顯示，實測兩個方向都有效；截圖 `evidence/m7.3-opening-guide.jpg`。`smoke-macos.py` duel seed 7／42 與 duel-ai seed 42（917 秒 AI 勝）皆通過，無錯誤 |
| M7.4 | `.pyromod` 安裝包＋乾淨帳號安裝測試 | DONE（2026-11-24，以模擬乾淨安裝結案，見 decisions.md；選單操作留給 M7.6 試玩者實測）：`package-mod.py` 產生 `epoch_rts-0.4.0.pyromod`（66 檔、壓縮後約 90 KB、可重現），`mod.json` 升為 0.4.0；安裝說明 [INSTALL.md](INSTALL.md)。2026-11-24 模擬乾淨安裝（暫時移開本機 0ad 使用者資料與快取）：`open` 該檔由 R28 自動安裝，安裝後的 zip 雜湊與包相同；從安裝後的 zip 以 duel＋epoch_petra 跑完整局，AI 917.4 秒勝、0 錯誤 0 警告；繁中開場說明正常顯示。未驗證：真正的新 macOS 帳號、Finder 雙擊、Mod Selection 與對戰設定的選單操作（合成點擊對全螢幕遊戲無效） |
| M7.5 | GitHub Release v0.4.0 | DONE（2026-11-25）：[Release v0.4.0](https://github.com/boboidvtw/0ad/releases/tag/v0.4.0)（tag `v0.4.0` → `cacbcfd`），附 `epoch_rts-0.4.0.pyromod`（90,058 bytes）與 `.sha256`；GitHub 回報的資產 digest 與本機建置相同（`823a18dc…7ca64`），重新下載後 `shasum -c` 通過。說明與已知限制見 [release-notes-v0.4.0.md](release-notes-v0.4.0.md)。repo 的 Issues 是關閉的，回報管道暫定為「回報給提供連結的人」 |
| M7.6 | 1–3 人試玩＋回饋整理 | IN PROGRESS（2026-11-25）：試玩包 [m7.6-playtest-kit.md](m7.6-playtest-kit.md)（邀請訊息、5 題問卷、對應決策）與回饋整理頁 [m7.6-feedback.md](m7.6-feedback.md) 已備好；等本人找人並傳出邀請，目前 0 人 |

## 已知限制（摘要）

T14 不限 FPS 未達門檻、混合交戰尾段 FAIL；T15 candidate42 FAIL；T16 海戰／death gate FAIL；T17 潛艇暫緩；T18 GUI／停機位未完成。T14–T18 的契約與證據檔從未 commit 進 repo，舊文件裡約 275 個連結失效。細節見 [progress.md](progress.md)。

## Backlog（M7 之後再排）

| ID | 項目 | 來源 | 何時重新考慮 |
|---|---|---|---|
| B1 | 效能回歸測試（不限 FPS、混合交戰） | T14 | 單位或內容量明顯增加時 |
| B2 | 海戰與專用攻擊檢查 | T16 | M8 選海戰方向時 |
| B3 | 潛艇垂直切片 | T17 | B2 完成後 |
| B4 | 空軍：停機位、彈道畫面、save／network | T18 | M8 選空軍方向（選項 B）時 |

## 待本人處理

- `0ad-t14` 每 5 小時的排程：本機的 Claude 排程與 Codex 本機資料庫都找不到。請在 Codex app 的 Automations 裡停用它，或改成「每天跑一次 smoke test＋回報」。
- Git LFS：本機沒裝 `git-lfs`，0.5 暫緩；要做的話先跑 `brew install git-lfs`。
