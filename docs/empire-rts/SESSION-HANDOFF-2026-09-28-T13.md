<!-- Purpose: Exact continuation checkpoint for the T13 closeout. Created: 2026-09-28. -->
# T13 Session 交接

Repo：`/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`

先核對Git、progress與官方R28 runtime，再讀本文件及 `evidence/t13-validation.md`、`evidence/t13-results.json`。交接起點為`46045f8bfe9029951066821ffcf648ca93ff1584`（T12本機提交，未push）。2026-09-29已依使用者授權完成T13本機提交；提交識別以包含本次收尾紀錄的commit為準，其父提交為46045f8。

## 驗收決策

T12已限定DONE。T13從這個提交接續；使用者於2026-09-28明確核可「載入狀態完全還原、AI功能續局通過、雙客戶端同步通過」作為限定驗收，不要求讀檔後每一步與不中斷場完全相同。原生athen/Petra對照也有終局差異；保留相關失敗，不把它寫成重現一致或已定位上游根因。

目前兩seed、三時點的原生存讀檔矩陣已全數通過，8場各38項T12功能檢查。兩場真實雙客戶端對局與原生full／quick hash審計均通過，最終seed7涵蓋研究佇列觀測與雙端關閉順序修正。T13已限定DONE，所有驗證程序正常結束，無背景任務。

## 變更範圍

- 主Mod只修正 `maps/scripts/epoch_rts/T12Validation.js`：付款wrapper在每次指令查詢目前Trigger，避免原生load後引用舊實例。沒改AI決策／資源／C++。
- `tools/epoch-rts/t13-harness/`：opt-in測試Mod，原生SaveGame／StartSavedGame、列明狀態快照、雙端指令與同步觀測；主Mod不依賴它。
- `t13-macos.py`、`t13-network.py`、`t13-audit-network.py`及四份 `test-t13-*`：本機runner／native hash審計／工具回歸。
- T13契約、progress、journal、evidence、此交接。不要覆蓋T12原歷史source manifest。

官方app位於 `../runtime/0 A.D..app`，版本0.28.0。binary SHA256：`531981d016596b0abde110cd239feaed98998c3fdaa837d0fa8d6f75482c81ef`；public.zip：`ccb24dedee399e6d2810ccb62b0b1b77a937999d9f1dedffbc189b3e359f2429`。已驗codesign，未修改官方app。不要使用早期 `work/t13-runtime/client.app` 副本；它新增Mod資源後簽章不符，沒有重簽或繞過。

使用者Mod目錄的 `epoch_t13_harness` symlink指向repo工具內的harness。只在測試時以額外-mod啟用，不設定為預設Mod。存檔以唯一 `t13-*` 前綴保留；兩份最終基準局的 `native-saves/` 也已封存副本，勿刪私人存檔。

## 證據與重跑原則

最終save基準：
- Seed42：`work/t13-save/20260928T024918799142Z-save-42`
- Seed7：`work/t13-save/20260928T092618453821Z-save-7`

六個load場及原始result／engine.log／來源manifest的hash均列於 `evidence/t13-results.json`。公開來源表 `evidence/t13-source-manifest.json`；每場自己的source manifest則保留當時執行版本。

不用重跑已通過矩陣來「熟悉專案」；先比來源hash與證據，只有改動受影響程式或發現證據不足才做必要回歸。不要重做T05–T12既有驗收，不直接重寫AI，不改C++，不擴張T14。

根目錄未追蹤的 `profile.txt`、`profile2.jsonp` 是runtime產物，不要提交或刪除。`work/` 中包含失敗紀錄、舊副本、原始log／replay／存檔，維持本機不提交。未push，未建立排程。

## 2026-09-29 本機提交收尾

使用者已明確授權T13本機提交。核對129檔來源全部吻合、官方R28版本／兩項hash與codesign通過；八場存讀檔result／engine.log／manifest hash與公開結果一致，六次載入快照與基準相等，六份原生存檔及封存副本hash一致。兩場成功網路與一場保留失敗的原始result／native-audit／replay／HTML hash吻合，從封存replay重新比對到final的原生hash通過。七份既有工具測試紀錄與兩張GUI截圖已核對。

本次只更新提交狀態與收尾紀錄，未修改程式或重跑已通過的引擎／GUI驗收；逐檔提交T13範圍，排除profiles與work。T13保持限定DONE；T14需另行明確開工。

最終網路：`work/t13-network/20260928T093541710725Z-7`，另有首場seed42 `20260928T024238463836Z-42`；各自result、native-audit、封存native-commands與unique HTML日誌。工具輸出保留 `work/t13-tools`。目前可以安全關閉session；T13本機提交完成，沒有push。
