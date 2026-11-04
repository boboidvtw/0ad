<!-- Purpose: continuation after source-only native-query boundary feasibility. Created: 2026-10-06. -->
# T14 Query Mod 層觀測可行性交接

Repo `/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`。核實際Git/progress/diff/R28/runtime來源/鎖/退出，不能僅依交接。HEAD726a3aefcae830f605de438cd13192cc6330414e/index空；T13限定DONE，T14仍PARTIAL，全部T14未commit。

按[t14-query-observability事前契約](t14-query-observability.md)只核官方固定commit binding/loader，新增runtime0／產品修改0。詳[validation](evidence/t14-query-observability-validation.md)、[results](evidence/t14-query-observability-results.json)，source/provenance/review/closeout/lock見work/t14-query-observability。

最小候選原prototype ResetActiveQuery wrapper被來源flags排除：ICmpRangeManager→InterfaceScripted→Wrap defaults ENUMERATE|READONLY|PERMANENT，JS_InitClass安裝prototype，cachednativeinstance/QueryInterface保身份，GetPrivate讀this reservedslot。預期descriptor是来源支持推論，runtime descriptor/loader NOT RUN。own shadow／Proxy／QueryInterface全局改寫不視為保留原descriptor／物件身份；不宣稱全部Mod替代方法絕對不可能。不複製UnitAI實作，不改C++。直接候選REJECTED，查核限定PASS，不等於新observer PASS。

本批新增5官方binding來源；既有5份來源與固定commit上游逐byte再核，installed UnitAI byte吻合。任何binding timing含conversion與observer，parent減inner union非純filter/order/exclusiveCPU。

前批1有效profiler遊戲strict2148Flush search/403entity，同handler與同turn跨handlerentity重複0，最大107=107及152=152；不證無所有冗餘、不做去重。原no-profiler mixed FAIL／所有歴史FAIL／前批Resistance流程attempt1 FAIL與唯一retry用完均保留。entity288先Death再Timer搜尋再Flush未解，唯一根因/修復仍Insufficient data，修復效果/overhead/正式勝負NOT RUN。

2026-10-08接續已完成legacy artifact核對：有效raw27檔沒有legacyprofile，根profile.txt224 snapshot/77query列且宣告Sep26，runner/result root_profiles_unchanged:true；不是本場逐callquerydata，不混用平均legacy與profiler2。成本仍Insufficient data。相關既有JS wrapper suite、Python9一般/9-O測試PASS，原生descriptor/loader實測NOT RUN。本批沒有新遊戲或observer。

剩餘工作：精確query成本、caller/reason/唯一根因及修復沒有足夠依據；不得再跑被flags排除的原prototype替換。另選writable JS觀測須具体不同問題與新事前契約，回歸/review/lock/guard通過才runtime；不擴矩陣、不改C++/玩法。來源可行性與legacy查核已完成，不重做同一離線批。

保留產品256／measured128／T13_129／674/809資料／raw45／profile.txt/profile2.jsonp/work；前批71穩定鎖不含live progress/plan/journal，新mutable更新以prior/final-state與review SHA追蹤，歷史manifest不改。官方R28 binary531981d016596b0abde110cd239feaed98998c3fdaa837d0fa8d6f75482c81ef/public ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429。退出／ports／鎖以本批seal為準。無commit/push/刪檔/背景/排程，不重做T05–T13或擴空戰/潛艇；重複性／長壓／GPU熱頻率／跨硬體等仍未驗收。持續更新progress/plan/journal/evidence/交接。
