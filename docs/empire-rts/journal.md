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

### 2026-09-20～21 T09 引擎修改決策

- 起點master ac4cbff、clean，沿既有repo接續。讀T07／T08規格、原始JSON、來源manifest及T07 controller／command routing，完成Mod／共享JS／C++方案比較。
- 唯讀核對T07共68檔、T08共75檔均與來源manifest相同；T08 runner、實際R28 binary／public.zip與runtime manifest一致，Mod連結正確。核對結果存evidence/t09-decision-audit.json；這是檔案核對，不是新增引擎實測。
- 決策維持官方R28與獨立Mod，不啟動C++；防空即時傷害保留。完整潛艇、精確空中彈道、停機位／建築避碰仍未完成，不抹除T07/T08限制。
- 專用攻擊檢查列T16 TODO；明定新命令、既有攻擊、自動索敵、PerformAttack及原生攻擊者混用邊界。T17列潛艇最小垂直切片，T18列精確彈道／停機位擴充；目前均只有規格，未實作驗收。
- t09-engine-decision.md定義重新評估native修改的正確性／3D需求／性能／同步門檻；沒有證據就不因概念複雜而修改C++，也不保證Mod可以滿足全部需求。
- 唯讀審查通過；文件連結、JSON、來源雜湊、Git diff與任務狀態一致性核對完成。T09 DONE、M3 DONE只涵蓋限定原型／調查／決策；主線下一步T10。T05–T08本次未重跑。
- 全部變更是文件與核對紀錄，本機提交、未push；無背景任務或遊戲進程。新接續入口SESSION-HANDOFF-2026-09-21.md。

### 2026-09-21 T10 暫用房屋與原生匯入完成

- 起點master 6221d74、clean；R28 ARM64 binary／public.zip核對與T08一致，既有75個Mod檔未變。未修改C++、M2玩法或上游public。
- 新增原創參數房屋、標準庫COLLADA／PNG exporter、actor／模板、隔離地圖／13項探針與runner。來源、署名、授權、尺寸／UV與重現方法記於assets/epoch-rts/t10-house/README.md；工具4測試及--check通過。
- 實際原生匯入產生PMD／DDS；最終seed42／7各13項PASS，兩重播suite／來源一致、EOF exit0；無hash行，不宣稱多人同步。GUI13項、三張截圖、藍／紅玩家色與選取300HP，正常exit0。全部0錯誤／0警告；M1載入回歸PASS，T05–T08不重跑。
- 修正色帶被屋簷遮蔽與極小尺寸門高；後者改比例縮放及測試。最終程式唯讀複查通過；所有最終場次來源固定，證據evidence/t10-*。
- T10 DONE只涵蓋靜態暫用匯入；M4 IN_PROGRESS，T11 TODO。未用Blender、未做人物骨架／動畫、LOD、效能、建造／毀滅或正式HUD；模型與繼承footprint有空白邊界。
- T07精確彈道／停機位、T08攻擊gate與T16–T18未完成限制保留。只本機提交，不push；最新交接SESSION-HANDOFF-2026-09-21-T10.md。

### 2026-09-21～22 T11 原創美術垂直切片

- 按T10交接從master 9d36013、clean開工；實際官方R28 binary／public.zip與T10一致，82個既有Mod檔逐檔保留。只新增隔離T11子模板／actor／map與工具，沒有C++、上游public或M2正式模板修改。
- 先寫t11-art-slice.md最小範圍及A11-01～06；調查本機工具與固定v0.28.0 PMD／PSA／skeleton匯入器。PATH及/Applications無Blender／Assimp，採Python標準庫原創rigid7骨、5clip、色塊貼圖與3圖示；重用原T10房屋exporter但獨立輸出。來源／授權見assets/epoch-rts/t11-slice/README.md。
- 首輪原生匯入即產生PMD／PSA；修正驗收將@parent誤列玩法比較的3項誤判。補上worker Builder唯一house引用重映射，讓原創圖示連到原創施工／完工；新增施工狀態、房屋數量及50木扣款檢查。
- 最終seed42／7各126項PASS、兩原始重播suite／來源相同且EOF exit0；兩GUI均126項、正常exit0、0錯誤警告。無hash行，不宣稱完整狀態同步。09-22补拍含手動按鈕建房、50木扣款、人口20→30、揮矛雙姿勢、不可用提示、人物近照；這些為suite後操作，未混稱原兩seed重播內容。
- 5項工具測試、確定性--check、JS語法與來源核對PASS。原生5個PSA均7骨、有限數值且多幀變化；詳見evidence/t11-*。來源程式本機逐項檢視；未使用子代理，未宣稱獨立審查。未重跑T05–T10已完成限定驗收。
- T11／M4 DONE只限低面數樣板。完整人体rig／所有採集／跑步／動畫過渡／材質／LOD／正式HUD未完成；鷹架仍public。M4／16GB、小場景57–60 FPS僅觀察，T14未驗收。主線下一步T12先定義最小AI及官方R28 Petra介面調查。
- T07即時防空、90m落地區、精確彈道／停機位／建築避碰限制與T08攻擊gate未完成保留；T16–T18 TODO。沒有付費、push／發布、背景任務或私有記憶同步。交接入口SESSION-HANDOFF-2026-09-22-T11.md，本批本機提交由Git歷史追溯。

### 2026-09-22 T12 接續核對與初步探針

- 核對master d372345、起始clean；T11 manifest105檔符合，T10時82個Mod檔未變，官方R28 binary／public.zip及Mod連結符合。T11／M4限定完成範圍不變，未重做T05–T11驗收。
- 實際public.zip顯示Petra的structures/{civ}路徑與epoch_rts目錄不同；phase_epoch_iron前綴符合，完整phase鏈與class仍需調查。未修改AI、模板、C++或上游public。
- 兩seed短探針後加入固定AI seed的兩局與官方athen對照。重播header確認Petra設定，但三份重播均無cmd記錄；正向觀測尚未建立，不能推論epoch AI失效或相容。所有場次受控停止，未做重播執行或GUI。
- 最小候選驗收、來源雜湊、失敗／限制與下一步寫入t12-ai-preflight.md及evidence/t12-preflight.json。T12／M5 IN_PROGRESS僅代表調查開工，AI經營／升級／進攻未完成。
- 本次只本機文件與探針紀錄，未commit／push；沒有背景任務。下一步先完成官方Petra的有效AI行為觀測，再選接入架構。

### 2026-09-24 T12 未提交接續檢查點

- 使用者要求新session接續指令，將目前工程與證據保存在SESSION-HANDOFF-2026-09-24-T12.md。HEAD仍d372345；本輪T12未commit／push。
- 09-22已完成局部Petra適配：AI自身的模板路徑／phase链與進攻plan分類；未改舊Mod模板或C++。原生Petra實際能經營，早期無cmd重播不能推論AI停擺。
- 最終兩seed各37項PASS，884.6／894.6秒勝利；兩次重播suite相同、自然EOF。GUI37項與seed42 suite相同、exit0、無錯誤／警告；人工看過基地、升級／勝利及投石兵HUD。截圖尚未整理至evidence。
- 本日唯讀再核對5份113檔manifest完全相同且符合現有來源；T11的105個manifest檔仍相同。沒有pyrogenesis进程。
- T12 PARTIAL：尚待完整審查、工具驗證／必要回歸、公開證據／GUI紀錄及文件定稿。未追蹤profile.txt／profile2.jsonp留原位，勿誤提交或刪除。無背景任務或排程。


### 2026-09-26～27 T12 限定驗收收尾

- 依09-24交接，先核對HEAD d372345、全部未提交變更、官方0.28.0 binary/public.zip及五場113檔來源。T11 manifest105檔仍相同；保留profile.txt/profile2.jsonp，未刪、未stage／commit。
- 本機逐檔審查adapter、地圖、觀測、兩runner及測試；查對官方R28 phase、attackPlan collections／buildOrders、TechnologyManager研究事件及Commands正常交易。未使用子代理，不宣稱獨立審查；AI／C++／既有模板未改。
- 修正parser忽略損壞frame的缺口，新增房屋容量驗收。8項Python測試、Node instance隔離／collection mock及JS語法PASS；非以mock替代引擎。
- 最終兩seed各38項PASS，884.6／894.6秒AI勝利；兩重播suite相同／EOF／exit0，兩GUI引擎場均38項／exit0。09-27補拍採集、勝利與鐵刃步兵137/140HP HUD，Cmd-Q正常退出；全部最終場來源113檔相同、無錯誤／警告。
- 官方athen／Petra回歸125個sample、1241秒，經營／建造／生產／升級有實際證據；引擎自然exit0，因未到1800秒標記，probe complete=false／runner exit1仍原樣保存。另11項正向回歸PASS，不混稱定時觀測完成。
- 整理evidence/t12-*來源、結果、失敗hash、6張原圖及GUI紀錄；更正09-22第二張截圖沒有勝利通知。初步調查與旧交接加歷史標記，定稿t12-ai-acceptance.md、baseline與progress。
- T12標限定DONE，M5仍IN_PROGRESS；未重做T05–T11，未開T13。沒有push／發布、付費或背景排程。完整原始證據留work，公開摘要去除個人絕對路徑；本批全部未commit。收尾交接SESSION-HANDOFF-2026-09-27-T12.md。

### T12 本機提交

- 使用者選擇「先做T12本機commit」，明確授權限定提交，不push。再次核對T12來源113檔、額外工具3檔及T11保留105檔均符合manifest；只調整文件提交狀態，未改已驗收程式，因此不重跑引擎。
- 精確納入T12 Mod、runner、測試、文件及證據；profile.txt／profile2.jsonp與work不納入。提交識別以本紀錄所在Git commit為準，父提交d372345。T13未開工。

### 2026-09-27 T13 開工

- 使用者確認繼續T13；核對46045f8、僅兩profile未追蹤，官方R28 binary/public.zip雜湊符合T12。定義t13-save-network.md，不重做T05–T12。
- 查對實際public.zip的autostart與存檔GUI，以及官方Gitea v0.28.0的SavedGame、GameSetup、Paths與Network來源。GitHub舊鏡像無R28，改用官方Gitea。計畫獨立測試Mod與-writableRoot app副本，避免共享日誌覆寫；未改官方來源。

### 2026-09-28 — T13 原生存讀檔與網路實測（進行中）
- 核對HEAD 46045f8，保留既有profiles；官方R28 binary/public.zip hash與T12相同，codesign驗證成功。
- 原生存檔在120/480/700秒成功；480秒讀檔的列明狀態完全一致。觀測器在讀檔後捕捉舊Trigger實例，漏記付款，已改為每次正常指令時查詢目前Trigger，新增生命週期mock回歸；沒有改AI決策。
- 原生athen/Petra對照同樣出現不中斷場與讀檔續局的最終狀態差異（1575.2秒對1552.2秒），載入瞬間一致、兩場同一勝方、無ERROR/WARNING。因此不把未證實的逐步續局一致性寫成PASS；後續須分開報告功能續局和相同行為。
- 放棄app副本+writableRoot方式：副本曾退出-9且缺少可判定原因的日誌；副本新增資源會破壞簽章。改用未修改官方app、每程序-unique-logs、原生獨立replay目錄及各自stdout/work目錄。共用user設定只讀CLI覆蓋，system_info/userreport診斷檔共用，不宣稱全使用者目錄隔離。
- 首次讀檔bootstrap未載入（mainmenu使用ES module與明列腳本，不會讀任意pregame目錄檔）；改用可選測試Mod的最小page_pregame入口呼叫官方StartSavedGame。失敗產物保留work/t13-save。
- 最終seed7第一次回歸（20260928T092918101412Z-7）在共同final後發生主機送封包失敗；整局快照及原生hash一致，但no_errors=False，保留FAIL。調整僅network模式的GUI關閉順序為主機3秒、client10秒，讓server關閉時peer仍存在；新增角色／延遲／save-load分支mock，重新跑seed7。舊GUI來源封存work/t13-source-before-network-exit，存讀檔矩陣不因這個network-only收尾調整重跑。

### 2026-09-28 — T13 限定驗收收尾
- 使用者接受列明狀態還原＋AI功能續局＋真實雙客戶端同步，不保證讀檔後逐步重現；原生對照及失敗留存，未改寫AI或C++。
- 兩seed各三個原生存檔／新程序讀檔，8場各38項功能PASS；六次快照完全相等，研究中／研究後時點證據及存檔hash齊全。修正付款觀測器舊Trigger引用與快照Map漏序列化。
- 兩場實際loopback雙客戶端完整對局PASS，各端發出正常命令並驗執行，原生full／quick hash從起點至final連續一致；兩端exit0，無錯誤／警告／OOS。seed7為最終觀測器來源回歸。
- 付款生命週期mock、5項parser（一般／-O）、3項native hash負例及既有T12 adapter／8項parser PASS；完成程式與工具審查、GUI截圖、129檔來源表、公開結果與交接。T05–T11未重做。
- T13標記限定DONE，T14未開工；T13未提交、未push。profile.txt/profile2.jsonp保留原9/26時間；所有自啟驗證程序已結束，無排程或背景任務。

### 2026-09-29 — T13 本機提交核對

- 使用者明確授權僅限T13本機提交。起點46045f8；官方R28 0.28.0、binary與public.zip SHA-256及codesign均通過，129檔來源與公開manifest完全一致。
- 核對八場存讀檔原始result／engine.log／source-manifest hash，重新解析日誌快照與result一致；每場38項PASS，六次loaded與saved快照相等，六份原生存檔及封存副本hash吻合。存讀檔manifest唯一現行差異為network關閉順序GUI，舊版封存hash吻合，符合原交接說明。
- 核對兩場成功網路與一場保留失敗的result、native-audit、封存replay與HTML hash；從封存replay重新檢查到共同final的連續full／quick hash一致。失敗場仍保留FAIL。七份工具測試紀錄及兩張GUI截圖已核對；人工檢查T13差異、runner、harness與測試，未發現影響限定驗收的提交阻礙。
- 本次只改文件提交狀態；程式、manifest及原始證據未改，因此不重跑已通過的引擎／GUI驗收。提交前檢查文件連結、diff空白與限定暫存清單。提交識別以本紀錄所在commit為準，父提交46045f8。
- profile.txt、profile2.jsonp及work維持本機、不提交或刪除；T13限定DONE，T14未開工，無AI重寫或C++修改，未push或建立背景任務／排程。
