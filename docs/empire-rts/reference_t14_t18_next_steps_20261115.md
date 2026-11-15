<!-- Purpose: prioritized continuation after2026-11-15closeout. Date:2026-11-15 Asia/Taipei. -->
# T14–T18 下一次接手順序

先讀[本次詳細收工](SESSION-CLOSEOUT-2026-11-15-T14-T18.md)與[STATUS](handoff-data/2026-11-15/STATUS.json)。Actualrepo `/Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad`，projectcwd不是repo；本機最新checkpoint v18。舊11/12「三報告都缺」是歷史，目前Python/JSAPI已完成，勿重跑。

| 優先序 | 必要工作 | 前提與完成證據 |
| --- | --- | --- |
| P0必要 | 恢復原CODE的正式交付權限 | 查原parent/actor當次permissions，不把額度恢復當可寫；不得改model/替代角色或繞限制。可寫後由同CODE本人建立原指定JSON/MD並驗SHA/manifest/85coverage/reasoning/findings |
| P0必要 | 新root親讀與獨立准入 | 前root85只繼承；本chat本人3/85。三正式報告、全部85內容/role/完整功能推理/歷史契約由接手root實讀核對；未齊不實作，不借他人已讀冒領 |
| P1必要 | 明確source-scope/ownership | 僅三正式完整DESIGN核可及root驗證後，另限定派生新source與targetedmodeltests範圍；保留舊approvedsource，不能直接跑producer/fullhost/engine |
| P1必要 | 後續完整SOURCE核可與R08閉合 | exact current freeze、CODE/Python/JS SOURCE、actual getters/transforms/caller/realm/clone/serialization/mutation/fullhost/runtime/profile/raw/order/limits等全部依原契約；modelPASS不等native |
| 獨立待決策 | 原guard一次刷新例外 | 使用者須對原具體方案明確決策；收工/push/一般continue不是例外授權，不重採不改guard、不建rootreport/capsule/EXEC/attempt |
| 後續必要 | T14–T18各未完工作包 | 依11/5評估R01–R18依賴續作，不重跑耗用案例、不放寬gate；實機/native/GUI/save-load/network/parking/交付仍需各自證據 |
| 操作必要 | 排程接手 | 既有0ad-t14 ACTIVE每5h，target本chat；先讀既有設定，只原id移轉，不複製schedule。無新資訊安靜，不反覆重驗DONE或寫synthetic進度 |

下次第一動作：liveusage→確認actualrepo/HEAD/branch/index/dirty→STATUS/v18與正式檔存在性→確認原CODE可寫。仍唯讀且無新必要可行工作時保留BLOCKED，不空等報告、不重新開審查者。若使用者要停止自動續作，明確暫停既有同id即可，勿另建排程。

Quickreference：manifest e73e6c48/85；原checkout d5133455/codex/t14-t18-closeout-20261104；公開收工branch codex/t14-t18-closeout-20261115；三casesNOT_RUN；24helpersconsumed；11obligationsOPEN；guardSTOP/refreshpending。原work/raw/seals不得刪除。
