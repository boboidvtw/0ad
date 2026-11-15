<!-- Purpose: Current bounded T14 checkpoint after map-seed7 match. Created: 2026-10-03. -->
# T14 接續交接 — 2026-10-03

Repo `/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`。HEAD仍`726a3aefcae830f605de438cd13192cc6330414e`，T13限定DONE；全部T14未commit/push、index空。先核對Git、progress、現有變更、官方R28與引擎程序；保留profile.txt、profile2.jsonp、work及所有FAIL。

## 最新限定驗收

[地圖seed7契約](t14-match-seed7.md)、[驗證](evidence/t14-match-seed7-validation.md)、[結果](evidence/t14-match-seed7-results.json)：10-01立約、10-02實測、10-03收尾。seed7新對局、不載save/T12Validation；既有epoch_petra難度3對固定防守，**AIseed仍42**。sim0至正式勝負、無暖機排除、cap60/1×，一次正式量測限定PASS，無FAIL或重跑。

- wall897.149422秒、sim894.6秒、50448幀、888 timing samples、181活動快照。
- p95 18.622070ms、p99 18.814941ms、sim/wall0.997158308；15個連續窗口皆PASS。
- 5幀>50ms、max159.337158ms全部保留，不能說零卡頓。
- AI8→83單位、1→19建築，採集food5803/wood2843/metal1692、訓練75、鐵器首次觀測sim529.4秒、ATTACKING首次sim864秒（7快照、最多20），正式勝利。
- 防守方損失8 Unit＋1 Structure，AI無損。不是雙AI互攻或大混戰。
- M4/16GiB/R28 ARM64/macOS27.0 26A428/AC；1280×800 GL、25設定讀回、固定AI基地相機起終一致。visual_verified:false，不宣稱遠處戰鬥全可見。
- CPU整程序中位25%、RSS峰值550.953MiB，含載入/收尾，不是無leak或長壓證據。
- raw：`work/t14-performance/20261001T223438386185Z-match-7`。

seed42先前完整局PASS仍有效且原始三份證據未修改：wall887.646982秒、sim884.6秒、15窗口PASS。兩場AIseed均42，地圖seed不同；**不是同條件重複性驗收**。

## 來源與必要回歸

現行[evidence/t14-match-seed7-source-manifest.json](evidence/t14-match-seed7-source-manifest.json)174檔；本場measured126檔。原match174、strike166等是各自歷史manifest，禁止覆寫。唯一工具差異為t14-macos.py刪除拒絕match seed7的兩行，仍限制42/7、cap60/no-profiler。原runner封存`work/t14-match-seed7-sources/pre-seed7-t14-macos.py`；主Mod/AI/C++未改。

76項Python一般/-O各PASS、5份JS mock PASS；CLI錯seed/cap/profiler拒絕與seed42 raw精確重解析PASS。另一段直接raw核算（未import正式parser）重組167 chunks、重算50448幀/15窗口/活動/勝負通過；這是同一工作者另一路徑核算，不是獨立代理審查。見`work/t14-match-seed7-sources/preflight-checks.json`、`pre-run-review.json`、`raw-audit.json`。

27場歷史raw/hash、T13 129檔來源/主Mod集合及原證據/profiles hash一致；本場source/root profiles不變、exit0、無ERROR/WARNING。未重跑T05–T13或舊T14引擎矩陣。官方runtime雙hash/codesign/ARM64確認：binary `531981d016596b0abde110cd239feaed98998c3fdaa837d0fa8d6f75482c81ef`，public.zip `ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429`。

## 累積狀態與剩餘缺口

**整體T14仍PARTIAL。** 七場不限FPS基線有效但sim/wall未達，200重複性FAIL保留。600 cap60對照只支持本機緩解，頻率平滑不是已證實唯一根因。兩seed經濟/late、飛行、即時AA、對地攻擊片段PASS皆仍是限定負載；原late錯讀total與flight輸出缺失FAIL保留。歷史詳見[10-01交接](SESSION-HANDOFF-2026-10-01-T14.md)。

下一步優先評估同地圖seed42/AIseed42完整局的同條件重複性，**先在repo定樣本數、比較方法、離散度門檻與停止條件**，再量測。現有兩場可作既有觀測，不能事後替它們訂通過標準。另可先立雙AI負載契約，但不得重寫AI或改C++。本次seed7授權範圍已完成，不擅自擴跑矩陣。

雙AI互攻、大混戰、長時間壓力/記憶體/熱穩定、多人與跨硬體、返航/停機位、精確空戰仍NOT RUN；潛艇缺自動偵測/hidden gate等前置機制，NOT RUN，不為效能擴功能。不是通用完整遊戲效能驗收。

無遺留測試引擎，未建立背景任務或排程；未commit/push、未刪profiles/work/失敗資料。接續仍需以實際Git與文件為準。

## 2026-10-03 同條件重複性最新收尾（接續以此節為準）

依[事前契約](t14-match-repeatability.md)完成3場全新map42/command AI RNG seed42、cap60、固定防守完整局：[本批限定重複性PASS](evidence/t14-match-repeatability-validation.md)。每場sim0至正式勝負884.6秒、wall887.872329/888.016490/887.135872秒，45窗口全部PASS；全局p95 max/min1.003423、p99 1.010223、simwall差0.000989，14共同完整分鐘離散度皆PASS。每場AI83單位/21建築、訓練75、鐵器/攻擊/勝利；6個>50ms幀及最大136.531982ms全部保留。

準備階段誤列HP曲線且過早啟動，人工停止45.501133秒attempt保留FAIL（engine exit0但缺完成payload、runner exit1），無效能結論。勘誤/原契約/hash在正式R1前封存，所有門檻/工具/負載未改，正式3樣本無重跑；舊seed42/7不納樣本。17項match Python普通/-O及JS mock、歷史/新raw重解析與另一代理直接raw核算PASS；174/126來源、T13 129、原285檔hash/30raw資料夾相符。新repeatability manifest174檔與工具來源內容不變，原證據保留歷史。

整體T14仍PARTIAL；原不限FPS/200重複性FAIL不變，雙AI/大混戰/長壓/多人/跨硬體/返航/精確空戰/潛艇NOT RUN。下一步優先評估既有雙AI限定契約，不直接擴跑、不改AI/C++。HEAD726a3ae/index空、無commit/push/刪檔/排程；引擎及runner已退出。[最新交接](SESSION-HANDOFF-2026-10-03-T14.md)。

正式raw：

- work/t14-performance/20261003T050115131137Z-match-42
- work/t14-performance/20261003T051755284421Z-match-42
- work/t14-performance/20261003T053451541418Z-match-42

本批現行來源看evidence/t14-match-repeatability-source-manifest.json（同174檔內容），詳見results/validation、work/t14-repeatability-sources/contract-lock.json、runs.json、r2-pair-check.json、independent-raw-audit.json與preservation-audit.json。AIseed42是command控制，非payload直接readback；RSS/背景/熱條件與首尾camera證據限制照報告保留。本契約3正式樣本已完成，禁止無故續跑第四場或擴矩陣。

## 2026-10-03 雙AI互攻最新收尾（接續以此節為準）

依[t14-dual事前契約](t14-dual.md)完成1場全新map42/AIseed42、兩既有epoch_petra難度3/observer/conquest：[限定PASS](evidence/t14-dual-validation.md)。sim0無暖機至P2正式勝利、wall1519.504454秒/sim1514.6秒，84395幀/1505 samples/305快照；p95 18.667969ms/p99 18.952881ms/simwall0.996772333。25完整分鐘窗口PASS，19.278455秒短尾觀測保留；2個>50ms/max141.791992ms保留。

真實readback確認Seed/AISeed42、雙席AI/diff3/observer/conquest；雙方各訓練130、鐵器/採集/ATTACKING快照40/61、共同38，Unit損失127/47、Structure10/0。同時觀測峰值176單位/43建築，非大混戰。P1初始+訓練-final與Unit分類損失差11原因未由快照確立，勿把全部消失單位稱combat killed。

隔離新增dual工具/測試，runner僅opt-in增量；88 Python一般/-O、6JS mocks、4CLI拒絕、5歷史match精確重解析、語言/整合review与另一代理直接raw核算PASS。本批一次正式量測無FAIL/重跑；原工具/契約準備測試clock錯誤保留紀錄，未弱化gate。新現行來源182檔（原174+8新、只舊runner hash改變），measured126檔；舊runner封存、324原檔/34 raw資料夾/原FAIL/profiles與T13 129/主Mod不變。

整體T14仍PARTIAL、舊不限FPS/200重複性FAIL不變；雙AI跨seed/重複性、大混戰、長壓/記憶體/熱穩定、多人/跨硬體、返航/精確空戰/潛艇NOT RUN。下一步先盤點可持續活動的長壓限定契約，不直接擴跑、不改AI/C++。HEAD726a3ae/index空、無commit/push/刪檔/排程，引擎及runner已退出。

raw：work/t14-performance/20261003T093837016903Z-dual-42；17:38 Asia/Taipei啟動。本批現行來源看evidence/t14-dual-source-manifest.json（182檔），原repeatability/seed7/match174等仍為歷史，不覆寫。必要讀t14-dual.md、evidence/t14-dual-validation.md/results.json與work/t14-dual-sources/pre-run-lock.json、prepared-source-manifest.json、independent-raw-audit.json、preservation-audit.json。dual mode限制seed42/cap60/no-profiler；原match42/7命令和parser語義仍不變。工具mod link epoch_t14_dual指repo tools/epoch-rts/t14-dual-harness，只有此新opt-in入口，不影響產品預設。

本限定單場已完成，禁止無故再跑seed7或雙AI重複性；下一次先建立新長壓或有理由的限定契約。原不限FPS/200重複性FAIL與頻率平滑假說未解，不擅自改C++/AI。退出狀態/HEAD/index/profiles/work仍需先以現場核對為準。

## 2026-10-03 600單位30分鐘性能／RSS最新收尾（接續以此節為準）

依[t14-soak事前契約與唯一配置修正](t14-soak.md)完成[限定PASS](evidence/t14-soak-validation.md)：sim0無暖機、600既有T11單位正常往返/cap60，wall1800.014206秒/sim1793.2秒/99692幀/1813 timing samples/390快照，p95 18.660889ms/p99 19.082031ms/simwall0.996214360。29完整分鐘＋59.739388秒尾窗，30窗全部受gate皆PASS；600同ID存活、commands1→180、每窗7–13個真實位移達標段。開局1幀>50ms/max54.836914ms保留。

RSS baseline430.203125→late442.125000MiB、+11.921875MiB/ratio1.027712200/OLS0.602904437MiB/min皆達事前工程容差；OS clock/coverage gate通過，峰445.609375MiB保留。31熱輸出皆unavailable，熱／頻率仍NOT RUN，不證明無leak。無AI/經濟/戰鬥；mapSeed600是人口fixture，不是地圖seed42，AISeed42讀回但無AI。

首場完整30min相機250→200控制FAIL與原raw/result/來源/契約保留；官方default max200 clamp證據明確，唯一工具修正retry先立註記/回歸/審查/重鎖，只soak顯式max250與boundsreadback，不放寬門檻或改產品預設。retry實際起終camera=(384,210.821105957,180)/rotation(.8500061035,0)/zoom250完全一致。兩場不能算同條件重複性。

100 Python一般/-O各PASS、7JS mocks、4CLI拒絕、35歴史raw精確重解析/語言及整合reviewPASS；現行來源191（原182+9、原集合僅runner改），measured128，早期manifest不覆寫。T13/主Mod/原FAIL/profiles不改；HEAD726a3ae/index空、engine/runner退出，無commit/push/刪檔/背景或排程。整體T14 PARTIAL；原不限FPS/200重複性FAIL仍在，AI/戰鬥長壓、大混戰、熱、多人/跨硬體、精確空戰/潛艇仍NOT RUN。下一步先盘點既有機制的大規模交戰負載可行性，事前契約後才測，不直接擴跑。

raw：work/t14-performance/20261003T135306193387Z-soak-42；原FAIL：work/t14-performance/20261003T131605349810Z-soak-42。現行來源[evidence/t14-soak-source-manifest.json](evidence/t14-soak-source-manifest.json)，較早dual182/match174等仍為歷史。

接續必要補讀t14-soak.md、evidence/t14-soak-validation.md/results.json/source-manifest.json、work/t14-soak-sources/retry-pre-run-lock.json、camera-config-diagnosis.json、first-run-camera-audit.json與獨立retry raw audit/closeout-audit。原runner在pre-soak-t14-macos.py；首場版本first-run-*；retry版本以191現行manifest為準。唯一retry已使用，禁止第三場補跑或無故重測30分鐘。soak入口限制units600/seed42(未使用)/cap60/no-profiler，max250僅此入口生效；其他ground/match/dual語義不變。沒有任何後續背景工作。

本soak收尾獨立代理未import正式parser，直接raw核算30窗口/600 ID活動/時鐘/RSS/相機/來源PASS、issues空；證據work/t14-soak-sources/independent-retry-raw-audit.json。首場前336歷史檔與retry前376含首場FAIL檔原hash保留，正式parser重解析精確一致；最終Git/129 T13/191來源/鏈結與程序核對見work/t14-soak-sources/closeout-audit.json。

## 2026-10-04 最新交接指向

初始600同種士兵地面交戰單場限定PASS與最新200來源/剩餘工作，接續改讀[10-04交接](SESSION-HANDOFF-2026-10-04-T14.md)。本檔原有歷史結果/FAIL/manifest保留，不覆寫。
