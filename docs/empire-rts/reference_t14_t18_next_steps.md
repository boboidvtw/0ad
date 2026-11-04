<!-- Purpose: prioritized exact continuation after closeout. Date: 2026-11-04 Asia/Taipei. -->
# T14–T18 後續作業

第一個動作：讀 [收工交接](SESSION-CLOSEOUT-2026-11-04-T14-T18.md)與原機 canonical `work/t14-t18-session-transfer-20261026/current-checkpoint.json`；GitHub 只有 archival copy，入口在 `handoff-data/2026-11-04/latest-state.json`。不要從舊 handoff 的歷史 NEXT 重新開始。

| 優先序 | 必要工作 | 前提／完成證據 |
| --- | --- | --- |
| P0 必要 | 查 live ordinaryUsageAllowed、實際 Git HEAD/index/dirty，核未變更 exact d69d/fd1948 | 歷史 quota、HEAD、trusted JSON 不能取代當次實讀；保留既有工作 |
| P0 必要 | 接續 `/root/source_v2_python` 的 progress-v12 最後 joins／正式 JSON+MD | 同模型／設定／固定 packet；若舊 agent 不可用，必要新的獨立 Python reviewer 須先讀回完整進度並補足缺口。不得捏造或代簽；無 import/compile/tests/helpers/producer |
| P0 必要 | 根端完整驗 Python 正式報告，合併既有 CODE+JSAPI 核可 | exact manifest、113 physical/53 inner、完整內容、兩 digest、六 history joins、實際 reasoning/findings；舊 CODE/JSAPI 不重做 |
| P1 必要 | 全三方 SOURCE 核可後，才準備當次 physical-runtime-resource-owner/rootabsence 讀回、獨立 freshguard | 各 sampler 真實獨立、freshness／capsule joins／資源與owner符合，另一 root call 才能執行 |
| P1 必要 | 原固定 F01/F02-R/F02-W 三負向案例 | 僅原 v1/execution-v1、原IDs/order/caps/20s/120s/retry0/seedfalse；unexpected/UNKNOWN即停，保留partial，不換leaf／重試 |
| P2 必要 | 依原契約處理後續 coverage、metadata／save-load／GUI/network、T15 本機封包及T16–T18剩餘驗收 | 必要新有界契約／獨立審查／來源鎖／freshguard先行；不能升級source/model為native或official |
| P2 必要 | 若要合併遠端 master，先處理獨立交接分支與遠端差異 | 本次沒有merge/PR/force-push；保留本機652項原 dirty記錄及所有其他未提交工作 |

Quick reference：manifest SHA `d69d3456754b19f0592682824c4772c72d62169799fc9c02f0466d8291f951d4`；controller `fd1948d65cdd57cb851f651128639499f958a59f003707889bfb32e9f6f24e9b`；physical digest `f75394caf7e909cc6ccdd5817204d5e646b35f6e2a301c9375b95d441d84f184`；expanded `bcbb171acdda034552fc462203570edb9aad9d6726718d4446177b3b3f9ad104`。

永久保留：24 memory helpers 已耗用不可重跑／加；tiny bridge已耗用；T14 storage/parser/runner/dense/count/delta/offline/P144/382/T15reader51/package159等DONE不重跑。所有FAIL/STOP/UNKNOWN/raw/seals、T14 PARTIAL/SQLitecause Insufficient data、原600/6x90/30/80/cleanup90/42thenconditional7/retry0不改。無C++、未另授權的push/commit/發布/刪除/外部訊息/付費/reset/換model繞限。收工這次的push授權不等於未來無限push權限。既有0ad-t14每5h提供恢復機會，未變更或新建排程。
