<!-- Purpose: resume bounded Timer/Health profiling with preserved T14 FAILs. Created: 2026-10-05. -->
# 2026-10-05 T14 Timer／Health細分診斷交接

Repo：`/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`。HEAD `726a3aefcae830f605de438cd13192cc6330414e`，index空，T14未commit。仍沿官方R28／既有Mod，不改C++／AI／武器／死亡玩法，不擴空戰／潛艇；無commit／push／刪檔／背景／排程。先核實際Git、runtime、progress與來源、engine／runner／HTTP狀態，不只依本摘要。

優先讀本文件、progress／plan／journal、[事前契約](t14-fine-profile.md)、[validation](evidence/t14-fine-profile-validation.md)、[results](evidence/t14-fine-profile-results.json)、[現行231來源](evidence/t14-fine-profile-source-manifest.json)。再讀[前批simulation離線交接](SESSION-HANDOFF-2026-10-05-T14-SIM-DIAGNOSIS.md)及[profiler交接](SESSION-HANDOFF-2026-10-04-T14-PROFILE.md)，按需讀mixed／battle／soak／dual／match等舊證據。220／209／200等manifest保持歷史，不覆寫。

## 最新限定結果

| 項目 | 結果／邊界 |
| --- | --- |
| 整體T14 | PARTIAL，原no-profiler mixed、原不限FPS／200重複性FAIL保留 |
| 官方R28細分prototype觀測可行性 | 靜態來源限定PASS；constructor全域、排序載入、dynamic method lookup與profiler2 bindings核對 |
| 新Timer／Health單場 | 原生scope／coverage／早期活動與獨立核算限定PASS；有profiling／attribute／marker／GET擾動，不是性能修復PASS |
| 唯一根因／overhead／修復改善 | Insufficient data／NOT RUN |
| nativequeue大小／每Destroy／Deinit與allocator | NOT OBSERVED；不改C++補機制 |
| 正式勝負／混合性能或重複性／戰鬥長壓／熱頻率／GPU等 | 未驗收，既有限制保留 |

新raw：`work/t14-performance/20261005T020409961988Z-fine-profile-42`。新批只1場、無FAIL／retry，不是前批工具retry已用完後的第三次重跑。隔離harness7檔、runner／scope parser／兩測試共11新檔；原220來源全未改，現行231／本場measured124。主Mod／AI／C++／原武器未改。

600初始每席150 T11 EpochMelee HP100／150 Slinger HP60、原Melee／Ranged／Projectile，無AI、平坦192grid、Seed42／AISeed42（無AI未參與）、每席一次正常attack-walk、無補兵／回血／再派、sim0／cap60／1×／endless。GUI105.116412秒／sim101.2、5653intervals／22snapshots／106timing samples；首次軍隊耗盡收尾。末P1只有Slinger133／P2全0，Unit loss167／300，states仍active，正式勝負NOT RUN。起終camera `(384,158.23118591308594,220)`、rotation `(.850006103515625,0)`、zoom180／bounds50–200、25畫面設定相符，visual_verified:false。

帶擾動p9525.879150／p9952.903076ms／simwall0.962742144只作描述；65個>50ms及max92.815918ms全部保存。原no-profiler gate投影全局／第一窗性能未達，第二窗性能较好但混合活動不足；不得以取證PASS掩蓋局部結果，原mixed FAIL不改。

## trace與細分證據

16main＋2overview／60,737,663bytes，GUI0→20.008826秒terminalseq1003／sim18.4。1004 marker精確匹配、1003連續完整frame91–1093、92strict-contained sim update／turn0–91。每turn恰1 `T14FineTimerUpdate`、timeBefore嚴格推進，`T14FineHealthDeath`／`T14FineHealthCorpse`各70call，fixture entity／同entity祖先與call完整性核對。四組早期ATTACKING snapshots3／3／2／3、timer advance2／3／2／3。

Timer p9535.086／max46.872ms、HealthDeath p950.189／max1.320999、Corpse p950.127／max1.163998。Timer scope包括scan、所有callback／catch-up，還不是逐callback耗時；Death／Corpse call數不代表nativequeue或成功屍體數。70個call涵蓋到20秒marker；terminal前最後snapshot wall15.045390／sim14.0秒的Unit loss41是較早粗區間，不是同區間帳差29。全局／逐turn／有界5秒bins／union與邊界不確定calls保留，巢狀inclusive不相加、不相減分位數、不命名exclusive CPU／wait／GC／GPU。

92次最長直接子label Update67／Motion9／Flush16；18慢sim update中Flush12／Update6，29慢GUI是另一集合。最慢frame818／turn66 parent75.681ms、Flush52.053999ms；**同turn**Timer18.460001ms、四Death call union0.272998ms／四Corpse union0.243998ms，Corpse嵌套Death不能相加。GUI14.313194→14.402370秒，不是pre-sim0。不能把52ms清理長尾命名corpse建立成本；也不能由上游死亡scope小排除死亡觸發之後的清理成本。queue量、各Destroy／Deinit或allocator仍未知。

首frame91 native1.304527→1.555383012跨sim0 marker1.413001001；末1093 21.421627→21.439579001跨terminal21.421836。wholemax250.856012含marker外載入，不稱純GUI0–20；strict frame1001／max89.271ms另列。generic strict Flush1186=frame92＋sim92＋interpolate1002，不能全算sim cleanup。75個來源有界負frame間隙與所有raw保留。

## 核算與收尾

事前11fine Python／27既有native parser一般／-O各PASS、6clock helper、1fine JS mock（原fixture＋官方Timer/Health＋descriptor／return／throw等）、8CLI拒絕PASS，獨立PRE-RUN APPROVE。審查問題在量測前修正、契約與source重鎖，沒有事後改gate。獨立raw audit標準庫直接重建，不import正式parser／runner／helper，核所有call／turn／bins／聯集、epoch bracket／最大case／22逐ID／HP／owner／weapon／官方loss／全5653interval與兩窗PASS。

`work/t14-fine-observability`保存preflight、611保留hash、pre-run lock／231source、26官方來源、回歸／兩次文件對齊審查封存、same-sample-regions、independent-raw-audit、final-review與closeout。收尾逐核231／舊220／T13 129／offline43、611份先前資料與42raw資料夾、HEAD／index與engine／runner／HTTP退出。原profile.txt／profile2.jsonp與work/均不刪除或提交。

既有單兵battle、600移動30分鐘、雙AI單seed、固定防守seed42／seed7與事前3場同條件重複性仍各自限定PASS；原FAIL、soak首場camera FAIL、準備repeatability attempt FAIL、late／flight輸出FAIL保留。雙AI分類損失帳差11未知；cap60僅支持本機模擬落後緩解。飛行／AA／strike只片段。AI戰鬥長壓、雙AI跨seed／重複性、定量熱頻率、多人跨硬體、精確空戰／返航／停機位、潛艇hidden／自動偵測等前置未驗收，不為效能擴功能。

## 下一步

先用既有本場離線縮小Timer子callback與Flush的可觀測部分；核官方JS Destroy／Deinit以及callback路徑能提供何種scope，哪些native工作仍看不到。不因一次52ms指定某元件根因，也不靠C++／AI／武器修改救FAIL。

若需要新的觀測處置，先另寫最小單一變因、樣本／對照／擾動、seed／實際負載／HP／武器／ownership／畫面／camera／時長／活動與全局及局部gate／比較／stop／FAIL與retry契約，回歸／審查／source freeze後才量測。不擴跑矩陣；限定取證PASS不是完整遊戲效能驗收。持續更新progress／plan／journal／evidence與新交接，結束核退出狀態，無commit／push／刪檔／排程／背景。
