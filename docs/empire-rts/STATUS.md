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
| M7.2 | 最小平衡，一局 10–20 分鐘 | DOING：基準 AI 局 15 分、本人局 18 分，時長已在範圍內。唯一調整：市中心 HP 1000→2000（原本 AI 軍隊到達後約 18 秒就結束，防守方來不及反應），AI 局變 15.3／15.6 分。另一個觀察：本人局 836 秒前只蓋 1 棟房屋，人口卡在 30，交給 M7.3 開場提示。待本人玩 3 局記錄時長 |
| M7.3 | 遊戲內繁中開場說明 | TODO |
| M7.4 | `.pyromod` 安裝包＋乾淨帳號安裝測試 | TODO |
| M7.5 | GitHub Release v0.4.0 | TODO |
| M7.6 | 1–3 人試玩＋回饋整理 | TODO |

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
