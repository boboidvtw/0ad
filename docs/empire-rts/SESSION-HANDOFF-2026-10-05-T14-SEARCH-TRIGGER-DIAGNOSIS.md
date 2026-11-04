<!-- Purpose: continuation checkpoint for bounded offline search trigger diagnosis. Created: 2026-10-05. -->
# T14 搜尋觸發路徑離線交接

Repo：`/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`

HEAD仍為`726a3aefcae830f605de438cd13192cc6330414e`，index空，T13限定DONE；T14仍PARTIAL，全部T14尚未commit。先查實際Git、progress、最新證據與engine／runner，不能只依本交接。

## 本批結果與界線

按[t14-search-trigger-diagnosis.md](t14-search-trigger-diagnosis.md)事前契約，僅離線核既有raw與官方來源；新runtime0、產品修改0。核算與獨立審查限定PASS。完整量化與來源見[evidence](evidence/t14-search-trigger-diagnosis-validation.md)、[results](evidence/t14-search-trigger-diagnosis-results.json)，原始逐turn／逐call在`work/t14-search-trigger-diagnosis/turn-results.json`。

- 全93turn、7914方法call、371外側call、2148 Flush搜尋均保留。44turn同時有Death／Flush搜尋，49turn兩者皆無；這是同場共現，不是因果或93場重複性。
- 71 Death scope全部在同turn Flush前；Flush搜尋entity與同turn Death entity交集0。2144 Flush call前後snapshot存活，4 call前存活後缺席，不能插值當下HP／死亡時間。
- 最大Flush frame840／turn66為55.284001ms，152搜尋entity聯集48.145009ms，與先前Death IDs204／514／570／734分離。前後快照152均存活，4 Death IDs後缺席。
- 所有parent同turn／同entity搜尋與Death配對只有兩例，皆Timer：348／turn46搜尋先於Death；288／turn81在Death19.221126002→19.221244999後，搜尋19.228147001→19.228416，Flush前。不能稱全部Timer搜尋為存活者，不能反寫288先搜尋後死。
- 官方DestroyEntity排隊、components至Flush才移除、未取消Timer可能繼續callback，使上述288時序來源上可行；其實際callback、入口HP與trigger仍未知。
- 官方Ownership→Resistance.OnOwnershipChanged→Attack.StopAttacking(TargetInvalidated)→UnitAI.ProcessMessage→FSM下一WalkAndFight訂單搜尋鏈，與Flush ancestry相容，但沒有實際target→attacker／reason／caller證據。根因Insufficient data。

首次離線工具把整場68慢GUI與trace30誤比的FAIL保留於`first-fail-*`；修正後兩集合分別保留。all-parent補齊前、queued-death解釋前與舊review版本保留，不覆寫歷史錯誤為已驗證。一般／-O與獨立raw核算須以最新review hashes為準。

## 來源、原場與保留

產品集合仍[evidence/t14-search-profile-source-manifest.json](evidence/t14-search-profile-source-manifest.json)的243檔；前場measured126，前231產品來源未改。本批離線來源另封[evidence/t14-search-trigger-diagnosis-source-manifest.json](evidence/t14-search-trigger-diagnosis-source-manifest.json)。官方v0.28.0 source commit為`a2cae4d69f816e9e9d7eecb6bf88f762afc0c90d`；binary SHA531981d016596b0abde110cd239feaed98998c3fdaa837d0fa8d6f75482c81ef，public.zip SHA ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429。21來源輸入／17歷史來源核對，674既有資料、search90鎖、T13 129來源及43raw資料夾保留。收尾以`work/t14-search-trigger-diagnosis/closeout.json`及evidence-lock為準。

前場raw `work/t14-performance/20261005T094516506020Z-search-profile-42`，600初始近遠各半、每方300、Seed42／AISeed42未參與（無AI）、flat192、cap60／1×／sim0／無暖機、endless、各一次attack-walk。GUI105.045351秒／sim101.4；16main＋2overview，7914方法＝Timer5765／Flush2148／Motion1，全部入口WALKINGANDFIGHTING。整場68慢幀保留；p9525.223145ms／p9951.855957ms／sim-wall.965297359；原gate投影全局與第一窗性能FAIL，第二窗混合活動FAIL。P1末端133Slinger／P2零，官方state仍active；軍隊耗盡不是正式勝利。camera起終相同、zoom180、visual_verified:false。詳[前批交接](SESSION-HANDOFF-2026-10-05-T14-SEARCH-PROFILE.md)。

原no-profiler混合FAIL、broad profiler首次工具PARTIAL與唯一retry、fine／search單場診斷限定PASS均保留；profiler不補過原FAIL、不證明擾動或修復效果。既有soldier battle、600移動soak、固定防守3場、雙AI單seed等僅各自限定PASS，原不限FPS／200重複性、late、flight、soak camera等FAIL不改。

## 下一步授權邊界

優先評估既有 **Resistance.OnOwnershipChanged** 單一wrapper，target entity與msg.from／to，加既有search scope，回答Flush invalid-owner handler的包含貢獻。候選、修復、overhead、正式胜負皆NOT RUN；這個候選不回答post-Death Timer 288路徑。

先在repo寫新事前單場契約：範圍理由／樣本數、初始與實際units／HP／owner／武器、mapseed／AIseed、控制／camera／畫面、時長、活動證據、全局／窗口門檻、比較／停止／FAIL保留與工具retry邊界。然後才最小工具調整、回歸、審查、source lock與必要本機量測。不得直接包全部callback、改AI／C++／玩法、擴跑矩陣。保留descriptor／this／arguments／return／throw／原Set iteration；不得複製／清空／重排Resistance.attackers或預掃攻擊者。記錄creation／transfer／death及非初始600（corpse／local／mirage等），不得把未知ID丟棄或判fixture FAIL。

混合／雙AI重複性、AI戰鬥長壓、熱／頻率／GPU、多人跨硬體、精確空戰／返航／停機位仍未驗收。潛艇缺自動偵測／hidden gate，不為測效能擴功能。不要重做T05–T13或無故重跑既有矩陣；不commit／push／刪profile或work／建立背景或排程。持續更新progress、plan、journal、證據與交接，結束確認engine／runner退出，分列PASS／PARTIAL／NOT RUN。
