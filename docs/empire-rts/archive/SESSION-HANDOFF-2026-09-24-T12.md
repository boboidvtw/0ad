<!-- Purpose: Preserve unfinished T12 implementation and verified evidence for the next session. Created: 2026-09-24. -->
# T12 接續交接

> 歷史檢查點，已由[2026-09-27收尾交接](SESSION-HANDOFF-2026-09-27-T12.md)取代。下列PARTIAL與37項為當時狀態；最終為38項限定DONE。

**T12 PARTIAL：實作與限定引擎／重播已通過，尚未完成證據整理、完整程式審查及正式收尾；不可標DONE。** 使用者要求切換session，先保留現有工作，不擴張到T13。最後核對日2026-09-24；HEAD仍是master `d372345`（T11）。本輪T12全部未commit／未push。

## 工作位置與邊界

- 真正repo：`/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`；聊天工作目錄不是repo。
- 官方R28 app：`../runtime/0 A.D..app`；Mod：`binaries/data/mods/epoch_rts`；沿用官方public.zip，勿用repo舊public。
- 接續前核對Git、progress與runtime。本輪末核對T11 manifest105個檔案全部相同；T10以前82個Mod檔未改，不重做T05–T11已完成限定验收。
- T11／M4僅原創低面數樣板DONE。T07即時防空／90m落地區、T08原生hidden攻擊問題與T16–T18 TODO限制不變。T13–T15未完成。

## 已實作

- `simulation/ai/epoch_petra/{data.json,_epochbot.js}`（相對Mod）：新增獨立可選AI，import官方R28 Petra，未複製整套AI、未改C++或public。
- 僅此AI的GameState映射 `{civ}`→epoch_rts，明列青銅／鐵器phase鏈；原M2模板未改。
- 包裝此AI的attackManager.update：鐵器完成才組織進攻；重新建立該plan的單位分類／collections，使用Swordsman與Slinger。沿用Petra經濟、資源佇列、生產、尋路與作戰；沒有把軍人偽裝為可採集CitizenSoldier。
- `maps/random/epoch_t12_{public_probe,epoch_probe,validation}.json`及`maps/scripts/epoch_rts/{T12Probe,T12Validation}.js`：隔離探針／驗收。正式驗收player2為AI，player1固定開局軍隊standground且不生產；正常指令付款，觀測程式不替AI做決策。
- `tools/epoch-rts/t12-probe-macos.py`：唯讀觀測runner；probe目前仍設定1800秒觀測，不能期待對局提早自然結束也有complete標記。
- `tools/epoch-rts/t12-macos.py`：正式驗收、重播、GUI runner。結果以短JSON chunk逐行輸出及重組，避免長行截斷。runner的visual_verified刻意為false，人工畫面證據需另記。

## 已驗證的固定來源場次

全部在 `work/t12-validation/`，每場包含result.json、source-manifest.json、engine.log及本機重播（原始場為commands-0.txt）。2026-09-24核對五份manifest完全相同，共113檔（fullMod112＋validation runner1），且與目前檔案符合。

| run_id | 實際結果 |
| --- | --- |
| 20260922T093246827695Z-validation-42 | seed42／AI seed42，37項PASS；884.6秒AI勝利，exit0，無錯誤／警告 |
| 20260922T093300612186Z-validation-7 | seed7／AI seed7，37項PASS；894.6秒AI勝利，exit0，無錯誤／警告 |
| 20260922T093319002362Z-validation-42 | seed42重播，完整suite相同、自然EOF／exit0 |
| 20260922T093340440180Z-validation-7 | seed7重播，完整suite相同、自然EOF／exit0 |
| 20260922T093404473733Z-validation-42 | 實際GUI，observer／20×／zh_TW；37項PASS、suite與seed42相同、exit0、無錯誤／警告 |

37項涵蓋雙方標準開局F300/W250/S100/M0、人口8/20/100、AI身分、五類採集速率無加成；food/wood/metal實際採集、房屋／兵營完工、工人／鐵刃步兵生產及正常付款；鐵器400F/200W/100M付款、兵營／青銅前置、至少60秒研究；主動進攻、市中心扣血、勝負、無cheat命令、1800秒上限。不是37種策略能力，未做全狀態hash／多人／存讀檔驗收。

GUI人工看過AI基地採集與農田、到達鐵器通知、勝利通知及投石兵／矛兵選取HUD。未截到鐵刃步兵HUD與進攻中的畫面；鐵刃生產由引擎事件證明。F2原始截圖在 `/Users/liyungchih/Library/Application Support/0ad/screenshots/`：

- screenshot0001.png：2026-09-22 17:34:57台北，AI基地。
- screenshot0002.png：17:35:30，勝利通知與敵方原市中心位置。
- screenshot0003.png：17:35:57，AI基地及投石兵HUD。

截圖尚未逐檔檢查／複製到repo evidence，正式GUI證據文件尚未完成。未宣稱1× GUI、完整UI操作或AI設定選單驗收。

## 調查與失敗紀錄

- 早期重播無cmd記錄，不能據此說AI不動；直接觀測證明原生Petra在官方文明及epoch均會採集／生產。最初t12-ai-preflight.md保留歷史調查，不是最新能力結論。
- 原生Petra與epoch的建築路徑、phase鏈、軍隊class不一致。局部映射後可升級但不出軍；編軍修正後可勝利，但可能未造鐵刃就贏，故固定本次「鐵器後鐵刃＋投石兵」進攻策略。
- 長單行JSON輸出被截斷，改短行chunk framing後可完整解析；不要回退到大字串一次print或未分行的片段拼接。曾嘗試空白padding，已移除；不是最終方案。
- GatherRates物件鍵順序不同曾造成比較誤判，最終逐項數值檢查，沒有降低數值要求。
- 所有中間失敗場留在work/t12-*；公開證據尚未整理，勿將歷史失敗結果當作最終結果。

## 下一session依序處理

1. 保留所有未提交變更，核對上述五場來源與結果；不要重做已完成調查或直接重寫AI。
2. 審查adapter與runner／驗收觀測程式，特別是attack plan collections重建、phase需求映射、研究完成事件、正常付款／錯誤處理與source manifest。尚未做獨立程式審查或完整工具測試；不宣稱已通過。若修改來源，只重跑受影響驗收並固定最終來源。
3. 補有意義的工具／parser驗證與必要相容性回歸，核對官方Petra未受影響。既有原生Petra正向觀測在work/t12-observed-probe/20260922T091903541560Z-public-42，但早於最終adapter來源，需明確區分。
4. 整理公開evidence/t12-*摘要、來源manifest、GUI截圖及失敗案例；如缺乏必要畫面，可用現有runner補GUI，避免覆寫／删除原始圖。將驗收草案定稿、更新progress／journal／使用說明，再決定T12能否限定DONE。
5. 清查Git。repo根的未追蹤profile.txt、profile2.jsonp是runtime產物，尚未處置，勿誤加入commit或刪除；可先核對來源再移至work。沒有其他人原有變更被覆寫。
6. 僅本機工作；不push、不安裝付費工具、不開背景排程。此交接未建立自動背景工作。2026-09-24核對沒有pyrogenesis進程。

重現範例（在repo根）：

```sh
/usr/bin/python3 tools/epoch-rts/t12-macos.py --app '../runtime/0 A.D..app' --seed 42
/usr/bin/python3 tools/epoch-rts/t12-macos.py --app '../runtime/0 A.D..app' --seed 7
/usr/bin/python3 tools/epoch-rts/t12-macos.py --app '../runtime/0 A.D..app' --seed 42 --visual --timeout 180
```

visual用observer20×，只代表加速視覺驗收。重播需同時提供`--replay <commands-0.txt>`與`--baseline <result.json>`。遊戲共用日誌，場次必須依序執行，不可平行啟動。
