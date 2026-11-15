<!-- Purpose: continuation checkpoint for observed invalid-owner handler containment. Created: 2026-10-05. -->
# T14 Resistance ownership 觀測交接

Repo `/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`。先查實際Git、progress、變更、官方R28、來源與鎖、engine／runner，不能只依交接。HEAD仍726a3aefcae830f605de438cd13192cc6330414e／index空，T13限定DONE，全部T14未commit，整體T14 PARTIAL。

## 最新限定結果

依[t14-resistance-profile契約](t14-resistance-profile.md)完成單一既有Resistance.OnOwnershipChanged wrapper，target/from/to，沿既有search/fine scope；主Mod／AI／C++／玩法改動0。有效raw `work/t14-performance/20261005T105101310412Z-resistance-profile-42`，取證PASS。[validation](evidence/t14-resistance-profile-validation.md)與[results](evidence/t14-resistance-profile-results.json)保留窗口／慢幀／最大病例；全部逐handler/search/turn/5秒bin在raw result。

- 16main／2overview、69,303,836bytes；1001markers／1000選定連續frame／1128全部完整frame／93strict turn。
- 674全部handler＝600creation＋74invalid-owner；71strict invalid（70有search、1無）、3invalid marker外；creation全部owner與fixture一致。transfer／other／未知非初始0只是本場結果，synthetic非初始大ID／transfer／marker外PASS，不能排除corpse/local/mirage或拿未知ID判FAIL。
- 7914strict search：**2148 Flush皆實際巢狀於invalid-owner handler**；Timer5765及motion1無此handler ancestry。282marker外search／603marker外handler／248 GUI5秒boundary search保留。
- 71strict invalid target皆配同turn同target較早Death scope；未測Attack caller/reason、實際attackerSet關係、入口HP、native queue。handler聯集738.998989ms含search聯集654.026116ms，nested不相加、不當exclusiveCPU／因果占比。
- 最大Flush frame809/turn66 54.127997ms；4handler target570/204/514/734聯集53.715999ms，152search聯集47.460015ms。最大單handler target590/turn47 39.506002ms含107search/34.859991ms。同場包含關係不是整條官方鏈逐入口證明、唯一根因或修復。
- 前場entity288 post-Death Timer未解，本場Timer亦不能全部稱存活者搜尋。根因/caller/reason仍Insufficient data。

600初始近遠各半、每方300；Seed42/AISeed42無AI、flat192、cap60/sim0/1×/endless、固定camera。GUI105.124610秒/sim101.2秒，5654intervals/22snap，末133Slinger/0、loss167/300、官方statesactive，不是正式勝利。全局p95 26.241211/p99 53.828125/simwall.962667：性能投影FAIL；第一窗性能FAIL、第二窗混合活動FAIL，全70慢幀/最大94.716797、17慢sim與trace32慢GUI保留。原no-profiler mixed FAIL與所有歷史FAIL不補過。

## 首次流程FAIL與唯一retry

首場 `20261005T104832965402Z-resistance-profile-42` 真實啟動，但主代理hash前置失敗未阻止shell後續launch。發現後停止，engine exit0但缺completion、measurement_valid:false/PARTIAL；流程FAIL在`work/t14-resistance-profile/attempt1-failure.json`，22份raw與source/review/輸出保留，不能稱NOT RUN或PASS。

重審最後5秒摘要、原gate與契約附錄，相關一般/-O/JS回歸、133來源重鎖、獨立guard PASS後執行唯一retry。**本批runtime attempts2、有效samples1、retry用完，無第三場。** 兩個合成測試FAIL、事前gate草稿修正及獨立audit的marker外/strict Death集合誤比FAIL也全保留；沒有raw/門檻/玩法救場。

74相關Python一般/-O、JS官方Set live iteration/search/fine/fixture、新runner clock6、CLI9拒絕PASS；正式raw replay一般/-O相同，獨立stdlib raw audit所有call/turn/Death/max病例PASS。審查與hash以work review-pre-runtime／post-runtime／docs-final-review為準。

## 來源鎖與收尾

官方v0.28.0 source commit a2cae4d69f816e9e9d7eecb6bf88f762afc0c90d；binary SHA531981d016596b0abde110cd239feaed98998c3fdaa837d0fa8d6f75482c81ef、public.zip SHA ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429。Resistance/UnitAI/FSM installed zip與沿用reference逐byte相同。舊243產品source/前場126不變；現行256新增13隔離檔、有效measured128，歷史manifest不覆寫。T13 129/search90/674資料/离線81/82/43旧raw保留；實際收尾見`work/t14-resistance-profile/closeout.json`、新evidence-lock，全部45raw保留，engine/runner退出、所有觀測ports關閉。

不commit/push/刪檔/背景任務/排程；保留所有既有變更/profile.txt/profile2.jsonp/work。下次先離線評估同場target→搜尋集合、官方Attack/FSM成本規則與下一個最小候選；若需要Attack.StopAttacking單一wrapper，先另立事前契約、語義回歸／獨立審查／source lock，不同批包全部callbacks，不直接改AI/C++或武器/HP/玩法。不以本包含關係直接選修復或聲稱唯一根因。

修復效果/overhead/正式勝負仍NOT RUN；混合/雙AI重複性、AI戰鬥長壓、定量熱頻率/GPU、多人跨硬體、精確空戰/返航/停機位與潛艇前置仍未驗收。不重做T05–T13，不無故重跑矩陣。持續更新progress/plan/journal/證據/交接，分列PASS/PARTIAL/NOT RUN。
