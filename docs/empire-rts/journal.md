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

## 2026-09-07 — T03 兩時代規則定稿

- 使用者要求繼續下一步；本次交付 T03 設計規格，起點 `f157f014db233c5f3afb4f793490b3ba319f49cf`，開始時 Git clean。
- D08：原型固定青銅→鐵器、拓荒聯盟、4 資源、4 單位、6 建築；只保留一次時代升級與一項軍事科技。所有成本、時間、初始配置、人口與勝負條件記錄於 m2-rules.md。
- D09：以官方 R28 的希臘／羅馬美術暫用，獨立規則清單移除原版額外科技、兵種、捕獲及文明加成；不新增付費素材或服務。正式原創美術仍依 M4 執行。
- 閱讀固定官方 public.zip 的 Trainer、TechnologyManager、Foundation、Conquest／ConquestCommon 與候選模板，區分訓練全額退款、地基按最高進度退款及人口預留。研究開始前複查兵營是新增規格要求，尚未實作。
- 新增 m2-rules.md 與 m2-acceptance.md，更新 README、plan、progress。驗收清單共 26 個案例，全部標為 NOT RUN；T03 的靜態檢查涵蓋範圍、成本、解鎖依賴與開局可達性。
- 本批僅文件變更；檢查 Markdown 相對連結與 diff 格式，不執行遊戲 Build 或對局，也不宣稱數值平衡完成。提交版本由本節 Git 歷史識別。
- T03 DONE，M2 IN_PROGRESS；下一步 T04：epoch 文明與模板、duel 地圖、經濟及生產實作。T04–T06 尚未開始，M1 既有證據維持不變。

## 2026-09-07～2026-09-08 — T04 經濟、生產與實際引擎驗收

- 使用者要求繼續下一項，並於 2026-09-08 要求繼續完成。起點 `707e4e664a574189b6bf88a8456896ec09c1850e`，開始時 Git clean；保留本次未提交進度接續工作。
- 建立 Frontier Union 玩家／文明、四單位與六建築模板、duel 地圖及初始化腳本；0.2.0 保留 M1 地圖。研究入口與完整時代介面留給 T05。
- D10：固定 R28 的建造指令未強制 Builder 清單，科技失敗分支亦未在扣款前返回。以 epoch 專用指令包裝補上清單、科技與單位佔位檢查，不修改原引擎或非 epoch 玩家的建造規則。
- D11：遊戲實際顯示繁中缺字方框；原型改用可讀英文，繁中字型／翻譯列入 T05。epoch 小地圖邊框暫借雅典背景；來源加入 assets。
- 建立專用引擎驗收地圖與腳本，分清可控制資源／工作時間的整合案例，以及正常模擬時間的採集、建造、維修與跨基地移動。測試結果不是完整對局或平衡證明。
- 修正驗收工具的 JSON 邊界：引擎 print 後可能緊接 Turn 文字；完整解析結果後才終止，部分寫入會等待下次讀取。重現方式與實際結果見 evidence/t04-validation.md。
- 接續 T05：時代升級、軍事科技、HUD 與繁中字型；AI、多人、存讀檔與正式美術仍未驗收。
- 最終結果：T04 DONE；seed 42／7 各 177 項斷言通過。M1 兩 seed smoke 及新版 Pioneer GUI 選取／移動通過；T04 與 M1 的 GUI 均正常退出 exit 0、0 錯誤／0 警告。截圖與去識別化結果已入 evidence，原始本機日誌／重播不提交。
- XML／JSON、JS／Python／Shell 語法、文件連結與實測程式 hash 核對通過；僅提交本批 Mod、測試工具及對應文件。提交版本由本節 Git 歷史追溯，沿用對 boboidvtw/0ad master 的既有授權推送。

## 2026-09-08～09 — T05 研究實作與部分畫面驗收

- 基於 b0efcaa 的 0.2.0，建立 0.3.0 鐵器與鍛造研究、共用生產佇列、開始前兵營檢查及退款、epoch 研究／取消命令所有權與場所白名單。未修改 C++。
- D12：R28 自帶繁中思源黑體；啟動時指定 zh_TW，新增 Mod 翻譯與時代／研究 HUD，不下載新字型、不新增付費。研究示範單次關閉失焦暫停，不改永久設定。
- D13：Researcher 開始前直接驗證科技前置，不使用會拒絕已排隊項目的 CanResearch。非 epoch 研究與建造沿用上游。
- 最終研究測試 seed 42／7 各 77 項 PASS（包含實際模擬時鐘及工人建鍛造所）；經濟各 183 項 PASS，M1 smoke seed 42 PASS。過大報告改為分段輸出；文字通知測試依 R28 改讀限時通知。失敗嘗試未算通過。
- GUI 已確認青銅／鐵器、排隊／百分比、解鎖與正常支付；保存四張截圖。9 日兩次示範正常 exit 0，但操作工具反覆 noWindowsAvailable，重置只短暫恢復。
- **T05 PARTIAL，任務 IN_PROGRESS，沒有宣稱 DONE。** 下一步在可操作的遊戲視窗補完鍛造研究、鐵刃單位與三類不足提示，見 evidence/t05-validation.md；T06 整局尚未開始。這是可接續的 checkpoint，不是完整對局驗收。
- 此批 scoped commit/push 沿用 boboidvtw/0ad master 的既有授權；來源 hash、測試與公開截圖一併保存，原始日誌和本機重播留在忽略的工作目錄／runtime 目錄。

## 2026-09-09 — T05 剩餘畫面驗收完成

- 接續 `2fa5cd91a4191a1b0ed2c47ab8f84141a3d6c64d`，沒有修改遊戲或測試程式；來源 manifest 逐檔核對，沿用已通過的引擎報告。
- 研究示範以正常指令完成鐵器、訓練鐵刃步兵、建鍛造所與鍛造兵器；觀察到研究進度及完成 HUD。視覺重播確認移動抵達與人口不足提示；另以標準 duel 確認兵營不足、建成後資源不足提示。保存八張截圖與去識別化實測摘要，詳見 evidence/t05-validation.md。
- 三次執行均正常退出；最後標準開局日誌 0 錯誤／0 警告。重播 metadata 的 researchedTechs 序列化為空物件，不用它證明科技完成；完成狀態依實際 GUI 觀察與既有引擎測試。
- T05 更新 DONE；M2 維持 IN_PROGRESS，下一項 T06 的戰鬥、勝負邊界與標準完整對局仍 NOT RUN。正式美術、AI、多人與存讀檔未完成。
- 本批只提交驗收文件與截圖，檢查連結、來源 hash、圖片格式與 diff；沿用 boboidvtw/0ad master 授權推送，提交可由本節 Git 歷史追溯。

## 2026-09-10～11 — T06 戰鬥、勝負邊界與標準整局完成

- 依 SESSION-HANDOFF 接續，起點 `8d5ee7b4e54f224a231d481557d151d75a015503`，核對本機／遠端 master 一致且 Git clean；R28 0.28.0 與既有 Mod 架構不變。T05 不重做，未改 C++ 或正式玩法元件。
- 新增 T06 專用 maps、Trigger 案例與 runner。兩 seed 各 8 場／191 斷言通過；8 場 replay 共 134 斷言通過。四單位實際攻擊、六建築 HP／抵抗、中心勝負、投降、研究中毀滅均有實測；所有最終場次 0 錯誤／0 警告。
- D14：同回合雙中心依 R28 確定性銷毀順序：先致命傷1再2，P2勝；先2再1，P1勝；兩中心均毀且只有一次勝負事件。重播事件、結果、時間一致；原始無畫面 replay 無 hash 行，不宣稱全狀態 hash 或多人同步已驗證。
- 標準資源整局只發正常玩家指令；seed 42／7 分別 649.8／621 秒勝利。對手保留初始固定防守、不經營經濟；不是 T12 AI。完整經濟到勝利步驟與支付快照見 evidence/t06-validation.md。
- seed 42 原始1×視窗整局 exit 0；11日視覺重播補取勝利通知、中心毀滅後鐵刃步兵選取與10:50摘要，exit 0、0錯誤／0警告，suite與原始場次完全相等。後期畫面均明示為重播，沒有另存正在交戰或研究完成瞬間截圖。
- 修正測試器：勝負即退出前取結果、攻擊移動處理迷霧、資源值快照、研究已開始／扣款檢查、replay metadata／EOF／MISMATCH／baseline 比對。程式唯讀審查及修正後複查通過。T04／T05共享程式未變，因此不重跑。
- T06／M2 更新 DONE，同步 progress、acceptance、rules歷史狀態、plan、README及evidence；下一步 T07 先調查 R28 飛行相關介面及定義最小案例。T07–T15 保持 TODO，不宣稱正式美術、AI、多人、存讀檔或效能完成。
- 公開證據排除本機路徑；原始日誌、重播與引擎產生的 profile 留在本機忽略工作目錄。本次只做 scoped 本機提交，未執行 push／發布或私人設定同步。

## 2026-09-13 — T07 獨立飛行原型完成

- 從本機 `cdcbffc`、clean worktree 接續；恢復同一官方 R28 ARM64，核對既定 DMG SHA-256。版本仍 0.28.0／Mod 0.3.0，沒有 C++、上游 public 或 T05 修改。
- 新增 EpochAircraft 控制器、R28 衍生 EpochAircraftMotion，以及僅分流飛機 walk／attack／stop 的 helper；飛機、機場、防空模板與 probe／validation／手動 demo 專用地圖。M2 建造白名單不增加現代單位。
- D15：Stop 返航最近己方有效機場，無機場則就地降落；採90公尺區域，不含精準跑道／停機位。原生 Stop 反轉 landing、目標移動保留 landing、未來位置秒／毫秒換算缺口，在獨立元件修正。
- D16：原生 AA 彈道多次未命中。放大 footprint 只過一 seed，已撤回；秒／毫秒修正及高速彈丸也未消除約6公尺取樣落差。原型 AA 改用原生即時 Ranged 傷害，對地仍彈道，精確空中彈道留待 T09。
- 最終兩 seed 各36項 PASS、各36項重播事件／結果一致且自然 exit0；probe 2項 PASS。防空 HP200→42.5；返航距機場5.534公尺；補實際滑跑停止、轉敵機場改降、敵方命令及移動目標追蹤回歸。無 hash 行，不宣稱全狀態同步。
- GUI 兩場正常 exit0、0錯誤／0警告。選取／起飛／對地傷害、房屋毀滅、受損110/200、返航、再起飛及 H 連按落地已見畫面；模型重疊是原型限制。第一場只擴充測試函式，舊 runner 來源雜湊不能證明初始整份 script；以最終 full Mod manifest 固定場次補核對，並修正 runner 啟動／結束 manifest 檢查。
- M2 回歸：戰鬥81項、兩 seed 整局各15項且649.8／621秒勝利、T04經濟183項、M1 smoke 通過；T05未重跑。來源、結果與7張GUI截圖見 evidence/t07-*。
- 唯讀程式審查提出的地面返航、移動目標追蹤、fixture與滑跑覆蓋問題均修正、複查通過。T07標DONE，M3保持IN_PROGRESS；下一步T08，T09待兩項調查齊備。
- 此批只做 scoped 本機提交，未 push、發布或同步私人設定。原始日誌與 replays 留在本機忽略目錄；提交版本可由本節 Git 歷史追溯。

### 2026-09-13 收工交接

- 使用者要求先收工；核對實作HEAD c0266d9、工作樹clean、無遊戲進程。建立 SESSION-HANDOFF-2026-09-13.md，保存T07實測、R28基線、限制與T08開工順序。
- 交接文件另作本機提交，未push；未安排背景工作。可安全關閉session，下一次從repo內交接文件接續。

### 2026-09-20 T08 潛艇／水下規則調查

- 依9/13交接接續既有repo；起點master e956ac6、clean，無遊戲進程；R28 0.28.0 ARM64、macOS26.6.2、Mod symlink及官方DMG SHA-256與基線一致，未使用舊public。
- 定義水面／水下、2秒切換、深度4／安全水深6、普通LoS＋60公尺偵測、艦砲／反潛／魚雷規則。規則與實作範圍分開；只做隔離探針，不接入M2經濟，不改C++。
- 實際public.zip、官方R28 Position文件與native runtime binding確認FloatDepth、SetHeightFixed、scripted Visibility、RequestVisibilityUpdate。高度本身不隱身；逐玩家可見性與偵測進出／轉敵／死亡／浮起可用。
- 兩seed各30項通過；水面20／海床8／潛深4，航行仍y16，船停在陸地邊界x508.5。原生hidden新攻擊2000→1956.26、失去偵測後持續攻擊1897.94→1854.20：確認需要專用attack gate，沒有宣稱需求已實作。
- 最終runner與fullMod來源固定，兩次重播事件／結果一致、自然EOF／exit0，沒有hash行，不宣稱全狀態同步。四階段GUI8項API檢查與四張截圖，exit0／無錯誤警告；暫用船桅杆露水、選取及盟友GUI未驗。M1載入回歸PASS，T05–T07未重做。
- 首次水位偏移與第二次passive自主逃跑造成的fixture問題已修正並重跑；失敗紀錄留work。重播profile產物改存各run輸出目錄；未刪檔。唯讀審查與複查無阻擋項。
- T08標DONE僅代表調查／決策；完整可玩潛艇延後。T09 TODO，下步比較獨立Mod狀態／偵測／攻擊gate，保留T07精確彈道與停機位限制。2秒切換、淺水路徑、動態武器矩陣、延遲傷害、多人／存讀檔／效能／實體魚雷全部未驗收。
- 證據見evidence/t08-*、規則t08-submarine-feasibility.md；本批只本機工作，不push，無背景服務或排程。
