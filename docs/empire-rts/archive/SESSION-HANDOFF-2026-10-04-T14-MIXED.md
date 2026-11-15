<!-- Purpose: Latest T14 checkpoint after single mixed melee/ranged real FAIL. Created: 2026-10-04. -->
# T14 混合交戰接續交接 — 2026-10-04

Repo `/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`，HEAD仍`726a3aefcae830f605de438cd13192cc6330414e`。T13限定DONE，T14 **PARTIAL**；所有T14未commit/push、index空。先核實際Git/progress/變更/官方R28/遺留程序/來源，不只依本交接。原[10-04單兵種交接](SESSION-HANDOFF-2026-10-04-T14.md)保留；本檔是其後續，不覆寫原證據。

## 最新有效實測、限定FAIL

[事前mixed契約](t14-mixed.md)、[驗證](evidence/t14-mixed-validation.md)、[完整結果](evidence/t14-mixed-results.json)、[現行209來源](evidence/t14-mixed-source-manifest.json)。**只1場、無工具錯誤/retry，不補跑、不改門檻。**

- 2026-10-04 Asia/Taipei 17:23，初始600：每方150既有T11 EpochMelee/HP100/Hack6/range3＋150 Slinger/HP60/Pierce4/range40/原生Projectile；每席HP24000/fullHP，兩交錯20×15/2.5m grid。
- 平坦192/Seed42與AISeed42讀回，無AI故AISeed未參與；固定布局不代表隨機地圖覆蓋。各一次正常attack-walk，commands2不變、不補兵/回血/重派/改武器/主Mod/AI/C++。
- sim0、無暖機排除、cap60/1×/no-profiler/nosound/1280×800 GL、25設定起終相符。camera實際起終(384,158.23118591308594,220)/rotation(.850006103515625,0)/zoom180一致，原bounds50–200、visual_verified:false，不宣稱全軍可見/逐tick畫面驗證。
- wall105.042832031秒/sim100.8秒、5667幀/106 timing samples/22 full unit快照。首次末快照P2軍隊0收尾，非120秒持續混合交戰。
- 全局p95 25.472167969ms PASS、p99 52.647216797ms **FAIL**、simwall.959608553 PASS，全局性能FAIL。
- 第一窗60.005966064秒：p95 35.623046875/p99 64.110107422/simwall.936573539，**性能三項FAIL、混合活動PASS**。
- 第二窗45.036865967秒：p95 19.797119141/p99 29.489013672/simwall.990299814，性能PASS，**混合活動FAIL**（P2近戰在50.066756104秒快照已0，窗口2的ATTACKING/timer推進均0）。兩窗≥30秒全受gate，合併皆FAIL。
- 64個>50ms/max95.558837891ms全部在第一窗，含開局global0/1 78.016113281/94.941894531，完整保留。不以全局活動PASS掩蓋局部FAIL。
- 全局活動PASS：20共同ATTACKING快照，實際合計同時攻擊觀測峰398（非600同時）；四組近/遠程各有3+活動快照與timer推進區段。逐ID/owner/template/HP/maxHP/武器/native lastAttacked單調，300−alive=官方unitsLost.Unit逐快照吻合。
- 各組初始150；末P1 Melee0/Ranged133，P2 Melee0/Ranged0；官方Unit loss167/300。原生Attack timer進展不足以逐發歸因命中/傷害來源/投射物總數。
- 純軍隊無ConquestCritical，官方endless/VictoryConditions[]、兩方末state active；軍隊耗盡不是正式勝利，正式混合勝負NOT RUN。
- 整程序OS106筆/CPU中位55.85%/RSS峰442.625MiB；短場不驗熱/頻率/RSS趨勢/leak。首窗較慢原因 **Insufficient data**，不同武器/HP/art/存活/背景的單場對照不能歸因或作paired regression。
- raw `work/t14-performance/20261004T092355508923Z-mixed-42`；engine exit0/0ERROR/WARNING/資料有效，runner exit1正確表示真實契約FAIL，不是工具崩潰。

## 回歸、來源及核算

原battle200＋9 mixed新檔=**現行209**，原集合只有runner hash改；本場measured128。6檔隔離mixed harness＋parser/Python/JS測試，runner only mixed opt-in/seed42/600/cap60/no-profiler/endless/180秒/link/source/report。原battle/parser/harness與ground/match/dual/soak语义、主Mod/AI/C++不改；更早manifest保留歷史，不覆寫。

原runner `work/t14-mixed-sources/pre-mixed-t14-macos.py`，prepared-source-manifest.json/pre-run-lock.json鎖定來源/契約；量測前121 Python普通/-O各PASS、9JS mocks、4CLI拒絕、38歷史raw新舊精確重解析PASS。額外stored-analysis核對初次exit1，原因早期smoke `20260929T000136173379Z-200`的舊passed:true缺effectiveConfig，兩版parser都拒絕Missing effective configuration；舊result/raw未改。不是新mixed回歸或正式基線PASS；見historical-reparse-cli.json。

主代理自己完成程式/契約審查（review.json）；另以不import任何正式parser的分離實作直接核算2253chunks/5667frames/兩窗口/ID/HP/weapon/timer/官方loss/控制/source與真實FAIL/64慢幀，audit PASS/issues空，`separate-raw-audit.json`。**非獨立代理審查**，不要冒稱不同代理核算；mock或audit PASS不代表效能PASS。

431份原raw/evidence/profiles hash與原38資料夾保留；共39 raw資料夾、T13 129/主Mod集合一致。根profiles/當場sources不變；結尾核對見同目錄closeout-audit.json。無commit/push/刪檔/背景任務/排程；engine/runner退出，下一次仍核現場。

## 先前限定證據與剩餘缺口

前次完整細節見[單兵種交接](SESSION-HANDOFF-2026-10-04-T14.md)與[10-03交接](SESSION-HANDOFF-2026-10-03-T14.md)，不因本場FAIL重跑/重寫：

- 同種T11初始600單場battle性能/活動限定PASS，wall90.058011/sim88.6、兩窗PASS、23慢幀、同時攻擊峰223；正式勝負NOT RUN。
- 固定防守map42/7完整局各限定PASS，AIseed均42；跨mapseed不是重複性。事前契約3場新map42/AI42完整局同條件重複性限定PASS、45窗/14共同分鐘；誤啟停止attempt FAIL保留。
- 雙AI難度3單seed完整局限定PASS、25完整分鐘、峰176單位43建築；不是大混戰，分類損失帳差11原因未明。
- 600地面往返30分鐘效能/活動/RSS工程容差限定PASS，30窗、RSS +11.921875MiB/OLS.602904437MiB/min；首場camera250→200配置FAIL與唯一soak-only max250 retry PASS都保留，禁止無故重跑。熱unavailable，不證明熱穩定/無leak。
- 經濟/late、飛行、即時AA、對地攻擊各自限定片段PASS；原late計數/flight輸出FAIL保留，不等於完整空戰。
- 原不限FPS simwall與200重複性FAIL仍在，cap60只支持本機模擬落後緩解，頻率平滑唯一根因未證實。

**混合交戰目前已測FAIL，不能列NOT RUN或PASS。** AI/戰鬥長壓、雙AI跨seed/重複性、定量熱/頻率、多人/跨硬體、正式混合勝負、精確空戰/返航/停機位、潛艇仍NOT RUN。潛艇缺自動偵測/hidden gate，不為效能擴機制。

下一步先離線診斷本mixed首分鐘慢幀/活動/配置及來源，不直接重跑。若要原生profiler/單一變因測量，**另寫事前範圍/樣本/對照/觀測/每窗/活動/停止/真實FAIL保留/工具retry契約再執行**；profiler資料不能直接當no-profiler門檻樣本。不可事後縮短本场或放寬混合活動稱PASS。仍沿R28/既有Mod、不重做T05–T13、不改AI/C++/未完成特殊機制、不commit/push/刪除profiles/work或安排背景工作。持续更新progress/plan/journal/evidence/新交接，報實測/推論/Insufficient data。
