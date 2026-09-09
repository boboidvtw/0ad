<!-- Purpose: T05 measured evidence and reproduction. Created: 2026-09-09. -->
# T05 時代研究與繁中介面驗收

基線：官方 0 A.D. 0.28.0 macOS ARM64，epoch_rts 0.3.0。測試日期 2026-09-08～09；來源指紋見 [manifest](t05-source-manifest.json)，提交由本文件的 Git 歷史追溯。

## 引擎實測

| 範圍 | 結果 | 證據 |
| --- | --- | --- |
| T05 研究，seed 42 | 77 項 PASS、0 錯誤／警告 | [完整結果](t05-seed-42.json) |
| T05 研究，seed 7 | 77 項 PASS、0 錯誤／警告 | [完整結果](t05-seed-7.json) |
| T04 經濟回歸，seed 42 | 183 項 PASS、0 錯誤／警告 | [完整結果](t05-economy-seed-42.json) |
| T04 經濟回歸，seed 7 | 183 項 PASS、0 錯誤／警告 | [完整結果](t05-economy-seed-7.json) |
| M1 smoke，seed 42 | 地圖與至少 100 turn PASS | [完整結果](t05-m1-seed-42.json) |

T05 涵蓋：工人用正常指令建造解鎖後的鍛造所、核對扣款與 500 HP；無／未完工兵營、逐資源少 1、錯誤建築／敵方研究與取消命令拒絕；工人與研究共用佇列；開始前失去兵營取消並全額退款且產生可翻譯通知、開始後失去兵營繼續；取消／研究場所摧毀退款與重新從零開始；鐵器 58 秒未完成、61 秒已完成；鐵刃步兵 30 秒訓練與成本；鍛造研究 28 秒未完成、31 秒已完成；舊與新長矛兵 Hack 8、鐵刃步兵 Hack 12，投石與採集不變；完成科技不可再扣款，重建場所保留科技。

時代與鍛造完成使用真正的模擬時鐘；其餘邊界案例允許設定資源、建立實體或直接推進生產。這是引擎整合測試，不是標準開局完整對局。183 項經濟回歸新增六棟建築的研究白名單，歷史 T04 的 177 項報告不覆寫。

## 畫面驗收

- 9 月 8 日已保存 [研究排隊](t05-research-queued.jpg)、[百分比](t05-research-progress.jpg)、[鍛造所鎖定](t05-forge-locked.jpg)、[鐵器解鎖](t05-iron-unlocked.jpg)。該次遊戲關閉後，9 日重新啟動示範接續驗證。
- 9 月 9 日再次以 GUI 支付 F400/W200/M100 研究，確認鐵器 HUD；兩次示範均正常退出（exit 0），未見引擎錯誤／警告。
- **整體 PARTIAL，T05 未標 DONE。** 桌面工具反覆回報 `noWindowsAvailable`，重新取得視窗及重置連線只短暫恢復。能讀取截圖、發送退出快捷鍵，但後續點擊不可靠。
- 待補 GUI：鍛造所完工後按鈕／成本、鍛造研究中與完成 HUD、新訓練鐵刃步兵可選取；分別確認缺兵營、資源不足及人口不足的繁中提示。引擎測試不能替代這些畫面案例。
- 恢復方式：保持 macOS 桌面解鎖、遊戲視窗可操作，重新啟動 `research-demo`；完成上述畫面案例並保存截圖後，才將 T05 標 DONE，再進入 T06。
- `research-demo` 初始四資源各 1000 與一座完成兵營；正式 `duel` 仍是 F300/W250/S100/M0、無額外兵營。示範以正常指令研究與建造，沒有免費完成科技。
- `duel` 與 `research-demo` 以本次啟動的 `zh_TW` 語系使用官方內建思源黑體；示範另關閉失焦暫停，兩者均不改永久偏好。

## 重現

```sh
EPOCH_RTS_0AD_APP='/path/to/0 A.D..app' tools/epoch-rts/launch-macos.sh research-demo
# 關閉所有遊戲後再執行，避免共用日誌互相覆蓋：
python3 tools/epoch-rts/smoke-macos.py --app '/path/to/0 A.D..app' --scenario t05 --seed 42
python3 tools/epoch-rts/smoke-macos.py --app '/path/to/0 A.D..app' --scenario t05 --seed 7
```

## 修正與限制

- R28 已排隊科技不能用 `CanResearch` 重檢，因為該方法會拒絕已排隊項目。改在第一份研究工作前直接檢查其前置條件，未滿足時由原生停止流程退款。
- R28 單實體 research／stop-production 命令未經群組所有權篩選。epoch 命令增加所有權、場所白名單與地基檢查；非 epoch 呼叫沿用上游。
- 通知測試起初讀取一般通知佇列，未能找到文字訊息；依 R28 實作改讀限時通知佇列後通過，沒有弱化預期訊息檢查。
- 經濟報告增加欄位後，一次輸出整份 JSON 未得到結果，前幾次回歸因而逾時，不算通過。將報告分成 4096 字元段輸出後，兩 seed 均可完整解析且通過；原始失敗日誌留在本機。
- Researcher、BuildLabel、selection_details 為固定 R28 的 GPL 程式衍生檔；升級 runtime 時需重新比較上游。沒有修改 C++。
- T06 標準整局、勝負、AI、多人、存讀檔、效能與正式美術不在本次完成範圍。

畫面包含 Wildfire Games 暫用美術；署名與來源見 [素材登錄](../assets.md)。原始日誌／重播包含本機資訊，不提交，公開 JSON 及截圖不含憑證。
