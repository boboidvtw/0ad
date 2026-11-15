<!-- Purpose: Quota-resume checkpoint for authorized T14–T18 local execution. Created: 2026-10-12. -->
# T14–T18 自主接續交接

人類已明確授權全部包含 T15 發行準備、T16 攻擊檢查、T17 潛艇與 T18 精確彈道／停機，依依賴自主執行。舊 heartbeat 的 T14 狹義文字沒有撤銷此授權。既有 automation `0ad-t14` 已經工具更新為同 chat 的 T14–T18 工作，ACTIVE、每五小時，不建重複排程；讀回在 work/t16-attack-contract/automation-scope-readback-20261012.json。額度不足保存 checkpoint 待下一次排程，不買 credits／reset券／繞限制；不保證恢復瞬間執行。

## T15 已完成的有界建包

最終 code 與 Python review APPROVE，11 tests 一般／-O PASS；原 BLOCK 與 Python 3.9 annotation 初始 FAIL 保留。字面依賴 512 visited／3471 refs／0 missing，完整 dynamic closure NOT PROVEN。38 個來源鎖與另 call guard 後，core-r1／core-r1-repro 各一次 retry0，ZIP逐 byte 相同。34 payload 檔、1160576 bytes、SHA `37462130b18df12ef67f3d8c57752f2426a6d17baef4ea833255e3d15997c3ef`。113 最終讀回／post-source checks PASS；159 檔 seal PASS SHA `01bca46f4613ed45fca6aa10b7274329255370eefd42b7f2e4a7a80c3188975b`。

包在 work/t15-release-preparation/packages/core-r1/epoch_rts.zip；建包契約 t15-local-package-contract-2026-10-12.md。此 seal 包含既有 T15 準備資料與產品／審查來源，不含持續更新的 tracking。不要再重建已完成的兩個包或覆寫 sealed artifacts。新候選包驗收仍需新的 work／契約／review／source-lock／guard。

T15 整體 PARTIAL：乾淨安裝、實際候選 R28 Duel seed42/7、經濟／升級／訓練／研究、GUI、受影響存讀檔／多人與完整 closure 尚未驗收。官方 source/ps/GameSetup/Paths.cpp 顯示 macOS 預設使用原使用者 profile，不能用修改 HOME 假稱隔離。候選驗收準備可用官方 app 的完整本機副本與 -writableRoot，逐 byte 鎖 binary/public/mod，資料與 logs 寫入新副本；需事前正式契約及真路徑讀回證據，不改原 app 或現有 Mod symlink。沒有本批 engine。

## T16 正在補齊正式驗收前準備

初審 HIGH：外部直接 FinishOrder 留下 ATTACKING FSM；MEDIUM：surface 初態 SUBMERGED。已用獨立官方 EpochNavalUnitAI clone/root-event 與 State fail-closed 修正；44 tests（包含忠實官方 FSM）PASS，component-review-final APPROVE。只限 components scope，不等於所有 fixtures／runner review。

獨立 harness 在 tools/epoch-rts/t16-harness。新 map／manual State／visibility／templates／trigger，runtime fixture 尚在補完整拒絕矩陣及 required-check-ids。固定 seeds42/7／size192／water20 terrain8／shorex520；instant 標準 Resistance 傷害、20pierce／2000HP／range90／repeat1000、不補血。hidden 新命令、失偵既有 forced order、redetect 不恢復舊命令、完整角色與非法目標矩陣、每拒絕≥3repeat HP不變是必要 gates。獨立 UnitAI schema 已補全，停用原 UnitAI。

新 runner tools/epoch-rts/t16-macos.py、t16_runtime.py、test-t16-runner.py 已有 14 normal／-O PASS。schema／CLI 在 t16-runtime-runner.md，review-inputs 在 work/t16-attack-contract/runner-preparation。來源鎖必涵蓋完整 core／harness／runner／smoke，required_check_ids 必須逐序精確；另 guard 綁 mode/seed/source-lock SHA、engine_allowed、attempt absent、fresh120s。不得未 review 就 launch。正式 run42/7、replay42/7、M1 回歸42/7，各一次 retry0，不 engine 並行。沒有本批正式 attempt。

camera 官方來源證據：rmgen exports g_Camera；render camera getters 在 GUI context，不可捏造 simulation API。nonvisual fixture 必須明列 map source 固定 camera，render camera readback NOT RUN；在任何 engine 前封口適用性，不能把 source expectation 當實測 camera 或測後弱化 gate。

## T18 初審失敗必須保留

P 隔離初版 20 mock PASS，但忠實 native 反例確認 GetPreviousPosition 使用目前高度，沒有歷史 y；速度預測與 lateness 插值 HIGH。證據 work/t18-precision-implementation/code-review*，未啟動 engine。worker 已新增 timestamped 3D History barrier，30 tests PASS，尚需最終 review manifest／獨立 code 與 JS review。禁止刪垂直案例或用人工 previous.y 救 PASS。新的正式 fixture／trajectory／runner／camera／GUI／save／network 尚待完成；K slot／runway／安全滑行尚未實作。T18 IN_PROGRESS。

T17 依 T16 真驗收後進行 2 秒浮潛／深度安全／自動偵測／命令 GUI／攻擊整合，再新存讀檔／多人與必要新機制效能驗收；不得用 T08／T13 舊 PASS 代替。

## 不得重跑與封存替代鏈

T14 原 storage6／parser8／runner8 proof、dense/count/delta、唯一 delta engine 與 offline attempt 都已消耗；不重跑、換名救 PASS 或擴舊量測。原48raw／partialDB／journal／result／190slowframes、原runner FAIL/PARTIAL、性能與尾活動 FAIL 全保留。原 SQLite cause Insufficient data；整體 T14 PARTIAL。

舊29 gap-assessment tracking → work/t16-attack-contract/prior-state；舊7207 tracking → work/t14-live-integration-gap-assessment/prior-state；舊4991 → work/t14-storage-runner-integration/prior-state；舊669 → work/t14-storage-parser-integration/prior-state；舊18 → work/t14-storage-failure-proof/prior-state；舊1114 → work/t14-live-storage-assessment/prior-state。其他原路徑／原seal不改。此次 tracking 前保存 work/t14-t18-resume-20261012/prior-state。保留原來源、舊 valid FAIL，不製造反覆 synthetic proof 進度。

Git HEAD 726a3aefcae830f605de438cd13192cc6330414e，已有大量本地變更；不 commit／push／delete／外部發布／外部訊息／C++／付費。後續依最新檔案與 review 實際狀態接續，不從本交接推定尚未完成的 review 或 engine PASS。

## 正式 run42 後更新（取代上方尚未啟動的現況）

T16 全 scope reviews及29一般/-O、44 JS、221 trigger準備通過後，149來源鎖SHA b425b1fde9a011e6a384036d8fb4bf6fc668fb6766d2a271973618112060c6b3及獨立guard啟動一次run42，retry0。實際FAIL：36/221完成且36PASS；死亡corpse模板缺Visibility.RetainInFog，5個native ERROR，TypeError: cmpPositionCorpse is null。185未完成，不稱全矩陣通過。raw在work/t16-attack-contract/runs/20261012T073217380782Z-run-42；attempt-run-42.json已消耗。run7／replay42/7／smoke42/7 STOPPED NOT RUN。原profile與source在本場前後一致，T16 PARTIAL。

修正前149份來源逐byte快照failed-run42-source/source-snapshots.json；313檔FAIL seal PASS SHA d019e9fa62304918a3d3348cf3dc5bfd0211e0b18a689cf2b5c94446375712c8。後續三template變更時舊source rows精確替代為149快照，raw／舊seal不改；不換名重跑舊221矩陣救PASS。

官方來源盤點work/t16-native-death-assessment確認Health.CreateCorpse與corpse filter疊加停用Visibility造成相容性錯誤。新不同必要問題t16-native-death-contract.md驗收死亡生命週期、標準致命傷害統計、偵測器／攻擊者死亡取消活動。三船base opt-in Health.DeathType=vanish，不生成屍體是明示限制。23來源準備15Python及官方VM121 PASS不是engine證據；CODE HIGH發現判定未獨立固定fatal delta5、座標與非負ledger時間，修正中。JS/API review進行中；新死亡engine／lock／guard／attempt NOT RUN，需最終三類review。

T15候選準備修正mutable資源alias及frozen NativeRunInputs，8來源manifest work/t15-candidate-runtime/fixes-review-inputs.json，29一般/-O與6忠實native alias JS PASS，CODE／Python／JS final APPROVE。副本／候選engine／attempt NOT RUN，不能套用舊七檔review；原封存包不重建。

T18P History15來源CODE／JS APPROVE、30mock PASS；新7來源fixture準備6組官方Timer VM PASS，55 requests／53issued／275turn，尚需fixture reviews及runner。native／GUI／save／network／K NOT RUN。T17依必要native相容性與新整合契約接續。

本次四tracking／交接先存work/t14-t18-resume-20261012/post-run42-prior-state。既有5小時heartbeat、T14 PARTIAL／原FAIL／SQLitecause Insufficient data保持；按最新manifest與review實際讀回接續。

## 最新：候選42與死亡42已耗用，均不得重跑

T15新版三類review後12source鎖SHA cb424b4386bd0780b35bf3ae42ab1b6adca8ee456fb0e8c367aa1e33456fce36，獨立安裝guard與run guard正式候選42一次retry0。原生177000ms完整28checks PASS僅offline讀回；runner suiteNone，print chunks無newline、實際logs位置work/t15-candidate-runtime/logs，wall120停SIGTERM/無hardkill/ERROR，runner FAIL保持。native replay settingsPASS，原app/profile及copyimmutable一致TRUE；seed7停止NOT RUN。62檔FAIL seal SHA 0de8c1021adace1e30fc0215fdcad18ec67990a11306c0908af308d74246d840；12source原bytes保存failed-seed42-source/manifest.json，原seal/raw不可改。新 source-only路徑／print assessment在work/t15-candidate-runtime-assessment，不能重命名重跑候選Duel42。

T16 native-death最新CODE/Python/JS APPROVE、23一般/-O，library f7eec3a3e6216d485f118129263dffb2319dfbb5873ed18ee148177a8e98ee39，160source鎖SHA d64b04b3b13d1283cbed30109a370b0c7a9eeedec9a0acee9d252fa2bf4027f5及另guard後正式42一次retry0。raw在work/t16-native-death-preparation/runs/20261012T121904834022Z-native-death-42，121完整check PASS，無ERROR/WARNING，source/profile一致。獨立fixed_checks/ledger/lifecycle/cycles/stats gates TRUE，observations gate FALSE：船隻native位置偏離固定contract。結果validFAIL，不放寬座標gate、不重試；native-death7停止NOT RUN，T16 PARTIAL。

246檔死亡FAIL seal SHA ec3db666dcae639e81122a32b7e8042449c993751f3244d059c7d01e3fad841b，160source逐byte快照failed-native-death42-source/manifest.json；未來新revision只用此精確source替代，原raw/seal不改。位置source-only評估work/t16-native-position-assessment：官方ship pushing/clearance與4m相鄰fixture重疊相容，但沒有nativepush逐次ledger，不稱唯一因果；新T17不同controller整合fixture事前須審足間距，不用新名稱救死亡121PASS。

T18P新7fixture+15History兩獨立review APPROVE，6fixture/30precision mocks PASS；新runner t18_precision_runtime.py/CLI/tests及新runtime契約由fixture worker製作中，只NEW files、不改已核可fixture。尚無T18 source-lock/guard/engine。T17 controller及K仍未實作；自主接續必要源碼工作，額度不足checkpoint待原5h排程，不使用credits/reset券。

此次四tracking／交接更新前保存post-native-death42-prior-state。原T14所有界線與313海戰FAIL封存替代鏈保持，沒有commit/push/delete/C++/外部發布／訊息。

## 2026-10-13 額度恢复接續：P非圖像驗收有界DONE

T18P原生42/7各一次retry0 PASS，不再重跑。每場55requests／275turn／31HIT22MISS2REJECTED／53issued清理完整，HP200→180／miss無傷／timing／3D／全部immutable18欄及拒射5欄gate通過。144source-lock SHA496007d7499b65d026d93930e58cf7d1c79724b8b64aed1e9bfb1d6be7045c68，每場另guard，seed7綁42byte-baseline。原始run目錄20261012T123601717686Z-run-42及20261012T123714642861Z-run-7在work/t18-precision-runtime/runs。382檔seal SHA b8acfc81b1f1fbc81abb41a5cee5579431bbc7905114b269496321f7993c1ca9，144逐byte來源快照native-source-snapshots/manifest.json；未來精確替代來源、原seal/raw不改。validation見evidence/t18-precision-native-validation.md。GUI／K／save/network／一般原生移動NOT RUN，不標整體T18 DONE。

T15新reader三來源CODE/Python APPROVE，24normal/-O PASS。新不同必要問題17來源鎖SHA4d22e01a5997392485d4b05bbb6e4c14dcec3ac12567f8f3355d9567a7b81778，另OFFLINEguard後唯一正式原84MiB讀取attempt1/retry0：83943126bytes/fullhash／2chunks／28checks／177000ms與2outside spans完整PASS，actualFILES宣告相符但freshness NOT PROVEN／actual_verified=false。51檔seal SHA c577ffba195109b7b698a507235fb50923a89476a6b95d5b6d0f2f4649496759，16非raw來源快照source-snapshots/manifest.json；原raw仍原路徑、原候選42 FAIL／62seal保持，不重跑此reader proof或原候選。T15 PARTIAL。

T17控制器source22groups及CODE／JS最終APPROVE；原externalFinishOrder HIGH/RED保留，最小改ProcessMessage nativeFSM事件，3combat態與queuedWalk／timers有忠實官方覆蓋。最新controller SHA553a6692c5dc06d7b8739c5220b3840a846f08f6ab30cdbf2f128ca78e75fe47。新native integration fixture／literalIDs準備中，source paths work/t17-submarine-fixture；未啟動native/guard/lock/attempt。OnUpdate後淺灘處理未證明移動防穿地，不能宣稱完整安全。原T16160與P144來源均不改。

K停機NEW11sources／17officialTimer mocks PASS，work/t18-parking-preparation/implementation-source-for-review.json SOURCE FROZEN，CODE review進行中、JS尚待。核心/T07/P不改；UnitMotion新component clearance2，外部離場點避免堵進場，地面command2.99與actual≤3、swept保守+0.001，原FAIL／beforebytes均保留。native排程還沒封口，完整3機路程可能超舊120s草案，必須事前新有限契約，不測後延時。

GUI新overlay準備由work/t18-precision-gui-preparation接續；native沒有Engine.TakeScreenshot binding，只有SDL screenshot hotkey→Renderer nextframe。不能捏造API或視覺PASS；需實際hotkey預設值、permission／官方spectator／camera與新PNG讀回。source-only捕捉request不等真圖像，root必須檢視實圖。不得改P144／382seal。

前次三workers quota-error未完成，最新工具ordinaryUsageAllowed=true／primary0已實核並接續，同5小時automation維持，不購credits／reset券。四tracking／交接先保存post-t18-native-prior-state。下一步依實際新fixture／K／GUI來源凍結獨立reviews→source-lock→另guard→必要新engine，無C++／commit/push/delete／外部發布／訊息。

## 2026-10-13 最新來源準備與可恢復界線

T17新145 literal integration fixture15source已CODE／JS核可，9 meaningful VM groups PASS；source manifest work/t17-submarine-fixture/implementation-source-for-review.json。官方GetLosVisibility modified fallback會立即ComputeLosVisibility，維持原+2000 mode gate；不加猜測延時。新typed runner/tests/runtime contract在work/t17-submarine-runtime-preparation，最近23一般tests PASS僅準備狀態，尚需finalfreeze與獨立CODE/Python，無新engine/link/lock/guard/attempt。

T18K地形HIGH修正11source／17API refs與21 meaningful groups、CODE／JS final APPROVE，latestmanifest work/t18-parking-preparation/terrain-high-fix/implementation-source-for-review.json。未知地形／swept disk corner／fixedconversion拒絕，approved11不改。新native方案在worker準備：200simsec／120nonvisualhost、8互相隔離field與12planes、兩seed各一次retry0；先固定新契約、完整literal／inventory與fixture/runner reviews，未native，不測後延時救PASS。

T18GUI overlay6source與19groups／syntax／XML準備PASS，work/t18-precision-gui-preparation/review-inputs-final.json，CODE review中、JS待審。唯讀original P55/fullledger、官方observer-1、3witness×3phase、nativecamera及HUDlabel；同lane較早actors可能重疊，label不是唯一pixel身份證明。原P144／382與T15reader51不改。

Root新game-window helper tools/epoch-rts/t18-window-capture.swift／contract compiled v3，work/t18-window-capture-preparation/review-inputs-final.json；binary SHAef48c503441b84a657359607b877b0eed9a92e78276557e754aa339bf21326cf。permission只讀preflight=true／AXfalse，3非法argv拒絕；没有正向capture或engine。只選actual siblingPID/exe/UID/startidentity唯一gamewindow，不desktop、不keyboard、不改permission；exclusive boundedPNG／metadata visual_verified=false。CODE review中、Apple API獨立review未做；error domain/code修正前source/binary原bytes保存error-domain-before，初compile source未保存仍NOT RECORDED。

新t18-precision-gui-runtime-contract.md事前固定graphical42→7／55simsec／180host／9PNG／retry0，GetMicroseconds primary JS_Now(epochus)對helperDate epoch；capture結束必≤requestwall+200ms，不把request當PNG時間。需正式runner／tests／全部獨立reviews／source-lock／另guard，actual images逐圖root看見才判，不fake visualPASS。尚無GUI appcopy/link/lock/guard/attempt。

GitHEAD726a3aefcae830f605de438cd13192cc6330414e／index空；原大量dirty保持。新tracking前四files存post-gui-source-prior-state。T14仍PARTIAL／原SQLitecause Insufficient data、T15/T16仍PARTIAL、T17/T18 IN_PROGRESS；原validFAIL／所有已耗用attempt/seal不重跑。額度primary94%secondary79仍ordinaryAllowed已讀；不credits/reset券，實際耗盡才存checkpoint待既有5h排程。

## 2026-10-13 16:30 resume and independent review gates

Quota recovery actually read back ordinaryAllowed=true primary0/secondary0; earlier three workers stopped on quota errors. No credits/reset used. HEAD726a3aefcae830f605de438cd13192cc6330414e/index empty.

T17 runner26 normal/-O initially passed but independent CODE found two HIGH: native HP events disagree with paired stable checks, and accepted profiles missing at exact Popen. Original4 source/manifest in code-high-before. Fix28 normal/-O and PY APPROVE bound dfb5bab2478ca2eb6eb03504a71ad82ce530ba89e0fe952678d2905bd047cf84. CODE re-review WARNING residual HIGH: cannon1980->1960 event18100 moved16100 during owner/stale held-fire before fresh command17900 still accepted. Four source/manifest preserved code-chronology-before. Worker now changes to full timeline command/controller/owner/LOS/diplomacy-authorized HP windows, not another isolated interval. NEW hashes require CODE/PY reviews. Root exact new mod symlink recorded mod-link-readback.json. No T17 engine/source-lock/guard/attempt.

K NEW native fixture9 sources/fixed plan4011157e0ce83b1551b31c2462d83d45c2a847fcebb2e2994ae929aec81c0a7b and7 meaningful Timer groups/static PASS. CODE HIGH: collision failure thrown before frame and inventory recorded, losing physical failure evidence. Review report pending, must preserve complete or explicitly partial error frame before gates. K11/P144 unchanged; typed runner and JS review pending; no engine/link/lock/guard/attempt.

GUI6 source CODE/JS APPROVE(19groups/22API); capture-v3 two sources/binary CODE/SwiftAppleAPI APPROVE(6SDKtypecheck/3invalidargv). No actual PNG/GUI engine. NEW typedGUI runner/tests work/t18-precision-gui-runtime-preparation in progress; fixed epoch200ms capturedeadline9PNG/55sim180host/retry0, source packet UTF16 surrogate splitting/fullunknown sidecars need meaningful tests. No app copy/install/source-lock/guard/attempt/root image judgment. P144/382 and T15reader51 remain immutable and DONE within their original bounded scope.

Four tracking preimages in post-chronology-review-prior-state. T14 PARTIAL/originalSQLitecause Insufficient data, T15/T16 PARTIAL,T17/T18 IN_PROGRESS. All old FAIL/raw/consumedattempts preserved. Existing0ad-t14 every5h; no duplicate/commit/push/delete/C++/external publish/message/paid service. Remaining HIGH blocks engine; new formal launch only after fixed-source independent reviews, full lock and separate callguard.

## 2026-10-13 latest formal T17 native42 FAIL / sealed continuation

T17 final whole-authority chronology CODE/Python APPROVE binds manifest6d7e05d1c5e45e6252cacc42692876aca8043521e63700318d8babfb234573b7/library1b1832750104807d28f76e32867e832936c26fc348a52d4ba57d441cb1e4ca73;30general/-O PASS. Root195source-lock fd12f151e664eb35cf628ca3f7a64ae1d662da994a045be6a3d92da3da89a356/fresh separate guard launched new native42 once1/retry0. Raw work/t17-submarine-runtime-preparation/runs/20261013T083535480195Z-t17-native-42. FormalFAIL ExtraData strict fullresulttailparser rejects ordinary native Turn logs. Exception lost local native stopdict/replayprelaunchfile-set; NOTPERSISTED/NOTPROVEN, not invented.

Observational actualraw JSONspan contains145nativechecks PASS,fulloriginalsuite_ok TRUE/noERROR_WARNING; finalcheck24800ms. Native stdoutlastTurn3380 at200ms, therefore60000ms engine-stop bound NOTPROVEN. Engine.log birth->mtime approx3.026s is file observation only, not persisted native elapsed/stopreason. Declared native replay path copied toassessment; actual map epoch_t17_submarine/seed42/size192/2epoch/noAI/endless metadata matches, replayfreshness NOTPROVEN(no persisted prelaunchfile-set). Source/runtime/originalprofiles unchanged readbackTRUE. Formal runnerFAIL unchanged, attempt consumed; stopped-native7.json confirms STOPPED NOTRUN. Do not retry/rename rescue native42 or treat observedsuite as formalPASS.

195 originalsourcebytes preserved failed-native42-source/manifest.json before future edits.445file FAIL seal PASS SHA c1d83dc7c8cbc59e109bd71f4415a46067886f94436e3cc3efb0f5666cad19af, failed-native42-evidence-lock.json/closeout. All raw/FAIL/unknown/fullledger/span retained. Evidence t17-controller-native42-validation.md; phrase map/seed192 in that immutable note means actual map/seed42/size192, clarified here with originalmetadata (not changing seal). OverallT17 PARTIAL; GUI/save/network/movingfloor/seed7 notvalidated.

Kfixture HIGH completefailedframe retention fixed:10meaningfulgroups,finalCODE+JS/API APPROVE9source/17API, K11/P144unchanged. New typedrunner/tests/native-runtime-contract work/t18-parking-runtime-preparation inprogress, noKengine/link/lock/guard/attempt. sample[0,200000]1000frames vs actual nonvisual stop/overshoot mustseparate; primary hard-stop/turnlimit feasibility under investigation before newengine, cannot guess10s or reuse. GUI NEW typedrunner work/t18-precision-gui-runtime-preparation continues, compiledcapturev3/observer source dualreviewsAPPROVE butpositivePNG/nativeGUInotrun; noGUIengine/copy/lock/guard/attempt. Strict JSONspan/fulloutsidebytes and persistence of partial native results are necessary NEW integrations, not permission to rerun T17.

Current fourtracking preimages post-t17-native42-prior-state. Existing P382/reader51/T15package159/T16FAIL313+246/T14legacyseals immutable; keep all exhausted attempts and T14 PARTIAL/SQLitecause Insufficientdata. T15/T16/T17 PARTIAL,T18IN_PROGRESS. Next authorized distinct GUI/save/network/parking questions only after necessary CODE+language approvals/fullsource-lock/separatefreshguard; noengineparallelsharinglogs/commit/push/delete/C++/externalpublish/messages/credits/reset. Existing5hheartbeat retained, no instantrecovery guarantee.
