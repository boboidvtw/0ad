<!-- Purpose: T08 closeout and bounded T09 restart instructions. Created: 2026-09-20. -->
# Session handoff — 2026-09-20

- 唯一repo維持本checkout；本次起點master e956ac6。開工核對實際HEAD及Git狀態，不拿本文件代替現況。
- T05–T07已有限定驗收，勿重做；T08 DONE僅指規則／可行性調查與範圍決策。完整可玩潛艇未實作。M3 IN_PROGRESS，T09 TODO。
- 先讀progress.md、plan.md、journal.md、t08-submarine-feasibility.md、evidence/t08-validation.md與t08-* JSON，再讀T07原型／證據的限制。以本文件取代9/13交接的下一步，但保留其歷史紀錄。
- 官方R28 0.28.0 macOS ARM64，runtime仍在`../runtime/0 A.D..app`，實測DMG hash與baseline一致。manifest另保存binary/public.zip及選定成員雜湊；舊repo public 0.0.27不能使用。Mod symlink仍指本checkout。
- T08新增隔離深水地圖、原生船衍生測試模板、EpochT08Visibility、Trigger探針與t08-macos.py。不覆寫原生Attack／Visibility，不改C++；M2生產建造白名單不變。
- 最終兩seed各30項PASS、兩次同來源與runner的重播事件／結果相同且自然EOF；hash_checks_ok=0，勿宣稱全狀態或多人同步。M1載入回歸PASS。
- GUI四階段：水面／隱藏／偵測水下／重新浮起，8項API檢查及4張截圖；正常exit0、無錯誤警告。暫用船桅杆仍露水，不是潛艇美術；未驗選取、小地圖洩漏、owner／盟友GUI。
- 關鍵實測：FloatDepth4在水位20、海床8時y16；SetHeightFixed可浮潛且沿ship路徑移動；depth本身不隱身。獨立IID_Visibility callback和RequestVisibilityUpdate可逐玩家顯示／隱藏；後者由探針顯式呼叫，尚無自動聲納管理器。
- 關鍵缺口：hidden目標的已知entity ID正常attack命令仍造成HP2000→1956.26；已在攻擊的單位失去偵測仍使HP1897.94→1854.20。CanAttack和PerformAttack不是LoS gate。探針的PASS包含『限制成功重現』，不代表攻擊需求已成立。
- T09下一單元：彙整T07精確空中彈道、停機位／跑道／建築避碰與T08攻擊缺口，先比較獨立Mod的controller／visibility／偵測更新／attack gate／無彈道傷害。沒有證據要求預先改引擎；若需要C++，另固定匹配R28源码并新增建置與回歸任務。
- 需另列的潛艇實作／驗收：2秒浮潛與停火、所有權／非法命令、6公尺淺水與海床安全、動態武器矩陣、延遲命中、失去偵測的取消、盟友共享、GUI控制、存讀檔、多人及效能。真實魚雷／獨立水下碰撞層未驗。
- 引擎測試串行，所有遊戲共用logs；runner會拒絕既有pyrogenesis。原始logs/replays/profile留忽略的work及遊戲replays，公開JSON不含私人路徑。只本機工作，未push；無排程或背景任務。
