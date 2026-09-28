<!-- Purpose: Bounded native save/load and loopback multiplayer evidence. Created: 2026-09-28. -->
# T13 驗證紀錄

狀態：**限定DONE**。HEAD起點46045f8；2026-09-29核對後納入本機提交，識別以本次收尾紀錄所在commit為準。官方R28 0.28.0／macOS ARM64；不改C++、官方app或public.zip，不push。T05–T12歷史驗收維持原限定範圍。

## 驗收邊界

2026-09-28使用者明確核可：載入狀態完全還原、AI功能續局通過、雙客戶端同步通過，即可限定驗收；不保證讀檔後每一步與不中斷場重現相同。這項修訂保留原失敗證據，不把事件／終局不一致改寫成一致。

存讀檔比較的欄位：兩玩家資源、人口三值、勝負、已研究科技、研究中科技及進度／剩餘時間、統計、各自所有實體ID／template／位置／朝向／HP／UnitAI狀態與命令／生產研究佇列／施工進度／攜帶資源。這是明列快照完全相等，並非宣稱AI內部、Gaia或每個引擎component都逐byte相同。

兩個官方R28程序以localhost建立真實網路對局，各自使用人類席位、送普通stance命令，並在另一端檢查所有權與命令執行結果。經濟與完整青銅→鐵器對局沿用T06標準資源fixture；這是網路同步流量來源，不重開T06驗收，也不宣稱兩位人類自由對戰或多人Petra已驗收。

## 最終結果

完整數據與hash：[t13-results.json](t13-results.json)；來源129檔：[t13-source-manifest.json](t13-source-manifest.json)。8場存讀檔使用相同126檔manifest；另3檔為收尾native hash審計工具、其測試與GUI關閉順序測試。最終GUI僅改network關閉順序，與存讀檔場的來源差異明列下方，不將舊manifest覆寫。

| Seed | 模式／存檔門檻 | 終局模擬秒 | 結果 |
| --- | --- | --- | --- |
| 7 | 基準＋三份存檔 | 894.8 | PASS，38項、exit0、0錯誤／警告 |
| 7 | 原生讀檔 120秒 | 947.8 | PASS，38項、exit0、0錯誤／警告 |
| 7 | 原生讀檔 480秒 | 934 | PASS，38項、exit0、0錯誤／警告 |
| 7 | 原生讀檔 700秒 | 896 | PASS，38項、exit0、0錯誤／警告 |
| 42 | 基準＋三份存檔 | 884.6 | PASS，38項、exit0、0錯誤／警告 |
| 42 | 原生讀檔 120秒 | 928 | PASS，38項、exit0、0錯誤／警告 |
| 42 | 原生讀檔 480秒 | 968 | PASS，38項、exit0、0錯誤／警告 |
| 42 | 原生讀檔 700秒 | 884.4 | PASS，38項、exit0、0錯誤／警告 |

六次loaded快照與各自saved快照逐欄完全相等；兩seed的480秒均為鐵器研究中，700秒均已完成。8場來源穩定，六次load與基準runtime／來源相同，六份原生存檔hash維持不變。續局事件與final不同均保留為observations=False，不是逐步重現PASS。

| 網路Seed | 快照數（含final） | 比對到final毫秒 | 原生hash覆蓋 | 結果 |
| --- | --- | --- | --- | --- |
| 42 | 66 | 660000 | 起始至final連續3300回合，full／quick hash全部相等 | PASS，雙端自然exit0、0錯誤／警告／OOS |
| 7 | 63 | 630000 | 起始至final連續3150回合，full／quick hash全部相等 | PASS，雙端自然exit0、0錯誤／警告／OOS |

Seed42為首版觀測欄位；seed7為Map研究佇列修正後的最終網路回歸。原生full hash與quick hash分別按R28週期產生，不把所有quick hash稱為full hash。雙端尾端退出時間不同，僅比較到共同final驗收時點，不以任意短共同前綴冒充整局覆蓋。

工具：T13付款生命週期mock、5項parser測試（一般及-O）、3項native hash失敗案例測試，以及既有T12 adapter mock／8項parser回歸全部PASS；JS與Python語法、文件連結、diff空白檢查通過。未重跑T05–T11。

## 修正與審查

| 發現 | 修正／處理 | 驗證 |
| --- | --- | --- |
| T12付款wrapper捕捉讀檔前Trigger實例，讀檔後付款漏記 | 每次正常指令查詢目前Trigger；原指令仍只委派一次；未改付款／AI決策 | 真實原生讀檔續局38項＋test-t13-payment.cjs生命週期回歸 |
| GetQueuedResearch回傳Map，直接JSON會變成空物件 | 快照以排序keys與原生GetBasicInfo明確序列化 | 480秒研究進度／時間及載入後完全相等 |
| 分段結果不能因Python -O而略過檢查 | 用明確ValueError檢查順序／總數／型別／完整性 | 正常與-O的5項parser測試 |
| 同時關閉雙端會讓主機送向已關閉peer | 僅network分支改為主機先關、client延後；舊來源保留 | 關閉順序mock＋seed7真實網路回歸，原失敗留存 |
| 單純沒有OOS訊息不足以證明同步 | 讀取兩端原生replay的full／quick hash，要求起點到final時間的連續turn全部相等 | t13-audit-network.py及缺失／分歧／損壞證據測試 |
| app副本加Mod symlink影響簽章，首場退出-9 | 不繞過簽章，改回原本官方app與-unique-logs | 原app codesign與binary/public.zip hash不變 |
| 任意pregame腳本不會被R28明列ES module入口載入 | opt-in harness覆蓋測試入口，直接走官方StartSavedGame→loading | 新程序load場有loaded快照；原失敗場保留 |

完整人工程式審查範圍：T12Validation wrapper差異、T13 GUI入口／session hook、read-only快照、網路trigger、兩個runner、分段parser與native hash審計工具。檢查正常委派、序列化資料形狀、計時／收尾、兩端角色、缺少結果不得PASS、timeout只清理自身程序、來源與存檔hash、無shell拼接、無遠端發布。原生API對照實際public.zip與官方v0.28.0來源。Mock／syntax不替代引擎證據；沒有聲稱獨立第二位審查者。

## 執行方式

僅以額外 `-mod=epoch_t13_harness` 啟用；主Mod不依賴harness。使用者Mod目錄有指向 `tools/epoch-rts/t13-harness` 的本機symlink。Runner拒絕在其他pyrogenesis仍執行時開始。每場輸出到 `work/t13-save` 或 `work/t13-network`；存檔採唯一t13前綴，不覆蓋私人存檔。

```sh
/usr/bin/python3 tools/epoch-rts/t13-macos.py --seed 42
/usr/bin/python3 tools/epoch-rts/t13-macos.py --seed 42 --load-run work/t13-save/<save-run> --checkpoint 480000
/usr/bin/python3 tools/epoch-rts/t13-network.py --seed 42
/usr/bin/python3 tools/epoch-rts/t13-audit-network.py work/t13-network/<network-run>
```

Save矩陣為seed42／7，各120000、480000、700000毫秒附近存檔；以實際snapshot時間為準。480秒必須有鐵器研究正在進行、700秒必須已完成。每份存檔用新引擎程序StartSavedGame，沒有用fixture重建狀態。速度20僅為存讀檔驗證加速；網路使用原生2倍速。

每個網路程序stdout／unique-log／replay分開；共用user設定由CLI僅在本程序覆蓋，system_info與userreport診斷檔仍可能共用，不納入雙端獨立證据。

## GUI

- [讀檔後鐵器通知](t13-loaded-iron.png)：seed42、480秒存檔原生載入，續局顯示鐵器完成通知與已建兵營；圖片為原生F2輸出。載入準確性由同場快照而非圖片單獨證明。
- [網路玩家2畫面](t13-network-player2.png)：首場兩程序網路對局，紅色玩家2的標準資源基地、HUD與單位；兩程序身分、雙向指令及同步由同場日誌／replay證明。

## 限制與保留失敗

原生athen/Petra對照：`20260928T023407700122Z-save-42`與`20260928T023704202712Z-load-42`；480秒載入明列快照相等，兩端單機場皆AI勝利、exit0且無ERROR/WARNING，但最終時間1575.2／1552.2秒不同。舊工具的continued_final_state=False保留。這支持不以相同後续轨迹為驗收條件，並不定位所有差異的根因。

早期失敗：`20260927T025903142553Z-save-42`（副本退出-9）、`20260928T023026124623Z-load-42`（入口未載入）、`20260928T023231436680Z-load-42`（舊Trigger漏記付款）。原始result/log保留work；未刪除舊副本或profiles。

未驗收：跨機／WAN／跨平台、掉線重連、多人AI、自由人類對戰、任意存檔、升版本存檔相容、特殊空戰／潛艇、長時間壓力或效能。T14未開工。關閉session前確認本次所有程序結束；沒有排程或背景任務。

另保留 `work/t13-network/20260928T092918101412Z-7`：共同final 630000ms以前原生hash一致，但final後host出現送packet失敗，所以原runner與native審計仍為FAIL。關閉順序修正只改network分支；舊 `zz_t13.js` 封存於 `work/t13-source-before-network-exit`，存讀檔場仍引用各自當時manifest，不冒稱與最終GUI檔案hash相同。
