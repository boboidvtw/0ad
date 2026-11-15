<!-- Purpose: completed unique delta runtime and separately validated offline ledger handoff; Created: 2026-10-09. -->
# T14 CanAttack delta：完整離線觀測 PASS／首次 runner FAIL

**本場已結束、attempt1已用完、retry0，禁止再次launch。** 原runner result仍FAIL/PARTIAL；有效遊戲、完整raw、同reviewed code/caps的離線重建及native分析PASS。T14仍PARTIAL。後續先核最終稽核／seal；本有界觀測目標已完成，不啟動額外量測；原prelaunch/launch checkpoint封存於work/t14-canattack-delta/handoff-before-closeout.md，不能當成新launch指令。

Repo `/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`，HEAD726a3aefcae830f605de438cd13192cc6330414e/index空；T13限定DONE，全部T14未commit。先核實Git/progress/plan/journal/locks/R28/engine-runner/ports，不只依摘要。

用戶明確授權hourly自動接續，實際automation0ad-t14 ACTIVE；本heartbeat已恢復quota中斷後工作，未買credits/用reset券。排程提供續作機會，不保證額度恢復瞬間執行。觀測有界目標已完成後保持安靜，不因原SQLite未知cause再量測。

新14產品工具（9harness＋runner/parser/3tests）保持原284，現298產品/130measured。固定typedarrays67976bytes、shard2048/1536完整flush、stack128；fullkeys/unknown/noninitial/nullmethod/parent/phase/returnthrow/descriptor/this/arguments/同步順序保留，不probe目標/Set、不合併gameplaycalls。caps/gates保持原契約：768MiB payload、70000chunks、record512、chunk12000、stdout1536MiB、metadata32MiB、line65536、SQLite2GiB、disk8/4/2GiB。11proofPASS／review44APPROVE／654source-lock／另一call獨立guardPASS後才唯一launch。原code/caps未修改。

### 2026-10-09 — T14 CanAttack delta：有效遊戲／完整離線 ledger PASS，首次 runner FAIL

新14隔離工具經review44／11proof／654source-lock／獨立guard後唯一量測，retry0。engine0無ERROR/WARNING、game/native捕獲gates PASS；首次runner SQLite/storage failure仍FAIL/PARTIAL，原部分DB/journal/result保留。相同reviewed code/caps以同raw離線重建與native分析PASS：5,277,402 CanAttack（true5,260,535/false16,867）、32,218methods、5,277,253keys、CRCacfc3828/SHAe851242f…；strict native1,460,757非phase1總數。獨立全5,277,253key核實相符，審後helper APPROVE／26fixtures一般-O及最終raw一般-O完全一致PASS。110.096GUI秒/98.8sim/5365interval，p99100.786/.897399全場性能FAIL，首窗性能FAIL活動PASS，尾性能PASS混合活動FAIL，190slow frames全留。末133Slinger vs0非正式勝利。原284不改、298產品/130measured、48raw全留。首次SQLite根因Insufficient data、overhead/安全修復/正式勝負NOT RUN；T14PARTIAL，禁止runtime retry與擴測。無commit/push/刪檔/C++/AI/玩法修改。hourly automation0ad-t14只續作未完驗證，不啟動額外場。[validation](evidence/t14-canattack-delta-validation.md) · [results](evidence/t14-canattack-delta-results.json) · [交接](SESSION-HANDOFF-2026-10-09-T14-CANATTACK-DELTA.md)。

先核實29raw lock、654source lock、最終獨立審查/一般-O/逐key比對、closeout/seal及engine/ports。唯一raw已存在且engine/runner退出，不能重launch。正式原result解析FAIL不得覆寫；新完整離線DB在work，來源未改，caps未弱化。兩次同raw完整重建成功但原SQLite cause未保留，唯一原因Insufficient data。完整觀測有界目標達成，整批自動runner與T14仍PARTIAL；不啟動額外量測，若需未來修復先不同问题/source證據/事前契約。本heartbeat保持安靜，不把unknowncause當需重跑理由。
