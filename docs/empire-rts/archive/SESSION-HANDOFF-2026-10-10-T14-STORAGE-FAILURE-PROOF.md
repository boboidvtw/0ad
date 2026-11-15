<!-- Purpose: bounded synthetic failure candidate closeout handoff; Created: 2026-10-10. -->
# T14 storage failure preservation 候選有界 DONE／整體T14 PARTIAL

實際repo /Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad，HEAD726a3aefcae830f605de438cd13192cc6330414e/index空，T14未commit。用戶要求自主繼續做完、不逐步詢問；本批[契約](t14-storage-failure-proof.md)只做無engine的resource lifecycle候選與合成proof。[results](evidence/t14-storage-failure-proof-results.json)/[validation](evidence/t14-storage-failure-proof-validation.md)及work review/guard/proof/closeout/seal是目前狀態依據，不只依摘要。

新增3isolated tools（helper/只選6fixture的CLI/tests），原301逐hash不改/現304。22unit一般/-O與兩獨立review一般/-O PASS、code/Python APPROVE、source-lock312（SHA6c3b73b926a3ed82d22c3bc670902062a3e0de34f164220d88801b38c5d9e005）及guard17 PASS後另一call正式6CLI各一次/retry0，actual exits0/1/1/1/1/1，diagnostic assertions/readback皆PASS。connect失敗不body/close，body/close各保cause且不互蓋，report-write拒覆寫stderrJSON/exit1，partial與原sentinel全留；fixtures全fake，importsqlite只造exception，不connect。

本批attempt-record與6個attempt-*.json存在，正式proof已DONE，禁止換name再跑救PASS。原delta engine與完整offline attempt也皆已消耗/retry0，不重跑dense/count/delta/已DONEpipeline。不改C++/AI/玩法，不擴長壓/熱GPU/跨硬體/空戰潛艇/T05–T13矩陣，不丟unknown/noninitial/fullkeys/原gameplaycalls/同步順序/returnthrow。

原18seal對3tracking使用本批work/t14-storage-failure-proof/prior-state；原1114seal對3tracking仍使用上批work/t14-live-storage-assessment/prior-state，其餘原路徑。tracking-prior.json記hash/bytes/替代路徑。舊18/1114seal不改，新本批evidence-lock另存。準備checkpoint逐byte存work/handoff-before-closeout.md，不當現在啟動指令。初次Python BLOCK/2resolved findings、各階段review與22/19tests logs/fixtures全留。

原partial DB/journal/result/raw48與190slowframes保持；首次live runner FAIL/PARTIAL、性能p99100.786ms/simwall.897399與尾活動FAIL、T14整體PARTIAL。原SQLite唯一cause Insufficient data，synthetic FULL/IO與report sentinel拒覆寫不能推出原場原因。quantitative overhead/安全玩法修復/正式勝負NOT RUN。新helper未接live runner、body回傳不作parser acceptance，live integration NOT RUN；不聲稱原runner已修。

本次已授權的有界candidate工作完成後保持安靜，不加量測。未來不同實作須先新契約，live integration若做需隔離入口、保留原source、解析result/gates/returnthrow/nonzero/report-write與cleanup fault tests/獨立review/source-lock，不能把這6fake proof當live驗收；新engine量測還需確實授權與不同問題、sample/seed/fixture/camera/時長/比較/gates/獨立guard。既有heartbeat持續提供恢復機會，不買credits/reset券，不建重複排程/改頻率。無commit/push/delete/外部訊息。

本批收尾盤點helper誤把總控attempt-record算入fixture共7而FAIL，preservation.json原檔保留；精確核六scenario檔名+1總控後preservation-final.json PASS，原source/raw/6proof未失敗且未重跑。
