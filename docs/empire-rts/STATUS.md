<!-- Purpose: 專案現況與下一步的唯一入口（≤80 行）；Created: 2026-11-15. -->
# STATUS

更新：2026-11-15

## 現況

| 範圍 | 狀態 | 一句話 |
|---|---|---|
| M1 Mod 骨架 | DONE | R28 macOS ARM64 可啟動，Frontier 地圖、選取與移動正常 |
| M2 兩時代流程 | DONE | 青銅→鐵器整局：採集、建造、訓練、研究、作戰、勝負 |
| M3 特殊機制 | DONE（原型） | 飛機／機場／防空原型、潛艇調查；維持 R28、不改 C++ |
| M4 美術切片 | DONE（樣板） | 原創低面數工人、長矛兵、房屋與 3 個圖示 |
| M5 AI／存檔／多人 | DONE（限定） | 兩 seed 對固定防守的 AI；存讀檔；本機 loopback 雙端 |
| T14–T18 | 凍結中 | 依重設計畫 Phase 1 結案，未通過的項目改記為已知限制 |

## 下一步

| # | 項目 | 狀態 |
|---|---|---|
| P0 | 重設計畫 Phase 0：止血 | DOING（只剩 0.1 排程、0.5 LFS） |
| P1 | Phase 1：progress.md 的 T14–T18 改為 DONE／DROPPED＋已知限制 | TODO |
| M7.1 | `epoch_frontier_duel` 接上 T12 AI，本人玩一局 | TODO |
| M7.2 | 最小平衡，一局 10–20 分鐘 | TODO |
| M7.3 | 遊戲內繁中開場說明 | TODO |
| M7.4 | `.pyromod` 安裝包＋乾淨帳號安裝測試 | TODO |
| M7.5 | GitHub Release v0.4.0 | TODO |
| M7.6 | 1–3 人試玩＋回饋整理 | TODO |

## 已知限制（摘要）

T14 不限 FPS 未達門檻、混合交戰尾段 FAIL；T15 candidate42 FAIL；T16 海戰／death gate FAIL；T17 潛艇暫緩；T18 GUI／停機位未完成。細節見 [progress.md](progress.md)。

## 待本人處理

- `0ad-t14` 每 5 小時的排程：本機的 Claude 排程與 Codex 本機資料庫都找不到。請在 Codex app 的 Automations 裡停用它，或改成「每天跑一次 smoke test＋回報」。
- Git LFS：本機沒裝 `git-lfs`，0.5 暫緩；要做的話先跑 `brew install git-lfs`。
