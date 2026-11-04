<!-- Purpose: Current bounded T14 checkpoint after ground-attack slices. Created: 2026-10-01. -->
# T14 接續交接 — 2026-10-01

> 2026-10-03更新：地圖seed7／AIseed42完整局已限定PASS，最新狀態與後續工作見[10-03交接](SESSION-HANDOFF-2026-10-03-T14.md)，現行來源改看[seed7 manifest](evidence/t14-match-seed7-source-manifest.json)。以下保留10-01歷史檢查點；其中seed7尚未量測與runner僅seed42等描述已由新版取代。

Repo `/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`，HEAD仍726a3ae。全部T14變更未commit/push，index空，保留根profile.txt/profile2.jsonp與work/。先核對實際Git、[progress](progress.md)及官方R28，不因本文件重跑已完成矩陣。

## 最新工作與實測

最新為[seed42完整局契約](t14-match.md)、[驗證](evidence/t14-match-validation.md)、[結果](evidence/t14-match-results.json)：官方R28新對局、既有AI難度3對固定防守、不載T12Validation，無暖機排除、sim0至勝負，限定PASS。wall887.646982秒、sim884.6秒、49156幀、179快照；p95 18.681885/p99 18.980957ms、sim/wall0.996567349，15連續窗口皆PASS；2幀>50ms及max150.273926ms保留。AI8→83單位/1→21建築，鐵器/採集/訓練75/7戰鬥快照/勝利均有證據；防守方損失8單位/1建築，AI無損。

本次只有一場、無FAIL/重跑，raw `work/t14-performance/20261001T120607620423Z-match-42`。camera立即設定後固定在AI起始基地、25設定readback一致，未視覺驗證全場可見。CPU整程序中位25.1%、RSS峰值538.828MiB，不代表長壓/無leak。單一seed、小規模固定防守完整局，不代表通用完整遊戲效能。

以下對地攻擊為本日前一批已完成的歷史結果：

[對地攻擊契約](t14-strike.md)、[驗證](evidence/t14-strike-validation.md)、[結果](evidence/t14-strike-results.json)：两seed各16原飛機/32原房屋，20秒暖機＋60秒wall、1×/cap60，限定PASS。兩場p95 17.708ms，sim/wall0.999917/0.999911。16機全程HP200、32→16存活目標、HP下降5749.395、Structure損失16，量測內16正常改派；12/12区段有傷害且末段持續。seed7一快照在改派切換期有效attack=0，仍符合事前≥8有效點，不稱逐tick無間斷。

本批無FAIL/重跑；實跑10-01 Asia/Taipei，raw UTC目錄`work/t14-performance/20260930T223240785297Z-strike-42`、`20260930T223425225893Z-strike-7`。GUI相機實際讀回起終一致；visual_verified:false，不聲稱所有實體同時可見。RSS全程序峰值316.66/403.56MiB，不能作leak/記憶體穩定結論。

## 累積狀態（T14仍PARTIAL）

- T13限定DONE，來源129檔與主Mod集合不變；不重做T05–T13。
- 七場不限FPS基線有效但sim/wall未達0.95；200重複性FAIL、600重複性PASS，1200只觀測。原失敗不得改寫。
- 600單位60/0/0/60與另兩場原生profiler已完成；cap60緩解模擬落後，頻率平滑仅候選解釋，唯一根因未證實。
- AI經濟/後期進攻四個限定片段PASS；原兩late讀total失敗保留，改Unit/Structure後才重跑PASS。不是完整局或大混戰。
- 64架持續飛行兩片段PASS；原首flight42巨大print缺活動raw仍FAIL排除，分段修正後重跑PASS。
- 64飛機/4即時AA兩片段PASS，飛機自然64→50/51、死亡14/13、全12段有傷害，無補血/復活。
- 16飛機/32房屋對地攻擊兩片段PASS；原武器/controller未改，不代表精確彈道或完整空戰。
- 最新seed42開局至勝負完整局限定PASS，15個連續窗口全達標；seed7尚未量測。

以上歷史細節見[09-30交接](SESSION-HANDOFF-2026-09-30-T14.md)及各報告。

## 來源與回歸

現行來源看[evidence/t14-match-source-manifest.json](evidence/t14-match-source-manifest.json)，174檔；strike166及更早AA/flight/workload/diagnosis/baseline manifests都是歷史版，禁止覆寫。舊runner在work/t14-match-sources/pre-match-t14-macos.py。本場measured manifest126檔相符。

76 Python一般/-O、5份JS mock/3新JS語法與獨立程式/raw審查PASS；初次discover跑0未列通過，之後逐檔兩模式確實76項。歷史26場raw/hash（含原FAIL）＋本批1完整局核對一致，不重跑引擎矩陣。T13 129來源/主Mod集合、官方runtime雙hash/codesign不變。官方app仍`../runtime/0 A.D..app` 0.28.0 ARM64；binary SHA256 `531981d016596b0abde110cd239feaed98998c3fdaa837d0fa8d6f75482c81ef`，public.zip `ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429`。

## 下一步與限制

下一個可實測範圍優先另立seed7同條件完整局契約，補跨seed覆蓋；或另定長時間觀測。現行runner僅允許match seed42，需先擴契約及工具回歸才測seed7，不直接繞過限制。先核對本文件、progress、Git/runtime/source，再寫負載/方法/門檻/停止條件，不重跑已完成矩陣。

返航/停機位性能、精確空戰/空對空、潛艇/自動聲納/隱蔽對抗、其他seed完整局、雙AI互攻、大混戰、持續長時間壓力、多人与跨硬體均NOT RUN。潛艇缺自動偵測/hidden gate，不為測性能擴功能。不重寫AI、不改C++、不開T16–T18。原不限FPS/重複性缺口與唯一根因仍未解，不把cap60小片段與單一固定防守完整局當完整T14 DONE。

無遺留引擎、背景任務或排程；未commit/push、未刪任何profiles/work/失敗。後續仍遵守本機限定與保存現有變更。
