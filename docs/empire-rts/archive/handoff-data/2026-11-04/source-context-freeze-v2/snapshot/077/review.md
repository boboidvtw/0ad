<!-- Purpose: independent full JS/API DESIGN review of required fault controls. Date: 2026-10-28. -->
# Required fault controls JS/API design review v1

**BLOCK** — 1 MEDIUM design gate ambiguity；0 other blocking findings identified across full scope。

Exact manifest `e488202701017b7a5c212bf3ad8cbf5ec43d4d8b00efb3ea2c8781615a668178`；55 full snapshots／1794240 bytes 均與 expected bytes/SHA 一致，當前55原件亦 MATCH。CONTRACT SHA `616f58093179f2af073b658dd0f9ac9c88121b10eb1456425b36e155dfda82d1`；oracle SHA `c29ae4c2b9cdd74d2ad9fde92c4867aea3921a07f6b77475ba28d854cb45c271`。逐binding、15完整 review axes、各case static literal audit 見 review.json。這是完整 design/interface review，未繼承歷史 source approval 作為本 controller 核可。

**JS-DESIGN-01 — MEDIUM／blocking，CONTRACT-v1.md:51（亦參:3）**：同一 dependency sequence 將 focused tests 放在 SOURCE freeze/review 前，後句卻禁止 fixture/producer `_run/import/test` 在「these gates」前執行。契約未明確將 DESIGN 後 pure helper tests 與 SOURCE＋freshguard＋distinct later call 後三固定 producer cases 分開。Root 轉達作者僅打算先 pure helpers，屬 intent，不能修改 sealed contract 的授權邊界。現文字可能同時被理解為測試必須等其自身 SOURCE approval，或 SOURCE 前 test 範圍包含實際 consumed cases。

最小修正：保留 v1，另建契約/freeze，列明三方 DESIGN＋root readback＋獨立 source-scope 授權後僅容許實作與有限 pure helpers；不得 import producer、呼 `_run/runtime_context/Capture.build`、setup observer、建立 fixed execution fixtures/root 或執行case。實際三cases仍必須 exact current triple SOURCE、physical/runtime/resource/ownership readback、獨立 freshguard 與 distinct later root call。固定三case／順序／根／retry0／caps不變；純 helpers 不算 producer attempts。新freeze需fresh full reviews。本 review 不改作者契約，也不准開始 tests。

其餘完整 scope 判斷：

- Two families／three distinct negatives（F01 permission reserve、F02-R fault reserve、F02-W real9byte partial write）有明確 target、once injection、primary/secondary、partial retention、close generation 及 stop/no-retry 義務。F01 在 capture-inputs reservation 得 SOURCE_TYPE／ARCHIVE_AND_SOURCES；F02 在 ABORT_NODE_LIMIT／FINISH 後 fault evidence 失敗不覆 primary。durableFault 一律 false，fault snapshot 不代表 final cleanup。
- 五個 SOURCE 的 literal ordering/type/base64/size/SHA、F02 CAPTURED 的13layers／selected／complete shadowed／root paths、selectedDigest與captureId、三組 raw canonical bytes/length/SHA 均 static MATCH。23bodycopies 為13+5+5。Literal ABORT／BytesIO 是 hand-authored source model；不證 Node 真發送、limit 真觸發、pipe／child lifecycle。Unmodified Node 的 official archive SHA 不等 synthetic archive；此契約沒有執行Node，也不聲稱它接受此 synthetic CAPTURED。
- Seven private config rebind 保留 d687 Python／e710 Node／schema280、原 runtime checks 與 limits；透明 os.open/os.write wrappers 只匹配實際 root identity＋FD generation＋basename，非matching forwarding。FD一次close/UNKNOWN、raw先record後send、stderr/primary、failed evidence/finalization保留、無healthycompleted與sentinel/preimages均有明確義務；未實作的observer仍須 SOURCE review，不能自稱全host/hiddenhandles closure。
- Additional tiny caps、20s inclusive case／setup30／cleanup30／overall120 為 cooperative boundary，沒有改producer600或保證硬OS中斷。完整 schema／wire／AST/name/UTF8/UTF16／preservation/count／FINISH後recheck與manifest身份語義均不變；三負例不增加FINISH/Acorn/healthy capture coverage。

全coverage/native仍 **OPEN／NOT_RUN**：real OS permission、negative child wait/reap/pipe、fullproducer／40roots／noProxy／native caller/clone/restore、largeZIP64／actual8–64MiB／RSS、fullhost／GUIACK／freshload／profilelocks／nativefreshguard與official capture。未import producer、未跑tests/fixtures/Node/Popen/_run/bridge/attempt/engine；原FAIL/DONE/raw與sealed source/作者檔未動。
