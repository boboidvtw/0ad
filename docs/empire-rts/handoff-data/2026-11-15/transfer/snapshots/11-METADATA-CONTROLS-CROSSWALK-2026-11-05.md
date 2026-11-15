<!-- Purpose: R06 metadata traceability crosswalk after project-plan publication. Date: 2026-11-05. -->
# R06：metadata 六欄／十一項技術缺口對照

**DONE只限本次跨計劃對照；十一項技術義務全部仍OPEN，關閉數0。** 這不是重做原已DONE source-plan／JS review，不增加模型或原生案例，不改85f93 comparator、舊48來源、任何wire/context／guard。

原plan manifest17eb3663的48份artifact已逐檔SHA／bytes核對MATCH。原JS review ccc2ef60僅APPROVE_DESIGN_ONLY，0blocking／1LOW；尚無完整三方目前metadata實作設計核可。完整資料見[機器對照](handoff-data/2026-11-05/METADATA-CROSSWALK.json)。

## 六欄對應

| metadata欄位 | 仍OPEN的義務 |
| --- | --- |
| engine_version | ENGINE_INFO_RUNTIME, PRECOMMIT_TRANSPORT |
| playerID | PRINCIPAL_CAPTURE, PRECOMMIT_TRANSPORT |
| mods | ENGINE_INFO_RUNTIME, PRECOMMIT_TRANSPORT |
| initAttributes | FULL_INITATTRS_PRODUCER, LOAD_NESTED_TIMESTAMP, REPLAY_START_AVAILABILITY, FUTURE_SCHEDULE_ABSENCE, PRECOMMIT_TRANSPORT |
| gui | CAMERA_CONTROL, GROUPS_INPUT_CLOSURE, FUTURE_SCHEDULE_ABSENCE, PRECOMMIT_TRANSPORT |
| description | STATIC_DESCRIPTION_HOST_FACTORY, PRECOMMIT_TRANSPORT |

只有metadata最外time走獨立epoch區間；nested initAttributes.timestamp保留精確值。各欄expected必在actual metadata前由獨立來源建立，不能由actual補值。

## 十一項下一步

| 義務ID | 下一工作包 | 必須補的證據 |
| --- | --- | --- |
| ENGINE_INFO_RUNTIME | R07 | 鎖實際binary／五mod選擇與完整order／四欄records，規格化同一guarded native GetEngineInfo caller與preSave持久化。 |
| PRINCIPAL_CAPTURE | R07 | preSave實際native GetPlayerID前後邊界及returned receipt綁case/PID/phase；literal1與payload.viewplayer分開。 |
| FULL_INITATTRS_PRODUCER | R05/R07/R08 | 完整source-owned boot/map/settings/trigger/native clone getter／所有writer閉合；未知key不得從actual學入expected。 |
| LOAD_NESTED_TIMESTAMP | R07/R09 | 每個fresh load自己的Replay startup control；timestamp精確值，不用origin值或outer-time interval替代。 |
| REPLAY_START_AVAILABILITY | R07/R09 | 優先規格化真正source-vouched GetInitAttributes候選與因果順序；replay可得性仍Insufficient data，禁warmturn/flush/wait/額外Save。 |
| CAMERA_CONTROL | R07/R09 | 新待審設計明列GetValue()→native float→JSON精確值；source getters與Save對應、setter fixed量化／load restore、preSave全程無mutation與rawlineage。 |
| GROUPS_INPUT_CLOSURE | R05/R07/R08 | 10組groups/ents exact empty來源、human/controlgroup/prototype/toJSON/clone/mutation完整控制；非空actual不得投影。 |
| STATIC_DESCRIPTION_HOST_FACTORY | R07 | host immutable case phase/checkpoint/ordinal只derive description literal；source API拒actual/archive metadata作輸入。 |
| PRECOMMIT_TRANSPORT | R07/R08 | 獨立controls由source因果鏈在Save前建立；同PID/caller/realm及raw順序須證。Host先持久化controls與固定expected，再讀actual metadata；不另推定host落盤必先Save。 |
| FUTURE_SCHEDULE_ABSENCE | R05/R07/R08 | 完整producer/mutator/serializer closure與graph/queue/native證據；full equality不等absence，合法gameplay Timer不可刪。 |
| FULL_NATIVE_PIPELINE | R08/R09/R11 | 完整host/current source/runtime/original-copy/profile locks與原budget/freshguard；原生save/load/network實際證據另驗。 |

## 已釐清但未實作的修正

1. CameraController.cpp418–432 getter使用GetValue()。原sealed FIELD-MATRIX的smoothed字眼是既有JS-DESIGN-LOW-001；後續設計須明確修正語意，不替換原plan／原報告、不改C++。不得以GetSmoothedValue、nominal0.6、epsilon或rounding替代native getter。
2. Replay.cpp71–90 origin和load都改寫nested timestamp/engine_version/mods。StartGame只寫newline，Turn才flush；freshload L0不能藉多turn、flush、等待、第二次Save或延長5秒取得control。
3. full-value compare即使MATCH也不能證明future schedules不存在；兩邊同受污染仍會相等，producer/mutator/native clone與graph/queue閉合不可略過。

## 交給R07的最小設計範圍

只準備新的source-owned Prepare／Bind／Materialize設計及exact caller／phase／raw／precommit資料流；保留原schema／context六keys／ACK與時限，任何必要介面變更必先形成prospective reviewed amendment。禁止接受actual metadata作expected輸入；沒有真native control或完整caller／realm閉合時必BLOCK。先完成完整獨立設計審查與根端准入才寫metadata實作；source review與runtime准入各自另行。

R06完成使18個計劃工作包中1個文件對照工作包完成、17個尚未完成；**五個主功能任務仍未完成，沒有遊戲功能因此升DONE。** R01一次guard重取樣仍是同一待明確決策事項，不由本對照或一般接續授權推定。

## 2026-11-06 原文對齊更正

根端原表將HOST-API-DRAFT:10的兩項義務過度合併為host必在Save前落盤。兩個獨立來源調查確認原文只明訂controls在Save前由source因果鏈建立，並另要求host commit/readback與接收順序證明；未明文限定host disk時點也先Save。更正後可研究同callback capture→唯一Save，host保存controls與固定expected→才讀actual metadata的候選；全部caller/realm/body/immutability/raw/deadline與11 OPEN義務不減。原表preimage及初步BLOCK假說保留於work/t17-metadata-controls-design-20261105；此更正不是放寬原契約或implementation准入。
