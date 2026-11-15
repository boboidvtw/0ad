# Python / host 完整 DESIGN review

**APPROVE_DESIGN_ONLY** — exact manifest `e73e6c48bd2a7ea31742aef7ad4b1744e6f28dbed799c39b28b25a3f9079b93a`。

85 bindings / 1,447,275 bytes：本人全文閱讀85、partial0、unread0；current與snapshot全量bytes/SHA再次讀回一致。相同SHA只沿用本人先前全文（55→6、56→7、68→13、69→14）。未借用其他reviewer閱讀。完整逐檔記錄與推理見同名JSON。

沒有需修改本freeze的blocking或nonblocking finding。核可僅限prospective DESIGN；未准入實作、測試或native。

## Original authority and correction

The original source contract requires controls causally established before this Save and proof of host receive/commit/readback order; it does not explicitly require disk commitment before Save. Independently checked original text rather than treating derived R06 preimages or investigation hypotheses as authority. The corrected partial order is coherent: immutable prelaunch plan, same-callback capture/encoding/emission before sole Save, host durable controls then expected before this transaction actual metadata semantic read. No host barrier or invented mandatory pre-Save disk roundtrip.

References: `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/HOST-API-DRAFT.md:10`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:8`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:10`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:63`。

## Exact schema and bounded parser

A new strict consumer must validate exact outer/data/identity/control/gui/camera/mod-row key sets recursively, strict UTF8 and ASCII framing, duplicate keys at every depth, finite numbers, depth256 and complete encoded-frame cap16MiB. Unknown init transformations are not automatically allowed. Object key order is not JSON value identity; array order, mods order, group count and ordered lifecycle are identity. No projection, truncation or unknown-field learning is permitted.

References: `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:47`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:49`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:51`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:53`。

## Python numeric semantics

Comparator integer parsing preserves incoming literal -0 and rejects overflow to nonfinite; comparison converts JSON int/float to binary64 bits, with bool a separate type. Principal and tuple integer domains require exact int validation, not bool or float equality. Incoming -0 and +0 must remain distinguishable and ordinary 1/1.0 compare by JS Number semantics where schema permits. Existing prearm strict_json/same is unsuitable as an unchanged metadata value parser: it parses integer -0 as zero and uses Python equality for signed float zeros/type differences. This is a future SOURCE obligation, not a current DESIGN defect: the proposal explicitly adds a separate parser/materializer and preserves old prearm. Capture canonical JSON follows the actual JSON serialization path, which may serialize a source JS negative zero as 0; this cannot be used to normalize a received JSON -0 or round camera values. No claim of arbitrary pre-serialization IEEE bits surviving ordinary JSON.

References: `tools/epoch-rts/t17_save_metadata.py:78`, `tools/epoch-rts/t17_save_metadata.py:92`, `tools/epoch-rts/t17_save_metadata.py:112`, `tools/epoch-rts/t17_save_prearm.py:59`, `tools/epoch-rts/t17_save_prearm.py:114`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:80`, `work/t17-metadata-controls-design-20261105/RAW-STAGE-v1.json:61`。

## Tuple, once, stage and provenance

All ten identity fields join independently fixed boot/case/phase/source/seed/checkpoint/ordinal/archiveName/S. Origin five transactions and each load one transaction require exact controls-to-SAVE_CALL/SAVE_RETURN/REQUEST_READY/ACK bijection with no gap/duplicate/late/extra. [1,1], nonce, schema, source hash and stage labels are correlation data, never native attestation. Host must associate owned PID stdout and actual loaded producer/body/realm/caller/source guards; unavailable proof blocks.

References: `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:28`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:49`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:55`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:59`。

## Independent static plan and full initAttributes

The immutable factory may consume fixed contract and independently checked source/runtime/profile inputs; never decoded actual metadata. Full base mapType/map/script/settings/PlayerData/binding plus positive source-authorized transformation schema is required. A complete final initAttributes authority is explicitly OPEN; materialization refuses without it. Capturing a getter does not authorize unknown keys. Replay rewrites timestamp/version/mods for each fresh load, so origin actual metadata cannot supply new expected values. Nested timestamp remains exact; only outer metadata time uses its separate original epoch interval.

References: `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/HOST-API-DRAFT.md:8`, `work/t17-save-metadata-expected-controls-preparation/source-plan-v1/HOST-API-DRAFT.md:18`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:24`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:26`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:36`。

## Origin verified ancestry and actual read boundary

Fresh load may use only previously independently verified origin-control ancestry. Existing origin archive copy/hash/CRC/readback and official StartSavedGame reading already verified origin metadata are compatible with this transaction gate. The host must not semantically read the new actual metadata before expected commitment or use load bootstrap parsed metadata as controls. That distinction avoids both actual-to-expected contamination and an impossible ban on normal saved-game loading. Load camera fixed/float restoration must be checked through current getters and origin lineage, not assumed byte-equal in advance.

References: `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:38`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:63`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:65`。

## Six full fields and native producer contract

GetEngineInfo must be genuine and agree with actual binary and all five complete four-key mod records in order; package version and compatibility projections are insufficient. Native GetPlayerID before/after must be literal1 and remain distinct from viewed ScriptCall caller. Groups come from ten source-fixed empty records, with actual group capture checked against independent plan. Camera maps GetValue position/rotation/zoom to six exact finite JSON Numbers without epsilon or nominal-value substitution. Description derives solely from immutable phase/checkpoint literal and original Save argument authority.

References: `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:32`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:34`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:35`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:37`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:38`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:39`。

## No mutation or hidden future schedules

Detached lexical control values/immutable encoded strings must not freeze shared live objects or execute unknown accessors/toJSON/customSerialize. All native clone/constructor/prototype/serialization/getter/mutator closures remain required between A-controls-QO-B or L0-controls-QL-L1. Full metadata equality cannot prove absence of future schedules when both sides share contamination. All40 gameplay roots, legitimate Timer/native events, queuecount0 and Complete/command evidence remain mandatory, without discarding real gameplay state.

References: `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:20`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:36`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:41`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:43`。

## Evidence exclusive file lifecycle

Exactly the two allowed leaves per original tuple ordinal, metadata-controls.raw.json and expected-metadata.raw.json, reside in host case evidence, not native profile/moddata. Reserve with O_EXCL/O_NOFOLLOW0600; preserve partial bytes on failure; fsync, once-close and postclose original length/SHA readback precede commitment. An uncertain close is UNKNOWN and must not be retried; a secondary close/readback error must not mask the first failure or turn partial output into success. Existing prearm first-error/once-close machinery is relevant context, not blanket approval of new lifecycle integration. No overwrite/rename/delete/alternate leaf or raw reconstruction. Parent/path/inode ownership and exact derived destination assignment still need actual SOURCE review; no existing directory implementation is certified.

References: `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:61`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:67`, `tools/epoch-rts/t17_save_prearm.py:245`, `tools/epoch-rts/t17_save_prearm.py:266`, `tools/epoch-rts/t17_save_prearm.py:370`, `work/t17-metadata-controls-design-20261105/FUTURE-TEST-PLAN-v1.json:18`。

## Raw preservation and aggregate capacity

Preserve complete received stream with offsets/length/SHA and join each original controls frame to exact evidence. 16MiB frame cap includes envelope, expected retains comparator16MiB/depth256, and controls share unchanged64MiB case receive cap. Two retained files plus original stdout copies must fit original aggregate retention limits; per-frame allowance is not an entitlement to multiply capacity across five records or six cases. Overflow/partial/late bytes stay FAIL or UNKNOWN, with no cap increase, dropped evidence or truncation. Final reader/drain/reap/readback integration is explicitly a future SOURCE gate.

References: `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:53`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:59`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:61`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:67`。

## First error and expected commitment state

A new state machine must not set expected-committed after only emission, parse success, open/write return, buffered fsync claim, or in-memory digest. Both actual evidence files require completed write/fsync/known once-close and actual postclose readback. Any unknown state blocks dependent actual reads/ACK. Preserve the primary exception plus secondary uncertainty and retained partials, without retrying ambiguous side effects. These requirements are specified by design failure rules and targeted firsterror test obligation; they are not claimed to be implemented.

References: `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:59`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:61`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:63`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:80`, `work/t17-metadata-controls-design-20261105/FUTURE-TEST-PLAN-v1.json:18`。

## Same callback and original deadlines

The only prospective delta is synchronous read-only capture after original A/first L0 and before original SAVE_CALL/sole Save. Capture/encode/emit error is sticky and prevents Save; emission does not assert delivery. No warm getter to replace L0, no extra turn, flush, wait, retry, second Save or host barrier. All new work shares D=t_arm+5000000000ns and original600/6x90/prelaunch30/stop80/cleanup90/enginecutoff540/final600. Runtime feasibility and noninterruptible IO hard bounds are NOT PROVEN; no native result is demanded as a prerequisite to reviewing this prospective design.

References: `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:16`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:18`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:43`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:59`。

## Old reader compatibility and source ownership

Current prearm scanning/endpoint behavior is not silently upgraded by declaring a new stage. A complete new reader/lifecycle and derived GUI source must be assigned and reviewed separately; original SOURCE-approved GUI/comparator/prearm and seals stay preserved. Exact new source filenames/ownership are a future root assignment, not permission for this reviewer to implement or select runtime paths. Absence of implementation is intentional for DESIGN_ONLY and not an additional circular native gate.

References: `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:67`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:71`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:73`。

## Typed root and historical review boundaries

Personally read complete original48 context, prior reviews and current typed-root registry; prior CODE/JS reports are context, not substitutes for my reading. Typed profiles preserve40 ordered gameplay roots plus separate command/return/error contexts, full descriptors/prototypes/aliasing/ordered collections and absence semantics; unknowns fail closed. Metadata JSON value comparison has its own finite JSON semantics and does not replace the typed graph codec. Existing prior design/source approvals are not inherited native approval.

References: `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:4`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:16`, `work/t17-save-network-preparation/save-source-design-20261018/typed-root-fix/source-registry.md:1`。

## Bounded tests and authority laundering

The16 future named assertions,8MiB retained inputs,1MiB/model and20-second model budget are prospective only. Targeted structural refusal/order/fault tests may check new code after separate admission; no old24 fault helpers, native getters/producer/fullhost/fixture/engine/cases are executed. Every structural expected result stays native_verified=false/runtime_bound=false. Arbitrary JSON/frozen objects/hashes/public factory labels cannot close body/caller/provenance or fullhost BLOCK.

References: `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:73`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:75`, `work/t17-metadata-controls-design-20261105/FUTURE-TEST-PLAN-v1.json:22`。

## Admission and final decision

No material internal contradiction requiring DESIGN change remains after complete independent review. Approve only this exact prospective DESIGN: all three complete DESIGN reports and root explicit source assignment must precede bounded implementation; all complete SOURCE reviews/root readback and full current transforms/getter/caller/realm/clone/mutation/runtime/profile/body/raw/order/timing/archive/queue/fullgraph closure precede native admission. Eleven technical obligations remain OPEN, R07 PARTIAL, original guard STOP/FAILs unchanged. This verdict cannot certify five-second native feasibility or clear R08/fullhost BLOCK.

References: `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:71`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:75`, `work/t17-metadata-controls-design-20261105/DESIGN-v1.md:83`。

## 限制與下一步

十一項技術義務仍OPEN；R07仍PARTIAL；原guard STOP、FAIL、raw與seals保持原判定。先由root消費三方正式設計報告並另分派source ownership；實作後仍需完整三方SOURCE review及root readback。完整來源與runtime/profile/guard/5秒/queue/fullgraph等門檻未關閉前，禁止native准入。

本次未import、compile、執行authorcode、tests、helpers、producer、profile、probe、fixture、guard、engine或attempt；無network/commit/push/delete/C++/付費/reset/換model。僅寫本人Python progress及本正式JSON/MD；未改85輸入或他人檔案。先前quota中斷保留，同task/settings續作。
