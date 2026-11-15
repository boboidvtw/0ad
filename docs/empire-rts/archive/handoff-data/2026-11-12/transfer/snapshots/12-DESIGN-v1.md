<!-- Purpose: prospective R07 metadata-control causal capture DESIGN; no implementation or runtime authority. Date: 2026-11-06 Asia/Taipei. -->
# R07 metadata controls：同 callback pre-Save capture／host 先 controls 後 actual（DESIGN ONLY）

本 v1 是新的待審設計，不是實作准入、三方核可或 native acceptance。原 17eb/48 plan、ccc2ef60 單一 JS DESIGN approval、十一 OPEN 義務、85f93 comparator 與所有既有 FAIL/STOP 原件不變。原 guard afb3339b 一次刷新仍待具體決策，本設計不涉及該 actor 或原三 case。

## 1. 精確問題與衍生表述更正

原 HOST-API-DRAFT.md:10 要求 controls 由 source 因果鏈在該 Save 前建立，且 host commit/readback/接收順序必須實作證明。原 FUTURE-SCHEDULE-ABSENCE.md:12 要 independently precommitted controls。它們沒有逐字要求 host 的 disk commit/readback 必先於 Save。R06 crosswalk 的 host-before-Save 文字是本次根端多加的更強解讀；它不是原規範，不可拿來製造原契約不可能的 BLOCK。前版、調查初步假說與更正理由均保留。

本提案精確分開：(a) launch 前 source-owned static plan 固定；(b) 同步 GUI callback 中、唯一 Save 前，獨立 getter controls 被擷取、驗證、轉成不可變原字串；(c) 同 callback 立即原唯一 Save，不等待 host；(d) host 在讀取任何 actual metadata 前，先接收完整 controls、持久化及讀回、固定 expected。不能改成 actual→expected。Source 因果控制存在於 Save 前，host durable commitment 與 actual-read 另有明確順序；並不謊稱 (d) 發生在 Save 前。

若任何完整獨立 reviewer 認為原規範要求更強的 host-before-Save 因果證明，須以原 authority 精確引用 BLOCK，而不是引用 R06 推論。未澄清時不實作。

## 2. 不變項與 prospective delta

原 context exact 六 keys、request/ACK/boot/prearm WIRE、phase/case/ordinal/names、40 roots、A/B/L0/L1、native queue0、normal commands、Complete count、windows、600/6×90/30/80/cleanup90、42 then conditional7/retry0及 D=t_arm+5,000,000,000ns 一律不變。Freshload FIRST native action仍 pause；upstream restoration 後第一個完整 graph 就是 L0，不能用 warm query 或另一份 graph 替代。沒有 extra turn、flush、poll/wait、host barrier、第二 Save、rearm、額外 branch 或新 engine attempt。

唯一 prospective 功能 delta：在原 GUI transaction 已取得 A 或 L0、決定固定 phase/checkpoint/ordinal/name 之後、原 SAVE_CALL/SaveGame 之前，新增同步 read-only metadata-control capture；以既有 ordered stdout emitter 加一種新的 external raw stage METADATA_CONTROLS_CAPTURED_V1。這是明文的新 raw-stage schema，尚未部署；不是既有 request/context/ACK 新 key，不在 native profile 新增檔案／inventory exception。

該新增 native getter 呼叫、record producer、外部 host consumer 都須在後續 exact SOURCE review 計入完整 caller/realm/read-only/serialization/mutation closure。尤其 A→controls→QO→B / L0→controls→QL→L1 不可因 getters 或 capture 而改 serialized graph/queue/native state；來源未閉合或實際不等均 BLOCK/FAIL。只說 getter readonly 不構成證明。

## 3. Prelaunch static control plan

由 source-owned host factory從固定 contract/case tuple與獨立實際 source/runtime/profile guard inputs建立 immutable plan；不接受 actual archive/metadata作參數。Plan保存原完整 campaign/case/source/seed/phase/checkpoint/ordinal/archiveName 對應、literal principal1、description factory、五 mod完整四欄records/order、origin base initattrs及完整允許 native transformations、origin/load control ancestry、原 runtime/source/profile identities。Known static values必從既有 frozen primary或未來當次實讀取得，不猜 compiled engine_version、不把 package version當 native version。

Static init base含 mapType/map/script/settings及完整 PlayerData／T17SaveReceiptBinding，不能僅投影已知七欄或把未知 startup writes 當合法。每個 native/static transformation 都須正向source authority及 exact schema；尚未 source-resolve的完整 final initattrs layout 是 OPEN admission item，不能由觀測 getter 的未知 key 學成 expected。這個 proposal不虛構已閉合的 transformations manifest；缺它時 host materialization必拒絕。

Plan與 capture 資料中的 nonce/source SHA/binding只是資料 join，不自認 native attestation；actual PID/body/source/profile provenance需 R08 實際守門。

## 4. 同 callback 的 source-owned capture

以真 native principal1／原 viewed-player與ReadSaveContext binding邊界進入。來源固定的新 capture producer只從已鎖 actual current GUI/native call chain讀 Engine.GetEngineInfo、Engine.GetPlayerID、真 official GetInitAttributes及 native camera getters；不從 saved archive、metadata、caller supplied expected dict或 simulation future schedules取得值。

- engine_version/mods：GetEngineInfo native body與SavedGame來源對應；完整 mods四 keys/order對 prelaunch plan，不用 compatibility projection。實際 binary/build與enabled mount/body關係仍須 source/runtime closure。
- playerID：literal1與capture前後 native GetPlayerID、viewed/querycaller原邊界核對；payload.player不能授權。
- initAttributes：真 GetInitAttributes回傳完整值；native viewed caller/realm/cross-compartment clone及全 producer/mutator/descriptor/Prototype/toJSON/stringify effects須 closure。Source static base逐值核；origin與每次 freshload各自保留 Replay產生的 nested timestamp/engine_version/mods，不拿原 archive三值當新 expected，不將 outer time例外遞迴用到nested timestamp。
- gui.groups：expected來自source固定10個 exact {groups:{},ents:{}}；擷取時核實 actual source-owned groups 與獨立 plan一致。這是可觀測 before-Save control，不是從actual metadata投影。所有 group inputs/hotkeys/human/prototype/native serialization effects仍須 closure。
- gui.camera：精確 native GetValue() float getters，mapping position.x/y/z→PosX/Y/Z、rotation.x/y→RotX/Y、zoom→Zoom；不使用 GetSmoothedValue、nominal0.6、epsilon／rounding。Load upstream restore的fixed/float重轉另由當次getter及已驗 origin控制 ancestry核對，不先假定相等。
- description：僅由 immutable phase/checkpoint定義 T17 save origin <checkpoint> 或 T17 save load <checkpoint>；與實際唯一 Save argument同源但不同於archive讀取。

在 source-owned private lexical closure建立 detached control value及其 canonical ASCII JSON原字串。不得 freeze/mutate共享 g_Groups/InitAttributes/native graph；不能執行不明getter/toJSON/customSerialize來製作detached copy。Full encoder與轉換來源必完整審查。字串不可變不等 native provenance或安全閉合；沒有來源證據即 BLOCK。

新record必在同callback原 SAVE_CALL stage之前，由原 emit路徑送出；一旦 capture/encode/emit錯誤就 sticky BLOCK並不呼叫Save。emit成功只證producer呼叫沒有當時throw，不證host已收到／磁碟durable；buffered/late/lost raw由host門檻使FAIL/UNKNOWN，不加flush/wait。原唯一 Save保持原順序，getSavedGameData／nativeSerialize間不得有未審mutation；不存在expected失敗後第二次擷取或重新Save救PASS。

## 5. External raw stage exact schema

沿原 frame prefix T17_SAVE_GUI、strict ASCII JSON與原行結尾，outer exactly {kind,data}；kind literal METADATA_CONTROLS_CAPTURED_V1。data exactly schema,identity,principalBoundary,controls（四 keys）。schema literal T17_METADATA_CONTROLS_V1。

identity exactly campaignNonce,caseNonce,sourceManifestSHA,seed,caseID,checkpoint,phase,transactionOrdinal,archiveName,S。值與原boot/transaction tuple相同；capture在已觀測固定S／paused內，不能自己宣告runtime proof。principalBoundary exact [1,1]，兩項都是當次native getter觀察；原context/view caller額外邊界原封保留。

controls exactly engine_version,playerID,mods,initAttributes,gui,description，與既有 comparator expected六欄同型；playerID必 literal int1。mods完整array各exact mod/name/version/ignoreInCompatibilityChecks；gui exactly groups/camera，groups exact10項各groups/ents empty objects；camera exact PosX/PosY/PosZ/RotX/RotY/Zoom，每項finite JS Number。initAttributes完整 schema由第3節source-resolved plan權威核定；未知 transformation/key不被本proposal豁免。

Raw record外層cap=16MiB，包含encoded envelope全部bytes，depth≤256、strict UTF8/duplicate keys/unknown keys/nonfinite拒絕。既有case完整received cap64MiB和各deadline不變，controls佔原總預算，不增加cap。Controls expected本體仍用既有comparator16MiB/depth256 gate；本體可小於外framecap，超任何cap停止不truncate。

Origin每transaction一筆，共5筆；freshload每branch唯一1筆。No duplicate/gap/mismatch/wrongorder/late/extrarecord。Sequential record identity、原 SAVE_CALL、SAVE_RETURN、REQUEST_READY及ACK/full raw lifecycle必bijection；stage名、payloadnonce或控制旗標均不能代替 source實際執行與ownedPID stream關係。

## 6. Host 接收／persist／expected／actual 明確順序

Host既有外部raw recorder保存全部received bytes、完整offset/length與causal records；先驗exact frame／預承諾tuple／independent control producer provenance與source-resolved static constraints。buffered record允許較晚收到但仍須完整無歧義且所有工作在原D與outer cutoffs內；沒有及時完整record就FAIL/UNKNOWN。

在打開／解碼任何 origin或roundtrip actual archive metadata前，host將controls完整原frame bytes與解碼expected六欄分開以 fixed evidence filenames O_EXCL/O_NOFOLLOW0600記錄（host本身的case evidence tree，非native profile/moddata；prospective file allowlist限每originaltuple ordinal的 metadata-controls.raw.json 與 expected-metadata.raw.json）。partial寫入、fsync/once-close/postclose length+SHA readback任何不確定都停止；保留partial，無覆寫/rename/delete或alternative leaf。與原raw recorder來源offset/SHA一一join，完成後才標記本次 expected commitment完成；它不是native/case PASS。

Prelaunch plan→source causal preSave capture→原Save→host controls receive/persist/readback→materialize expected→host expected persist/readback→首次actual archive metadata read→既有85f93完整比較，是唯一允許partial order。若existing integration提前開actualarchive、用actual metadata補timestamp/camera/mods、把原archive當load expected權威、或不能證順序，即BLOCK。Host可在controls接收前觀察process/stdout/request existence，但不得先讀actual archive metadata以建立expected。Source/runtime/profiles/actual body/realm/current caller與latebytes的完整證據仍R08另gate。

此處 host actual-read gate限定本transaction拿來與新expected比較的metadata語義讀取。先前已由獨立origin controls驗證的origin archive／metadata仍可作官方StartSavedGame載入資料；load前既有完整archive hash/copy/CRC/readback不被本提案取消。不得把該已讀origin metadata或load bootstrap解析值拿來建立本次fresh controls／expected。原native StartSavedGame正常讀origin metadata不等host由actual自建expected。

同callback內新GUIstage不是對host目前stage reader的暗中相容；新的完整reader/lifecycle整合、exact file保留量、錯誤／UNKNOWN保存須新SOURCE評審。若2個evidence文件加既有stdout份數無法在原既有aggregate bounds內保存，FAIL，不提高cap或丟raw。Replay disk start既不作必需controlprovider也不需要flush/wait。

## 7. SOURCE-only 實作階段與未准入項

A：現在僅寫本新設計／schema/test plan/context與獨立完整CODE/Python/JS DESIGN review。三份報告綁完整exact new manifest與全部current normative primary/source；任何BLOCK保留。三核可後root另明確限定source ownership才B；本proposal不自行授權實作。

B（future, not admitted）：只新增獨立 metadata-control structural parser/materializer source、GUI causal capture producer／受影響transaction derivation與針對新行為的tests；不覆寫原SOURCE-approvedGUI／comparator／prearm或舊sealedsource。實際新檔名和新派生GUI入口由root source assignment固定，保留前版與delta。輸入是實際verified control bytes與source-owned staticplan的結構規則；任意 JSON/typed object/frozen dataclass/hash不能宣稱native binding。Model tests只證結構／拒絕／順序狀態模型，不執行native getter/producer、fullhost、fixture、engine或原cases。任何結構性EXPECTED值輸出必永遠 native_verified=false/runtime_bound=false，真正native provenance由R08守門而不是任意public BindNative dict factory。

全source實作後，完整CODE/Python/JS SOURCE reviews與root readback仍各自必需。Full current transform authority、actual getter/caller/realm/clone/read-only/noFutureSchedule/profile/source-runtime/producer/body/raw/phase/order/5秒／actual archive/count0/fullgraph與全部R08已知未解項閉合前，禁止native copy/Popen/Save/engine/case或native acceptance。不得以本DESIGN或modelPASS清R08/fullhost原BLOCK。No stub產生假的native receipt，No new paid/reset/model/schedule/commit/push/delete/C++。

## 8. 三方評審必答與完成邊界

CODE：新stage的source/dataflow/原權威precommit解讀／getter到Save與hostexpected到actual序列是否完整；來源與serialization mutation closure義務是否保留；是否存在不必要scope／偽授權。
Python：strict raw/parser/value semantics（含int/bool、binary64/-0/duplicates/depth），exclusive evidence partial/closeUNKNOWN與first error，tuple/once/order、原限制與模型邊界、host是否可能先讀actual。
JS/API：真GetEngineInfo/GetPlayerID/GetInitAttributes/clone/camera GetValue call contract，freshload FIRSTpause/L0/noWarm/noWait/soleSave、samecallback/precommit causal path、rawstage不污染serializedstate，原request/ACK/context完整保留。

只能給APPROVE_DESIGN_ONLY或BLOCK_DESIGN。APPROVE不認證native可在5秒內完成、不代表74來源body實際載入、binary與HEAD完全同源或完整getter/mutator實作閉合。十一技術義務目前仍OPEN，本次僅形成可審查的SOURCE設計，R07整體仍PARTIAL。
