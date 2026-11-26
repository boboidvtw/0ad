<!-- Purpose: GitHub Release v0.5.0 notes for the epoch_rts 16-age play-test build. Created: 2026-11-27. -->
# Epoch RTS 試玩版 v0.5.0

這是在官方 **0 A.D. Release 28（0.28.0）** 上執行的原創 Mod。玩法是 1 對 1 對 AI：在 16 個時代（史前→太空）之間發展，消滅對手。預設從青銅時代開局，一局大約 15–20 分鐘。

> An original 16-age RTS prototype mod for official 0 A.D. Release 28: one 1v1 map against the Epoch Petra AI, with selectable start and end ages. Install steps are in Traditional Chinese.

## 下載

| 檔案 | 說明 |
| --- | --- |
| `epoch_rts-0.5.0.pyromod` | 試玩包本體（92 個檔案，約 110 KB） |
| `epoch_rts-0.5.0.pyromod.sha256` | 檢查用雜湊 |

SHA-256：`9532e71977289e4ae70162aa7395d13d293f59b4c436216ed3e051dec2df4666`

這個包可以重現：在這個 tag 上執行 `python3 tools/epoch-rts/package-mod.py`，會得到完全相同的雜湊。

## 安裝與遊玩

完整步驟見 [INSTALL.md](https://github.com/boboidvtw/0ad/blob/v0.5.0/docs/empire-rts/INSTALL.md)。重點：

1. 先裝好 0 A.D. R28，再雙擊 `.pyromod` 安裝。已經裝過 v0.4.0 的話，先刪掉舊的 `epoch_rts` 資料夾（見 INSTALL.md）。
2. **Settings → Mod Selection** 啟用 `Epoch RTS — Frontier Prototype`，按 Save and Restart。
3. 開局選地圖 **Epoch RTS - Frontier Duel**，玩家 2 的 AI **一定要改成 Epoch Petra (experimental)**。
4. 選用：在對戰設定的「玩家」分頁，用「開局時代」「結束時代」選時代範圍。

## v0.5.0 新增（相對 v0.4.0）

- **16 個時代**：史前、石器、銅器、青銅、鐵器、黑暗、中世紀、文藝復興、帝國、工業、原子（一戰）、原子（二戰）、原子（現代）、數位、奈米、太空。文藝復興以前每升一級需要 1 棟上一時代的代表建築；帝國以後只要資源，給數值加成。
- **開局時代／結束時代**：對戰設定新增兩個下拉選單，預設青銅→太空。
- **新建築與單位**：馬廄、攻城工坊、騎兵、騎士、攻城槌、射石砲。
- **AI**：Epoch Petra 會依時代階梯升級，升級排在組軍隊之後，讓對局維持在 20 分鐘內；進攻部隊會編入騎兵與攻城武器（多半在第二波以後才出現）。

時代數值與規格見 [age-ladder.md](https://github.com/boboidvtw/0ad/blob/v0.5.0/docs/empire-rts/age-ladder.md)。

## 已驗證

| 項目 | 結果 |
| --- | --- |
| 遊戲內自動檢查（seed 42／7） | t04 183 項、t05 77 項、16 時代 185 項、早期開局 48 項全過；duel 開局正常 |
| AI 對不操作的玩家（seed 42／7） | AI 在 1106／1126 秒獲勝，無錯誤無警告 |
| AI 對不操作的玩家（A4 調整時 5 個 seed） | 961–1126 秒，全部在 20 分內 |
| 本人實機點選（2026-11-27） | 「開局時代」「結束時代」下拉選單正常；史前開局、結束時代文藝復興可正常遊玩 |

## 已知限制

- 只在 macOS（Apple Silicon）上驗證過。Windows／Linux 的 R28 理論上可用，但沒測過。
- 只有一個文明、一張對戰地圖；AI 只在這張地圖的 Medium 難度驗證過。
- 開局說明（Ctrl+P）固定寫青銅→鐵器的流程；從其他時代開局時內容會對不上。
- 換開局時代不會改起始單位與資源；從史前開局時，起始的 2 名長矛兵要到銅器時代才能再訓練。
- 舊單位不會被新時代淘汰；帝國以後的時代沒有新單位，只有數值加成。
- 騎兵、騎士與攻城武器的數值還沒平衡。
- 真人對局時長還沒有 16 時代版的樣本；兩個 AI 互打通常要 25 分鐘以上才分出勝負。
- 預設的 Petra AI 沒有針對這個文明調整，玩家 2 必須手動改成 Epoch Petra。
- 安裝後 Mod 不會自動啟用，要到 Mod Selection 手動啟用。
- 建築與部分單位暫用 0 A.D. 原版的希臘、羅馬素材，不代表最終美術。
- macOS 預設音效輸出是 HDMI 電視或螢幕、而且裝置沒回應時，遊戲會一直跳 OpenAL 音效錯誤；這和 Mod 無關，把輸出改成內建揚聲器就好。

## 回報問題

請到 [GitHub Issues](https://github.com/boboidvtw/0ad/issues) 開一則新問題，說明你卡在哪一步，並附上 `~/Library/Application Support/0ad/logs/mainlog.html` 裡的錯誤訊息。Issues 是公開的，貼上前請刪掉裡面的使用者名稱與家目錄路徑。沒有 GitHub 帳號的話，回報給提供你下載連結的人也可以。

## 授權

- Epoch RTS 的程式碼與設定採用 GPL-2.0-or-later，見包內的 `LICENSE.txt` 與 `COPYING.txt`。
- 遊戲中引用的 0 A.D. 原版素材由 Wildfire Games 與各素材作者提供，依 CC BY-SA 3.0 使用（<https://www.wildfiregames.com/>、<https://creativecommons.org/licenses/by-sa/3.0/>）。這個包沒有複製任何原版素材檔。
- 時代名稱參考《Empire Earth》（世紀爭霸）的時代制度；本 Mod 不使用原作任何資產。
- 本專案與 Wildfire Games 沒有關聯，也沒有得到官方背書。
