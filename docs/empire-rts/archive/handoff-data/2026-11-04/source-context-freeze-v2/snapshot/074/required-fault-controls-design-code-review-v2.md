# Required fault controls v2 — APPROVE_DESIGN_ONLY

Purpose/date: fresh 完整獨立 CODE DESIGN review，2026-10-29。

Freeze `f597e8d5c5bcf214ccb6a74d7e0920914441c3dece4b6851aa895a5c4607b2d4` /64full primary、2061637 snapshot bytes。CONTRACT-v2 `8afebe343e3529236e775f9e8cbab214fc67ed419a2f7bb2a25364b242c1eef6`；原oracle `c29ae4c2b9cdd74d2ad9fde92c4867aea3921a07f6b77475ba28d854cb45c271`。需currentmatch的全部rows與64snapshot均符合，physicalnofollow/regularnlink1/size/hash/identity已核；每筆與provenance列JSON。

沒有新finding。原v1 helper/producer gate歧義由本freeze規範解決：StageA僅設計；StageB須三DESIGN+rootphysicalreadback+另行sourceassignment，先靜態檢查才准inertcontrollerimport，只允許preregistered至多24memory-only assertions/20秒、每input1MiB/aggregate8MiB；禁止producer、observer、runtimeprobe、hostfixture、eval/exec與campaignroot。StageC仍須fresh完整三SOURCE、rootruntime/resource/ownership/absence readback、independentfreshguard及distinctcall，才可建立原fixture與執行三consumedcases。

## 完整範圍

已審完整64normative/current source/tests/oldv1三報告與rootcloseout/context，而非只驗一finding。currentd687/e710/schema280及不變producerinterfaces與完整oldnormative條款，對errno分類、wire/raw/faultcleanup、FD-generation透明open/writeobserver、onceclose/restore/UNKNOWN、9byte真write後EACCES、firstprimary/evidence、caps/deadlines/resources與可實作性逐項核對。新source實際實作與所有sourcegates仍待獨立審查。

完整三case literaloracle重新以純文件資料重建核對：BEGIN+ABORT98bytes、13layers/5selected/23bodycopies、fixedpaths/shadows/digest/captureId、全SOURCE/CAPTURED/FAULT fieldorder/rawbytes/SHA、實際LFstderr、9byteinvalidJSON prefix及sentinel均MATCH。這是靜態設計資料完整性驗證，不是StageB helper執行。原preparation-v1/execution-v1 namespace與三caseorder/retry0/caps不變，v2 executionroot明禁；兩個namespace本次均ENOENT。

## 邊界

僅 APPROVE_DESIGN_ONLY，未授權或執行implementation/import/test/fixture/producer/engine/bridge。StageB另行准入與StageC全部SOURCE/guard/call條件不得以此報告替代。原v1BLOCK/oldFAIL/raw/seals、consumedtinyR07不變；實OSpermission、independentPythonwait/directionpipe/fullhost/fullproducer/largeZIP64/truebounds/RSS/official/native/GUI/save/freshload/profile保持OPEN。

## Review Summary

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | 0 | pass |
| HIGH | 0 | pass |
| MEDIUM | 0 | pass |
| LOW | 0 | pass |

Verdict: APPROVE_DESIGN_ONLY — 不是source或campaign核可。
