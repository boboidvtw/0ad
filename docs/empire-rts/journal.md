<!-- Purpose: 可追溯決策與工作檢查點；Created: 2026-09-06. -->
# 決策與工作紀錄

[進度主表](progress.md) · [開發計畫](plan.md) · [美術規格](art-direction.md)

## 決策索引

| ID | 日期 | 決策 | 原因／重新評估條件 |
| --- | --- | --- | --- |
| D01 | 2026-09-06 | Total Conversion Mod 優先，局部引擎修改按需 | 沿用既有 RTS 基礎；有可重現 Mod 限制或效能證據才重新評估 |
| D02 | 2026-09-06 | 首版一套文明、兩時代、一張地圖 | 先驗證完整玩法，避免時代與內容量膨脹 |
| D03 | 2026-09-06 | 空戰與潛艇風險提早調查 | 簡模可提早暴露底層問題；不等大量美術製作完才確認 |
| D04 | 2026-09-06 | 原創風格、共用骨架、模組化建築 | 兼顧辨識度與製作成本；先暫用素材，後正式樣板 |
| D05 | 2026-09-06 | 不從零重寫，也不預設完整複製原作 | 目前沒有證據表明全面重寫必要；以跨時代體驗為產品方向 |
| D06 | 2026-09-06 | repo 文件為進度紀錄來源 | 後續工作需能恢復上下文；狀態必須有證據，不依賴聊天記憶 |

## 2026-09-06 — 建立規劃基線

### 目標與授權範圍

使用者確認前述技術與美術方案，要求先把規劃、目標與進度寫入 `boboidvtw/0ad`。本次交付限定專案文件，寫入指定的 `master`；沒有執行遊戲實作、付費採購或遊戲發行。

### 檢查與證據

- 確認 repo 為 `https://github.com/boboidvtw/0ad`，預設分支 `master`，目前帳號有 push 權限。
- 來源快照：`a2b5838b181e1c3b770ae4e665811a87bd436fac`。
- 讀取根目錄與 docs 目錄清單、README.txt、LICENSE.txt、public/mod.json；根目錄與 docs 目錄沒有 AGENTS.md，新增的專案文件目錄此前不存在。
- 前期已閱讀 TechnologyManager.js 與 UnitMotionFlying.js；只構成原始碼層的初步可行性依據，沒有運行驗證。
- 本次只新增 5 份 Markdown 文件，原始程式碼、README.txt、授權與署名保留。

### 變更內容

- `README.md`：Fork 入口與文件導覽。
- `docs/empire-rts/plan.md`：產品目標、範圍、技術選擇與里程碑。
- `docs/empire-rts/art-direction.md`：美術方向、首批資產與驗收。
- `docs/empire-rts/progress.md`：T00–T15、依賴、狀態與證據規則。
- `docs/empire-rts/journal.md`：決策與本次工作檢查點。

文件發布的 commit 可從[此檔案的 Git 歷史](https://github.com/boboidvtw/0ad/commits/master/docs/empire-rts/journal.md)取得，避免在自身 commit 內填入尚未存在的 SHA。

### 驗證範圍與限制

本次驗證只涵蓋文件內容與相對連結、變更範圍及發布後檔案核對，不包含 Build、Lint 或遊戲測試。M0／T00 完成，其餘仍待實作。此紀錄不宣稱已建立 Mod、可玩原型或正式美術。

### 恢復工作的下一步

執行 T01：確認開發與首測環境，固定並驗證可運行基線；接續 T02 建立獨立 Mod。T03 需定稿兩時代規則與最小兵種表。所有後續結果回填 progress 與本紀錄。

## 後續紀錄格式

每次新增一節，記錄：日期、任務 ID、目標、重要決策、變更檔案與 commit、實際驗證（版本／環境／步驟／結果）、外部操作 ID（若有）、未解問題、下一個動作。不要填入憑證或不必要的私人資料。

## 2026-09-06～2026-09-07 — M1 Mod 與基線，畫面驗收待完成

- 使用者要求開始第一階段；工作涵蓋 T01、T02 與對應進度更新。
- 起點為 `f03b7d7173abea8bd05120cabb6f2f1a1e25ea96`。獨立 shallow／sparse checkout，開始時 Git clean；未發現 repo 的 AGENTS.md 或 CODING_RULES.md，依使用者全域規則工作。
- D07：選用官方 0.28.0 macOS ARM64 runtime；原 repo 引擎不升級、不宣稱已 Build。確切來源、平台與 hash 見 baseline。
- 新增 epoch_rts 0.1.0、Frontier 01 地圖、Pioneer 模板、macOS 啟動器、非視覺 smoke test、基線與素材登錄。
- 修正 R28 地圖 API 與 ES module 入口差異。最終 seed 42／7 真正引擎測試通過，無記錄錯誤／警告；驗收 JSON 已保存。
- Computer Use 回報輔助使用／螢幕錄製權限待完成。使用者提供系統設定截圖並詢問如何加入；已說明將 ChatGPT Computer Use 圖示拖入清單，不代替使用者擴大系統權限。
- T01 DONE；T02、M1 PARTIAL。畫面、選取與移動、正常退出尚未驗收；兩時代、正式美術、AI、多人與效能均未宣稱完成。
- 下一步：權限就緒後執行 evidence/m1-validation.md 的畫面步驟，完成後更新 T02／M1，再執行 T03。
- 完整 runtime、下載檔與本機日誌不入 Git；只提交本專案程式與去除私人資訊的驗證結果。此批 commit 可由本紀錄的 Git 歷史取得。


## 2026-09-07 — M1 最終畫面驗收完成

- 使用者回報已開啟權限並要求繼續。Computer Use 現可讀取並操作遊戲視窗。
- 使用程式 commit `4bd8e2ceb7031cc4c8260280fde969620b745d6d`，未修改 Mod 或引擎程式。
- 使用啟動器進入 Frontier 01，確認實際場景及自訂單位名稱；選取 entity 244，右鍵移動至空地並確認抵達。
- 保存 `m1-pioneer-selected.jpg` 與 `m1-pioneer-moved.jpg`；只含遊戲視窗及匿名測試玩家，保留暫用美術來源署名。
- 遊戲正常退出（exit 0），最終日誌 778 messages、0 errors、0 warnings；完整驗證與範圍見 evidence/m1-validation.md 及 m1-visual.json。
- T02／M1 更新為 DONE；保留先前 PARTIAL 紀錄作歷史，不改寫非視覺測試 JSON 為視覺通過。
- 下一步 T03：兩時代最小規則；M2 尚未開始。沒有把兩時代、正式美術、AI、存讀檔、多人或效能標為完成。
