<!-- Purpose: T09 decision closeout and T10 restart. Created: 2026-09-21. -->
# Session handoff — 2026-09-21

## 目前狀態

- 唯一repo保持本checkout；T09起點master ac4cbff，完成後先核對實際HEAD與Git。只做本機工作，未push。
- M1、M2完成；M3 DONE僅涵蓋T07限定空戰原型、T08潛艇調查、T09架構決策，不代表完整海陸空完成。
- T09決策維持官方R28與獨立Mod，暫不啟動C++。主線下一步T10暫用素材與匯入樣板；T16攻擊檢查、T17潛艇垂直切片、T18精確彈道與停機位仍TODO。
- 先讀progress.md、plan.md、journal.md、t09-engine-decision.md及evidence/t09-decision-audit.json。T07／T08歷史證據與限制原樣保存，不重做已完成限定驗收。

## 基線與未完成限制

- 官方R28 0.28.0 macOS ARM64，app在`../runtime/0 A.D..app`，Mod在`binaries/data/mods/epoch_rts`。repo舊public不是R28，禁止混用。T09核對binary/public.zip及T07／T08來源雜湊均一致，未跑新的遊戲測試。
- T07仍為即時防空傷害、90公尺降落區；精確空中彈道／停機位／建築避碰未完成，移動目標只驗追蹤，沒有完整命令佇列、AI、多人或存讀檔。
- T08只證明深度、ship平面航行及逐玩家visibility可用。手動更新不代表自動偵測。hidden新命令及既有攻擊仍扣血；專用攻擊gate尚未實作。
- T16規格涵蓋每次發射與所有入口，並明定原生攻擊者混用的缺口；不得把專用元件當成能保護所有原生攻擊。T17與T18不得因T09完成標DONE。
- 現有重播只事件／結果一致、沒有hash行，不宣稱多人同步。若要引擎修改，依T09第5節取得重現與替代方案比較，再固定匹配R28原始碼與Build，不直接用舊repo引擎。

## 下一個完整工作單元：T10

1. 核對適用規則、Git、runtime、progress，讀art-direction.md與assets.md。
2. 選既有M2的一個單位或建築作暫用資產／匯入樣板；優先沿用已登錄的官方R28素材，不增加付費服務或擅用Empire Earth素材。
3. 定義來源、授權、模型／材質／動畫依賴、單位比例、匯出／匯入方法、可重現檢查及遊戲內驗收；先調查實際工具與格式，不能把模板路徑引用當完整匯入驗收。
4. 交付最小樣板及至少一個模型實際引擎／GUI證據；不足就標PARTIAL，正式原創美術仍屬T11。
5. 更新assets、progress、journal及必要交接；引擎場次串行，保存原始證據，依受影響範圍回歸，不重跑無關T05–T08。

沒有排程、背景執行或外部發布授權。新需求若要優先處理T16可另改順序；本交接預設按主線進T10。
