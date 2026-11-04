# Required fault controls — CODE DESIGN review: BLOCK

Purpose/date: 完整獨立設計審查，2026-10-28。Manifest `e488202701017b7a5c212bf3ad8cbf5ec43d4d8b00efb3ea2c8781615a668178`，55 primary/full snapshots、1794240bytes；全部依 physical nofollow、regular nlink1、size/hash/identity核對，需currentmatch的rows均符合。

[MEDIUM] DESIGN-CODE-F01 — pre-SOURCE focused tests 的授權邊界不明確

File: `required-fault-controls-preparation-v1/CONTRACT-v1.md:51`，另見第3行。依序列 focused tests 在 DESIGN/root readback 後、SOURCE freeze前；同段又說「No fixture/producer _run/import/test before these gates」，開頭也未授權test。test/import範圍與these gates所指未明確區分pure controller helper與producer/三固定consumedcases。嚴格讀法禁止必要focusedtests；寬鬆讀法可能提前允許producer import/case。這是設計gate歧義，未發現已發生未授權執行。作者chat意圖不是freeze內條款。

修法：用新normativefreeze明列，三DESIGN+rootreadback/獨立source scope後只允許哪些purehelper/AST/literal檢查，及若需要tinyhostfiles其專用範圍；明定inert controller import是否允許。producer import/_run、execution-v1固定case roots/fixtures與三consumedcases，必須留至完整freshSOURCE/rootreadback/freshguard/另行執行呼叫後；helpers不可消耗case或形成retry。原freeze不修改。

## 完整範圍

已讀55完整inputs與snapshots/current source/tests/normative base/terminal/preservation/enumeration/coverage/context。核對Deadline.io errno分類、Output reserve/write/onceclose與_run faultcleanup；rootFD+open-generation透明wrappers、未匹配syscalls原樣轉送、9byte真prefix後exception、controller evidence隔離、restore/firstprimary/UNKNOWN；bounded raw/ledger/tree/resource/deadline/finalization與fixedexclusivecaseorder/retry0。保留hiddenZipFile/iterator/nativeFD不可證明邊界。

完整三case oracle由獨立literal表純靜態重建：98byte BEGIN+ABORT、13layers/5selected/23bodycopies、paths/shadows/digest/captureId、SOURCE/CAPTURED/FAULT fieldorder與全stdout bytes/SHA、實際LF stderr、9byteinvalidJSON prefix、sentinel全部吻合；未producerimport/run或由actualmetadata生成。F01 SOURCE_TYPE/ARCHIVE_AND_SOURCES 與F02 ABORT_NODE_LIMIT/FINISH、durableFault=false均符合當前source，permission不是實OS權限證明。

未執行test/import/fixture/_run/Node/bridge/engine、未改source或frozenpacket。Implementation/source/actual3cases尚未核可；所有fullcoverage/native/fullhost/independentPythonwait/directionpipe/realpermission/largeZIP64/truebounds/RSS/official/GUI/save/network保持OPEN，舊FAIL/raw與acceptedtinyR07不升級。

## Review Summary

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | 0 | pass |
| HIGH | 0 | pass |
| MEDIUM | 1 | clarify before approval |
| LOW | 0 | pass |

Verdict: BLOCK — 凍結條款釐清helper與consumedcase的不同gates後重新review。
