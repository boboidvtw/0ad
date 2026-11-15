<!-- Purpose: independent complete CODE DESIGN history-context representation review. Date: 2026-10-30 Asia/Taipei. -->
# CODE DESIGN review — APPROVE_DESIGN_ONLY

Exact manifest `20e7e2e53967afdce38b7b594c8cedab0e83cbd9aec61fb7af09e5a24a6b914e`。沒有新的 DESIGN finding；僅核可這份明確提出的 full-byte 歷史表示方式。

獨立實讀／核對94個原件/effective inputs＋94 full snapshots（3,409,262 bytes）、舊68a60的126 full snapshots/effective inputs（2,988,296 bytes），另逐一實讀53個 whitelist 原檔。全數 bytes/SHA MATCH；未用 author/root readback 或舊摘要替代。每項 path/bytes/SHA 與三組完整readback均在同名JSON。

獨立 streamed data arithmetic 重算53 entries：decoded1,042,748 bytes、base64 payload1,390,392、canonical encoded1,408,405、預測SHA `2caa72716cb1ac21e4c9163ce6ca2461851fc71ba0381f785a04515d5c18ce74`，全部吻合。沒有建立實體 bundle、validator 或執行來源。

128 physical bindings／32 MiB encoded snapshots 上限不變；138 logical 仍明示138，53完整歷史body變一個physicalcontainer只使physical成86。153logical／101physical僅包含15個未來檔案的reservation，未知bytes仍須新freeze重新實測。沒有以摘要、reference、dedup或漏body降低數量。53固定白名單與64個f597必備direct contexts、currentcontroller/helper/plans/interface均無交集，三個未選historysource仍direct。

契約要求canonicalASCII/keyorder、全部duplicate/BOM/nonfinite/UTF8/trailing/type拒絕、strictbase64重編相等、逐entry大小/SHA/fulloriginalbytes、2MiBencoded／1MiBdecoded／256KiBentry／64entries／depth4及配置前界限。Schema明示不足以單獨保證語意，必須完整semanticchecks；不解包或執行歷史source。完整encodedbody算入32MiB，decoded另報。

未來SOURCE-v2必須將physicaldigest、expandedlogicaldigest、containerSHA/counts/schema/inventory與全per-inner讀回連至完整三方SOURCE reports、root、freshguard和capsule/admission/postreadback。新interface及report-v2路徑保留v1BLOCK；沒有trustedtag捷徑或current-only hash取代decode。實作尚未開始，DESIGN核可不等於舊loader已支援。

原356c／68a60仍三方SOURCE BLOCK、三個unique defects未修，原severities/raw/preimages/seals保持。24controls DONE，不重跑或加新。沒有import/compile/test/helper/producer/observer/probe/fixture/guard/attempt/engine；sourceApproval=false、campaignApproved=false、native=false。

## Review Summary

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | 0 | pass |
| HIGH | 0 | pass |
| MEDIUM | 0 | pass |
| LOW | 0 | pass |

Verdict: APPROVE_DESIGN_ONLY — 仍需全部exact三方DESIGN與root gates後另行授權source-only實作；actualSOURCE與case gates尚未核可。
