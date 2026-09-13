<!-- Purpose: Session closeout and next-session startup. Created: 2026-09-13. -->
# Session handoff — 2026-09-13

## 工作位置與狀態

- 唯一工作 repo：`/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`。不要另建專案或回到舊 ChatGPT 工作目錄實作。
- 收工前實作 HEAD：`c0266d9`（T07）；上一個 `cdcbffc`（T06），T05為 `8d5ee7b`。本交接另作文件提交，開工先讀實際HEAD。
- 收工檢查：原工作樹clean，無pyrogenesis執行中；没有背景工作、排程或待回覆核准。未push。當時本機origin/master記錄仍為8d5ee7b，未重新fetch，不把它當即時遠端狀態。
- M1／M2完成，T05勿重做；T06／T07已完成限定驗收。M3 IN_PROGRESS；下一項T08 TODO，T09 TODO。

## 必讀順序

1. 適用AGENTS.md與Git狀態；[progress](progress.md)、[plan](plan.md)、[journal](journal.md)。
2. [baseline](baseline.md)、[T07規格](t07-air-prototype.md)、[T07實測與限制](evidence/t07-validation.md)。
3. [T07來源manifest](evidence/t07-source-manifest.json)、引擎／回歸／GUI JSON（同目錄t07-*）；必要時讀[T06證據](evidence/t06-validation.md)及[m2-rules](m2-rules.md)。
4. 既有Mod、`tools/epoch-rts/launch-macos.sh`、`t07-macos.py`。先調查官方runtime實際介面，再寫新測試。

## 固定架構與環境

- 官方R28 0.28.0 macOS ARM64；app：`/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/runtime/0 A.D..app`。
- 9/13曾恢復同一DMG，SHA-256：`8c53566123fed9a79766c364e543d6e9dc7c84f642c78d2bb5892eeea9c4c052`。新session仍先核對實際存在與版本。
- Mod：`binaries/data/mods/epoch_rts`，版本0.3.0；依序載入mod/public/epoch_rts。使用者Mod symlink應指向本checkout。
- repo內上游public是舊0.0.27，不能與R28混用。R28參考來自官方app的public.zip；本機work/r28-reference只是參考快取。
- 不改C++或上游public；新機制留在獨立Mod沙盒，不擴充M2工人建造白名單。
- sparse checkout可能要求`git add --sparse`；保留其他人的變更。Python目前為/usr/bin/python3 3.9.6，勿假定3.14。遊戲共用log，所有引擎測試串行執行。

## T07交付與實際證據

- EpochAircraft controller、R28衍生EpochAircraftMotion、EpochAirCommands；aircraft／airfield／anti_air模板；probe／validation／demo地圖與runner。
- seed42／7各36項引擎檢查及36項重播PASS；原生probe2項PASS。重播是事件／結果一致且自然EOF，無hash行，不宣稱全狀態同步。
- 返航距機場5.534公尺；AA十秒內HP200→42.5；包含實際滑跑煞停、毀機場就地降落、機場轉敵改降、非法命令拒絕、移動目標追蹤。
- GUI兩場exit0、0錯誤／0警告，7張截图；選取／起飛／對地攻擊／受損／返航／再起飛／H連按落地。最終固定manifest的demo另核對來源未變。
- M2回歸：戰鬥81項、兩seed完整對局各15項且649.8／621秒勝利、T04經濟183項、M1 smoke PASS。T05未重跑。
- 唯讀code review的問題已修正與複查；沒有未解HIGH/MEDIUM審查項。

## 必須保留的限制

- AA採原生無彈道Ranged即時傷害。原生飛行彈道多次未命中，放大footprint、修正時間單位及提高彈速都不足以證明精確命中；最終未放大footprint。精確空中彈道待T09評估。
- 寬鬆90公尺降落區，不含精準跑道／停機位或建築避碰；GUI會與兵營暫用模型重疊。
- 移動目標只驗證追蹤座標，實際扣血用固定房屋。沒有完整命令佇列／編隊／空對空／燃油／補給。
- 通用AI、存讀檔、多人、效能、正式美術及完整在地化未完成；不得因T07 DONE而擴大宣稱。
- 初次手動demo期間只擴充測試函式，舊runner的結束時hash不是初始整份script證明。最終runner已用啟動前fullMod manifest＋結束核對；詳細範圍在GUI JSON。

## 下一個完整工作單元：T08

1. 先定義水面／水下狀態、浮潛切換、敵我可見性、偵測、可攻擊目標與魚雷需求，提出可逆的最小規則。
2. 讀官方R28船舶、Position／水位、視野與目標判定介面；建立最小原生探針，用實際runtime確認可行／不可行範圍。
3. 依證據決定T08實作範圍或延後條件，不預設必須改引擎。若涉及畫面需保留GUI證據，靜態閱讀不能替代runtime驗證。
4. T08只有調查與決策，不擅自把所有潛艇功能或T09標完成。T09待T07限制與T08結果齊備，再比較Mod與引擎方案。
5. 將實際結果、版本、證據、限制及下一步同步寫入repo的progress、journal及驗收文件。必要回歸才重跑；未驗證項目維持NOT RUN／PARTIAL。

本次未取得新的push／發布授權；新session預設只做本機可逆工作與scoped提交，不推送遠端。
