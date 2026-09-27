<!-- Purpose: Record complete local review scope, findings, fixes and limits. Created: 2026-09-27. -->
# T12 程式與工具審查

本機逐檔審查完成；未使用子代理，不宣稱獨立第三方審查。範圍包括adapter/data.json、3個map JSON、T12Validation.js、T12Probe.js、兩個runner及新增工具測試。依固定官方R28 public.zip原始檔核對；不是依repo舊public推測。

| 審查重點 | 發現／結論及證據 |
| --- | --- |
| AI隔離及授權 | import官方Petra，不複製整套AI或修改其prototype。GameState.applyCiv/phases及attackManager.update僅該實例覆寫；明拒非epoch文明。沿用GPL-2.0-or-later，无新依賴或網路服務。 |
| phase鏈 | R28 common-api/gamestate.js的currentPhase由已研究科技判定；明列青銅、鐵器，requirements經GetTechnologyBasicDataHelper取得；原M2科技400F/200W/100M、60秒及兵營前置未改。 |
| attack collections | R28 attackManager.js在update後段建立plan，下一輪才updatePreparation。wrapper於建立後、下輪準備前重映射。舊category集合unregister，新集合從同plan.unitCollection篩選並registerUpdates；buildOrders五欄引用符合attackPlan.js:273–280。保留總集合及metadata，不偽造CitizenSoldier。epochClasses避免每輪重建。 |
| 進攻限制 | Bronze只跳過進攻manager，HQ其他經濟／防禦流程不改。僅有MeleeInfantry的default／huge plan重映射；Rush／Raid不是本次能力保證，見限定契約。 |
| 付款與事件 | g_Commands包裝保留args及return；原生train/research/construct仍執行。立即資源差額配合完工／訓練事件；ResearchFinished.player/tech符合R28 TechnologyManager.js:120，非queue metadata推測。 |
| 人口驗收缺口（已修） | 原37項只有房屋完工；新增built.house-capacity及built事件人口上限。兩seed重跑各38項，房屋完工確實增加容量。 |
| framing缺口（已修） | 原parser忽略JSON解析失敗片段，可能把損壞額外frame略過。改parse_result嚴格驗證所有frame、數量／順序／型別、payload和checks/pass一致性；損壞回傳None，runner不得PASS。 |
| runner程序安全 | app版本、Mod symlink與既有遊戲進程檢查；subprocess參數列表無shell插值；超時只terminate/kill自己啟動的程序；使用唯一run目錄，不刪原始證據。exit0、suite、錯誤與來源均需通過；重播另需EOF及suite一致。 |
| source manifest | 記錄full Mod112檔及validation runner1檔，執行前後SHA核對；六場最終來源相同且与目前檔案一致。工具另存manifest。R28 binary/public.zip與既有官方基線同值。 |
| 探針邊界 | T12Probe僅觀測、每10秒輸出；1800秒前自然結束時complete=false是保守結果，不能宣稱定時觀測PASS。最終125個有效sample另支援官方Petra經營正向回歸。 |
| 共享日誌 | 兩runner禁止並行遊戲；interestinglog是輔助檢查，舊警告最多導致保守失敗。主要證據用各場stdout、結果及hash，不能用共用日誌替代其他場。 |
| 測試品質 | 8項Python測試涵蓋損壞／缺失／重複／亂序／錯型別／不一致PASS／空結果及5場舊log相容。Node測試檢查實例隔離、phase、Bronze gate、collection生命週期、buildOrders與重入；使用mock，不當作真引擎證明。 |

未對save/load、多人或全部Petra分支給出PASS。資料檔保留experimental及原調查期說明，能力與完成範圍以[t12-ai-acceptance.md](../t12-ai-acceptance.md)為準，AI選單呈現未納入此驗收。runner不是不可信log的安全沙盒；它解析自己啟動的固定引擎，不對外來任意JSON提供安全保證。

最終review後未改AI來源；只修觀測／解析器，全部受影響T12引擎、重播與GUI已補跑。T11 manifest105檔完全相同，T05–T11既有驗收不重做。測試來源及結果見[t12-tool-manifest.json](t12-tool-manifest.json)、[t12-tool-results.json](t12-tool-results.json)。
