<!-- Purpose: Final bounded T12 AI contract and reproduction instructions. Created: 2026-09-27. -->
# T12 兩時代 AI 限定驗收

**限定 DONE**：官方 R28 macOS ARM64、`epoch_petra`、Frontier Duel 192 tiles、正常難度3、map／AI seed 42與7；AI自行經營、建造、研究鐵器及進攻固定防守方。不是通用策略AI或完整M5完成。[證據](evidence/t12-validation.md)。

## 固定條件

- 玩家1固定開局部隊 `standground`，不生產；玩家2使用 `epoch_petra`。双方 epoch 文明，6工人、2長矛兵、1市中心，F300/W250/S100/M0，人口8/20/100。
- 延用正常迷霧、M2模板與原生生產／研究／付款。五類初始採集速率直接核對；無額外資源、免費科技或cheat命令。CLI的CheatsEnabled設定不等於發出作弊命令。
- 攻勢採鐵器後的鐵刃步兵／投石兵；AI沿用Petra經濟、生產、尋路、攻防。觀測程式只固定防守方姿態、記錄正常命令前後的資源差額與引擎事件，不替AI下經營指令。
- 每局1800秒模擬時間上限。驗收地圖隔離，不改既有Duel或T05–T11驗收。

| 要求 | 最終證據 |
| --- | --- |
| 標準開局、AI身分與無採集加成 | 兩方資源、人口、身分及每方5種速率，16項 |
| 經濟 | food／wood／metal累計採集增加，工人生產完成與50F／人扣款 |
| 建造 | 房屋及兵營完工、50W／150W+50S扣款、房屋完工時人口容量高於初始20 |
| 升級 | 400F/200W/100M扣款，青銅／已完工兵營前置，ResearchFinished事件及至少60秒研究 |
| 進攻 | 鐵刃步兵完成及80F+40M／人扣款、attack或attack-walk命令、市中心扣血、AI勝利與對方敗北 |
| 執行 | 無cheat命令、1800秒內完成、程序exit0、無錯誤／警告、來源未變 |
| 重播及GUI | 兩seed完整suite重播一致、自然EOF；observer20×繁中GUI、基地／勝利／鐵刃HUD截圖 |

引擎suite共38項，其中37項延續原验收，新增1項房屋人口容量。38項不是38種策略能力；付款檢查證明至少一次符合成本的正常交易，不是全局財務形式驗證。

## 使用與重現

先依[基線](baseline.md)登錄Mod，關閉所有遊戲實例。在repo根執行：

```sh
/usr/bin/python3 tools/epoch-rts/t12-macos.py --app '../runtime/0 A.D..app' --seed 42
/usr/bin/python3 tools/epoch-rts/t12-macos.py --app '../runtime/0 A.D..app' --seed 7
/usr/bin/python3 tools/epoch-rts/t12-macos.py --app '../runtime/0 A.D..app' --seed 42 --visual --timeout 240
```

GUI為觀察者20×；地圖玩家2雖顯示 `Frontier Defender`，實際身分為AI。可用小地圖查看基地／戰場及點選單位；驗收結果寫出後用Cmd-Q正常退出。選取與鏡頭操作不替AI發出模擬指令。`visual_verified=false`是runner保留欄位，人工畫面驗收另記。

重播使用同一原始場的 `commands-0.txt` 與 `result.json`：

```sh
/usr/bin/python3 tools/epoch-rts/t12-macos.py --app '../runtime/0 A.D..app' --seed 42 --replay work/t12-validation/<run-id>/commands-0.txt --baseline work/t12-validation/<run-id>/result.json
python3 tools/epoch-rts/test-t12-tools.py
node tools/epoch-rts/test-t12-adapter.cjs
```

場次必須依序，遊戲日誌共用，勿平行啟動。公開版證據保留相對run_id及雜湊；原始日誌、重播及完整本機報告在忽略的 `work/t12-validation/`。其他主機需重新執行，不能只靠歷史檔案測試。

## 明確限制

- 只驗兩個seed、指定正常難度及平地固定防守；不承諾任意文明／地圖、不同難度／人格、AI對AI、Rush／Raid、海戰、空戰或潛艇。
- AI介面仍標experimental；未驗證設定選單、1×完整視窗對局、所有HUD功能及進攻中截圖。主動進攻與傷害由引擎事件證明，截圖證明勝利結果與單位呈現。
- 沒有逐回合全狀態hash、多人、存讀檔或效能認證；T13／T14仍TODO。AI的非序列化instance方法包裝需在T13另做還原相容性驗收。
- T11原創人物樣板未接入M2正式單位，本次畫面仍可見public暫用素材；不變更T11限定完成範圍。
