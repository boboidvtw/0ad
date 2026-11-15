# JS/API metadata controls 設計審查 v1

結論：**APPROVE_DESIGN_ONLY**。角色 `JSAPI`；manifest SHA256 `e73e6c48bd2a7ea31742aef7ad4b1744e6f28dbed799c39b28b25a3f9079b93a`。

本人已完整閱讀 manifest 與 85/85 bindings，並逐項核對全部 current／snapshot 的 bytes 與 SHA256，全部 MATCH。合計 1,447,275 binding bytes；partial/unread 為 0。未發現設計層 blocking finding。完整逐檔記錄、閱讀範圍、SHA reuse 與功能推理均保存在同名 JSON。

這份結論只認可設計。完整 SOURCE 三方審查、root 另行准入，以及所有 R08/native/source-body/caller/realm/prototype/serialization/五秒證據仍必須完成；十一義務仍 OPEN，R07 仍 PARTIAL，原 guard STOP、原 cases NOT RUN 與消耗紀錄保持。

## JSAPI-D01 原權威與 host causal correction

原 HOST-API 要求獨立 controls 在 Save 前由 source 因果建立，並另證 host commitment/read 順序；沒有明文要求 host 磁碟寫入先於 Save。此設計明確 source pre-Save capture、同 callback sole Save、host controls 與 expected 持久化讀回後才首次讀取當次 actual metadata。撤回較強衍生說法有原文依據；保留歷史 preimage，不以 actual 補 expected。已驗 origin archive 的官方 load/hash/CRC 不是當次 expected authority。

證據：`work/t17-metadata-controls-design-20261105/design-freeze-v1/003-HOST-API-DRAFT.md:10`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/002-FUTURE-SCHEDULE-ABSENCE.md:12`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:6-12`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:57-65`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/077-ROOT-CAUSALITY-CORRECTION-v1.json:1`。

## JSAPI-D02 GetEngineInfo 與 mods 返回型別

原生 GetEngineInfo 建立含 engine_version 與 mods 的 JS object 並 deep-freeze；mods 是完整有序四欄 records，mod/name/version/ignoreInCompatibilityChecks 不可投影或按 compatibility filtering 更改。版本不得由 package version 或猜測取代。返回 object 已 frozen 只證該路徑行為，不證實際已載入 binary/body、caller 或 native provenance；設計把這些留作實際 SOURCE/R08 gate，沒有用 immutable JSON 洗成 PASS。

證據：`work/t17-metadata-controls-design-20261105/design-freeze-v1/041-JSInterface_Mod.cpp:31`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/041-JSInterface_Mod.cpp:113`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/035-Mod.cpp:1`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:24-28`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:32-43`。

## JSAPI-D03 principal、view caller、GuiInterface clone 與 official getter

GetPlayerID 回傳實際 game int，無 game 為 -1；literal expectedPrincipal=1 或 payload principal 不構成 native 身分。GuiInterfaceCall 使用 native viewed player 作 ScriptCall caller，跨 realm clone 入參與返回。GetInitAttributes 是 official GuiInterface 的 exposed JS method，返回 simulation global InitAttributes，不是獨立同名 C++ getter。須核實實際 constructor/prototype/exposedFunctions/global binding、所有 caller/SetPlayerID/SetViewedPlayer 與 loader/realm/clone closure。設計保留 ReadSaveContext 六 keys、actual caller 與 principal 的區別。

證據：`work/t17-metadata-controls-design-20261105/design-freeze-v1/040-JSInterface_Game.cpp:62-67`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/008-JSInterface_Simulation.cpp:46-64`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/024-GuiInterface.js:202-205`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/024-GuiInterface.js:2066`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/024-GuiInterface.js:2128`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/055-session_transaction.js:48-58`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:32-41`。

## JSAPI-D04 FULL_INITATTRS transformations 與 fresh load

Simulation2 保存完整 m_InitAttributes，LoadMapSettings deep-freeze 並建立 readonly global；startup/trigger 等完整寫入來源仍須逐項 authority。Replay startup 會寫 timestamp/engine_version/mods；fresh load 不能假定 nested timestamp 沿用 origin。除 comparator 已定義 outer metadata.time 區間外，不得把 nested timestamp 當任意差異豁免，也不得由觀測 getter 未知 key 學成 expected。完整 current transformations/layout 仍 OPEN，設計要求缺 authority 就拒絕 materialization；這是合理後續 gate，本次不循環要求先跑 native 才能審設計。

證據：`work/t17-metadata-controls-design-20261105/design-freeze-v1/038-Replay.cpp:75-82`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/045-Simulation2.cpp:798-810`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/045-Simulation2.cpp:852-853`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/042-JSInterface_SavedGame.cpp:1`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:24-28`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:75-83`。

## JSAPI-D05 camera GetValue、fixed/float/native JSON

舊 FIELD-MATRIX:33 的 smoothed 說法與 actual CCameraController getters 不符；418-432 使用 GetValue。新設計明確採真 native float getters，position xyz 到 PosX/Y/Z，rotation xy 到 RotX/Y，zoom 到 Zoom。entity_pos_t fixed 15.16 setter 及 ToFloat、FocusHeight/SetupCameraMatrix 可改變 nominal 值；native float 提升到 JS Number 與 native JSON encoding 的精確語義須保持，不可用 0.6、epsilon、rounding 或 GetSmoothedValue。fresh load official restore 重新經 setter，必由當次 getter 加已驗 origin ancestry 判定，不預設 getter 等於 origin。原 LOW/sealed 資料保持，設計另行更正而非追認舊文字。

證據：`work/t17-metadata-controls-design-20261105/design-freeze-v1/001-FIELD-MATRIX.md:33`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/027-CameraController.cpp:418-451`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/031-JSInterface_GameView.cpp:76-110`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/032-Fixed.h:151-177`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/039-SavedGame.cpp:102-122`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:38`。

## JSAPI-D06 groups、structured clone 與 native Serialize 之間 mutable state

getSavedGameData 返回 live g_Groups.groups；source constructor 的十個 EntityGroups 各有 groups/ents，expected 十個 exact 空 records 來自獨立 plan，不能將非空 actual 投影成空。SaveGame wrapper 是 void，先 WriteStructuredClone GUI metadata，SavedGames::Save 隨後 SerializeState，再讀 native attrs/mods/player、GUI clone、camera、description 與 StringifyJSON。暫停、相同 S、同 callback 或 frozen detached bytes 都不能證 serializer/prototype/toJSON/getter/clone 及 group/camera/attrs 不受變動。新設計明文禁止未知 hooks/shared freeze，保留全 caller 與 read-only/no-mutation closure；source-level 節點尚未完成，未偽稱已證。

證據：`work/t17-metadata-controls-design-20261105/design-freeze-v1/022-selection.js:1`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/023-session.js:584`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/042-JSInterface_SavedGame.cpp:46`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/039-SavedGame.cpp:80-122`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:37-43`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/070-source-registry.json:1`。

## JSAPI-D07 A/L0 → controls → sole Save → B/L1 與 first pause

既有 transaction 先 context 與 A/L0 graph/checkpoint，再 ordinal/name、SAVE_CALL、cameraSame、唯一 SaveGame、B/L1、request write/readback；fresh-load first graph 已傳入 transaction。新 capture 只插在原 A/L0 及固定 identity 後、原 SAVE_CALL 前，同 callback 不加 wait/yield/flush/turn/barrier/新 graph 替代或第二次 Save。capture/encode/emit 錯誤 sticky BLOCK 且不呼叫 Save。FIRST pause 的既有承諾限 wrapped session init 首個 native action，不能擴張為早於全部 GUI top-level/init/restore/Deserialized/Interpolate。原 fullgraph、actual CommandQueue count0、A-QO-B/L0-QL-L1、no rearm/no warm、noFutureSchedule 不變。

證據：`work/t17-metadata-controls-design-20261105/design-freeze-v1/055-session_transaction.js:167-184`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/055-session_transaction.js:261-265`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/055-session_transaction.js:296`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:18`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:30-43`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/070-source-registry.json:1`。

## JSAPI-D08 prospective external raw stage 與原 request/ACK/context

新 METADATA_CONTROLS_CAPTURED_V1 是 prospective producer/raw-reader/source integration 變更，不是現有 parser 已接受或舊 SOURCE approval 自動延伸。outer exact kind/data，data exact schema/identity/principalBoundary/controls，controls exact engine_version/playerID/mods/initAttributes/gui/description；campaign/case/source/seed/phase/checkpoint/ordinal/archiveName/S tuple 與 once/order 必核實。完整 ASCII frame/cap/depth/duplicate/unknown/type gates 須 fresh SOURCE review；原 request/ACK/ReadSaveContext keys、native serialized state/profile inventory 不擴張。現有 prearm endpoint 只處理 GUI_ACK_VERIFIED 也不證 full reader 兼容新 stage。

證據：`work/t17-metadata-controls-design-20261105/design-freeze-v1/075-RAW-STAGE-v1.json:1-91`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/057-t17_save_prearm.py:600`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/055-session_transaction.js:48-50`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/055-session_transaction.js:179-195`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:14-18`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:45-55`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:73-75`。

## JSAPI-D09 host durability、expected-before-actual 與 first error

host 每 original tuple ordinal 只在自己的 evidence tree 以 O_EXCL/O_NOFOLLOW 0600 建 controls raw 與 expected raw，保留 partial，fsync/once-close/postclose size/SHA readback 完成才 commit；不覆寫、rename/delete 或改 leaf。raw offset/SHA 與 source tuple 要 join，不能提前開當次 actual metadata、以 actual camera/mods/timestamp 補 expected、或 origin archive bootstrap expected。UNKNOWN/late/lost/partial 必停止，沒有補 capture/Save。source emit 成功不等 host receive 或 durable；新設計明確不謊稱 host disk commit 在 Save 前。

證據：`work/t17-metadata-controls-design-20261105/design-freeze-v1/003-HOST-API-DRAFT.md:1`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:43`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:57-65`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/075-RAW-STAGE-v1.json:82`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/076-FUTURE-TEST-PLAN-v1.json:15-16`。

## JSAPI-D10 固定五秒與 outer deadlines

D=t_arm+5e9ns 不重設；load 的 pre-Popen reserve、guards/startup 和新增 capture/persist/readback 全吃同一 budget，原 80/90/540/600 秒外層限制也保留。endpoint 為完整 GUI_ACK_VERIFIED 的 host receive，必 start<=receive<min(D,workEnd)。不能以 emitter 呼叫、buffered stdout、稍後 ACK 或另開 timer 替代；不加 wait/flush 解決。是否實際能在五秒內完成仍 Insufficient data，本次設計 approval 不認證可行性也不授權執行。

證據：`work/t17-metadata-controls-design-20261105/design-freeze-v1/057-t17_save_prearm.py:46`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/057-t17_save_prearm.py:522`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/057-t17_save_prearm.py:633`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/055-session_transaction.js:147`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/055-session_transaction.js:195`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/075-RAW-STAGE-v1.json:67`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:75-83`。

## JSAPI-D11 comparator 與 structural tests 邊界

既有 85f93 comparator 不變：完整 exact 六 controls 對 metadata 七欄，只有 outer time 為既定 interval；nested 結構、bool/int 區別、有限 binary64、-0/+0 與完整 mods/order 不得寬化。新 canonical/ASCII/JSON 型別與 depth/duplicate/unknown rejection 須獨立 source/static/model 驗證。未來 structural parser/materializer tests 即使 PASS 也永遠 native_verified=false/runtime_bound=false，任意 frozen object/hash/public binding dict 都不能升格 native receipt。FUTURE-TEST-PLAN 是未執行測試計畫，本人沒有執行。

證據：`work/t17-metadata-controls-design-20261105/design-freeze-v1/056-t17_save_metadata.py:1-160`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/075-RAW-STAGE-v1.json:1-91`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/076-FUTURE-TEST-PLAN-v1.json:1-28`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:73-75`。

## JSAPI-D12 完整 packet、typed roots 與 admission 結論

本人完整閱讀原 17eb/48 source plan/primary、ccc2ef60 設計及 LOW、typed-root/prototype/absent actor/full Timer registry、receipt/prearm/GUI 完整嵌入 WIRE、host/comparator、兩調查與 root correction 及新三份設計。registry 的 assignment/constructor catalog 不是 actual own-key/native conformance 證明；未知 accessor/proxy/function/prototype、serialization/clone caller closure、actual body/loader/binary provenance 仍 BLOCK 後續 admission。未找到必須修改本 frozen design 才能表達要求的實質矛盾。十一技術義務仍 OPEN、R07 PARTIAL、原 guard afb3339b STOP/一次刷新待具體決策、原三 cases NOT RUN；歷史 consumed attempts/FAIL/STOP 不變。本角色的 approval 只認可可送後續 SOURCE 審查的設計，不構成三方一致或 root source-scope admission。

證據：`work/t17-metadata-controls-design-20261105/design-freeze-v1/013-SPEC.md:1`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/014-wire-schema.json:1`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/049-review.json:1`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/055-session_transaction.js:1-297`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/057-t17_save_prearm.py:1`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/060-SPEC.md:1`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/062-WIRE-EXTENSION.json:1`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/070-source-registry.json:1`；`work/t17-metadata-controls-design-20261105/design-freeze-v1/074-DESIGN-v1.md:69-83`。

## 完整閱讀與獨立性

This actor did not author the design or either preliminary investigation. All packet content was personally read; no other reviewer reading or approval was borrowed. Historical reports are packet inputs, not inherited approval. Same task/settings continued across reported quota interruptions.

相同 SHA 的本人全文 reuse：55→6、56→7、68→13、69→14；各對 current/snapshot 均另行核對。070 registry 的全部 247,916 bytes 分批本人讀完，沒有用 catalog/hash/摘要取代全文。歷史 review 的 catalog 不遞迴成為本次其他檔案的核可。

## 逐 binding 記錄

| Index | 原路徑 | Bytes | SHA256 | 閱讀／核對 |
| --- | --- | ---: | --- | --- |
| 0 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/CONTRACT.md` | 1015 | `0c1555dc923ac8e631944390273dc497f478fdb828929696217ee5d9705ebbd8` | FULL / current+snapshot MATCH |
| 1 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/FIELD-MATRIX.md` | 9024 | `46c39e138d5000490411bd00761770af199827504d7e3d404a05bce524d2ed59` | FULL / current+snapshot MATCH |
| 2 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/FUTURE-SCHEDULE-ABSENCE.md` | 2980 | `ebc80f289f848639200f3f46cab489a07d5b18fb5765ef6bcaa561ca57a48fa1` | FULL / current+snapshot MATCH |
| 3 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/HOST-API-DRAFT.md` | 5202 | `b7cb74ad399938c3445325b9d98f1323559078b9555e156f870e5356aa3091d5` | FULL / current+snapshot MATCH |
| 4 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/OPEN-obligations.json` | 2839 | `b699853bc8fc25b095556fc4b0e86b9343d0bc80c55efd3f01538e8694f28426` | FULL / current+snapshot MATCH |
| 5 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/checkpoint.json` | 1376 | `e72cf3b68a5c00e49ad4536cb6f734ec2fb4b569d7411c54c81ede249a382091` | FULL / current+snapshot MATCH |
| 6 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context/tools/epoch-rts/t17-save-harness/gui/t17_save/session_transaction.js` | 69380 | `ec8c8a23d79b7f6e4fce11230b4a6f25a5c89861d2518a3a3de0b3522408e885` | FULL / current+snapshot MATCH |
| 7 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context/tools/epoch-rts/t17_save_metadata.py` | 5818 | `96d9e51e6280b1998410d7a591eaf65c11dfd11bc68c3816255201bac30bfd43` | FULL / current+snapshot MATCH |
| 8 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context/work/t17-save-allocation-consumer-integration-preparation/native-loader-closure/primaryrefs/source/simulation2/scripting/JSInterface_Simulation.cpp` | 8060 | `b9dfa717c7317c9f5731c6ed9fd4c4c4b4be12b430f9903bde5a19127932ce40` | FULL / current+snapshot MATCH |
| 9 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context/work/t17-save-metadata-preparation/code-review-v1.md` | 6732 | `49b761dbbe8ad1d14c0ddc817c95fcb8be6d5a90f1d65f23d31bff0e4923fde6` | FULL / current+snapshot MATCH |
| 10 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context/work/t17-save-metadata-preparation/completion-source-only.json` | 1756 | `4167dc102b3075f50e6d45c96e50c15b3ca4e524c3ccbca7fdfe7e61ddf64e28` | FULL / current+snapshot MATCH |
| 11 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context/work/t17-save-metadata-preparation/manifest.json` | 4534 | `85f93c30ba9484b2cce4129e0ec930b7f85449ef7d5e363da94ae8814a4b4d30` | FULL / current+snapshot MATCH |
| 12 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context/work/t17-save-metadata-preparation/python-review-v1.md` | 5646 | `8d8a6b9b8f1c43788ac91a652aa11afa8231a58c758452d68a2a1be7795b7dff` | FULL / current+snapshot MATCH |
| 13 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context/work/t17-save-network-preparation/save-source-design-20261018/typed-root-fix/SPEC.md` | 41941 | `ccaf88f75461745a82d4aba67622d38cb30cf94b522d02d025ff70fac142903b` | FULL / current+snapshot MATCH |
| 14 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context/work/t17-save-network-preparation/save-source-design-20261018/typed-root-fix/wire-schema.json` | 28262 | `412e813bae6ae3de4d35fe7fd58a8e4d1306993b7966ccf7a4c6cbdc7ad189de` | FULL / current+snapshot MATCH |
| 15 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context/work/t17-save-session-transaction-preparation/map-script-fix/code-review-v1.json` | 36970 | `bb2bdb8bbd8e295ef8a396f601a894acb4bd84df68850581e7832bead78cea5b` | FULL / current+snapshot MATCH |
| 16 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context/work/t17-save-session-transaction-preparation/map-script-fix/completion-source-only.json` | 1537 | `a296be8ebc5e142b8cdc578d9990417c27866639bee70dba6d75a413e72c0431` | FULL / current+snapshot MATCH |
| 17 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context/work/t17-save-session-transaction-preparation/map-script-fix/js-api-review-v1.json` | 60034 | `071cc8318e875f70e1d3500cfa032f5146e4fd04090d0bbc76cee0773141f832` | FULL / current+snapshot MATCH |
| 18 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context/work/t17-save-session-transaction-preparation/map-script-fix/manifest.json` | 27089 | `06a9cd6b7f8651d03daf5d57103d0aacc3025af0c92ab9c97b053d09ba0f1c9a` | FULL / current+snapshot MATCH |
| 19 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/context-bindings.json` | 4844 | `591322503804584305793e9f69ae5e063954bbffcecebdcb9c495653989c34b1` | FULL / current+snapshot MATCH |
| 20 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/official-bindings.json` | 886 | `5ca0aacaadc5b442df61f06b531a1235b8685ccc785124f5d2d52b145065cace` | FULL / current+snapshot MATCH |
| 21 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primary-bindings.json` | 8005 | `d426f3d161bb5c65deef3fffbb81352342aeb5bc099af577c9b3b10656ce46b4` | FULL / current+snapshot MATCH |
| 22 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/official-public/gui/session/selection.js` | 14510 | `55d296bddff20db103bf81f6a61a5c7f435ebfab0cb89fdd5f2206a6c7c7d049` | FULL / current+snapshot MATCH |
| 23 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/official-public/gui/session/session.js` | 25386 | `04649d5ef27fe135adcdec6e85df07296d4bb085cce2df5b9ef3feaf61a9750e` | FULL / current+snapshot MATCH |
| 24 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/official-public/simulation/components/GuiInterface.js` | 73967 | `9eaf481d5c965cc4df0cbe1fd51d2db81af162cea26c50fc67484633dd867b40` | FULL / current+snapshot MATCH |
| 25 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/graphics/Camera.cpp` | 14760 | `612b86c16a0bd62189a07ea5d767e7b0411a61e5f3edb58f24244bf6a5cbd0ae` | FULL / current+snapshot MATCH |
| 26 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/graphics/Camera.h` | 4549 | `d3da9c24b67686586a84b0f76e2199d6d04ff03fae6f5e239fcb9e170084f4f9` | FULL / current+snapshot MATCH |
| 27 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/graphics/CameraController.cpp` | 22474 | `025e6176b09730bc22f70bb9f8b14f2563e2b0852e84a00ed71ea3a97ff23d6d` | FULL / current+snapshot MATCH |
| 28 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/graphics/CameraController.h` | 3573 | `4d75277bde51e38c9c7220a49bc9026256531c1c06399dac8fd0fbca77a7bedf` | FULL / current+snapshot MATCH |
| 29 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/graphics/GameView.cpp` | 10458 | `707449873cae736f9413dc0aa743bd9575c32a9821e2f1a2c22bf0143a06f51c` | FULL / current+snapshot MATCH |
| 30 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/graphics/GameView.h` | 3102 | `6290324c12a10a09dc65a09ae174f45fe3c6a8e172a7a035c512dd420525dc23` | FULL / current+snapshot MATCH |
| 31 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/graphics/scripting/JSInterface_GameView.cpp` | 6184 | `6503fba660c6d38f2392b9e96557dd4d4d8a52871bd27f4399ec5cccd68fe64b` | FULL / current+snapshot MATCH |
| 32 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/maths/Fixed.h` | 12193 | `a79e050e2d47e44203d51fcd192527363b8169684343373259153431ae3543ea` | FULL / current+snapshot MATCH |
| 33 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/ps/Game.cpp` | 13301 | `766c220c7b8568d26ad04bcde19eeddfdc9fdd6539e56dba9fbf8d472a6e4a8a` | FULL / current+snapshot MATCH |
| 34 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/ps/Globals.cpp` | 2497 | `b774643b17b636ac84dfca6d91ef83474771128bb25991a24ae4543f37a087f7` | FULL / current+snapshot MATCH |
| 35 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/ps/Mod.cpp` | 10443 | `c8252d851566ac8a4065420f2c9a1f3cd1f5b592fc4efbecace93bfb5c00fcab` | FULL / current+snapshot MATCH |
| 36 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/ps/Mod.h` | 3765 | `3c1ad042624f0bf355afde8f9dcd6b893f9e7e58c6226da1ace2b1d1c18ae7c9` | FULL / current+snapshot MATCH |
| 37 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/ps/Pyrogenesis.h` | 1175 | `13e88bd20b945638cd4634f3760ed7fcd5464ef3efbbe38259f5b7b68d479dcc` | FULL / current+snapshot MATCH |
| 38 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/ps/Replay.cpp` | 10344 | `18d01f424d0ea6627dd92b004e70d108d0286124719cdcd188b5e79f9f3546ad` | FULL / current+snapshot MATCH |
| 39 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/ps/SavedGame.cpp` | 10000 | `6fa08d0a0f57b386484bc328ec95b41e73120b9358aeb48afc7d216f662d5267` | FULL / current+snapshot MATCH |
| 40 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/ps/scripting/JSInterface_Game.cpp` | 4759 | `ac71e18e4361f079de5295535014c4b9263a61b11c0f389fa27061c86139b7bc` | FULL / current+snapshot MATCH |
| 41 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/ps/scripting/JSInterface_Mod.cpp` | 5679 | `5a916c62580cd26d41fba808a0c81529ccd2dee5b9697f6434a5c4af4fa72eb0` | FULL / current+snapshot MATCH |
| 42 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/ps/scripting/JSInterface_SavedGame.cpp` | 4664 | `59716fec2776d0e6e9fa2f3ddecbab0abcda7379b81c2de779282487d360a42a` | FULL / current+snapshot MATCH |
| 43 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/scriptinterface/ScriptConversions.cpp` | 9827 | `7342f0a5ce4f99ca242a4d699572cec836d394aa0077db7f6720c4a413da07c6` | FULL / current+snapshot MATCH |
| 44 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/scriptinterface/ScriptConversions.h` | 4622 | `e97e4a6769b8ab74e75c973ccd8fae510e2189a3067a3b8577f36d7929745ffe` | FULL / current+snapshot MATCH |
| 45 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/simulation2/Simulation2.cpp` | 31497 | `78260ac802da5569bbf19abca7de69297788aa458f1551553b7fdf8593e096ed` | FULL / current+snapshot MATCH |
| 46 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/simulation2/helpers/Position.h` | 1316 | `342921a030bc603efb4c2158c4c7c7fe2f3b7bed3d470964cd795f48be1094c0` | FULL / current+snapshot MATCH |
| 47 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/primaryrefs/source/simulation2/system/Entity.h` | 3303 | `4bc98f0256b8173e9ddccb6e971e43bd4c20e4a96ae77d646c78b87e67c5e062` | FULL / current+snapshot MATCH |
| 48 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/manifest.json` | 12729 | `17eb3663cc51be04f880be2d2045bbbc1d5fe8fcf461cc2a82191ed9aa85e599` | FULL / current+snapshot MATCH |
| 49 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1-review-js-v1/review.json` | 48313 | `ccc2ef605452c2748626eb7305a72de5dc976636f0042d1b96395101b62315fe` | FULL / current+snapshot MATCH |
| 50 | `work/t17-save-metadata-expected-controls-preparation/source-plan-v1-review-js-v1/review.md` | 3216 | `4ec61b9d59353c6afccb21bdf96f6fb76d6b04a17a66f7ce207fd8d7569d26f7` | FULL / current+snapshot MATCH |
| 51 | `docs/empire-rts/METADATA-CONTROLS-CROSSWALK-2026-11-05.md` | 5600 | `7870cb6f94937d493c228af1d24ada0a4f8b0784602806955e10d5952fe2b951` | FULL / current+snapshot MATCH |
| 52 | `docs/empire-rts/handoff-data/2026-11-05/METADATA-CROSSWALK.json` | 9887 | `ff7570e2ec7dfa81c4770235c6f4c8a8856ad4d4797b4a060913402dd8f11034` | FULL / current+snapshot MATCH |
| 53 | `docs/empire-rts/PROJECT-ASSESSMENT-2026-11-05.md` | 11805 | `922a2439c6fb13f86f6bca4289f673ccc3581435423358d9a47f8e0ae2bdb54c` | FULL / current+snapshot MATCH |
| 54 | `docs/empire-rts/handoff-data/2026-11-05/ASSESSMENT.json` | 17288 | `531d43cf61d36dd768fa78a81a4951d2a8df9e9b776a603cca077d5b63e17ab5` | FULL / current+snapshot MATCH |
| 55 | `tools/epoch-rts/t17-save-harness/gui/t17_save/session_transaction.js` | 69380 | `ec8c8a23d79b7f6e4fce11230b4a6f25a5c89861d2518a3a3de0b3522408e885` | FULL / current+snapshot MATCH / 本人 SHA reuse 6 |
| 56 | `tools/epoch-rts/t17_save_metadata.py` | 5818 | `96d9e51e6280b1998410d7a591eaf65c11dfd11bc68c3816255201bac30bfd43` | FULL / current+snapshot MATCH / 本人 SHA reuse 7 |
| 57 | `tools/epoch-rts/t17_save_prearm.py` | 36753 | `4a892751fb9bf8924bb96b05c23695d1def1cca7e9fae070e48e2618ea1d62bd` | FULL / current+snapshot MATCH |
| 58 | `work/t17-save-host-prearm-preparation/source-scope-v1/SCOPE-RATIONALE.md` | 2490 | `3e800200307b62ad5285680fc0f65d340034c9c4ca335f0528d48939fc51c76e` | FULL / current+snapshot MATCH |
| 59 | `work/t17-save-host-prearm-preparation/source-scope-v1/completion-source-scope-only.json` | 1627 | `14a0630ddc1ee54b3a1df2a55621026504741d4a468a1f834e64303533aead65` | FULL / current+snapshot MATCH |
| 60 | `work/t17-save-session-transaction-preparation/prearm-deadline-amendment-v2/SPEC.md` | 6167 | `bbde20a000d4e3e5bdaed90073c1a9d3a886048d3e9602d46af3ed665c93410e` | FULL / current+snapshot MATCH |
| 61 | `work/t17-save-session-transaction-preparation/prearm-deadline-amendment-v2/SPEC.json` | 35505 | `2271dfdee03523a3438527bfbb8a480de6757fff8925d9d09fc5c51ea61f4009` | FULL / current+snapshot MATCH |
| 62 | `work/t17-save-session-transaction-preparation/prearm-deadline-amendment-v2/WIRE-EXTENSION.json` | 5731 | `05ee5b55406a5d88af2331782afd9ef18452e374572fbb843b8c2c9c67747baf` | FULL / current+snapshot MATCH |
| 63 | `work/t17-save-session-transaction-preparation/prearm-deadline-amendment-v2/timeline.json` | 1639 | `0c18f3ccfe551cdbf6a9986336ec1dccafab396b08fed8de1699c44805b393f4` | FULL / current+snapshot MATCH |
| 64 | `work/t17-save-session-transaction-preparation/prearm-deadline-amendment-v2/manifest.json` | 6579 | `7c07a7de8e959ecd2711a29e892eaa3a34669a80a7420ab5dbe51bc627d76ee5` | FULL / current+snapshot MATCH |
| 65 | `work/t17-save-session-transaction-preparation/prearm-deadline-amendment-v2/code-design-review-v1.json` | 7362 | `42384e8486999f79cf54e2e2fc102fdd5dc01235b1092ed540be61e324466634` | FULL / current+snapshot MATCH |
| 66 | `work/t17-save-session-transaction-preparation/prearm-deadline-amendment-v2/js-api-design-review-v1.json` | 16482 | `041858593dba7b11b6e112e64ce26fe08f40447ccc341e6fb572092f7d740630` | FULL / current+snapshot MATCH |
| 67 | `work/t17-save-session-transaction-preparation/prearm-deadline-amendment-v2/completion-design-only.json` | 991 | `ac8aa276c96afe5c6c2eec7b829d8ac9556b1cc159d5f051bec466ea436ab690` | FULL / current+snapshot MATCH |
| 68 | `work/t17-save-network-preparation/save-source-design-20261018/typed-root-fix/SPEC.md` | 41941 | `ccaf88f75461745a82d4aba67622d38cb30cf94b522d02d025ff70fac142903b` | FULL / current+snapshot MATCH / 本人 SHA reuse 13 |
| 69 | `work/t17-save-network-preparation/save-source-design-20261018/typed-root-fix/wire-schema.json` | 28262 | `412e813bae6ae3de4d35fe7fd58a8e4d1306993b7966ccf7a4c6cbdc7ad189de` | FULL / current+snapshot MATCH / 本人 SHA reuse 14 |
| 70 | `work/t17-save-network-preparation/save-source-design-20261018/typed-root-fix/source-registry.json` | 247916 | `3e6278f49bfe22d5298e8539497819fc14406319d695fe975a6e0e091995674b` | FULL / current+snapshot MATCH |
| 71 | `work/t17-save-network-preparation/save-source-design-20261018/typed-root-fix/source-registry.md` | 23583 | `5ff62cf4c16b584827f583b54f2ada09f69f665fce70168a4593c6ca82aa469b` | FULL / current+snapshot MATCH |
| 72 | `work/t17-save-network-preparation/save-source-design-20261018/typed-root-fix/code-review.json` | 20162 | `c25a6e9ac8e6c24bba5be10115119ff80c36b8b16ea81b2eaac763edf4e427cb` | FULL / current+snapshot MATCH |
| 73 | `work/t17-save-network-preparation/save-source-design-20261018/typed-root-fix/js-api-review.json` | 16383 | `3b16e62ff2e2e93c2a67ea0f26ef1124a0a064f706154120d1a4173f68fcca84` | FULL / current+snapshot MATCH |
| 74 | `work/t17-metadata-controls-design-20261105/DESIGN-v1.md` | 14580 | `d190ebf684348feba069fed69f8a92587fda378bc1fd7a9a5391c8867e1b1284` | FULL / current+snapshot MATCH |
| 75 | `work/t17-metadata-controls-design-20261105/RAW-STAGE-v1.json` | 2266 | `b641b520ab8ebb5a3273a63947edc776c3c671c21896152caefeaba6c71e9681` | FULL / current+snapshot MATCH |
| 76 | `work/t17-metadata-controls-design-20261105/FUTURE-TEST-PLAN-v1.json` | 1401 | `20374b2ee6154a67386f35f16874c90ce5da355732abdb96ee0e505f18121608` | FULL / current+snapshot MATCH |
| 77 | `work/t17-metadata-controls-design-20261105/ROOT-CAUSALITY-CORRECTION-v1.json` | 621 | `2c284dacef98520457e7ce45ce2833f60621c2fc3b6a1ee6cb551a042fca1cd3` | FULL / current+snapshot MATCH |
| 78 | `work/t17-metadata-controls-design-20261105/host-design-investigation-v1.json` | 9773 | `9c51cda36c3f0a3263775d0bb060b0c0b172c6ab5264d9b8e3412143854e8a90` | FULL / current+snapshot MATCH |
| 79 | `work/t17-metadata-controls-design-20261105/host-design-investigation-v1.md` | 17105 | `da798cc2c6a9337adadb1e1437f6e02de7eace56cdd4b032e6742a274f4486a4` | FULL / current+snapshot MATCH |
| 80 | `work/t17-metadata-controls-design-20261105/native-design-investigation-v1.json` | 12866 | `f3f3c735cfab0af0faf93fde164815477e579ccb05d60296f13133b5d75e2ee8` | FULL / current+snapshot MATCH |
| 81 | `work/t17-metadata-controls-design-20261105/native-design-investigation-v1.md` | 20319 | `45c5bb6941a008ee54790ad4191a77cdfb9bda2a393c8769defc9a7de8267aba` | FULL / current+snapshot MATCH |
| 82 | `work/t17-metadata-controls-design-20261105/context-manifest-v1.json` | 28197 | `f3ca2c1e38538f8a80921f7fa1c53898004231e4fac0b10e949a43ada649c02a` | FULL / current+snapshot MATCH |
| 83 | `work/t17-metadata-controls-design-20261105/before-r06-causality-correction/docs/empire-rts/METADATA-CONTROLS-CROSSWALK-2026-11-05.md` | 4882 | `5397dcd51de5e0811e93253db256462c068eef22e36455899abf66296c1d5c15` | FULL / current+snapshot MATCH |
| 84 | `work/t17-metadata-controls-design-20261105/before-r06-causality-correction/docs/empire-rts/handoff-data/2026-11-05/METADATA-CROSSWALK.json` | 9378 | `10960a9b2d4d7a02c40335e53df4065a5971ed41c2ce21b580fa4dce4b47e5db` | FULL / current+snapshot MATCH |

## 限制與執行範圍

- Design-only static review. No authored imports, compile, tests, helpers, profile operations, producer, probe, fixture, guard, attempt, engine, native copy or runtime execution.
- No Git transport/object fetch, commit, push, deletion, C++ edit, paid service, credit/reset/model/schedule workaround.
- Only this role progress and final reports written; all 85 frozen inputs/current sources and other workers files preserved.
- Actual runtime body/caller/realm/prototype/toJSON/native JSON provenance and full transformation/no-mutation/noFutureSchedule closure are future mandatory gates, not certified by immutable capture bytes.
- No claim of five-second runtime feasibility, native binding, archive save/load success, visual/network/release acceptance, three-party unanimity or root implementation admission.
- Prior reported usage errors retained exactly to available provenance; unavailable raw error bytes not reconstructed.

本次只讀取／雜湊／靜態分析並寫入本角色 evidence。沒有執行計畫中的測試，也沒有改動任何 frozen input 或其他工作者檔案。
