<!-- Purpose: T06 actual combat, boundary and standard match evidence. Created: 2026-09-11. -->
# T06 作戰與標準完整對局驗收

**T06 C01–C05 PASS，M2 兩時代最小流程完成。** 完成範圍限定以下案例；不代表通用 AI、多人或正式產品完成。

## 環境與範圍

- 開始版本 `8d5ee7b4e54f224a231d481557d151d75a015503`；開始時 Git clean，本機與遠端 master 一致。
- 固定官方 Release 28／0.28.0 macOS ARM64，沿用 epoch_rts 0.3.0。讀取實際 public.zip 的 Attack、Resistance、Health、Player、EndGameManager、Conquest 與 ConquestCommon；沒有修改 C++、正式戰鬥元件或既有 T05 程式。
- 新增 T06 專用 maps、Trigger 驗收及本機 runner。完整流程與邊界 fixture 分開；來源見 [manifest](t06-source-manifest.json)。未新增依賴或素材。
- 2026-09-10：seed 42／7 各 8 場、191 斷言全部通過；8 場重播共 134 斷言通過。所有場次 0 錯誤／0 警告。完整原始輸出留在本機 work，公開結果見 [引擎報告](t06-engine-results.json)。

## 實測結果

| 案例 | 操作與結果 | 證據限制 |
| --- | --- | --- |
| C01 | 四單位的 HP、傷害類型、射程、500 ms 準備／1000 或 1500 ms 週期、抵抗均符合 v0.2；六建築 HP／抵抗正確且無攻擊；四單位無捕獲、Promotion、Bonus、Splash。使用正常 attack 指令：12 秒內三近戰各命中建築 12 次，投石命中 8 次；傷害符合 `damage × 0.9^resistance` | 數值為實際解析元件與引擎扣血，非平衡性或效能測試 |
| C02 | 敵方唯一中心毀滅後 P1 won、P2 defeated；事前建立的房屋及原始工人仍活著。己方中心毀滅或正常 resign 指令均 P1 defeated、P2 won；每場僅一勝一敗事件 | 致命傷／房屋由隔離 fixture 注入，非整局；剩餘實體依 R28 轉 Gaia |
| C03 | 同一回合依序對兩中心施加致命傷，再 flush 銷毀。順序 1→2 時 P2 won；2→1 時 P1 won；兩中心均已不存在。一次勝利／一次失敗，兩 seed 與重播一致 | 沿用 R28 銷毀與玩家狀態處理順序，不新增平手模式 |
| C03 研究 | 已付費、排隊且開始研究鐵器，進度已前進；開始約 59 秒時摧毀中心。科技未完成、研究佇列清空、F400/W200/M100 全額退回，僅一次勝負事件 | 遊戲在勝負後停止；不把終局後未運行的額外回合標為測過 |
| C04 | seed 42 由 F300/W250/S100/M0、8/20（上限100）、青銅開局，正常採集、建兵營、訓練、付費研究鐵器、建鍛造所、鍛造兵器、訓練六鐵刃步兵、攻擊移動到敵基地並摧毀中心，649.8 秒勝利 | 玩家由測試腳本發正常指令；不加資源、不免費研究、不加單位、不直接傷害。GUI 與重播證據另列 |
| C05 | seed 7 相同主要流程在 621 秒勝利 | 對手只有原始 6 工人與 2 長矛兵，standground 固定防守，不經營經濟；不是 T12 AI |

完整流程的攻擊移動會先消滅守方工人與部隊；本次兩整局勝利時守方工人均為 0。C02 另以保留工人／房屋的獨立案例驗證「中心毀滅即結束」，不將兩者混為同一證據。

| 標準流程里程碑（模擬秒） | seed 42 | seed 7 |
| --- | --- | --- |
| 完工兵營、工人訓練至12名 | 91 | 91 |
| 投石兵已訓練、支付鐵器 | 197 | 184 |
| 鐵器完成 | 257 | 244 |
| 鍛造所完工 | 319 | 303 |
| 支付鍛造兵器 | 320 | 304 |
| 鍛造完成 | 350 | 334 |
| 六名鐵刃步兵完成、進軍 | 574 | 546 |
| 敵中心摧毀、勝利 | 649.8 | 621 |

## 重播一致性

兩 seed 的 double12、double21、research、full 均讀取原始 commands.txt 跑到 EOF，exit 0 並輸出 Final state；完整 suite（案例、實際值、預期值、事件順序、步驟與時間）與原場次完全相等。Runner 核對 map／seed／mode，遇到 MISMATCH 即失敗，不能用其他 replay 冒充指定案例。

**這些無畫面 autostart 記錄沒有 hash 行，`hash_checks_ok=0`。** 本次證明事件與結果可重現，不宣稱逐回合全狀態 hash、跨平台確定性、存讀檔或多人同步完成。

## GUI 證據

- 2026-09-10 原始標準視窗場次：gameSpeed=1，seed 42，649.8 秒勝利；exit 0，日誌 0 錯誤／0 警告。已保存 [採集與兵營建造](t06-standard-economy.jpg)。原始結果的 `visual_verified=false` 保留，工具自動報告不替代人工畫面觀察。
- 2026-09-11 從該原始場次進行視覺重播，補取畫面。重播檢視可調速，與原始 1× 對局分開記錄。[重播 1× 狀態](t06-replay-speed-1x.jpg)。
- 已保存 [鐵器經濟與訓練](t06-replay-iron-economy.jpg)、[勝利通知與重播結束](t06-replay-victory.jpg)、[敵中心毀滅及選取鐵刃步兵](t06-replay-centre-destroyed.jpg)、[10:50 勝負摘要](t06-replay-summary.jpg)。摘要玩家1為勝者花環，玩家2為敗者骷髏；鐵刃步兵 140/140 HP。
- 重播以 1×、2×、5× 檢視，到達終點後 Command-Q 正常退出，exit 0、0 錯誤／0 警告，完整 suite 與原始視窗場次相同。[視覺驗收摘要](t06-visual-validation.json)。
- 沒有另存研究完成瞬間或正在交戰的截圖；戰鬥扣血依 C01 引擎證據，終局畫面直接證明勝負與軍隊存活。後期截圖明確屬於視覺重播，不冒充原始現場截圖。

## 可重現操作

在 repo 執行，先關閉其他 0 A.D. 實例以避免共用日誌互相覆寫：

```sh
python3 tools/epoch-rts/t06-macos.py --app '/path/to/0 A.D..app' --mode combat --seed 42
python3 tools/epoch-rts/t06-macos.py --app '/path/to/0 A.D..app' --mode full --seed 7
python3 tools/epoch-rts/t06-macos.py --app '/path/to/0 A.D..app' --mode full --seed 42 --visual --timeout 1100
```

`--mode` 支援 combat、victory、defeat、resign、double12、double21、research、full。重播必須提供 `--replay /path/to/commands.txt --baseline /path/to/original/result.json` 並使用相同 mode／seed；加 `--visual` 為視覺重播。只有 full 是標準資源對局，其餘為隔離測試。正常玩家遊玩仍使用原有 `launch-macos.sh duel`。

## 本次修正與驗證邊界

- 初版勝負後延遲輸出，無畫面引擎已先退出；改在實際勝負回呼／flush 後取得終局結果。
- 初版直接攻擊迷霧中的敵中心無法前進，改用正常 attack-walk，保留戰爭迷霧。
- 資源快照改為值複製，避免歷史步驟被後續庫存值覆寫。
- 程式審查補強研究開始／扣款／進度斷言與重播 EOF／metadata／MISMATCH／baseline 比對；複查通過。初版失敗保留在本機，未當作 PASS 證據。
- T05 未重做；未修改共享玩法，故未重跑 T04／T05。T07–T15、一般經濟 AI、多人、存讀檔、效能、正式美術仍未驗收。
