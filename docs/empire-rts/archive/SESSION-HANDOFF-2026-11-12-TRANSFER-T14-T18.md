<!-- Purpose: durable local session transfer for T14–T18. Date: 2026-11-12 Asia/Taipei. -->
# T14–T18 新 session 接續

Actual repo /Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad。使用者明確要求換新session繼續。先live get_usage_limits，再完整讀本交接與work/t14-t18-session-transfer-20261112/current-state.json；逐驗每binding original+snapshot SHA/bytes及HEAD/branch/index空後，僅新增child-readback.json，不改anchor。父chat讀回MATCH後移轉唯一既有0ad-t14同id ACTIVE每5h，不新建排程。

最新metadata checkpoint v11，root-independent-read-progress-v5是舊根端已讀64/85、partial0、unread21的閱讀紀錄，不是三方核可或新根端個人閱讀。新根端必明確標示繼承與本人閱讀，不借用64當自己親讀，亦不重做已DONE source review/tests。新根端可續獨立root source review，但不得替代原三role簽署。餘indices：6,13,14,15,17,18,24,45,48,49,68,69,70,71,72,73,78,79,80,81,82；各自完整範圍見progress，不以hash或index代全文。

三原metadata DESIGN reviewers仍只在更早父chat01a1ab0d-bce1-7f31-b9a9-33be9aaf3f6a：/root/r07_design_code_review、/root/r07_design_python_review、/root/r07_design_jsapi_review。最新CODEv10=69full/16unread、Pythonv6=78full/1partial/6unread、JSAPIv13=68full/1partial/16unread，三正式JSON/MD均不存在。原quota error保留，不假定跨chat可操控，不為quota重開替代reviewers/model。全85 manifest e73e6c48bd2a7ea31742aef7ad4b1744e6f28dbed799c39b28b25a3f9079b93a，85bindings/1447275bytes原檔與freeze不改。

三正式完整DESIGN核可後，root仍必本人實讀驗角色/manifest/85coverage/findings/functional reasoning，另獨立source-scope准入才實作。未齊不得authoredimport/compile/tests/helpers/profile/producer/probe/fixture/guard/attempt/engine。完整Nov6handoff/Nov5assessment/R06crosswalk/原canonical/contracts仍必讀，尚未完成的歷史全文閱讀不能宣稱完成。

Root目前已記錄但未定案的整合問題：camera Update用real time且該路徑無pause gate；setter fixed量化/FocusHeight可調Y，不能nominal值作expected。host prearm strict_json/same與metadata binary64/-0語意不同。current GUI實際只有SAVE_CALL/REQUEST_READY等raw，SAVE_RETURN是request.callOrder marker並無獨立emit；新reader不得捏造原rawstage。這些是已讀source觀察/待釐清，未單憑局部判BLOCK或改設計。完整推理見root progress。

R06更正：controls來源因果capture必Save前；host controls/expected落盤與readback必current actual metadata首次語意讀前，原文未必host disk先Save。historical更強preimage保留。新controls所有工作仍原t_arm+5秒及outercaps內，不延deadline/wait/warmturn/flush/多Save/重試，不用actual bootstrap。

SOURCE-v2三SOURCE核可及sampler/wrapper限定SOURCE保留不重做。原fixedguard afb3339b與約79秒超60 STOP不變；一次guard刷新/固定檔替換仍待具體人類決策，不重採/重寫，不建立rootreport/capsule/EXEC/attempt，三正式cases NOT_RUN。24helpers耗用，全部原FAIL/STOP/UNKNOWN/raw/seals保留，T14 PARTIAL/SQLite Insufficient data。metadata十一技術義務全部OPEN；19主task14限定DONE/5未完、18工作包R06文件DONE/17未完；舊tiny bridge R07 DONE不可與新metadata R07混淆。

只本機：無C++/commit/push/delete/外部訊息發布/付費/reset/credits/換model/新排程。Git object用GIT_NO_LAZY_FETCH=1 GIT_ALLOW_PROTOCOL=。額度不足只保存versioned checkpoint等同一5h排程；狀態無變且無可行必要工作安靜。
