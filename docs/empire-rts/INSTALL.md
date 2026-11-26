<!-- Purpose: M7.4 player install guide for the epoch_rts .pyromod on official 0 A.D. R28. Created: 2026-11-24. -->
# 安裝與遊玩：Epoch RTS 試玩版 v0.5

一局 1 對 1 對 AI：在 16 個時代（史前→太空）之間發展，消滅對手。預設從青銅時代開局，大約 15–20 分鐘。

## 你需要

| 項目 | 說明 |
| --- | --- |
| 0 A.D. **Release 28（0.28.0）** | 從官方網站 <https://play0ad.com/download/> 下載。其他版本無法載入這個 Mod |
| `epoch_rts-0.5.0.pyromod` | 試玩包本體（約 110 KB） |
| `epoch_rts-0.5.0.pyromod.sha256` | 選用：檢查下載是否完整 |

只在 macOS（Apple Silicon）上驗證過。Windows／Linux 的 R28 理論上可用，但沒測過。

## 安裝步驟

1. **安裝 0 A.D. R28**，先開一次遊戲確認能進主選單，再關掉。
2. **（選用）檢查檔案**：在「終端機」執行下面指令，輸出的雜湊要和 `.sha256` 檔內容相同。

   ```bash
   shasum -a 256 ~/Downloads/epoch_rts-0.5.0.pyromod
   ```

3. **安裝 Mod**：裝過 v0.4.0 的話，先刪掉舊資料夾 `~/Library/Application Support/0ad/mods/epoch_rts/`（或把它移到別處）。再直接雙擊 `epoch_rts-0.5.0.pyromod`，系統會用 0 A.D. 打開並自動安裝。遊戲會停在主選單，Mod 還**沒有啟用**。
   - 雙擊沒反應時，可以把檔案拖到 0 A.D. 的圖示上。
   - 安裝位置：`~/Library/Application Support/0ad/mods/epoch_rts/`。
4. **啟用 Mod**：主選單 → **Settings（設定）** → **Mod Selection（Mod 選擇）**。
   - 在上方「Available Mods」清單**雙擊** `Epoch RTS — Frontier Prototype`，它會移到下方「Enabled Mods」。
   - 按 **Save and Restart（儲存並重新啟動）**。以後開遊戲都會自動帶著這個 Mod。
5. **改成繁體中文**（建議，開場說明與單位名稱有繁中翻譯）：主選單 → **Settings** → **Language（語言）** → 選繁體中文 → 確定，依提示重新啟動。

## 開一局

1. 主選單 → **單人遊戲（Single-player）** → **對戰（Matches）**。
2. 地圖選 **Epoch RTS - Frontier Duel**。雙方文明會自動鎖定為「拓荒聯盟」。
3. **玩家 2 的 AI 一定要改**：點玩家 2 那一列的 AI 名稱，從清單選 **Epoch Petra (experimental)**，難度維持 **Medium（中等）**。
   預設的 Petra AI 沒有針對這個文明調整過，可能不會正常發展，你會一直等不到對手。
4. 選用：在「玩家」分頁用 **Start Age（開局時代）**、**End Age（結束時代）** 選時代範圍，預設青銅→太空。開局說明是照青銅開局寫的，選別的開局時代時內容會對不上。
5. 按 **Start Game!（開始遊戲）**。開場時畫面上方有一頁說明，按 **Ctrl+P** 隱藏或叫回來。

### 進階：一行指令直接開局

不想點選單的話，可以在「終端機」執行（App 裝在「應用程式」資料夾時）：

```bash
"/Applications/0 A.D..app/Contents/MacOS/pyrogenesis" -mod=public -mod=epoch_rts -conf=locale:zh_TW -autostart=random/epoch_frontier_duel -autostart-players=2 -autostart-size=192 -autostart-ai=2:epoch_petra -autostart-aidiff=2:3
```

## 解除安裝

1. **Settings → Mod Selection**，在「Enabled Mods」雙擊 `Epoch RTS` 停用，按 **Save and Restart**。
2. 刪除資料夾 `~/Library/Application Support/0ad/mods/epoch_rts/`。

## 已知限制

- 只有一個文明、一張對戰地圖；AI 只在這張地圖的 Medium 難度驗證過。
- 換開局時代不會改起始單位與資源；騎兵、騎士與攻城武器的數值還沒平衡。
- 預設音效輸出是 HDMI 電視或螢幕、而且裝置沒回應時，遊戲會一直跳 OpenAL 音效錯誤；把 macOS 的聲音輸出改成內建揚聲器即可，和 Mod 無關。
- 4K 螢幕全螢幕時介面字很小，可在 Settings → Options 調整介面縮放（GUI scale）。
- 建築與部分單位暫用 0 A.D. 原版的希臘、羅馬素材，不代表最終美術。
- 兩個 AI 互打通常要 25–35 分鐘才分出勝負；這只影響 AI 對 AI，不影響你對 AI。
- 回報問題：到 <https://github.com/boboidvtw/0ad/issues> 開新問題，附上 `~/Library/Application Support/0ad/logs/mainlog.html` 裡的錯誤訊息（Issues 是公開的，請先刪掉使用者名稱與路徑）。
