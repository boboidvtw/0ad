<!-- Purpose: whole-project evidence assessment and ordered remaining work. Date: 2026-11-05 Asia/Taipei. -->
# 專案評估與剩餘任務計劃（2026-11-05）

**結論：目前19項主任務中，14項限定DONE、5項未完成；整體PARTIAL。** T00是規劃任務；若只計T01–T18，則為18項、13項限定DONE、同樣5項未完成。這是已定義任務的盤點，不是遊戲完成百分比。完整時代／文明／戰役／全套美術仍未定稿，無法估算整個長期遊戲還需多少工時或案例（Insufficient data）。

## 已完成的成果與實際邊界

| 主任務 | 已完成成果 | 驗收邊界 |
| --- | --- | --- |
| T00 | 目標、架構、規格、任務及追蹤入口 | 文件完成 |
| T01–T02 | 官方R28 ARM64基線、獨立Mod／地圖、引擎與GUI操作 | 只限既定平台與基線，不代表repo C++ Build已驗收 |
| T03–T06 | 青銅→鐵器／拓荒聯盟、採集建造訓練、科技HUD、作戰整局 | 一文明、兩時代、固定規則與腳本場景 |
| T07–T09 | 飛行／機場／防空原型、潛艇可行性調查、Mod-first決策 | 完整潛艇、精確彈道、多機停機另列T16–T18；未改C++ |
| T10–T11 | 靜態匯入、原創低面數工人／長矛兵／房屋／三圖示 | 樣板切片，不是全套正式美術 |
| T12 | 兩seed固定對手的兩時代AI經營與進攻 | 非通用AI／平衡保證 |
| T13 | 限定存讀檔及本Mac雙端loopback | 不自動涵蓋新海空機制、WAN或任意存檔 |

各項原始證據鏈見[進度主表](progress.md#任務主表)。本次讀回既有結論，未重跑舊驗收，也不聲稱重新審核每份歷史raw。

## 五項未完成任務的實況

| 任務 | 已經具備 | 尚缺／主要風險 |
| --- | --- | --- |
| T14 效能 | 多項有界性能、完整局、診斷與隔離storage/parser/runner接線 | 有效mixed／尾活動FAIL保留；新功能live交接、必要對照與回歸未驗收；SQLite唯一原因Insufficient data |
| T15 本機交付 | 可重現包、有限靜態檢查及離線transport/path reader | 原candidate42 formal FAIL；獨立安裝／GUI／save/network及完整closure未齊，非正式發行 |
| T16 專用攻擊 | 隔離元件、tests/source與部分原生觀察 | 海戰／death formal gates FAIL；seed7 STOP，不得改名重跑 |
| T17 潛艇 | controller/GUI/save來源切片；五mod capture joint SOURCE核可；tiny bridge兩case有界完成；fault controller三SOURCE核可 | GUI/native整合/save/network/fullhost/fullproducer缺項；過期guard STOP；三負向案例NOT_RUN |
| T18 彈道與停機位 | 精確彈道兩seed非圖像有界PASS；停機／GUI／transport來源工作 | GUI42、K42、protocol42與ownerGUI42失敗均保留；visual/parking/save/network未完成 |

## 最新已完成的來源與資料工作

- SOURCE-v2：manifest `d69d3456754b19f0592682824c4772c72d62169799fc9c02f0466d8291f951d4`；113 physical／165 logical／53 history。CODE、Python、JS/API正式APPROVE_SOURCE_ONLY且原根端已驗。舊「Python缺報告」只屬Nov4歷史快照。
- controller `fd1948d65cdd57cb851f651128639499f958a59f003707889bfb32e9f6f24e9b` 不變；24 memory helpers已耗用，不新增／重跑。
- sampler v5／wrapper v2為APPROVE_LIMITED_ORCHESTRATION_SOURCE_ONLY，尚未執行。
- 原freshguard約78.977秒後才進root，超age60而正確STOP；原SHA `afb3339b0471f8ecd857957c18752dafc291854e6cd4d54f9c5b6baf4d6257f5`保留。rootreport／capsule／EXEC仍未建立；3正式cases NOT_RUN。
- Nov5移轉13原檔＋13快照MATCH；既有0ad-t14由原chat完成同id移轉、ACTIVE每5h。本次不新建排程。

這些完成項目只證來源或資料範圍，不能代替runtime/native/GUI/save/network/official驗收。

## 剩餘工作包與順序

以下18個工作包是本次為五項未完成主任務整理的執行分解，**不是18個正式case**。case數量與工時須依各prospective contract決定；未知保留。先做R06唯讀對照，guard支線先等R01，其他原生工作須各自必要的新契約。

| ID | 所屬 | 工作包 | 現況 | 依賴／完成門檻 |
| --- | --- | --- | --- | --- |
| R01 | T17 | 一次 guard 重取樣明確決策 | PENDING_USER_DECISION | 無前置執行；原 guard、STOP、preimages 完整保留；僅原具體方案獲明確一次例外才可刷新；換 session／一般接續不代替例外。 |
| R02 | T17 | 原門檻 readiness 與 distinct admission | BLOCKED_DEPENDENCY | R01；同一已授權獨立 actor 可用；原 d69d/fd1948、113+53、runtime/resources/owner/absent-root 由各 actor 實讀；age≤60s、remaining≥120s、TTL120–600；任一 UNKNOWN 即停。 |
| R03 | T17 | F01／F02-R／F02-W 三個固定負向案例 | NOT_RUN | R02；原 v1/execution-v1、原 IDs/order/caps/retry0/seedfalse；另一次 root call；保存完整 outer exit/raw/FD-generation/partial/first-error；unexpected 即停後續。僅 injected-errno／手寫協定 models。 |
| R04 | T17 | 剩餘 coverage 與 limits 的具體驗收契約 | NEEDS_BOUNDED_CONTRACT | R03；以已完成 coverage reconciliation 為基礎，只處理未證的 sparse ZIP64、size/retention/RSS 等必要缺項；先確認哪些需實體量測，不能憑空新增 RSS 上限／stress 或重跑已 DONE tests。 |
| R05 | T17 | 完整 producer／五 mod inventory 與 caller 來源閉合 | SOURCE_GAPS_OPEN | R03；補足 actual producer/noProxy/full40、writer/export/intrinsic/child/native caller/clone/restore/consumer 與官方 archive 等原必要 gates；source-only 與 binary runtime compatibility 分開；未閉合不可 official capture。 |
| R06 | T17 | metadata 六欄與十一項缺口的跨計劃對照 | READY_READ_ONLY | 無前置執行；對既有 source-plan、唯一 JS DESIGN review、目前 host/control 契約作新執行計劃 crosswalk；指出 GetValue 修正、精確來源與待審／待實作／待量測；只完成對照，不重做舊 review 或升核可。 |
| R07 | T17 | metadata 獨立 expected controls 設計／實作核可 | BLOCKED_DEPENDENCY | R06；先完成必要完整設計審查，再限定實作、全來源審查；六欄、native getter、full initattrs mutation closure、precommit timing 與 future absence 必須獨立；禁止 actual metadata bootstrap。 |
| R08 | T17 | save host 完整來源與真實 consumer 閉合 | BLOCKED_DEPENDENCY | R05、R07；原 host full freeze BLOCK 不因 SOURCE_SCOPE 核可清除；producer/caller/realm/transport、loader、來源/runtime/original-copy/profile inventory locks 全部有明確證據。 |
| R09 | T17 | 新 save/load 契約及原生分支驗收 | NOT_RUN | R08；按原六 family／origin+fresh-load 分支與600/6×90/30/80/cleanup90等實際完整契約，42完整PASS才conditional7、retry0；L0零Advance、不得 warmturn/flush/多存檔或由actual值建立expected。 |
| R10 | T17 | owner/LOS GUI 與正常命令剩餘驗收 | NOT_RUN | R08；原 ownerGUI42 FAIL、zeroPNG、stdout0/backup27309 mismatch、seed7 STOP 不改；必要不同 GUI 問題先有新具體契約／完整審查與guard；不得重拍舊耗用場次。 |
| R11 | T17 | 新機制本機雙端同步驗收 | NOT_RUN | R09；兩個實際獨立 app/data/log/profile roots；正常網路命令、同turn native state/hash/events、無OOS；固定port/budget/seed/stop/retry先契約化；不得沿用T13 PASS。 |
| R12 | T16 | 專用攻擊檢查尚缺原生驗收 | PARTIAL_REQUIRES_DISTINCT_SCOPE | 無前置執行；原海戰42 36/221 FAIL、death42 121checks觀察但位置gate FAIL／seed7 STOP永久保留；先釐清仍缺 criterion、是否存在真正不同必要問題與新授權，無自動重跑原矩陣。 |
| R13 | T17 | 潛艇完整垂直切片整合收尾 | BLOCKED_DEPENDENCY | R09、R10、R11、R12；mode/2秒切換/深淺水/自動偵測/撤銷/所有權外交／正常命令與GUI及受影響回歸逐criterion合併；原 controller42 formal FAIL/145 observed 非正式PASS不改。 |
| R14 | T18 | 多機停機預約／排序／避碰剩餘驗收 | PARTIAL_REQUIRES_DISTINCT_SCOPE | 無前置執行；K42 malformed raw FAIL／seed7 STOP不改；必要新問題須先約geometry/physical/native motion與transport完整證據、budget/stop/retry與獨立review/guard；不重跑K42。 |
| R15 | T18 | 精確彈道 GUI 與共同 save/network 整合 | PARTIAL_REQUIRES_DISTINCT_SCOPE | R09、R11；原兩seed非圖像55requests/275turn/31HIT22MISS2REJECTED已DONE不重跑；GUI42/installation-drift/protocol42 FAIL保留，剩餘visual與serialization/network各自依新必要契約驗收。 |
| R16 | T14 | 必要新功能負載 live integration／效能回歸 | DEFERRED_UNTIL_CONCRETE_WORKLOAD | R13、R14、R15；只在新功能產生必要不同workload時建具體契約，可信producer/context/lifecycle及global/per-window gates分開；overhead須有效對照；原mixed/尾活動FAIL、190slowframes、SQLite Insufficient data不變。 |
| R17 | T15 | 本機兩時代候選剩餘安裝／runtime驗收 | PARTIAL_REQUIRES_DISTINCT_SCOPE | 無前置執行；已完成可重現包／159 package checks／51 reader checks不重跑；原candidate42 FAIL、28 observed非正式PASS、freshness未證保留；只處理不同必要未驗收的安裝/GUI/save/network與closure，不重跑原Duel42。T16–18 sandbox不默默混入core。 |
| R18 | T15 | 本機交付整合與最終證據／限制收尾 | BLOCKED_DEPENDENCY | R13、R14、R15、R16、R17；清楚分開兩時代core與特殊sandbox；逐檔payload/依賴/授權/安裝隔離與必要驗收有證據；T14 PARTIAL時不能稱完整品質發行DONE；公開遊戲發行仍需另授權。 |

## 目前執行選擇與停止條件

1. 先完成本次評估、主表修正、完整文字證據包與GitHub獨立分支讀回。保留master及所有未選scope的dirty工作。
2. 發布後接R06：讀既有完整source-plan與review，完成跨工作包對照及最小待審修正清單。R06完成只表示計劃可追溯，十一個技術缺口仍OPEN。
3. R01仍是[一次準備重取樣方案](handoff-data/2026-11-05/one-time-refresh-proposal.md)的同一待決策事項。一般「按計劃繼續」不推定為覆寫固定guard的具體例外；不放寬60秒、不增加retry、不換actor/model救PASS。
4. 任何SHA漂移、不完整寫入、UNKNOWN、資源或owner異常、既有leaf存在均停止依賴工作並保存；不自動重採樣／重試。
5. 未完成完整必要獨立review／當次來源與runtime鎖／freshguard，不做producer import、fixture、engine、case或native save。原已耗用正式FAIL不可改名重測。

## 資料、計數與恢復入口

- [機器可讀評估／18工作包](handoff-data/2026-11-05/ASSESSMENT.json)
- [完整文字證據包與限制](handoff-data/2026-11-05/README.md)
- [逐檔SHA／bytes](handoff-data/2026-11-05/FILES.json)
- [最新來源核可／STOP交接](SESSION-HANDOFF-2026-11-05-SOURCE-APPROVED-READINESS-STOP.md)
- [按計劃接續入口](reference_t14_t18_next_steps.md)

本次GitHub授權僅文件與資料更新，不是公開遊戲發行、遠端master合併、付費、刪除或C++修改授權。完整舊work/raw/seals、runtime與未提交實作仍須保留原機；GitHub資料包不構成可執行備份。
