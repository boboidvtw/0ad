<!-- Purpose: reviewable DESIGN ONLY repair for archive/input integrity and exclusive output capture. Created: 2026-10-25 Asia/Taipei. -->
# Five-mod inventory capture repair — DESIGN ONLY

本契約只修 a6d26 的 archive authority 與 output freshness/containment。CODE 2M、JS 1H1M 與所有原反例保留，不覆寫原 tool/test/manifest。未實作、未測新程式、未核可 source/native closure。Root 同意方案方向仍須完整獨立 CODE+Python（Node protocol 另 JS）DESIGN review，正式核可後才能分工實作。

## 固定範圍與分工

新增 `tools/epoch-rts/t17-save-five-mod-capture.py` 由 Python author 負責：stdlib archive/FD/authreader/output/protocol 与其專用測試。新增 `tools/epoch-rts/t17-save-five-mod-source-inventory-v2.cjs` 由本作者負責：原 Acorn AST semantics 的必要 copy、strict UTF8、NDJSON orchestration、其專用測試。舊 source 不改；沒有依賴安裝/自寫 ZIP parser/新 native component。Python 的 runtime ZIP parser 是 stdlib zipfile，必須綁本機實際 Python 版本與 zipfile/hashlib/io/json/os 原碼或可核依賴資訊；缺平台 nofollow/dirfd/pread/ZIP64 支援就 BLOCK，無降級。

唯一 candidate stack：public archive → epoch_rts → epoch_t16_harness → epoch_t17_save_harness → epoch_t17_save_allocation_witness。四 loose roots 與 default direct-child JS folders、固定 map JS/JSON/mod.json 完全沿原契約。所有層的 mod.json 作 input metadata 保存；最高 sameVFS source 勝出、shadowed來源完整保存。map/final GUI bytes bind ec8c8a23d79b7f6e4fce11230b4a6f25a5c89861d2518a3a3de0b3522408e885（06a9已 SOURCE-only 雙核可）；actual map/RMS/runtime 未測。不是 native VFS solver：implicit engine/user/rdata mount、DELETED、loose/archive/order/mtime/profile/startup/jobs/hotload 等仍 unsupported/OPEN。

## Archive authority：同 FD、一次串流、每次 authenticated return

Python 用逐個 physical parent 的 directory FD + O_DIRECTORY|O_NOFOLLOW 打開來源；archive leaf 用 O_RDONLY|O_NOFOLLOW，fstat regular file。來源 path 是 AUDIT authority 的既定絕對 path，expected SHA 固定 ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429；正式 production caller 不可傳別的 expected hash/path。測試可在 private module harness 傳 synthetic FD/expected digest，CLI 不暴露改 authority 選項。已知原 zip 3,508,827,314 bytes；不整檔 readall/copy、無 unzip pathname reopen。

持有同一 archive FD 至 terminal。第一次用固定 4MiB chunk 順序 pread 全檔，更新完整 SHA256 與每 chunk SHA256；expected full SHA 不符、短讀、大小/metadata identity 變動即 terminal BLOCK。chunk table 在 Python 私有記憶體，不接 Node 提供。full digest 把此 pass 的有序 chunk sequence 綁到權威 bytes；後續不以 mtime 或 inode 相同當內容證明。

ZipFile 僅接 private seekable AuthenticatedReader：read/seek/tell/readinto 全部讀取都走同 adapter（若實作不需要 readinto 可不提供；不能 fallback raw FD）。每個欲傳回的 range 必先以 pread 取得其涵蓋完整 chunk 的 immutable bytes，核 chunk SHA，再從此同一 bytes slice 回傳；至多 cache 一個已核 chunk。cache 是已驗 immutable 原 bytes，可安全重用，不是重新讀被改過的 FD。跨 chunk read 逐塊驗後才組合，任何 chunk 不符不得把該次 read 的部分 bytes 回 ZipFile。seek負值/越界、未知whence、不合理 read size 都 BLOCK；EOF只允許已知 size 邊界的正常0bytes，chunk內短讀禁止。全檔與table不匹配不可重建 table 救通過。

archive pathname 改指別檔不影響 held FD；candidate authority 明確指「驗證過的持有 FD bytes」，不宣稱 pathname 此刻仍同檔。若 held FD 被原地改動，未cache chunk 必須逐次驗；A→B→A 中間若 parser 收到任何 B bytes 就必驗失敗，若已回原 A 再讀則只會回 authority A bytes。解析、列舉、entry extraction、CRC 都不得有 raw/path reopen bypass。ZIP64 使用 zipfile 原生支援；不實作新 ZIP64 parser。Zip centraldir read 超 LIMITS 上限即 BLOCK，不能為限制放行篡改內容。zipfile 的 metadata/entry buffers 另有上限，4MiB cache不等於程序總RAM只有4MiB。

ZIP directory entry 可先僅移除一個標準末尾 `/` 再檢查；regular entry 不作此正規化。ZIP entry 名拒 absolute、空段/`.`/`..`、NUL、backslash、drive/colon、重複完整 path、symlink/nonregular類型（directory entry可列舉但不能作source）。候選檔只取固定 direct folders/map/metadata，不 extractall。ZIP64有效小樣本與 >4GiB sparse synthetic archive測記必區分：可在limits下接受ZIP64，正式3.5GB首pass只在新source核可後有界 capture，不能假測真archive改動。

## Loose source 與 candidate snapshot

Python 同樣以 parent/leaf nofollow FD capture loose source，對每個 selected 固定 path 讀完整 immutable bytes後計 SHA；單檔8MiB/合計64MiB、fstat before/after（含size/dev/ino/mtime_ns/ctime_ns）。同一 capture session 保存 layer inputs與selected snapshots；全候選層 enumeration、所有mod.json與shadowed metadata也有bytes/count上限，metadata overlimit不省略而BLOCK。不能 Node 重新讀 path 然後套舊 SHA。FINISH 前對 retained loose source FD 重新讀/核 digest與 metadata，變化即 BLOCK；已有 immutable captured bytes仍保留。這證每個 snapshot 的捕獲 bytes，不證所有不同檔於同一瞬間存在、也不證 native mounted VFS。enumeration 的根/dir/層 metadata source-inputs 一併保留；symlink/異常file type BLOCK，無recursivefollow。來源變動即本次停止，沒有 retry或第二快照偽裝第一次。

## Output：單程序持有 physical anchor，所有 writes exclusive

正式 CLI 只收 outputLeaf，ASCII `[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}`，不收任意 output path。parent 固定 NEW repair prep 的 `captures/`；由核可工具逐個 component nofollow 開 physical directory chain，若固定 captures 尚不存在只可相對已持FD以單層 mkdir建立。程式不得 recursive mkdir 或 follow ancestor symlink。最後 outputLeaf 以 nonrecursive mkdir 原子取得，EEXIST一律 BLOCK；不把舊目錄當新輸出。

mkdir 後 openat leaf O_DIRECTORY|O_NOFOLLOW，核 stat/fstat dev/ino/mode/owner，持 rootFD到結束。每個內部子dir從 held parentFD以 mkdir+nofollow open 建立，不從外部拼完整path開檔。每個 artifact 僅 O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW mode0600；每個 dir0700，拒特殊檔與同名既有項，無 truncate/rename-replace/append覆寫。依 fixed filename set exclusive write、處理短寫、flush/fsync/file fstat，completed最後寫並fsyncroot。Node永不 fs.writeFile/mkdir/unzip，stdout/stderr不做authoritative artifact落盤；Python owns protocol raw logs及所有 snapshots/analysis/manifest/fault。測試 harness 本身的 raw證據必使用同等新目錄 exclusive規則，不能修工具同時覆原case。

phase開始、每次artifact前、COMPLETED前核 root/parent anchor 與預期 path 的 nofollow identity，不符即停止。保證是 OS dirfd object anchoring + exclusive nooverwrite，不能誇稱能禁止另一同UID process任意rename/retarget整個namespace。任意敵對同UID可於check/write間rename已開dir，檢查無法原子鎖整條樹；本工具沒有 sandbox/OS lease，故「保持邏輯path一直在prep」依 cooperating namespace/no concurrent ancestor relocation 的明確前提。若此 threat 必須無條件防止，需額外OS隔離而非再做前後realpath假保證。本次設計對既有 symlink/preflight/concurrentfile-root scenarios 保證不follow、不覆寫；可偵測的替換/rename BLOCK，未偵測競態不能冒充完整 containment證據。

## 證據與 fault 語義

所有 source、raw protocol、失敗/部分 JSON 保留，不 delete/unlink/rename cleanup、不retry。closeFD/terminate-child是資源清理，不刪證據。正常 terminal須 child COMPLETED frame+exit0+exclusive completed.json內容digest一致；單有exit0或檔案存在都不算完成。timeout/EOF/kill/closeerror/fsyncerror/半檔/協定錯誤皆 BLOCK或UNKNOWN，不補寫 healthy completed。若 fault證據無法落盤，保留已有partial、stderr只報固定code與phase，不能聲稱 durable fault已存；Node同樣不能繞過Python寫fault。timeout固定600s，Node停止依賴與終止child無重啟；必要 reap一次，無盲目重試。

接受成功名稱僅 CAPTURE_COMPLETE_CANDIDATE_ONLY；sourceClosure=false、native=false固定由Python寫入，Node不得改。AST parse/UTF8 fail可產完整capture但狀態 CAPTURE_COMPLETE_WITH_ANALYSIS_BLOCKS，逐檔reason保留，絕不變sourcePASS。完整 CODE+Python+JS source reviews、current full freeze 後才允許新有界真capture；不能用設計approval觸 engine/activation。

Design-fix-v1 amendment: machine exact FINISH tagged unions and source-dependent relationships now live in ANALYSIS-SCHEMA.json/SOURCE-RELATIONS.json. These supersede only the original incomplete analysis field list. Unknown source semantics are retained OPEN. Shared JS/Python 1H schema finding is addressed for independent re-review, not self-approved.

Design-fix-v2 preserves original analyzer producer: topLevel variable name is raw source but function name decoded Identifier.name. functions.name/context ordered branch semantics are frozen in NAME-PRODUCERS.json; no source implementation or semantics changes. Prior a1e159 CODE1M and both approvals remain historical and do not approve this new freeze.
