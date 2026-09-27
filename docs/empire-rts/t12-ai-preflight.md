<!-- Purpose: T12 scope draft and initial handoff audit. Created: 2026-09-22. -->
# T12 AI 最小規格與初步調查

> 歷史調查紀錄，保留當時未知事項與失敗觀測。最新為[T12限定DONE證據](evidence/t12-validation.md)及[定稿契約](t12-ai-acceptance.md)；下列IN_PROGRESS／尚未驗收不是目前狀態。

**IN_PROGRESS：完成交接核對與初步探針，尚未完成AI接入或行為驗收。** 起點master `d372345`（T11），工作樹乾淨。T11／M4 DONE的範圍與限制不變。[核對資料](evidence/t12-preflight.json)。

## 限定驗收草案

沿用M2 epoch文明、青銅→鐵器、192 tiles平地雙人地圖、標準迷霧及人口上限100；每人6工人、2長矛兵、1市中心、F300/W250/S100/M0。AI使用正常命令，不由測試腳本代替決策，不額外發資源或免費科技。首輪對手為固定防守，不據此推論通用AI對戰能力。

| 項目 | 可觀察通過條件（尚未驗收） |
| --- | --- |
| 經營 | 自主分配工人，food／wood／metal實際累積採集量增加，正常付費訓練至少1工人 |
| 建造 | 自主完成至少1房屋與1兵營，核對扣款、施工及人口容量增加 |
| 升級 | 正常支付F400/W200/M100，滿足兵營／青銅前置，完成60秒鐵器研究 |
| 進攻 | 正常訓練鐵刃步兵，主動出兵並實際傷害敵方市中心；另記錄勝敗與時間 |
| 有界執行 | 候選每局上限1800秒模擬時間，超時記錄失敗及停滯原因；門檻需在正式驗收前固定 |
| 證據 | 固定Mod／AI／runner／runtime來源，map及AI seed各42／7；保存失敗局、事件、命令、重播及至少1場GUI；不宣稱完整狀態hash或多人同步 |

正式驗收前需固定對手配置、觀測方法與經濟倍率。T13／T14與完整美術不納入此契約。

## 核對與相容性

- 官方app `../runtime/0 A.D..app`版本0.28.0，binary及public.zip SHA-256與T11相同。105個T11 manifest檔全部符合，9d36013時的82個Mod檔與HEAD逐檔相同。沒有重跑T05–T11既有驗收。
- 實際R28 public.zip的 `simulation/ai/common-api/gamestate.js:33` 查找 `structures/{civ}/civil_centre`，166–168行直接置換文明代碼；文明為epoch，現有模板位於 `structures/epoch_rts/`。Petra headquarters對house、barracks、field、forge等有同類路徑假設。
- 現有 `phase_epoch_iron` 符合common-api的phase前綴篩選，不能誤判缺少前綴。完整phase鏈、class、Builder／Trainer白名單尚待逐項核對。
- 上述為靜態差異，未證明是runtime表現的根因，不足以決定重寫AI或修改C++。

## 探針結果與限制

原始資料在忽略目錄 `work/t12-petra-probe/`。所有場次受控終止exit -15，不是自然結束或勝利。

1. 首輪seed42／7至少100 turns、stdout無錯誤，未記錄重播，不作行為證據。
2. 第二輪 `20260922T004759Z` 固定map／AI seed42與7。重播header確認玩家2為Petra、difficulty3、balanced、epoch；stdout最後turn為3028／2553。兩份重播無 `cmd ` 記錄，stdout及interestinglog無錯誤／警告。
3. 僅官方public、mainland／athen／Petra對照局也無 `cmd ` 記錄。因此尚未建立有效的AI正向觀測，不能由命令缺席推斷epoch AI停擺，也不能由零錯誤判定相容。
4. CLI autostart啟用CheatsEnabled，本次未發cheat命令，difficulty經濟倍率未驗證。重播header的StartingResources／PopulationCap不是FrontierDuel trigger之後的狀態；stdout EPOCH_DUEL_INIT確認F300/W250/S100/M0及上限100。正式驗收需直接核對實際状态與倍率。
5. 本輪未執行重播、GUI或AI內部狀態／實體行為觀測，沒有AI能力PASS結果。公开摘要保存來源與日誌／重播雜湊；沒有修改Mod、上游public或C++。

## 下一步

先建立直接確認AI初始化、更新與經濟動作的觀測，使官方Petra對照局通過，再用相同方法重測epoch。定位模板路徑、phase鏈及class的實際影響後，比較局部Petra適配與獨立Mod AI的修改量及回歸成本，目前未選架構。完整兩seed行為驗收通過才能將T12標DONE。
