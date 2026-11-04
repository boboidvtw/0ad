<!-- Purpose: resume bounded T14 native CPU diagnostic with preserved failed capture. Created: 2026-10-04. -->
# 2026-10-04 T14 profiler 交接

Repo：`/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`。HEAD仍`726a3aefcae830f605de438cd13192cc6330414e`，index空，全部T14未commit。官方R28／既有Mod架構，不改C++或AI。本批engine／runner／127.0.0.1 profiler HTTP皆退出，未push／commit／刪檔／背景工作／排程。

優先讀本文件、progress／plan／journal、[契約](t14-mixed-profile.md)、[validation](evidence/t14-mixed-profile-validation.md)、[results](evidence/t14-mixed-profile-results.json)、[現行220來源](evidence/t14-mixed-profile-source-manifest.json)。再按需讀mixed、mixed-diagnosis及先前battle／soak／dual／match證據。下次先核實Git、runtime、來源與遺留程序，不只依此交接。

## 最新狀態

| 範圍 | 結果／限制 |
|---|---|
| 整體T14 | PARTIAL，原不限FPS simwall／200重複性FAIL保存 |
| no-profiler mixed600 | 有效實測FAIL：全局p99、第一窗口性能與第二窗口混合活動FAIL，不因本批取證PASS改寫 |
| 官方R28 GUI profiler binding／native region來源 | PASS，固定v0.28.0 commit `a2cae4d69f816e9e9d7eecb6bf88f762afc0c90d`，Git blob SHA1／SHA256驗證，不採local HEAD |
| profiler首場 | PARTIAL／取證失敗：parser同步基準工具錯誤、無completion；原檔保存 |
| 唯一profiler retry | 資料／coverage／早期活動限定PASS，具profiling／marker／GET擾動，不是性能修復或repeatability驗收 |
| 唯一根因／修復改善／overhead因果估值 | Insufficient data／NOT RUN |
| 熱與頻率／GPU／AI戰鬥長壓／雙AI跨seed與重複性／多人跨硬體／精確空戰返航停機位／潛艇前置機制 | NOT RUN，不為量測擴功能 |

既有單士兵battle、600移動30分鐘、雙AI難度3單seed、固定防守seed42／seed7完整局與事前3場同條件重複性皆各自限定PASS；原FAIL、soak camera首場FAIL、準備repeatability attempt FAIL、late計數／flight輸出FAIL均保留。雙AI分類損失帳差11原因仍未知。cap60只支持本機模擬落後緩解，不證明頻率平滑唯一根因。飛行／AA／strike仍各自片段，不是完整空戰。

## 本批原始證據

- 首場：`work/t14-performance/20261004T102121578227Z-mixed-profile-42`，只1份main query，2ns／1ns同步回退被parser high-water傳遞錯拒，無遊戲completion。`passed:false/status:PARTIAL`不改。
- 唯一retry：`work/t14-performance/20261004T103345111872Z-mixed-profile-42`。原600fixture，每席150 EpochMelee／150 Slinger，HP100／60、原生近遠程武器與Projectile；兩正常attack-walk，Seed42／AISeed42／無AI、平坦192、endless、sim0／cap60／1×、原camera與25設定。
- GUI wall105.068489秒／sim101.2，5616 intervals／22 snapshots／106 timing samples，首次P2耗盡收尾。末P1 Slinger133、P2全0；Unit loss167／300，states仍active，正式勝負NOT RUN。70個>50ms／max94.529053ms全保留。帶擾動p95 26.996094／p99 53.645020／ratio.963181263只作描述；不套no-profiler gate補PASS。
- 主trace GUI0→20.000755秒、terminalseq986／sim18.6秒，17main＋2overview、67,179,569 bytes；987精確marker／986連續完整frame／93sim updates，四組早期攻擊與原生timer推進gate PASS。UTC／monotonic HTTP和OS bracket、receive時間、source與raw hashes保存。
- camera起終 `(384,158.23118591308594,220)`／rotation `(.850006103515625,0)`／zoom180、bounds50–200一致。`visual_verified:false`，不是全部單位可見或逐tick驗證。

## 重要診斷與邊界

首frame94（native1.190588→1.411704006）跨sim0 marker1.293426002；末frame1079（21.294041→21.311672）跨terminal21.294191。whole frame max221.116006與progressive load102.926001包括marker前載入／邊界，不得稱純GUI0–20成本。額外strict-contained統計保留，不裁切raw；frame984／max85.640997，sim update93／p9562.862001／max74.334，render986／p956.810998／max53.406998，observer3／max3.528。whole observer4／max6.410003包含sim0前初始snapshot；whole render987源於首frame真正兩次render，不是dup。

選定8種native區段中，34個早期慢GUI區間有33個最大單一觀測交集為sim update、1為render；無慢區間與T14Observer重疊，不等於observer零成本或因果證明。最大sim update74.334ms／Flush Destroyed Components51.166001ms位於frame794、GUIseq701→702／14.044236→14.129803秒，parent `frame→sim update→Flush`，strict-contained，不能當pre-sim0載入或猜是哪個component／死亡造成。Sim - Update只包CMessageUpdate broadcast；outer update包含其他phase／cleanup／GC，不加總inclusive／不相減分位。

Limiter／wait無專屬label；main query region及CondenseBuffer未觀測，GPU timestamp關閉。residual不可命名等待或GPU時間。GUI epoch/native橋接只bounded enter／leave；type4 attribute沒有獨立timestamp，不聲稱精確同時計。103個來源有界跨frame負間隙與各capture重複觀測保存，其他倒序仍拒絕。

## 工具與保留

新增隔離profile harness6檔、runner／trace parser／3測試檔，共11新增；原209來源完全未改，現行220。本場measured集合122；原mixed128、battle200／measured128、soak191、dual182等manifest保留歷史，不能覆寫。

首場源碼和220manifest／契約／審查／回歸封存 `work/t14-profile-sources/first-attempt-tools`、`first-attempt-locks`，兩變更檔hash精確符合首場來源；首場manifest另存evidence attempt1。已證實工具錯誤後，僅在真sync chunk首依float32 halfULP＋9位JSON／binary64不確定度處理解碼，不改timestamp，不擴原玩法／負載／停止／coverage。唯一retry已用完，無第三場。

154項Python一般／-O各PASS、10份JS mock、8項CLI拒絕、39歷史raw精確重解析PASS。舊smoke stored passed:true但缺effectiveConfig、兩版皆拒絕的歷史差異不改。獨立代理不import正式parser／runner／helper直接raw核算PASS，含逐snapshot ID／HP／weapon／owner／template與官方損失帳，源碼審查及region邊界核對PASS。審查／raw獨立script／最大case／provenance／preflight／兩pre-run lock／closeout位於`work/t14-profile-sources`。

446份先前raw/evidence/profiles＋首場11檔 hashes、T13 129來源、主Mod與全部41raw資料夾相符。原profile.txt／profile2.jsonp與work/均保留，不刪除或提交；HEAD／index／退出狀態重新核對PASS。

## 下一步及續作限制

先離線縮小 **simulation update／CMessageUpdate broadcast／destruction queue** 候選：對照本場原生parent、turn／seq／活動與官方固定版，列出已有label能回答什麼、缺逐component／queue量／CPU-exclusive／GPU／OS同步的什麼，不把一次51ms queue等同根因。現有證據足夠定位範圍，尚不足支持具體修復；不靠擴跑或改C++救FAIL。

若需新量測，先在repo另立單一變因、合理對照／樣本數、相同map與AI seeds、實際負載／武器／HP／ownership、控制／畫面／camera、時長、活動／全局／每窗口門檻、比較／停止、失敗保存與工具retry邊界。完成工具回歸、獨立審查與source freeze後才啟動。不重跑已完成矩陣，不重寫AI／C++，不改武器或擴空戰／潛艇；本批profiling場不能事後改稱mixed性能PASS、正式勝利、重複性或戰鬥長壓。

持續更新progress／plan／journal／新證據及交接；不commit／push／刪檔／排程／背景工作。結束前確認engine／runner／HTTP退出，報PASS／PARTIAL／NOT RUN與實測、推論、Insufficient data。
