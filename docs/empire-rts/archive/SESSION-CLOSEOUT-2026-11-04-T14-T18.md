<!-- Purpose: user-requested session closeout and GitHub handoff. Date: 2026-11-04 Asia/Taipei. -->
# T14–T18 收工交接：整體 PARTIAL

本次使用者明確要求「收工，並寫好交接文件和資料，且推上GitHub」。此授權僅用於本次文件／資料快照的 scoped commit/push；未授權新的 engine、案例重試、C++、發布版本或其他服務。既有未提交實作、原始證據與失敗記錄均保留。

| 項目 | 收工狀態 | 證據／限制 |
| --- | --- | --- |
| Nov2 session 移轉 | PASS，限移轉讀回 | 16 原檔＋16 快照 MATCH；既有 0ad-t14 移轉 receipt 保留，仍每5h，收工未修改排程 |
| SOURCE-v2 資料完整性 | MATCH，限資料 | 113 physical、165 logical、53 full-history；原 freeze SHA d69d3456754b19f0592682824c4772c72d62169799fc9c02f0466d8291f951d4 |
| CODE 獨立審查 | APPROVE_SOURCE_ONLY，根端已讀回 | 正式 JSON 191340 bytes／0fce6590b93571a4222072cfc4957e429b7b7531fc68d1aaa5aae8a995a1c001 |
| JS/API 獨立審查 | APPROVE_SOURCE_ONLY，根端已讀回 | 正式 JSON 439600 bytes／bb06b9e1e479941d4072ff1ebf217653bb3491a8481adc8ce8510307085588bc |
| Python 獨立審查 | PARTIAL：正式報告尚未建立 | progress-v12 已保存全文閱讀／剩餘 final joins；不得以進度或聊天文字冒充核可 |
| 三個正式 errno／protocol 案例 | NOT RUN／attempt NOT CREATED | 全三方核可、當次根端讀回、獨立 freshguard、另一 call 均未齊備 |
| 24 memory helpers | 已耗用；本輪未重跑 | 禁止重跑／新增；不等於 SOURCE/runtime 驗收 |
| T14 | PARTIAL | 原 SQLite cause：Insufficient data；原 FAIL/STOP/UNKNOWN/raw/seals 不改 |
| T15–T18 | 未完成 | 發行包、海戰／潛艇／精確彈道／停機位所需 native、GUI、save/network 與其他必要 gates 仍開放 |

## 入口與資料位置

- 本機 actual repo：`/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`；ChatGPT 專案 cwd 不是 repo。
- 本機 canonical checkpoint：`work/t14-t18-session-transfer-20261026/current-checkpoint.json`。
- [後續作業與開工第一步](reference_t14_t18_next_steps.md)。
- [GitHub 交接資料包](handoff-data/2026-11-04/README.md)及其逐檔 `FILES.json`。
- [完整進度](progress.md)、[計畫](plan.md)、[決策日誌](journal.md)。
- 本機收工前完整 preimages／原始 Git status／差異：`work/t14-t18-closeout-20261104/`。舊 transfer snapshots、seals 與 raw 不改。

資料包保留原 manifest、110 份文字 snapshot、完整 history container、兩份正式核可報告與 Python 進度、移轉16快照與 receipts、根端資料讀回及最新 checkpoint。三個 runtime binary 只記錄原 bytes/SHA，不上傳。這是有明確缺項的歸檔資料，不是113 binding全部可從GitHub恢復、可執行套件、全機備份或新的 runtime 證據。完整舊 work/raw/seal 資料仍在原機，不應因遠端有交接快照而刪除。

## 關鍵決策與踩坑

1. SOURCE 的完整閱讀、資料 SHA MATCH、memory models、正式 runtime 是不同層級；兩方核可不能取代缺少的 Python 正式報告。原 controller fd1948 未改，所有原 BLOCK／severity 留存。
2. 四個 historyFalse provenance rows 只引用原 immutable snapshots；tracking 更新前先保存完整 preimages，不用新版 tracking 取代當時來源。
3. Root 初次驗 JS/API 報告時曾遇 relative manifestpath 與 absolute reportpath 表示差異；修正的是根端路徑正規化比對，原觀察保留，未改來源、報告或任何案例結果。
4. 審查多次因 quota 中斷，依角色 versioned progress 續未讀內容，從未 reset、購買 credits 或換 model 繞限。最後兩個 reviewer 回週額度限制，既有正式報告已保存；本次收工不重新啟動 Python 審查。
5. 遠端 master 已是8d5ee7b4e54f224a231d481557d151d75a015503，本機原基準為726a3aefcae830f605de438cd13192cc6330414e。交接採獨立 `codex/t14-t18-closeout-20261104` 分支，不 force-push、不覆寫遠端 master，不把652項既有 dirty entries 全部提交。

## 發布與安全關閉判定

這次只提交明確列出的 README、tracking／handoff、後續清單與交接資料包。既有大量 source、profile、raw、未提交檔仍保留本機。GitHub push 成功以實際分支／commit 與本機 `work/t14-t18-closeout-20261104/push-receipt.json` 為準；資料包 checkpoint 是發布前快照，不自稱包含自身未來 commit SHA。

不能把整個 repo 判為 clean 或整個專案 DONE。交接完成後仍須保留原工作目錄；下一位依後續清單接續，不能重跑已耗用案例或清掉既有 dirty files。

## English handoff

This is a scoped documentation/data closeout, not a release or runtime approval. CODE and JS/API formally approve only the exact frozen source; the Python final report is missing. All three formal cases remain NOT RUN. The archive exports 110 text snapshots and preserves three binary identities as local-only requirements. Keep the original working directory, raw evidence, seals and intentional uncommitted work. Resume only the missing Python final joins/report and root validation before any separately gated campaign preparation.
