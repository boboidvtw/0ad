<!-- Purpose: M7.5 GitHub Release v0.4.0 notes for the epoch_rts play-test build. Created: 2026-11-25. -->
# Epoch RTS 試玩版 v0.4.0

這是在官方 **0 A.D. Release 28（0.28.0）** 上執行的原創 Mod。玩法是 1 對 1 對 AI：從青銅時代發展到鐵器時代，消滅對手，一局大約 15–20 分鐘。

> An original two-age RTS prototype mod for official 0 A.D. Release 28: one 1v1 map against the Epoch Petra AI. Install steps are in Traditional Chinese.

## 下載

| 檔案 | 說明 |
| --- | --- |
| `epoch_rts-0.4.0.pyromod` | 試玩包本體（66 個檔案，約 400 KB） |
| `epoch_rts-0.4.0.pyromod.sha256` | 檢查用雜湊 |

SHA-256：`823a18dcec6fb7f4abae8663d92d61ef00cf07be6e316020c8e3e8d57fa7ca64`

這個包可以重現：在這個 tag 上執行 `python3 tools/epoch-rts/package-mod.py`，會得到完全相同的雜湊。

## 安裝與遊玩

完整步驟見 [INSTALL.md](https://github.com/boboidvtw/0ad/blob/v0.4.0/docs/empire-rts/INSTALL.md)。重點：

1. 先裝好 0 A.D. R28，再雙擊 `.pyromod` 安裝。
2. **Settings → Mod Selection** 啟用 `Epoch RTS — Frontier Prototype`，按 Save and Restart。
3. 開局選地圖 **Epoch RTS - Frontier Duel**，玩家 2 的 AI **一定要改成 Epoch Petra (experimental)**。

## 這一版有什麼

- 一個文明「拓荒聯盟」、兩個時代（青銅、鐵器）、一張 1 對 1 地圖。
- 專用 AI「Epoch Petra」：進入鐵器時代後才進攻。
- 開局時有一頁繁體中文說明，按 Ctrl+P 可以隱藏或叫回來。
- 繁體中文翻譯（單位、建築、科技與開場說明）。

## 已驗證

| 項目 | 結果 |
| --- | --- |
| AI 對不操作的玩家（seed 42／7） | AI 在 917／935 秒獲勝，無錯誤 |
| 本人實玩 2 局 | 1068／1094 秒（約 18 分），皆 AI 勝 |
| 模擬乾淨安裝（暫時移開本機 0 A.D. 資料） | 由 R28 自動安裝；安裝後的檔案雜湊相同；從安裝檔跑完整局，0 錯誤 0 警告 |

## 已知限制

- 只在 macOS（Apple Silicon）上驗證過。Windows／Linux 的 R28 理論上可用，但沒測過。
- 只有一個文明、兩個時代、一張對戰地圖；AI 只在這張地圖的 Medium 難度驗證過。
- 預設的 Petra AI 沒有針對這個文明調整，可能不會正常發展，所以玩家 2 必須手動改成 Epoch Petra。
- 安裝後 Mod 不會自動啟用，要到 Mod Selection 手動啟用。
- 4K 螢幕全螢幕時介面字很小，可在 Settings → Options 調整介面縮放（GUI scale）。
- 建築與部分單位暫用 0 A.D. 原版的希臘、羅馬素材，不代表最終美術。
- 兩個 AI 互打通常要 25–35 分鐘才分出勝負；這只影響 AI 對 AI，不影響你對 AI。
- 未驗證：在真正的新 macOS 帳號上安裝，以及 Finder 雙擊、Mod Selection、開局設定這些選單操作。這些會由第一批試玩者實測。

## 回報問題

請回報給提供你這個下載連結的人，附上 `~/Library/Application Support/0ad/logs/mainlog.html`，並說明你卡在哪一步。

## 授權

- Epoch RTS 的程式碼與設定採用 GPL-2.0-or-later，見包內的 `LICENSE.txt` 與 `COPYING.txt`。
- 遊戲中引用的 0 A.D. 原版素材由 Wildfire Games 與各素材作者提供，依 CC BY-SA 3.0 使用（<https://www.wildfiregames.com/>、<https://creativecommons.org/licenses/by-sa/3.0/>）。這個包沒有複製任何原版素材檔。
- 本專案與 Wildfire Games 沒有關聯，也沒有得到官方背書。
