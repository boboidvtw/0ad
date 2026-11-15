<!-- Purpose: continuation after valid game but incomplete CanAttack trace. Created: 2026-10-08. -->
# T14 CanAttack capture FAIL／PARTIAL交接

Repo `/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`。核實際Git/progress/diff/R28/locks/engine-runner，不只依摘要。HEAD726a3aefcae830f605de438cd13192cc6330414e/index空；T13限定DONE，T14仍PARTIAL，全部T14未commit。

按[CanAttack事前契約](t14-canattack-profile.md)新增單一JS own writable UnitAI.CanAttack wrapper，保留原方法/descriptor/this/arguments/return/throw/同步順序；targetKinds/未知/noninitial保留，不probe目標/Set、不同批包全部callback。新隔離工具14檔（10harness+runner/parser/tests4），原256未變，270產品sources／130本場measured。source/code review44 APPROVE、JS/14parser一般/-O/既有JS與Python9一般-O/clock6/CLI9 PASS；source360lock與單獨guard PASS後，另一call launch。

唯一新raw `work/t14-performance/20261008T005749621540Z-canattack-profile-42`：engine exit0/無ERROR-WARNING、measurement_validtrue/earlyactivitytrue、control/clock/source/rootprofiles相符。17main+2overview/69092157bytes/terminalcomplete，卻expected964只538完整frame markers（缺426）／549closed markers（缺415）；payloadmismatch0，11closed marker在不完整frame。640全completeframes、537selected noncontiguous、43selectedsimupdate。fine marker coverage mismatch使後續完整解析中止，runnerexit1／diagnosisPARTIAL，完整CanAttack貢獻Insufficient data。不能改parser gate補造缺失。

獨立stdlib raw一般/-O相同；觀測完整frame子集合469304CanAttack/3346Search/614Resistance，不是整段總量/完整turn或真CanAttack返回true。官方固定commit Profiler2.cpp59/335–387/832–853：4MiB ring/current snapshot query，密集events/1秒poll與缺口相容但不是唯一cause/quantitative overhead證明，也不把HTTPbytes當ringbytes。attempt1 raw28/source/stdout/FAIL全留，無runtime retry，不加query/bytecap、不縮trace救PASS。

全場105.103396GUI秒/97.8sim/5449interval/22snapshot；全局p99 77.529053/simwall.930512 FAIL，首窗p95 49.397949/p99 92.359131/.886535性能FAIL活動PASS，尾窗性能PASS混合活動FAIL，148>50ms全留。末133Slinger vs0，loss167/300，兩方active/endless，正式勝負NOT RUN。所有歷史no-profiler/工具/前場FAIL仍保留，前場Resistance唯一retry用完不與本批混算。

詳[validation](evidence/t14-canattack-profile-validation.md)、[results](evidence/t14-canattack-profile-results.json)，work/t14-canattack-profile的preflight/review/prelaunch-lock/guard、marker-diagnosis、兩independentaudit、capture-source-support、attempt1-raw-lock、docs-review/closeout/lock。原reviewer quotaerror已記，新docs-only reviewer不審自己parser不冒稱code/raw。官方R28 binary531981d016596b0abde110cd239feaed98998c3fdaa837d0fa8d6f75482c81ef/public ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429。保留old80/809/T13_129/674資料與原45raw＋新1＝46，profiles/work不刪。

下一步若繼續：**先離線/source評估method結束聚合/較低eventdensity的不同觀測設計**，核原生計時API與同步/return/throw/巢狀語義及事件量界線，聚合不是漏丟unknownID或合併原gameplaycalls；不得再跑同密集逐call方案救FAIL。先明確新問題/樣本/seed/fixture/camera/時長/gates/比較/停止retry契約、tests/獨立review/source-lock/獨立guard，再選是否量測。不同範圍目前NOT RUN，無安全修復或唯一根因。nativequery readonly prototype替換已排除、legacy無同場歸屬，不重做其離線批。entity288先Death再Timer再Flush仍未解，修復/overhead/正式勝負NOT RUN；長壓/重複性/熱GPU/跨硬體與未完空戰潛艇不擴。

收尾engine/runner/所有觀測HTTP關、HEAD/index/diff與hash以本批closeout/seal為準；無commit/push/刪檔/背景/排程，不改C++/AI/玩法，不重做T05–T13或既有T14矩陣。持續更新progress/plan/journal/證據/交接，分valid game／captureFAIL／PARTIAL／NOT RUN。
