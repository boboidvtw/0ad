<!-- Purpose: scoped T14–T18 session closeout and recovery explanation. Date: 2026-11-15 Asia/Taipei. -->
# T14–T18：2026-11-15 收工說明與接手紀錄

## 結論與收工範圍

整體仍為 **PARTIAL**。本次收工發布詳細文件與原樣文字證據，沒有新增遊戲功能、實作准入、native驗收或遊戲release。最新本機狀態為 metadata `current-checkpoint-v18.json`；公開對照見 [STATUS](handoff-data/2026-11-15/STATUS.json)、[證據包](handoff-data/2026-11-15/README.md)與[逐檔來源/bytes/SHA256](handoff-data/2026-11-15/FILES.json)。這份文件優先於11/12及更早快照的過時NEXT，原歷史內容與失敗不改寫。

| 項目 | 狀態 | 證據與限制 |
| --- | --- | --- |
| 11/14新session交接 | MATCH | 18原檔與18快照，共36 checks；Git HEAD/branch/index核對；child與父端收據保留 |
| 同id heartbeat移轉 | MATCH | 0ad-t14仍ACTIVE、每5小時、target本chat；本次收工未修改或新增排程 |
| 等不到報告的診斷 | 原因已定位 | 三原reviewer曾因usage-limit停止；排程移到新root後只檢查報告，原reviewer沒有自動續跑 |
| 使用者授權恢復 | 已實際執行 | 經原parent恢復同三thread/task/settings；新turn與新增progress可核，不開替代角色、不換model、不reset |
| Python DESIGN | 正式APPROVE_DESIGN_ONLY | JSON/MD已落盤，85/85本人全文，16項功能推理，findings0；後續turn再發生quotaerror不抹除已存在正式報告 |
| JS/API DESIGN | 正式APPROVE_DESIGN_ONLY | JSON/MD已落盤，85/85本人全文，12項功能推理，findings0，原turn完成 |
| CODE DESIGN | 正式交付BLOCKED | 原actor回報85/85與APPROVE_DESIGN_ONLY，唯讀環境不能落盤；正式JSON/MD仍缺，聊天內容不計核可 |
| 85-binding來源完整性 | 170 checks MATCH | 新正式報告出現後原檔與snapshot重新逐byte/SHA核對；hash不等全文閱讀或核可 |
| 新root親讀 | 3/85全文 | 本chat只親讀indices74/75/76（DESIGN/schema/futuretests）；前root85/85與13歷史全文只記繼承，不借名冒領 |
| 三方與implementation | NOT_ADMITTED | allThreeDesignApproved=false、implementationAdmitted=false；尚需正式CODE報告及root本人完整驗證與另source-scope |

## 時序、根因與教訓

1. 11/14新chat `01a1d802-8dc0-7b70-9bdc-f3c2f963d8f0` 完成exact交接讀回；父chat驗證後移轉既有heartbeat。原checkout仍HEAD `d5133455c3dffba7d2d3f2465f75b82532ebcd3d`、branch `codex/t14-t18-closeout-20261104`、index空，未靠清理既有dirty取得MATCH。
2. 使用者詢問久候無結果，live查得原parent idle，三reviewers最後於11/11約12:15台北usage-limit失敗，runtime為systemError。後來額度可用不代表失敗turn會自動恢復；讀取thread或輪詢磁碟也不會啟動產生報告的actor。前期以「等待有效變化」描述此情況不足，已明確更正。
3. 使用者明確同意傳訊原parent後，原三actors於11/14約11:15台北真實續作並寫新progress；約11:17再次usage-limit中止。active只證當時執行中，不能當完成；後續改為追蹤到正式交付或實際錯誤。
4. 11/14約16:35台北沿同授權恢復三原actors。Python與JS/API完成正式設計報告；parent與CODE再次usage-limit停止，Python正式檔在錯誤前已存在，不因turn失敗而重跑完成工作。
5. 11/14約21:37只恢復尚未完成的原CODE。它完成最後registry閱讀並回傳完整內容與設計結論，但原parent及CODE環境回報唯讀，無法建立正式檔案。此時根因已轉為權限/交付，不可繼續當作quota等待，更不能由新root代簽或重建正式核可。
6. 後續heartbeat只確認live quota、最新checkpoint及CODE檔案存在性；狀態不變不製造版本或重跑DONE項目。本次收工同樣保留該阻礙。

## 原角色、正式檔與歸屬

原parent為 `01a1ab0d-bce1-7f31-b9a9-33be9aaf3f6a`，題名「1105 | 功能 | T14–T18 接續與移轉核對」。原CODE `01a1ad19-e86c-72e1-aede-da700df4e484`；Python `01a1ad1a-1fe3-70f1-a10f-bc4706515125`；JS/API `01a1ad1a-585f-7dd2-8495-4f700a5037f7`。角色路徑分別為 `/root/r07_design_code_review`、`/root/r07_design_python_review`、`/root/r07_design_jsapi_review`。

[Python JSON](handoff-data/2026-11-15/metadata/design-review-Python-v1.json) / [MD](handoff-data/2026-11-15/metadata/design-review-Python-v1.md)；[JS/API JSON](handoff-data/2026-11-15/metadata/design-review-JSAPI-v1.json) / [MD](handoff-data/2026-11-15/metadata/design-review-JSAPI-v1.md)。SHA與存在性以STATUS/FILES為準。兩份JSON逐筆85索引、角色、manifest、readStatus及current/snapshot bytes/SHA已做結構核對；這不代替root完整實質內容准入。

exactmanifest為 `e73e6c48bd2a7ea31742aef7ad4b1744e6f28dbed799c39b28b25a3f9079b93a`，85bindings/1,447,275bytes。完整凍結文字已在繼承的[11/12資料包](handoff-data/2026-11-12/README.md)，本次只追加新進度/正式報告/收據，不修改舊freeze。原manifest內本機相對路徑保留，公開export路徑由FILES映射；文字source一律是歸檔，不能視為已安裝或已執行。

## 技術決策與仍未閉合的條件

- 正確因果順序是source在唯一Save前擷取獨立controls並編碼，host完整持久化controls與expected後才首次語意讀取本transaction actualmetadata。沒有杜撰host磁碟必須先於Save，也沒有actual→expected bootstrap。
- 新rawstage是未部署的prospective變更；不能把舊prearm或SOURCE核可自動延伸到新parser/producer。JSON binary64、bool/int、-0、duplicate/unknown/depth/caps、tuple/once/order、fsync/once-close/postclose readback與UNKNOWN/firsterror保留都需後續SOURCE驗證。
- 真GetValue camera、完整四欄有序mods、nativeprincipal與viewedcaller、GetInitAttributes完整transformation來源、clone/prototype/encoder/serialization/getter/mutator閉合、A/L0→controls→QO/QL→B/L1、actual40roots/noFutureSchedule、raw lifecycle及fullhost/R08仍不能由immutableJSON或hash自證。
- 同一D=t_arm+5s與outer600/6x90/30/80/cleanup90、42再conditional7/retry0不變。不得warmturn/flush/wait/第二Save或重設deadline；沒有證明native可在五秒內完成。

## 必須保留的原結果

T14仍PARTIAL，SQLite唯一根因仍Insufficient data；原runner/performance/tail活動FAIL、190slowframes與原raw/DB/journal不動。SOURCE-v2三正式核可與sampler/wrapper限定SOURCE DONE不重做。舊tinybridge R07與新metadata R07不同；24helpers已耗用，三正式faultcases仍NOT_RUN。

原fixedguard `afb3339b` 與79秒超60秒的readiness STOP保留；一次guard刷新/替換仍待使用者針對原具體方案決策。此次收工與push授權不構成該例外。十一metadata技術義務仍全部OPEN，19主任務14限定DONE/5未完，18工作包1文件DONE/17未完；不是遊戲完成百分比。

## GitHub發布與可關閉界線

使用者本輪明確授權收工、push與詳細文件。發布使用SSH origin `git@github.com:boboidvtw/0ad.git`，獨立branch `codex/t14-t18-closeout-20261115`，以先前checkpoint `fca88c4926574fc6403b0834a78744a504185763`為parent。以隔離index建立文件資料commit，不切換原checkout、不納入既有dirty產品source、不merge/master/forcepush。公開README EN/ZH、progress/plan/journal/CHANGELOG更新只在發布tree套用新增段落，本機原5份tracked dirty逐SHA保留；新收工文件與資料包另外建立。

驗證只涵蓋export bytes/SHA、JSON結構、報告角色與manifest、文件links、Git diff/commit/tree/遠端ref與保留狀態。Build/tests/helper/engine/native/case均NOT_RUN。本次沒有C++修改、新付費/reset/新排程、遊戲發布、全域memory或Codex-config同步。沒有虛構遊戲版本號；CHANGELOG記為有日期的文件快照。

可結束本次對話，但**不可刪除或當作可丟棄的完整專案**：原機work/raw/seals/runtime/privateprofiles與大量未提交實作仍只在本地；GitHub是限定文字歸檔，非完整備份。既有ACTIVE heartbeat仍可能喚醒此chat。未要求停用排程，因此本次不私自暫停；後續移轉或停用須明確處理。接手順序見[後續作業](reference_t14_t18_next_steps_20261115.md)。

## English closeout

This is a scoped documentation and exact-byte text-evidence closeout, not a game release or runtime acceptance. Python and JS/API have formal APPROVE_DESIGN_ONLY JSON/Markdown reports. The original CODE reviewer reports full reading and a design-only approval in chat, but its read-only environment prevented formal files. Three-way formal approval and implementation admission therefore remain false. Preserve all prior failures, consumed attempts, raw evidence and seals. Resume original CODE delivery in an authorized writable environment, then complete current-root personal verification and a separate source assignment. The original dirty checkout and active five-hour heartbeat are preserved; do not delete the local workspace.
