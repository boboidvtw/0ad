<!-- Purpose: User-requested fresh-session transfer with exact pending review gates. Created: 2026-10-15. -->
# T14–T18 新 session 接續

先讀本檔、work/t14-t18-session-transfer-20261015/current-state.json，再讀 2026-10-14／2026-10-13 交接、最新 progress/plan/journal 與 AUTONOMOUS-EXECUTION-T14-T18-2026-10-11.md。實際 repo：/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad；ChatGPT 專案目錄不是 repo。HEAD726a3aefcae830f605de438cd13192cc6330414e，index 空，原大量 dirty 保留。使用者明確要求換新 session 繼續做完全部授權本機工作，不逐步詢問。

## 現在真正的下一步

只接續 NEW output protocol runner 的最終獨立 CODE／Python reviews。兩 reviewer 在最新 e1f1 freeze 尚未完成任何核可，就遇到實際 usage limit（提示 08:40 可再試）。先讀實際額度；ordinary usage 恢復才接續，禁止購買 credits、使用 reset 券或繞限制。不要把先前16 tests 的 BLOCK 當成新19 tests 的審查。

- Fixture：work/t18-output-protocol-preparation/native-height-fix/fixture-source-for-review.json，SHA d27b1d38c72d0bdf2e7df3933be118cfe5873de1c21f81e1f232f24131c617f8。同目錄 fixture-code-review.json／fixture-js-review.json 均 APPROVE，僅 source readiness。8 fixture sources 不再改；本次交接核32個 entries 零漂移。
- Runner：work/t18-output-protocol-preparation/runner-high-fix/runner-source-for-review.json，SHA e1f1d308baeecc2928c9f9cecf5e02cbe453e5d83a03e4fda8806cda95ef203a。19 normal／-O tests PASS，3 sources 與 fixture8 sources 全程不變；本次交接核43個 entries 零漂移。最新 CODE／Python 仍 PENDING，應寫同 runner-high-fix 目錄的新 runner-code-review.json/.md、runner-python-review.json/.md，JSON sourceManifest.path/sha256 必須精確綁定這一 freeze。
- source_paths／verify_reviews 已只接受 current native-height-fix fixture 和 runner-high-fix runner 核可，舊 base BLOCK 僅 archival。完整 re-review，不只看修正行。舊 agent IDs 屬原 session，不假設新 session 能重用；依適用 repo 規則啟用獨立 reviewer。
- 實際 protocol engine／mod symlink／full source-lock／fresh guard／attempt 均未建立或耗用。四份 current approvals 全齊後，root 才建立 full source/runtime/profile lock、另一次 fresh callguard、確認 engine absent，執行唯一 NEW protocol seed42／retry0。沒有 seed7 case。

契約 docs/empire-rts/t18-native-output-protocol-contract.md：獨立 map epoch_t18_output_protocol、官方 R28、192、native flat20/water0、兩人類/noAI/endless/nonvisual、零 actors/commands、2000ms 三個固定 payload＋COMPLETE；host30 含 preflight/prelaunch/stop，20秒 capture/prelaunch cutoff，同一 Budget 不重設。不可取消 filesystem/Popen 的 hard stop NOT PROVEN。prefix+explicit newline／1200 UTF16 units／8192 wire bytes／2MiB record／8MiB raw／strict contiguous fragments／完整 independent ASCII 與 typed sidecars／原生 Obstruction observations；不分類 shape/physics。只接受完整 newline COMPLETE，完整 raw/partial/unknown/PID/cleanup/replay/diagnostics 必留；解析或 I/O 錯誤不得升格 PASS。此 probe 不重跑舊 K fixture，不修補原 raw，不代表 physics、GUI、save/network 或產品已驗收。

## 已修正並保留的審查問題

原 fixture constructor0 被初次 JS 審查誤判為 native0；constructor20 的暫時修正反而產生 native40。完整 official export 加 SEA_LEVEL20、乘92，再由 native /92，不再扣20。因此正確是 RandomMap(0) 匯出1840→native20，setWaterHeight(0) 直接 native0。最終 CJS 執行完整官方 MakeExportable，37249 samples 全1840，另驗 counterfactual20→3680/40。所有 issued APPROVE/BLOCK 與 before bytes 皆保留；詳 NATIVE-HEIGHT-INTERPRETATION.md、flat20-fix、native-height-fix/before。不要再改成 constructor20 或 water-20。

原 runner freeze04f064d6c9aa7082bbcc347f465e0cc4c5607d733a66e9e0871c3ad0aba477ec 的16 tests PASS，但 CODE-OUTSIDE-01 發現 unknown outside JSON arrays 被接受；PY-IO-001 發現先 log.write 再 feed，I/O error 遺失41 received bytes 且可中斷 drain。原 BLOCK／重現／3 sources／freeze／logs 在 runner-high-fix/before，RED 也保留。新19 tests 修正：拒絕前後 unknown arrays；received bytes 先存 lossless Base64 memory backup，再獨立 parser feed／best-effort file write；short write、write/flush error 都強制 FAIL、disk integrity UNKNOWN，仍保 PID/full received backup、繼續 signal/drain/reap 並持久化 native-stop。必須由兩獨立 reviewer 檢查本次完整 lifetime／deadline／freshguard／source binding／strict replay，不以 tests 代替 review。

## 不可重跑或覆蓋的結果

T14 整體 PARTIAL；SQLite 原因 Insufficient data。原48raw／partialDB／journal/result／190slowframes／原 runner FAIL/PARTIAL／性能與尾活動 FAIL 不變。storage6/parser8/runner8proof、dense/count/delta、唯一 delta engine/offline attempt、DONE offline pipeline 都禁止重跑。原7207 seal5903014a64b8ada482cce36b2fcde7b9c5f948eec857b092eb1fff4f8f4d9cf4 與 prior-state 替代鏈依舊交接。

T15 package159 與 offline reader51 有界 DONE 不再驗證；候選42正式 FAIL、7 STOP，不能換名救 PASS。整體 PARTIAL，最終新功能包／clean install／GUI／save/network 仍待必要驗收。T16 原 naval42／新death42 的 FAIL、耗用 cases／STOP 依舊交接，不重跑完整攻擊矩陣。

T17 native42 formal FAIL，445 seal c1d83dc7c8cbc59e109bd71f4415a46067886f94436e3cc3efb0f5666cad19af、195 source snapshots、seed7 STOP 不變。145 nativechecks 只 observed PASS，不能升格。新 save/network 尚未執行；原 source assessment 不改。新增 work/t17-save-network-preparation/pause-api／zero-advance-api 的 ASSESSMENT.md 與來源 snapshots，確認官方 GUI SetPaused 路徑及 source-compatible session init prehook；仍須實際 archive／零 Advance timer/graph 比較，不能重設 timer/rearm 或把來源推論當 native PASS。

T18 原 P144/382 非圖像 PASS 有界 DONE，不重跑。新 K42 正式 FAIL／retry0 consumed，seed7 STOP；191 source snapshots，344 evidence seal e982c8ef4b003fab4dd9518e58ef074e2ddb51137756dac66cb5b0a3170f4c62。實際 raw1337404 bytes，JSON colon error char471031，早於 lexical premature closure；unique corruption cause Insufficient data。實際 PID97841/-15/3.7555s/drain/reap，replay1000 closed turns/recorded bound200000ms，completed simulation NOT PROVEN，不接受 physics suite。原 K sources／raw／contract／runner 皆 immutable。

新 GUI42 正式 FAIL／retry0 consumed，seed7 STOP；200 snapshots、272 evidence seal4f9f9f14a346cd2521bebe4266f31b5548d98a0efcd9e92facd785fb901482ac。PID51411/-15，raw0／capture0，elapsed186.1428超過180 gate。後續 copied app 不見，213 locked files missing，時序／原因／與啟動關係 Insufficient data；不恢復副本重跑。原 official app／私人 profile／repo profile 當次 unchanged；visual NOT RUN。

## 接續順序與邊界

先 final protocol reviews → full locks/fresh guard → unique protocol42 的正式 closeout/seal；保留任何 FAIL/unknown，不 retry。其後按最新依賴準備 T17 owner/LOS-filtered GUI、原生 save/load、真正隔離 app roots 的 loopback／T18 尚缺 integration／T15 最終本機發行驗收。不能以新 probe PASS 修復舊 formal FAIL，不能任意重開已停分支。

macOS 有效 bundleURL 是 .app；兩次 Parent 決定 caseRoot/logs，app Resources/data 是 writable user/config/cache/saves/replays。GUI/save/network 須真正不同 caseRoot 的 app copies，不能僅 cwd／symlink／兄弟app共用logs。引擎序列運行、不得共用 logs；sample/seed/fixture/camera/時長/comparison/gates/stop/retry 先固定，原生之前完成實作、tests、獨立 CODE/語言/API reviews、來源鎖、另 fresh callguard。

無 commit/push/delete/C++/外部發布/外部訊息/新付費服務。持續更新本機 tracking 前保存對應 preimages；舊 seal/raw 不修改。本次 tracking-before-transfer 與 automation-before.toml 已在 work/t14-t18-session-transfer-20261015 保存。原0ad-t14 ACTIVE／每5小時；parent 會移到新 chat，禁止新建重複排程。以該 transfer 目錄的 automation-migration-readback.json 判定是否已完成移轉，不自行重複改排程。只在有意義進展、完成、失敗或必要使用者決策時通知，無變化保持安靜。整體 T14–T18 仍 PARTIAL，工作尚未全部完成。


## 2026-10-15 protocol42 正式 FAIL／完整封存

額度實際恢復 ordinaryAllowed=true primary2%/weekly0%，未使用credits/reset。Runner e1f1d308baeecc2928c9f9cecf5e02cbe453e5d83a03e4fda8806cda95ef203a 新完整獨立CODE/Python APPROVE，與fixture d27b1d38c72d0bdf2e7df3933be118cfe5873de1c21f81e1f232f24131c617f8 CODE/JS精確綁定。Root161-source lock6819fd899e22249e3cd9ee4808ac5610e072df11e240f4c8b983182c37efc196，另fresh guard153b84d14115abbb5002fd324b15d8a2ce86224d8ad207e9f44906076860f91b後執行唯一NEWprotocol42/attempt1/retry0；正式FAIL，無seed7、不retry。

原生Timer Emit報ReferenceError EpochOutputProtocol is not defined；零packet/零message/無COMPLETE，native template observation NOT CAPTURED。持續Turn輸出觸發Raw output exceeds8MiB，raw8388660 bytes/disk與完整receivedBackup逐byte相等。PID47123/-15/TERM+CONT，drain/reaped/engineabsent，host18.981079167s/30 PASS，raw8MiB FAIL。Replay404713 closed turns/recorded80942600ms，completed simulation NOT PROVEN，不能宣稱2000ms正常完成。source/runtime/profiles前後一致，161 source snapshots保存。181檔FAIL seal c2b0042536041196d26fb5cfca3620138e2434c04930c434b911617685f060b4零mismatch。詳docs/empire-rts/evidence/t18-output-protocol-native42-validation.md及work/t18-output-protocol-runtime/native42-closeout.json。

原因查核：native LoadScript逐檔CompileFunction scope，helper只有var而缺Engine.RegisterGlobal；原CJS共用VMglobal不能驗證cross-file registration。唯讀primary分析在work/t18-output-protocol-preparation/post-native42-analysis，原sources/reviews/raw不改，不換名重跑。下一必要新T17 owner/LOS-filtered GUI切片僅DRAFT準備，save/network與最終新功能包仍NOTRUN。原K344/GUI272/T17445 FAIL、所有STOP/DONE與T14PARTIAL/SQLitecause Insufficient data保持。既有0ad-t14已readback移至本chat/ACTIVE每5h，無duplicate。Tracking preimages：work/t14-t18-session-transfer-20261015/resume-01a13d60/tracking-before-protocol42-closeout。無commit/push/delete/C++/外部操作。


## 2026-10-16 T17 GUI來源核可／新fixture接續

最新接續：docs/empire-rts/SESSION-HANDOFF-2026-10-16-T14-T18.md與work/t14-t18-resume-20261016/current-state.json。實際ordinaryAllowed=true primary1%/weekly32%，無credits/reset。新T17 owner/LOS filtered API＋single-visible fixed mode action來源切片完成30/30 source/mock PASS、三syntax PASS；完整獨立CODE及JS/API APPROVE綁review-fix/source-for-review.json SHA3ea8469056462c6d429f166c1f2daa3a7055108084ab13a93c173b20fea0addb，152entries rootreadback零漂移。缺Position/Terrain/Water methods/invalidpoint與u32 entityalias均已修；真正nativecallthrows不吞。原RED、23/22兩次FAIL、25PASS、e97freeze/JSBLOCK、修前70檔與RED30/26PASS/4FAIL完整保留。nativebinding採a2ca viewed-player相容性來源，非authenticatedidentity/HEAD/binary等價，native/visual/save/network全部NOTRUN。

不修改該152freeze，另NEW epoch_t17_gui_native_harness依賴已核productmod。新fixture source contract在work/t17-gui-native-preparation/fixture-source-contract.md；source implementation/tests進行中，GUI driver/typedrunner未實作，無engine/copy/link/fullsource-lock/guard/attempt。單選action保持官方六格與5upstream，非同時兩個新鍵。save-slice DRAFT在work/t17-save-network-preparation/save-slice-contract，queue accessor/完整graph/零Advance roundtrip simulation.dat確定性與branch timing仍OPEN，不假裝savePASS。

原protocol42 formalFAIL181seal c2b0042536041196d26fb5cfca3620138e2434c04930c434b911617685f060b4/attempt1retry0已耗用；原K344/GUI272/T17445及全部STOP/DONE保持。T14整體PARTIAL/原SQLitecause Insufficient data。新fixture非重跑145或protocol probe，所有native須必要來源/tests/獨立reviews/具體contract/fullsource-runtime-profile鎖/另freshguard後才可。Trackingpreimages在work/t14-t18-resume-20261016/tracking-before-source-readiness。既有0ad-t14每5h，無duplicate/commit/push/delete/C++/外部操作。
