<!-- Purpose: Preserve bounded T12 completion, sources and next-session boundary. Created: 2026-09-27. -->
# T12 收尾交接

**T12限定DONE；M5仍IN_PROGRESS。T13／T14未開工。** 本次只做本機工作，沒有push、排程或背景任務；T12以本文件所在commit本機提交，父提交為master `d372345`；實際commit以Git歷史核對。不要重做T05–T12已完成限定驗收。

真正repo：`/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`；官方app `../runtime/0 A.D..app` 0.28.0。接續仍先核對Git、[progress](progress.md)與實際runtime；勿用repo舊public資料。

## 完成及限制

- [固定契約與重現](t12-ai-acceptance.md)：epoch_petra、正常難度、Frontier Duel192、map／AI seeds42／7、標準資源、固定防守對手。自主經濟、房屋／兵營、鐵器、鐵刃生產與進攻勝利；非通用AI對戰認證。
- [驗收](evidence/t12-validation.md)：最終兩seed各38項、884.6／894.6秒勝利；兩重播suite一致且EOF；兩GUI引擎場及09-27实际畫面／選取／正常退出。最後113檔manifest六場相同，T11原105檔未變。
- [審查](evidence/t12-code-review.md)：本機逐檔完成，非獨立審查。修正損壞frame未拒絕的parser及房屋容量驗收缺口；AI adapter未改。8項Python、Node隔離／集合生命週期及語法檢查通過。
- 官方Petra新來源正向回歸通過；探針因自然提早結束仍complete=false／runner exit1，不能當1800秒完成。完整限制及11項實際觀測結果已記錄。
- 截圖6張及原始來源hash在evidence/t12-*，新圖補齊鐵刃HUD；仍未保留進攻中截圖、1×GUI或AI選單驗收。引擎事件證明主動攻擊與市中心傷害。
- T13存讀檔／多人與T14效能仍TODO；不得由重播suite相同推論全狀態同步。進攻manager instance方法還原相容性需T13另驗。
- T11僅原創低面數樣板完成，正式M2仍暫用public角色。T07／T08及T16–T18限制不變。

## 重要檔案

| 範圍 | 路徑 |
| --- | --- |
| AI adapter | `binaries/data/mods/epoch_rts/simulation/ai/epoch_petra/` |
| 隔離觀測／驗收 | `binaries/data/mods/epoch_rts/maps/scripts/epoch_rts/T12{Probe,Validation}.js`及3個epoch_t12地圖JSON |
| runner／工具測試 | `tools/epoch-rts/t12-macos.py`、`t12-probe-macos.py`、`test-t12-tools.py`、`test-t12-adapter.cjs` |
| 正式證據 | `docs/empire-rts/evidence/t12-validation.md`及同前綴JSON／PNG |
| 原始本機場次 | `work/t12-validation/`、`work/t12-observed-probe/`，各場ID見驗收表 |

## 本機提交與下一步

使用者已明確授權T12本機commit；提交只涵蓋T12 Mod、工具、測試與相關文件／證據。根目錄未追蹤 `profile.txt`、`profile2.jsonp` 是runtime產物，可能隨引擎運行更新；不要誤提交或刪除。不要為清理狀態而混入其他工作。

本任務已收尾，不自動開始T13。本機提交排除profile及work；push仍需另外授權。若後續要求T13，從存讀檔與多人最小契約開始，不改寫已通過的AI或直接改C++。
