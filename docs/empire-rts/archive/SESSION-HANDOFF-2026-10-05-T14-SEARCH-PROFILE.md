<!-- Purpose: resume official R28 bounded search-method observability and retained T14 gaps. Created: 2026-10-05. -->
# 2026-10-05 T14 搜尋方法 entity／state 交接

Repo：`/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`。HEAD仍 `726a3aefcae830f605de438cd13192cc6330414e`、index空、全部T14未commit。以實際Git／progress／文件為準，先核官方R28、來源與保留hash、遺留engine／runner／HTTP。無commit／push／刪檔／背景／排程；保留work與profile.txt／profile2.jsonp。不改主Mod、AI、C++、武器、HP、FSM或未完成特殊機制。

優先讀本文件、progress／plan／journal、[新契約](t14-search-profile.md)、[validation](evidence/t14-search-profile-validation.md)、[results](evidence/t14-search-profile-results.json)、[243現行來源](evidence/t14-search-profile-source-manifest.json)、`work/t14-search-observability`內preflight／pre-run lock／獨立audit／reviews／closeout／evidence lock。按需再讀[callback離線交接](SESSION-HANDOFF-2026-10-05-T14-CALLBACK-DIAGNOSIS.md)、[fine runtime交接](SESSION-HANDOFF-2026-10-05-T14-FINE-PROFILE.md)與sim／mixed／battle證據；舊manifest不可覆寫。

## 最新單场限定結果

本批新觀測處置：保留fine Timer.OnUpdate／Health.HandleDeath／Health.CreateCorpse scopes，唯一新增 UnitAI.FindWalkAndFightTargets 方法 `T14SearchMethod` scope及entity／currentState attr。隔離harness8＋runner／parser／兩tests，共12新檔；原231來源全部未改，新現行243，本場measured126。樣本1／runtime FAIL0／retry0；不是重跑前批已用完的profiler工具retry，不是修復或overhead試驗。

官方R28 binary SHA `531981d016596b0abde110cd239feaed98998c3fdaa837d0fa8d6f75482c81ef`、public.zip SHA `ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429`，官方native固定v0.28.0 commit `a2cae4d69f816e9e9d7eecb6bf88f762afc0c90d`；不可用local HEAD當官方來源。UnitAI.GetCurrentState→FSM.GetCurrentState只讀fsmStateName；wrapper保留this／arguments／return／throw／descriptor與finally／不加instance資料。新增API與attr有擾動，錯誤可能阻止original或覆蓋原exception，不能宣稱無成本。

raw：`work/t14-performance/20261005T094516506020Z-search-profile-42`。固定600（每方150 T11近戰HP100＋150 Slinger遠程HP60）、原native武器、192平坦grid、MapSeed42／AISeed42、無AI故AISeed未參與、兩次正常attack-walk、sim0／無暖機排除／1×／cap60／endless。起終camera `(384,158.23118591308594,220)`、rotation `(.850006103515625,0)`、zoom180／bounds50–200與25設定相符；visual_verified:false。

GUI105.045351秒／sim101.4秒、5785intervals／106timing／22snapshots；末P1仅133 Slinger／P2零，Unit loss167／300、兩方states仍active，耗盡不是正式勝利。逐ID／HP／ownership／template／weapon／官方loss核對。全局p9525.223145／p9951.855957ms、sim/wall.965297359，68個>50ms／max97.547852ms保留。帶擾動原門檻投影全局與第一60.012985秒窗performance FAIL；第二45.032366秒窗性能較好但joint／mixed activity FAIL，不由診斷取證PASS覆蓋。

16main＋2overview／70,473,117bytes、GUI20.015394秒terminal／sim18.6；1037markers、選定連續完整frames94–1129共1036、93strict sim turn0–92各1Timer。所有query共1180完整frame均掃描，98個合法float32負framegap保留。

**7914 strict 方法call／600個不同entity**：Timer5765／聯集1312.150885ms、simulation直接Flush2148／403entity／聯集650.821014ms、MotionPostMove1／.570001ms；全方法聯集1963.541900ms、單call p95.366／max1.044989。全部進入時currentState是 **INDIVIDUAL.WALKINGANDFIGHTING**，不是完整FSM歷史、trigger或未攻擊證明。seat／template映射只按初始fixture，不是attr當下owner／HP。

5309 strict舊label各含1方法（Timer3160／Flush2148／motion1），另2605 Timer方法call未被舊label包，全部保留。舊label不是全部方法call且兩site範圍不同；不能稱纯native query或指定唯一caller。marker外371方法call及345舊label保留；strict方法本場無boundary_label關係。5秒完整bin1872／1548／2055／2290，另149 GUI bracket不確定不硬歸bin。全部逐call、entity／state／parent／seat／template／turn／GUI統計在raw與results。

**最大Flush frame840／turn66 parent55.284001ms**、sim82.509ms，152call／152不同entity聯集48.145009ms，P1／P2 122／30、近／遠13／139、entry state WALKINGANDFIGHTING；GUI14.198421→14.294919秒。**最大Timer frame1004／turn81 parent46.660999ms**、sim59.236ms，134call／134entity聯集39.513992ms、P1／P2 114／20、近／遠45／89，GUI17.529802→17.600591。`maximum_case.wall_ms`是整體sim，不能當Timer／Flush值；用native parent bounds／fine scope。nested wall不加總，不稱CPU-exclusive／死亡份額／unique root。

93turn直接最大label Update67／Motion9／Flush17；全部17慢sim update中Flush12／Update5；30慢GUI是另一个集合。Health Death／Corpse各71call，同entity嵌套核對；15.032940秒／sim14.0快照loss41截止較早，不是帳差30或全場死亡數。whole frame max239.657998包含marker外邊界成本。病例完整逐call在 `work/t14-search-observability/same-sample-search-regions.json`。

## 回歸、審查與保留

事前59Python一般／-O各PASS（search9／fine11／native27／mixed12），1新JS suite包含fixture与官方Timer／Health／UnitAI／FSM及語義測試，9CLI拒絕PASS。首個boundary合成trace測試資料錯誤log保留，修正後才量測；官方Flush label／allframe掃描／zero-search maxTimer偏差也在量測前修正，有專屬回歸，不改gate救場。

PRE-RUN code review APPROVE＋41項前置鎖後才啟動。直接raw標準庫核算無import正式parser／runner／helper，一般/-O PASS一致；草稿由source代理撰寫，因使用量限制由主代理補完，另一code-review代理審查與執行，不假稱受限代理執行。全部7914／371方法、1180frame、1037marker、93turn、fine／fixture損失帳／窗口／clockbridge與最大病例核對；POST-RUNTIME APPROVE，無helper／runtime retry。正常／optimized audit、stdout與空stderr保留。

644份既有raw／evidence／rootprofiles、舊231、T13 129、callback151與新增243在closeout重核；43raw資料夾保留。無commit／push／刪檔／背景／排程，結束engine／runner／HTTP54677及前批ports皆退出，實際以closeout為準。

## 歷史判定不可覆蓋

原mixed no-profiler600有效FAIL；首profiler工具錯誤attempt PARTIAL與唯一工具retry診斷取證PASS；原不限FPS sim/wall、200重複性FAIL、soak首camera FAIL、過早啟動repeatability attempt FAIL、late計數與flight輸出FAIL全保留。fine与新search取證PASS不能補過原性能／活動门檻，非配對場不估overhead／因果改善。

單士兵battle、600地面移動30分鐘、雙AI單seed完整局、固定防守seed42／seed7與事前三同條件完整局仍僅各自限定PASS。雙AI分類損失差11未確立；soak熱unavailable，不證明熱穩定或無leak；cap60支持本機落後緩解，不證明頻率為唯一根因。飛行／AA／strike僅限定片段；正式空戰／返航／停機位、潛艇hidden／自動偵測前置未完成，不為效能擴功能。

## 下一步與限制

目前**新方法觀測限定PASS、原mixed FAIL、整體T14 PARTIAL**。根因／觸發message／native queue／完整cleanup仍Insufficient data；修復／overhead／正式勝負NOT RUN。

優先利用既有raw離線對照最大Flush與Timer的具體entity、native ancestry、舊label關係與固定R28 UnitAI／FSM搜尋呼叫路徑，核哪些最小既有dispatch方法能區分觸發訊息。不要因全部entry state相同就認定唯一callback或直接改AI。若要新scope，先repo寫清樣本／單一變因／控制／門檻／停止與工具retry契約，完成mock／相關回歸／獨立審查／來源鎖再量測；不可先包全部callbacks、增加人工Deinit、改C++、擴矩陣或重跑既有完成矩陣。

AI／戰鬥長壓、混合重複性、雙AI跨seed／重複性、熱頻率／GPU、多人跨硬體与精確空戰／返航／停機位／潛艇前置仍未驗收。持續更新progress／plan／journal／證據与新交接；所有局部FAIL／慢幀／raw保留，限定診斷取證PASS不等於完整遊戲性能。
