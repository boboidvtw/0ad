<!-- Purpose: Latest bounded T14 checkpoint after initial-600-soldier battle. Created: 2026-10-04. -->
# T14 接續交接 — 2026-10-04

Repo `/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`。HEAD仍`726a3aefcae830f605de438cd13192cc6330414e`，T13限定DONE，整體T14 **PARTIAL**；全部T14尚未commit/push、index空。接續先核對實際Git/現有變更/progress/官方R28/程序/來源，不只依賴交接；保留profile.txt/profile2.jsonp/work及全部FAIL。無背景任務或排程。

## 本次最新限定PASS

[t14-battle事前契約](t14-battle.md)、[驗證](evidence/t14-battle-validation.md)、[結果](evidence/t14-battle-results.json)、[現行200檔來源](evidence/t14-battle-source-manifest.json)。10-04 09:34 Asia/Taipei單場正式量測，無本批FAIL/重跑。

初始600既有T11 soldier（每席300、HP100），固定平坦192 grid、mapSeed42/AISeed42讀回，無AI故AISeed未參與，固定布局不表示跨隨機地圖覆蓋。OnInit各一次正常attack-walk、null formation、不補兵/回血/再派/改HP/AI/C++/主Mod。純士兵缺ConquestCritical，使用官方endless且實際VictoryConditions=[]，**正式勝負NOT RUN**；耗盡不是正式won/defeated。

- sim0/無暖機、cap60/1×/no-profiler、1280×800 GL/nosound、25設定起終確認、observer−1。
- wall90.058011秒、sim88.6秒、4810幀/91 timing samples/19 full unit快照，首次末快照P1軍隊耗盡按契約收尾，未跑滿120秒。
- p95 18.929932ms、p99 41.628174ms、sim/wall0.983810313。
- 60.013393秒＋30.044618秒兩窗都≥30秒、性能與活動全受gatePASS；第一窗p9525.036865/p9945.520020/simwall.976448706較慢保留，原因未確立。
- 23個>50ms/max73.217041ms全部保留，包含global0/1開局，不排暖機。
- 17共同ATTACKING快照，Unit loss300/253、增損區段17/16；P1存活0/P2 47。每snapshot 300−alive與官方Unit loss相符、逐ID只減/HP不增/owner/template固定。
- 單方攻擊峰115/118，同時合計觀測峰223，不稱600同時攻擊/全程600交戰。首共同wall5.013431/末85.050649秒是快照時間。
- camera實際起終(384,158.231185913,220)/rotation(.8500061035,0)/zoom180完全一致；原bounds50–200，未繼承soak max250。visual_verified:false，未做全視錐/逐tick圖像驗收。
- CPU整程序中位29.6%、RSS峰444.781250MiB；短場不作RSS趨勢/熱/戰鬥長壓/leak驗收。
- raw：work/t14-performance/20261004T013433364110Z-battle-42。

官方R28 0.28.0 ARM64、M4/10 logical CPU/16GiB/macOS27.0 26A428/AC。binary SHA256 `531981d016596b0abde110cd239feaed98998c3fdaa837d0fa8d6f75482c81ef`、public.zip `ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429`，codesign相符。

## 來源、回歸與原證據

現行200=原soak191＋9新檔，原集合只runner hash改；本場measured128檔。新增6檔battle harness、t14_battle.py/Python/JS tests，runner僅battle opt-in/seed42/units600/cap60/no-profiler/endless/180秒及parser/link/source/evidence分支；ground/match/dual/soak語義不變。原runner封存work/t14-battle-sources/pre-battle-t14-macos.py。所有更早manifest保留歷史，不覆寫。

109項Python一般/-O各PASS、8JS mocks、4CLI拒絕、37歷史raw精確重解析、契約/語言/整合review均在首跑前完成；work/t14-battle-sources/pre-run-lock.json與prepared-source-manifest.json鎖定來源/契約。準備修OS樣本少不應把短耗盡誤當capture invalid，未放寬30秒活動gate。JS mocks只支持控制/protocol、不是runtime戰鬥證據。

另一代理未import正式parser，直接重組667payload chunks、4810frames/2windows/nativeHP及loss/clock/control/firstdepletion核算PASS、issues空，work/t14-battle-sources/independent-raw-audit.json。419原raw/evidence/profiles/37舊raw資料夾、T13 129來源/主Mod集合不變；當場source/profiles不變、exit0/0ERROR/WARNING。closeout-audit.json記最終Git/來源/鏈結/精確重解析/engine/runner退出。

## 已完成的先前限定範圍

先前詳細交接保留於[10-03交接](SESSION-HANDOFF-2026-10-03-T14.md)，不可將歷史章節NOT RUN誤當最新結果。

- 固定防守seed42與seed7完整局各限定PASS，AIseed皆42；不同mapseed只覆蓋跨mapseed，不是重複性。
- 事前契約的3場新map42/AIseed42固定防守完整局同條件重複性PASS，45窗口/14共同完整分鐘離散度通過；準備誤啟45.5秒停止attempt保留FAIL。
- 既有雙AI難度3单seed完整局限定PASS，wall1519.504454/sim1514.6/25完整分鐘窗口；共同攻擊/雙方loss/正式P2won，峰176單位43建築，不是600人戰鬥。P1分類損失帳差11原因未明。
- 600固定地面移動30分鐘性能/活動/RSS工程容差PASS，wall1800.014206/sim1793.2/30受gate窗口；RSS +11.921875MiB/OLS.602904437MiB/min。首場相機250→200配置FAIL保留，唯一工具修正retry明設soak-only max250後PASS；禁止第三場補跑。熱資料unavailable/定量熱NOT RUN，不證明無leak或AI/戰鬥長壓。
- 經濟/late、飛行、即時AA、對地攻擊片段仍僅各自限定PASS，原late legacy total/flight輸出FAIL保留，不等於完整空戰。

## 剩餘工作與接續約束

**整體T14仍PARTIAL。** 七場不限FPS基線資料有效但sim/wall未達，200單位重複性FAIL仍在；cap60緩解本機落後，頻率平滑不是唯一根因已證實。

本次補同種士兵地面交戰，不補混合兵種大混戰。雙AI跨seed/重複性、AI/戰鬥長壓、定量熱/頻率、多人/跨硬體、精確空戰/返航/停機位、潛艇仍NOT RUN；潛艇缺自動偵測/hidden gate等，不為效能擴功能。既有dual限定PASS不是NOT RUN。

下一步先盤點既有混合兵種（如EpochMelee/Slinger）與原生近/遠程武器的活動證據可行性，或說明更合適限定範圍；先寫樣本、初始/實際單位量、武器/HP/ownership、控制/時長/每窗/活動/比較/停止/真實FAIL保留契約，再調工具/回歸/審查/鎖定來源與量測。不要直接擴矩陣、無故重跑此單場/原T14或重做T05–T13；不重寫AI/改C++/補機制，無commit/push/背景/排程。正式勝負若需要另有可行性與契約，不替此endless場加事後標準。

收尾已確認engine/runner退出，沒有後續自動工作；下次仍需以現場核對為準。
