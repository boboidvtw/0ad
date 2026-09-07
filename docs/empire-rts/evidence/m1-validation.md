<!-- Purpose: Actual M1 acceptance evidence and outstanding checks; Created: 2026-09-07. -->
# M1 驗收紀錄

日期：2026-09-06～2026-09-07。結論：**PARTIAL；引擎基線與非視覺測試通過，畫面與操作待驗收。**

## 環境與版本

- macOS 26.6.2（25G83）、Apple M4、16 GB RAM，arm64。
- 官方 0 A.D. 0.28.0 macOS ARM64；DMG SHA-256 與[官方校驗檔](https://releases.wildfiregames.com/0ad-0.28.0-macos-aarch64.dmg.sha256sum)一致：`8c53566123fed9a79766c364e543d6e9dc7c84f642c78d2bb5892eeea9c4c052`。
- Bundle 與 public/mod.json 都為 0.28.0；自訂 Mod 0.1.0，沒有引擎程式修改。
- 測試方法見 [baseline](../baseline.md)，工具見 [smoke-macos.py](../../../tools/epoch-rts/smoke-macos.py)。

## 已執行結果

| 檢查 | 結果 | 證據及限制 |
| --- | --- | --- |
| 下載完整性與安裝 | PASS | SHA-256 一致；磁碟映像 CRC 驗證通過；app 複製到本地測試目錄 |
| 官方 runtime 啟動 | PASS | 遊戲程序啟動並完成顯示裝置初始化，1280×800；尚未取得畫面截圖 |
| Mod 相依與載入 | PASS（非視覺） | 引擎載入 public 0.28.0 與 epoch_rts 0.1.0，實際生成 Frontier 地圖並模擬 |
| seed 42 | PASS（非視覺） | [原始結果 JSON](m1-seed-42.json)：至少 100 回合後主動停止，無記錄錯誤／警告 |
| seed 7 | PASS（非視覺） | [原始結果 JSON](m1-seed-7.json)：同上 |
| 語法 | PASS | JSON／XML 可解析、JavaScript 以 ES module 語法檢查、啟動腳本通過 bash 語法檢查 |
| 畫面、模型與自訂名稱 | PENDING | 需要 Computer Use 輔助使用／螢幕錄製權限；未以日誌代替視覺證據 |
| 選取與移動 | PENDING | 權限就緒後實際操作 Pioneer，再檢查錯誤日誌 |

測試的 `exit_code: -15` 是測試在回合門檻後主動以 SIGTERM 結束自己啟動的程序，並非正常遊戲退出驗收。兩個 seed 只證明這兩組地圖設定的生成／模擬，不是全部隨機地圖、採集／建造流程、存檔、AI、多人或效能驗收。

地圖 marker `pioneers=2` 是生成器成功放置兩個自訂模板引用後產生的訊息；配合實際引擎模擬與無錯誤日誌，作載入驗證。它不能證明模型外觀、可選取性或移動表現，因此仍保留人工／畫面驗收。

## 已修正的相容性問題

1. R28 的 `playerPlacementCircle` 回傳物件，已改用具名欄位。
2. 舊 `isNomad()` 呼叫改為讀取 map settings。
3. R28 使用 `export function* generateMap(mapSettings)`；初版沿用舊入口導致載入未完成，非視覺路徑出現 `fmt::v7::format_error`。先用官方地圖確認引擎可運行，再修正入口並重新通過自訂地圖測試。

另曾試用 RL interface，但這個發行包的該啟動嘗試直接退出且沒有建立可用服務，未將它列為交付或驗證依據。最終測試使用實際可運行的 `-autostart-nonvisual`，不依賴額外服務。

## 尚待執行的畫面驗收

1. 執行 launch-macos.sh，確認 Frontier 01 載入成遊戲場景而不是停在載入頁。
2. 確認草地、市中心、基本資源與玩家單位沒有缺失貼圖或明顯異常。
3. 選取市中心附近的自訂單位，確認顯示 Epoch Pioneer／Frontier Pioneer 及原型說明。
4. 命令 Pioneer 移動到空地，確認位置改變與動畫正常。
5. 保存只含遊戲畫面的截圖，重新檢查日誌並記錄結果。通過後更新 T02／M1。

完整引擎日誌可能包含本機路徑及設定，僅保留本機；repo 中只提交去除私人資料的結果。此文件不附使用者提供的 macOS 權限畫面。
