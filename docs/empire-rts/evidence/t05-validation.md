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
- **T05 DONE。** 9 月 9 日已補齊下列 GUI 案例，整理於 [畫面實測紀錄](t05-visual-validation.json)。先前提交 `2fa5cd9` 因 `noWindowsAvailable` 保留 PARTIAL；本次恢復操作後完成驗收，歷史 checkpoint 保留於 journal。
- 實際研究示範：正常支付 F400/W200/M100 升鐵器；從兵營訓練並選取 [鐵刃步兵（140 HP）](t05-sword-selected.jpg)，下達移動命令。另保存 [兵營選單](t05-sword-menu.jpg)。
- 三位工人正常建成 [鍛造所（500 HP）](t05-forge-complete.jpg)，核對木材減 150、石材減 100；點擊鍛造兵器，金屬減 100，保存 [研究 43% 的畫面](t05-weapons-progress.jpg)。本次操作亦觀察到頂部「鍛造兵器已完成」，但未另存完成瞬間截圖；精確食物扣款、完成時間及傷害效果由上列引擎案例驗證。
- 同場重播完成後選擇留下，確認 [人口 20/20 與「人口上限不足」提示](t05-population-blocked.jpg)，並選取 [已抵達命令目的地的鐵刃步兵](t05-sword-arrived-replay.jpg)。這兩張來自視覺重播；觀察者介面不作為時代 HUD 的證據。
- 正式 `duel` 標準開局確認 [缺已完工兵營及資源提示](t05-missing-barracks.jpg)；六位工人正常建成兵營後，確認 [研究資源不足](t05-missing-resources.jpg)，缺兵營條件已消失，未建立研究佇列。
- 研究示範、視覺重播與標準開局均正常退出（exit 0）。標準開局退出後的最終日誌為 0 錯誤／0 警告；共用日誌會覆寫，不將該次數字當作其他場次的獨立日誌證據。
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
