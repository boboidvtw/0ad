<!-- Purpose: independent FULL fresh required fault controls v2 JS/API DESIGN review. Date: 2026-10-29 Asia/Taipei. -->
# Required fault controls v2 — JS/API review

**APPROVE_DESIGN_ONLY** — 0 findings。完整64-context review，並非只確認舊 finding。沒有 SOURCE／實作／helper execution／三cases／native 核可。

Exact manifest `f597e8d5c5bcf214ccb6a74d7e0920914441c3dece4b6851aa895a5c4607b2d4`；64 full snapshots／2061637bytes 全 MATCH，需 current match 的原件全符合。CONTRACT-v2 SHA `8afebe343e3529236e775f9e8cbab214fc67ed419a2f7bb2a25364b242c1eef6`。Original oracle `c29ae4c2b9cdd74d2ad9fde92c4867aea3921a07f6b77475ba28d854cb45c271` 未改。逐binding／完整review axes／三組 static oracle audit 見 review.json。

原 JS-DESIGN-01 在新契約中解除；e488/v1 BLOCK、所有原報告/raw仍保留原結論。CONTRACT-v2:4 明確替換舊 blanket no-test/dependency paragraph，:12/:16–23/:27–29 將 allowed operations 分成三階段：

- A 僅 preparation/full DESIGN review；不實作、不 import、不執行helpers或producer、不建runtime fixtures。
- B 必須三方 exact DESIGN＋root physical readback＋另行限定 source-scope admission。首次 inert controller import 前先靜態檢查，要求 guarded entry、stdlib-only ordinary imports、-B且無campaign/probe/producer/observer/write副作用。只允預先登記最多24個 memory-only assertions／20秒，每input≤1MiB、合計retained inputs≤8MiB；無producer import、實FD、syscall observer、hostfiles、fixtures或case。Helper結果不是 F01/F02，也不消耗case。
- C 仍需 exact current full triple SOURCE、root physical source/runtime/launcher/resource/owner/absent-leaf readback、獨立 freshguard與distinct later capsule execution call；只有此時才可建立原v1固定execution-v1／fixtures、import unchanged producer並執行原三cases。不得改成v2 root或拿舊guard/helperPASS代替。Body entry消耗case，preflight失敗也不授reuse/retry。

完整其他scope重新核對：d687 Python／e710 Node／schema280、base protocol/schema/name/relations/limits、terminal/preservation/enumeration、current tests與coverage/history、literal fixture/oracle和故障接口。F01 capture-inputs reserve EACCES仍是SOURCE_TYPE／ARCHIVE_AND_SOURCES；F02在ABORT_NODE_LIMIT／FINISH之後的fault reserve/write失敗保留primary，W只真寫9-byte `{"phase":` 再raise，不重寫partial。23bodycopies、SOURCE/CAPTURED/FAULT types/order、full13layer/root paths/selected/shadowed、selectedDigest/captureId與raw bytes/SHA均static MATCH。BytesIO literal ABORT與synthetic archive只屬source model，不證真Node limit／pipe／child，亦不冒稱unmodified Node的official archive constant接受synthetic CAPTURED。

透明原syscall forwarding、rootidentity＋FDgeneration matching／once-close UNKNOWN、raw先record後send、durableFault=false、fault snapshot不作finalseal、firstprimary／晚期evidence/close/finalization、原caps／cooperative deadlines與stop/retry0義務均維持。全層preservation和成功FINISH後recheck／manifest transitive binding沒有弱化；此三負例不替代其完整coverage。Concrete source仍須fresh full SOURCE與之後實際case證據。

**OPEN**：完整source/runtime/producer/permission/negativechild/pipe/wait/reap/fullhost、largeZIP64／actual8–64MiB／RSS、full40／noProxy／nativecaller/clone/restore/consumer、official archive／GUI/save/freshload/profile gates。本輪只有讀檔、雜湊、JSON與literal資料靜態關係核對；未import controller/producer、未跑helpers/tests/fixtures/Node/Popen/_run/observer/bridge/engine/attempt。只新增本review JSON/MD，不改作者／source／tracking／舊BLOCK/raw。
