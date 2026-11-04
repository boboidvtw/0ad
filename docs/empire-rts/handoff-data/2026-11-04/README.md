<!-- Purpose: explain bounded public archival handoff and local-only gaps. Date: 2026-11-04. -->
# 交接資料包 / Archival handoff data

此目錄是發布前的歸檔資料快照，入口為[收工交接](../../SESSION-CLOSEOUT-2026-11-04-T14-T18.md)、[最新狀態](latest-state.json)及[逐檔索引](FILES.json)。逐檔 SHA-256/bytes 與原始來源路徑列在索引；索引本身不自雜湊。

包含原d69d SOURCE manifest、110份完整文字snapshots（含53個完整歷史body的container）、兩份正式CODE/JSAPI JSON+MD、Python最後進度、root讀回、Nov2移轉16快照與receipts。三份本機runtime binary未上傳，原SHA/bytes及缺項原因完整列在FILES。Python標準庫來源依原[Python license](PYTHON-LICENSE.txt)保留；本專案來源／原始碼歷史維持各自原授權，見repo LICENSE.txt及檔頭。

**不可聲稱全部113個實體binding可只靠此目錄恢復或執行。** 本機canonical路徑、官方runtime與所有舊work/raw/seals仍是必要資料；此處source paths保留原值，不因換路徑自動取得原核可。請保留原工作目錄。沒有執行任何封存來源、helper、producer或正式案例。

The archive exports exact text evidence, not three local runtime binaries or the complete historical work directory. Original paths and hashes are retained. CODE and JS/API are SOURCE-only approvals; the Python final report is absent. This is not a release, runtime proof, or complete machine backup. The checkpoint is captured before push; verify publication using the actual GitHub branch/commit and local push receipt.
