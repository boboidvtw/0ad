<!-- Purpose: Auditable T12 bounded AI closeout evidence. Created: 2026-09-27. -->
# T12 限定 AI 驗收證據

**DONE僅限[固定契約](../t12-ai-acceptance.md)**：官方R28、epoch文明、正常難度、兩seed對固定開局防守方，AI能正常經營、升級鐵器與進攻取勝。M5仍IN_PROGRESS，T13／T14未執行。全部本機工作，已授權本機提交；未push或發布。

## 環境與來源

- 驗收起點HEAD：master `d3723459714a6b140572ee1dd3568bf057d1a2f0`；T12既有內容保留並補齊，本報告所在commit為本機收尾提交。2026-09-26核對交接的五場舊37項結果及113檔manifest全部相同。
- 官方app 0.28.0、macOS ARM64；binary SHA-256 `531981d016596b0abde110cd239feaed98998c3fdaa837d0fa8d6f75482c81ef`；public.zip SHA-256 `ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429`。沿用匹配官方資料，不使用repo舊public。
- 新最終場次共同[113檔來源manifest](t12-source-manifest.json)，包含full Mod112檔與validation runner；[其他工具來源](t12-tool-manifest.json)。六場逐檔相同並符合當前來源。
- T11原105檔manifest逐檔未變；未改C++、M2既有模板、上游Petra或T05–T11驗收。沒有安裝依賴、付費工具、排程或背景任務。

## 最終引擎與重播

[完整38項、events、結果及原始檔SHA-256](t12-engine-results.json)。每場exit0、無錯誤／警告、來源未變；重播自然EOF，與對應seed完整suite相同。

| 本機run_id（work/t12-validation/） | 用途 | 結果 |
| --- | --- | --- |
| 20260926T004323034695Z-validation-42 | seed42／AI seed42 | 38 PASS，884.6秒AI勝利 |
| 20260926T004344451799Z-validation-7 | seed7／AI seed7 | 38 PASS，894.6秒AI勝利 |
| 20260926T004441245479Z-validation-42 | seed42重播 | 38 PASS，suite一致，EOF |
| 20260926T004510728304Z-validation-7 | seed7重播 | 38 PASS，suite一致，EOF |
| 20260926T004607948253Z-validation-42 | GUI引擎場 | 38 PASS，suite與seed42一致；未單独記人工操作 |
| 20260927T023449080415Z-validation-42 | GUI實際畫面補驗 | 38 PASS，suite與seed42一致；F2截圖、單位選取、Cmd-Q exit0 |

修正只有驗收觀測及parser，AI行為未變；新增房屋人口容量檢查後兩seed勝利時間與舊37項場次相同。沒有全狀態hash，因此不宣稱多人同步或完整狀態等價。

## GUI

[逐張來源、SHA與人工檢視紀錄](t12-visual-validation.json)。官方R28 observer、20×、1280×800、zh_TW；鏡頭導覽及單位選取，不發玩家2命令。runner的visual_verified仍為false，與本節人工驗收分開。

| 圖片 | 可見證據 |
| --- | --- |
| [AI基地](t12-base.png) | 工人、農田、木材與礦區；單張不單獨證明資源收入，收入由引擎統計支持 |
| [勝利結果](t12-victory.png) | 鐵器通知、Frontier Defender勝利、Player 1敗北及敵方市中心消失位置 |
| [鐵刃步兵](t12-swordsman.png) | 鐵刃步兵選取HUD、137/140 HP、紅色玩家與軍隊 |

另外保存09-22三張原圖：[基地／勝利通知](t12-historical-base.png)、[敵方市中心原址](t12-historical-enemy-site.png)、[投石兵HUD](t12-historical-slinger.png)。**更正交接描述：screenshot0002沒有勝利通知；通知在screenshot0001。** 原始截圖未修改或刪除。

本次直接看到市中心燃燒倒塌，但F2存下的是倒塌後空址，不把截圖描述為「進攻中」或燃燒瞬間。未驗1×整局、AI設定選單或完整UI流程。T11人物樣板與M2正式單位分離，本場暫用public角色不代表原創美術回退。

## 審查、工具與必要回歸

[完整本機審查](t12-code-review.md)，未宣稱獨立審查。修正parser略過損壞frame以及缺少房屋容量斷言，未重寫AI。

[工具結果](t12-tool-results.json)：8項Python測試PASS，包含5場歷史成功log；Node mock測試PASS，驗證實例隔離、phase映射、進攻gate及collection/buildOrders生命週期；三個JS語法檢查PASS。Python AST與3個map JSON亦已解析通過。

[官方Petra回歸](t12-regression-results.json)：`20260926T004546519116Z-public-42`，athen／原生Petra、同時載入最終epoch Mod。125個sample由1秒到1241秒；AI採集food16648／wood25768／metal9523、訓練283單位、建造57建築，完成城鎮升級，exit0且無錯誤／警告。11項正向行為／來源檢查PASS，T11來源105檔相同。

**探針runner exit1／complete=false保留**：遊戲在1800秒定時標記前自然退出；不是超時終止或已完成1800秒觀測。正向經營回歸足以支持「此限定場原生Petra仍工作」，不能推論全部文明／策略不受影響。

## 失敗、限制與資料保存

[歷史失敗摘要](t12-failure-history.json)列出4場早期frame缺失結果與日誌hash，原始資料留work，沒有以成功場覆蓋。更早「無cmd重播」只證明該觀測方法不足，不代表AI停擺；[初步調查](../t12-ai-preflight.md)保留歷史語境。

T07即時防空／90m落地區與T08 hidden攻擊限制不變；T16–T18 TODO。T13存讀檔／多人與T14效能不納入。根目錄profile.txt、profile2.jsonp維持runtime產物，未刪、未stage或commit；它們可能隨本機引擎執行更新。

公開證據意指repo內可檢視且已移除個人絕對路徑的摘要，不代表已上傳。完整commands與engine.log保留本機work，各場摘要附hash。下一步如另行開始T13，先讀[收尾交接](../SESSION-HANDOFF-2026-09-27-T12.md)，不要重做本任務已完成範圍。
