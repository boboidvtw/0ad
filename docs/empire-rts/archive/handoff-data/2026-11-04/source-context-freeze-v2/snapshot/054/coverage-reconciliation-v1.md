<!-- Purpose: current required coverage reconciliation only; Date: 2026-10-28. -->
# Coverage reconciliation — PARTIAL，尚不可直接 official capture

最小下一依賴是新的有限 REQUIRED-GAPS 契約／review packet，先補兩個最便宜的明確缺項：R09.1 的 EACCES permission negative、R09.2 的 fault.json 寫入失敗。不是重跑目前68／Node17／harness33，也不是再跑已完成 tiny R07。兩項通過仍不足以直接啟動 official3.5GB；R05.3 sparse ZIP64 與 R10 尚未完整的邊界／記憶體證據須另外定額、審查。

這次已實讀新 bridge outerexit0／兩 case PASS，以及 CODE postrun audit＋supplement `ACCEPT_BOUNDED_SOURCE_MODEL_CONFIG_ADAPTED_ONLY`、0 anomalies。它增加真正 Node→Python OS-pipe/main tiny capture＋collision：ZIP517bytes、13 layer rows、5selected、23bodycopies、33producerfiles／28artifact／4completed hashes。Python OSwait、獨立 directional pipe／fullhost 仍 OPEN。並未重新執行或重做 postrun audit。

| 範圍 | 目前證據／剩餘界線 |
|---|---|
| R02 | parent symlink、existing root、兩 thread 單 winner、所有固定 artifact OEXCL 已有；新增 current test724 的 barrier concurrent inventory sentinel 已實測，舊缺項清單不可照抄。 |
| R03 | heldFD replacement、uncached mutation、ABA、forged fstat、restore、immutable cache 已有 tiny physical＋injection（test23–42、363–371）。 |
| R04 | firstpass short/truncate、uncached truncate、interrupt、crosschunk/partial/EOF/seek 已有（test31–43、372–389）；source38 review補 reader／ZipFile source-path 審查。不是 fullhost syscall attestation。 |
| R05 | stored/deflated/CRC、small force_zip64 已有；**TEST-PLAN:58 明列 sparse>4GiB，仍 NOT_RUN**。64MiB central 僅 CENTRAL_MAX=1 model；部分不合法 ZIP 為 ZipInfo metadata model（test390–419）。 |
| R06 | leaf/ancestor symlink、原 loose bytes變動、directory enum變動、persistent root replacement已有（test271/285/420/472）；P09 validFINISH為本地手造 frame，不能冒稱真 Node race。 |
| R07 | tiny real integration/collision 已接受；unknownfields/digest/base64/decoder等有 current Python＋Node方法／VM controls。舊矩陣寫 Node未review／base64未測已過時。正向 tiny run不等於所有 badwire realpipe 已跑。 |
| R08 | current17含 pinned actualAcorn／UTF8/BOM／escaped-astral／fatalRangeError；14 schema groups仍多為手造 shape。fullproducer／writer semantics OPEN；不要求重跑 old7。priority/shadow fixedfixture已核，不冒稱 old localeCompare 與新 UTF8 sort普遍等價。 |
| R09 | shortwrite/fsync/close/ENOSPC partial已有；**permission、fault.json-writefailure仍缺**。child terminal/error/timeout/reap有 VM controls，真實負例 OS kill/reap仍未量，不能被此次健康／collision lifecycle代替。 |
| R10 | counts／bytes／frame／raw／schema／deadline大多scaled；真1024byte path、Node16384 synthetic rows已測。256KiB內部source＋stdlib trace最大可見payload64KiB、無 whole phaseA body，**不是 RSS／8–64MiB／archive-scale量測**。完整 limits 尚未證明。 |

JSON逐一對照全部54 base rows、14 schema groups、P01–P09／SourceFix與 exact test/source line，並綁定 core38、目前 source/test SHA、accepted audit／raw。既存68 normal／68-O／memorycompile PASS只讀保留，沒有匯入或執行測試。

建議後續有限 partitions（本文件不授權執行）：

1. **F01/F02 tiny faults**：各新固定exclusive fixture、payload≤1MiB；在真 producer output boundary注入EACCES，及既有 failure中只讓 fault.json reserve/write失敗。核 primary、durableFault=false、raw與sent同bytes、無健康completed、partial保留與close-once。這是 errno/protocol injection model，不是填滿磁碟或真 child失敗。
2. **Sparse ZIP64**：新 validZIP64，tiny entry但local/central offset跨4GiB；固定literalSHA/oracle、logical/allocated bytes各明記。fullSHA首pass仍須讀整個logical>4GiB，不能把 sparse 說成小I/O；先審查disk/RAM/600s/read-size預算，不碰official archive。
3. **實際大小／memory context**：先列尚缺limits ledger，再凍結真8388608／+1 file、67108864／+1 selected（含selected mod.json）、archive/lowerlayer>64MiB但selected<64MiB、all-five metadata8MiB／+1 的有限body表及完整output envelope。量測 phaseA/phaseB／cache／request／RSS context；不改production limit冒充true-size。central/count/frame/raw/analysis的其餘edge由新契約決定模型或physical如何滿足，不能默默升PASS。
4. 以上確認接受範圍後，另做 official candidate-only capture 的 source/runtime/archive/target/resources/currentownership/readback/freshguard及明確後續工具呼叫。不能沿用已消耗tiny guard／原FAIL，也不引入T14/native/fullhost新工作。

契約解讀：base TEST-PLAN仍必需；amendment:34／enumeration:23允許小實體或明標scaled controls，因此**不是每一最大上限都自動要求physical stress**。但模型也不能被稱為真64MiB/RSS量測。RSS義務是retention/request instrumentation與誠實context，沒有既定Python絕對RSS上限可憑空宣布。full40/noProxy/native caller／clone／restore／consumer／GUI/save/network仍OPEN，且scope addendum明確不把獨立Python descendant/fullhost observer當窄R07前提。

本次僅read-only reconciliation＋新增本JSON/MD，沒有implementation、tests、runtime、engine、archive copy、locks或attempt。
