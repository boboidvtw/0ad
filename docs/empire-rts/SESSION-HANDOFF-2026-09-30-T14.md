<!-- Purpose: Exact bounded T14 closeout checkpoint. Created: 2026-09-30. -->
# T14 Session 交接

最新接續請讀[2026-10-01交接](SESSION-HANDOFF-2026-10-01-T14.md)，本文件保留09-30各階段歷史。

Repo：`/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`。HEAD仍726a3ae，全部本次變更未commit／push。先核對Git、[progress](progress.md)、[T14證據](evidence/t14-validation.md)、[結果](evidence/t14-results.json)、[契約](t14-performance.md)與官方R28。

## 狀態

T13限定DONE不變，129檔來源核對PASS，T05–T13未重跑。T14 **PARTIAL**：200／600各3次、1200一次；每場20秒暖機＋60秒wall量測，全數資料完整、引擎exit0、0 ERROR/WARNING。200／600幀間隔p95/p99達標，但simulation/wall分別0.900–0.940／0.863–0.897，均未達0.95。200重複性FAIL、600 PASS。1200僅觀測，sim/wall0.930，最大單幀146.861ms。

這是不限FPS、平坦192、固定camera、50%T11 worker／50%T11 soldier反覆walk的主循環間隔基線，不是GPU timestamp、整局或全部單位同時可見；無AI／戰鬥。兩時段背景負載未控制，原因尚未定位。

## 來源與證據

七場原始證據留`work/t14-performance/`；結果列明每場路徑及全部artifact hash。兩probe保留並排除：000021為API錯誤，000136為舊passed gate，雖passed:true但performance_target_pass:false，禁止稱效能PASS。

量測來源119檔一致，封存在每場source-manifest及work/t14-tools/matrix-source-manifest.json。正式矩陣後僅runner parser缺config防護／acceptance與負例測試更新；舊runner封存work/t14-tools/t14-macos-measured.py，現行來源表evidence/t14-source-manifest.json。七場raw以最終parser重讀與原analysis相等；10項測試一般／-O PASS，不需重跑引擎來驗證這個純parser補強。

官方app仍`../runtime/0 A.D..app` 0.28.0；binary SHA256 531981d016596b0abde110cd239feaed98998c3fdaa837d0fa8d6f75482c81ef；public.zip ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429。未改官方runtime、主Mod、AI或C++。

## 追加診斷已完成

[T14 FPS診斷證據](evidence/t14-diagnosis-validation.md)與[結果](evidence/t14-diagnosis-results.json)：600單位60/0/0/60四場，兩cap sim/wall約0.997通過、兩不限0.917/0.947未達；平均改善0.064956，預定支持條件PASS。另兩場profiler取得真實CPU ring buffer，分開記錄、不納入四場比較。來源顯示SmoothedFrequency倒數作delta，支持計時平滑偏差候選解釋，尚無逐frame dt精確證據，未判定唯一根因。

本批新增runner --fps-cap/--profiler及t14_profile.py，13 tests一般/-O PASS、獨立Python複查通過；六場raw重讀一致。原baseline t14-source-manifest維持歷史，現行改看t14-diagnosis-source-manifest；舊runner/test与官方只讀來源留work/t14-diagnosis-sources。前五場同版，第六場runner僅補工具失敗防護，harness/Mod未改。原不限FPS失敗仍成立，沒有改產品／使用者預設cap。

## 下一步

1. 固定FPS配對與原生profiler限定診斷已完成，不要為熟悉專案重跑；若需定位唯一根因，仍缺逐frame SmoothedFrequency／delta觀測，不預設C++修改。
2. AI經濟／後期進攻片段已完成下述限定量測，不重跑；後續特殊原型負載需先寫獨立契約。T07／T08效能、長時間／多人／跨硬體均NOT RUN；不擴張T16–T18或重做既有功能驗收。
3. 未取得明確授权，不commit／push；不要提交或刪除根profile.txt、profile2.jsonp、work/，既有失敗也需保留。

工具以使用者mods/epoch_t14_harness及epoch_t14_workload symlink opt-in；不設為預設Mod。所有本次引擎程序已退出，沒有背景任務或排程，可以安全關閉本session。

## AI片段追加完成（目前接續入口）

先讀[t14-workloads契約](t14-workloads.md)、[驗證](evidence/t14-workload-validation.md)、[數據](evidence/t14-workload-results.json)。兩seed各經濟／late共四場PASS；60fps、1×、官方R28與T13原生120/700秒save，載入快照及save hash全部相符。經濟24–28單位各60秒；late71–91／74–91單位165.010／176.699秒，非600單位大戰。sim/wall約0.996，p95低於19ms，late均有6個攻擊觀測點與9個損失增量、AI won。

原兩late場讀取舊total導致activity FAIL，保留排除。官方R28 LostEntity只遞增Unit／Structure分類；observer修正並保留legacyLossTotals，mock與兩場重跑PASS，不改主Mod或AI。完整raw與hash索引見results；現行來源改看t14-workload-source-manifest，較早baseline／diagnosis manifests為歷史版本不可覆蓋。六場workload raw重算一致，16項Python一般/-O、JS mock/語法及獨立審查完成。

T14仍PARTIAL：原不限FPS模擬落後及200單位重複性未解；特殊原型、完整對局、長時間／多人／跨硬體仍NOT RUN。後續先定範圍與門檻再量，不擴張未完成空戰／潛艇機制。HEAD726a3ae，未commit/push，根profiles與work保留。没有排程或遺留測試引擎。

## 特殊原型追加完成（最新接續入口）

先讀[t14-flight契約／缺口盤點](t14-flight.md)、[驗證](evidence/t14-flight-validation.md)、[結果](evidence/t14-flight-results.json)。64架既有T07飛機、seed42/7、每場20秒暖機＋60秒wall、cap60限定PASS：p95 17.706/18.701ms、sim/wall0.999800/0.993100；13快照每點64架離地移動、每對相鄰快照64架>5m位移、量測內6輪walk。這不是AA／對地交戰或完整空戰。

首場040315-flight42因巨大print未留下活動raw而FAIL排除，原timing達標不能追認PASS；改1200字元有序分段，僅重跑受影響42一次。兩成功場040630-flight42及040802-flight7來源相同，raw全留work/t14-performance。GUI實際camera與地圖requested不同，起終固定，已明列實際值；visual_verified:false不宣稱全機可見。

現行來源改看[evidence/t14-flight-source-manifest.json](evidence/t14-flight-source-manifest.json)的148檔；baseline/diagnosis/workload manifests全部保留為歷史版，不覆寫。舊runner/失敗GUI/parser在work/t14-flight-sources。T13 129檔與主Mod集合不變；歷史19場raw/hash、新3場raw、16+9 Python一般/-O、既有/新JS mock與語法、獨立重算通過。

下一步可另定既有AA／對地交戰短片段（負載會隨死亡減少，需真實交戰窗口、數量曲線、傷害證據，不能补血湊測試），或完整對局效能契約。潛艇自動偵測及hidden攻擊gate不足，水下性能NOT RUN，仍不開T16–T18。原不限FPS sim/wall與200重複性失敗未解；唯一根因、長時間、多人、跨硬體均未證實，完整T14 PARTIAL。

HEAD仍726a3ae，所有T14變更未commit/push；保留根profiles/work和失敗，index空，無背景任務／排程及遺留測試引擎。

## 即時防空追加完成（最新接續入口）

先讀[t14-aa契約](t14-aa.md)、[驗證](evidence/t14-aa-validation.md)、[結果](evidence/t14-aa-results.json)。初始64架既有飛機與4座既有AA、seed42/7、20秒暖機＋60秒wall、cap60限定PASS：p95 18.715/18.723ms、sim/wall0.996446/0.996392，存活64→50/51；HP池下降3565/3545、14/13死亡與官方unitsLost.Unit增量逐區段一致。13活動點、12/12區段含末段有傷害、四塔HP500，逐機HP無增加/復活。本批無失敗或重跑。

這是既有無Projectile即時防空對自然減員機群，不是64架全程存活或精確空戰。兩場原始資料work/t14-performance/20260930T093936443836Z-aa-42與20260930T094119929624Z-aa-7；GUI相機實際值與起終一致已記，visual_verified:false，不宣稱全部可見。

現行來源改看[evidence/t14-aa-source-manifest.json](evidence/t14-aa-source-manifest.json)的157檔；flight/workload/diagnosis/baseline manifests維持歷史，不覆寫。舊runner封存work/t14-aa-sources/pre-aa-t14-macos.py。T13 129來源及主Mod集合不變；歷史22場raw/hash與新2場raw核對PASS，37項Python一般/-O、三份JS mock、新JS語法及獨立raw審查PASS。

下一步可另定既有飛機對地攻擊片段（真實目標HP/命中、自然死亡與有效交戰窗口）或完整對局性能，不無故重跑飛行/AA或既有T14矩陣。返航/停機位與精確彈道未納入；潛艇缺自動偵測/hidden攻擊gate仍NOT RUN，不開T16–T18。原不限FPS模擬落後及200重複性未解，頻率平滑非唯一根因定論。完整T14仍PARTIAL。

HEAD726a3ae；全部T14變更未commit/push，index空，保留根profiles/work及全部失敗。無背景任務、排程或遺留引擎。
