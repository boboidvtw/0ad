<!-- Purpose: user-authorized T14–T18 execution scope, dependencies and checkpoints; Created: 2026-10-11. -->
# T14–T18 自主執行計畫

用戶2026-10-11明確確認「全部」包含T15–T18，按依賴自主執行，不逐步詢問。此新授權涵蓋本機準備、Mod隔離新功能、tests/review/新有界runtime驗收及修正；不代表commit/push/外部發布／付費／刪檔／C++／任意新時代文明。每次新engine先完整具體contract、review/source-lock/獨立guard，不重跑已消耗T14設計，原FAIL/gates/raw/seals不改。額度不足寫checkpoint；沒有提供automation工具且CodexUI平台拒絕存取，無法讀回或修改既有0ad-t14，不能保證quota恢復時立即執行，不建重複排程／不買credits/reset券。

## 目標、假設與完成條件

先在隔離Mod sandboxes實作可驗收特殊機制，再作本機prototype發行準備。正式兩時代內容保持青銅→鐵器、現有文明，不把現代海空沙盒強塞入古代經濟。精確彈道必須真延遲彈道與實際HP，不能由instant-hit代替；潛艇要T16封閉攻擊入口後才上GUI/commands；C++僅按T09重開門檻比較，不能為複雜度直接更改。T14有效FAIL無法透過新功能PASS補過；若新功能負載需效能驗收另立不同具體契約，總體PARTIAL如實保留。

## 任務、依賴與順序

| 項目 | 依賴 | 本批DoD | 狀態／下一動作 |
| --- | --- | --- | --- |
| T16專用攻擊檢查 | T09§4／官方R28 | 隔離component/templates、入口與武器矩陣tests、兩seed真HP／事件重播／必要M1及受影響回歸、審查／來源鎖／證據 | IN_PROGRESS：官方API/source查核、事前契約及實作 |
| T17潛艇最小切片 | T16 | 2秒切換／停火、深度安全、自動偵測與撤銷、所有權／外交、commands/GUI、兩seed、存讀檔／loopback／新feature負載掛接 | TODO：T16後實作；T08手動探針不升格 |
| T18精確彈道與停機位 | T09，可獨立source準備 | 分拆真彈道命中／移動目標／命中時gate與多機預約／排序／避碰，兩seed有界runtime，GUI與必要回歸 | PREPARATION：官方source與分拆契約 |
| T15本機發行準備 | T09/T11–T14、T16–T18結果與邊界 | 既有兩時代core明示allowlist、runtime依賴、資產來源署名、本機可重現包與乾淨安裝／啟動驗收、已知問題／scope，公開發布NOT AUTHORIZED | PREPARATION：清單／文件，可先靜態驗證；最後封包驗收 |
| T14必要後續 | 前批真live缺口盤點、新feature問題 | 保留原FAIL與190slowframes；在真正新feature有界workload必要時接可信live producer/context/lifecycle與完整runtimeevidence，量化overhead僅具有效對照時成立 | PARTIAL：舊dense/count/delta/offline不再執行 |

## 工作清單

- [x] 使用者確認T15–T18納入，自主本機執行。
- [x] 讀主表、T09/T08、官方R28既有工具／模板、封存README修正。
- [x] T16／T15／T18狹義子任務依AGENTS分派，檔案所有權分離。
- [ ] T16 source/runtime固定、實作/tests先行、code review、guard、真engine矩陣、修正、封存。
- [ ] T17 state/controller/commands/GUI与整合驗收。
- [ ] T18分拆實作與runtime驗收。
- [ ] 必要T14新feature負載／live接線驗收，保留NOT RUN與有效FAIL。
- [ ] T15可重現本機發行包、安裝驗收、文件／授權／已知限制。
- [ ] 更新各scope results/validation、主表、journal／handoff、hash與最終狀態。

## 驗證與checkpoint

先tests後新正式runtime；source-only／JS mocks／realengine／GUI／save-load／loopback／性能分開報。每必要criterion有實際證據才DONE；validFAIL保留，不弱化測試，不換name救PASS。工具bug最多事前限定一次修正retry，記原FAIL/source/contract與修正理由；同策略兩次失敗換假說／停止，不盲重跑。舊307/311產品逐列保留，新T16–T18放新harness，原profiles與raw不刪。

三tracking本次版先逐byte存在work/t16-attack-contract/prior-state，精確mapping见tracking-prior.json。將來核前批29seal三tracking用此prior-state；舊7207仍用live-integration-gap-assessment/prior-state，舊4991/669/18/1114替代依原交接，其餘原路徑。舊seal不改。所有source、未完問題、attempt狀態／中止原因留repo，quota不足先保存，不聲稱背景自動執行。
