<!-- Purpose: independent full Python/API DESIGN review only; Date: 2026-10-28. -->
# Required fault controls — BLOCK_DESIGN_ONLY

精確 freeze `e488202701017b7a5c212bf3ad8cbf5ec43d4d8b00efb3ea2c8781615a668178`；55 primary/snapshot 全 MATCH，完整 snapshot1794240bytes。CONTRACT `616f58093179f2af073b658dd0f9ac9c88121b10eb1456425b36e155dfda82d1`；oracle `c29ae4c2b9cdd74d2ad9fde92c4867aea3921a07f6b77475ba28d854cb45c271`。

[MEDIUM] PY-DESIGN-F01 — DESIGN後 pure-helper 例外未寫入凍結執行順序。

File: `required-fault-controls-preparation-v1/CONTRACT-v1.md:51`，相關4、18。

根因：dependency先列 DESIGN/rootreadback 後實作及 focused tests，末句卻禁止 fixture／producer _run/import／test 於整串 SOURCE／guard／另次toolcall 前。沒有區分 pure helper 與真正三個cases；line4亦是全稱no-test。作者／root訊息所述「DESIGN後只purehelper、no producer import/_run/execution-v1/3cases」合理，但不在 e488 frozen contract，不能用未綁定訊息替代規範。

修法：新immutable amendment/freeze 明寫 DESIGN＋rootreadback 僅允許 controller/oracle/helper source 與有限purehelpers；modulecontext保持真、不producer import/_run、不execution-v1／fixture／三cases，不將helperPASS計作F01/F02。若允許獨立unit-only hostroot，也須明列。真正fixture admission／producer import/_run／三cases只可在完整SOURCE＋currentreadback＋獨立freshguard＋另次明確call後。保留e488與歷史raw，勿改舊檔。

完整審查涵蓋55bindings、全部normative/source/test/runtimecontext、literaloracle／wire／classification、errno wrapper forwarding與restore、rootFD＋generation matching、observable close／UNKNOWN、partialwrite、firstprimary／finalization、caps／deadline、caseconsumption及scope。除上述gate語義外，未見其他blocking designfinding。

核對current d687實際路徑：F01 capture-inputs reserve EACCES確為SOURCE_TYPE／ARCHIVE_AND_SOURCES；五SOURCE後FAULT、23bodycopies及archive-auth保留。F02 validABORT先產ABORT_NODE_LIMIT primary，faultreserve或faultwrite失敗只secondary；W由原write實寫9bytes `b'{"phase":'` 後raise，一次close、不偽造有效faultJSON。terminal durableFault與faultsnapshot outputCleanupComplete皆false，不能作最終durable cleanup證明。

BytesIO含98bytes BEGIN＋ABORT；F01雖未解讀ABORT，current receive已buffer，failurepath會保留至inputraw。Oracle三組SOURCE／CAPTURED／FAULT compactraw、base64／SHA／長度、literaltable selected/layers/digest/captureId均只讀計算一致；stdout bytes1407／13363／13493。此為data-integrity審查，不是producer/helper執行。

FDgeneration只證觀察到的os.open與close attempt/outcome；ZipFile／scandir／native隱藏FD、全host、PythonOSwait／pipe均不升級。Controller source尚未存在，transparentwrapper matching/cardinality、exception-safe restoration、late deadlines、boundedledgers／recording failures仍須SOURCE審查與之後真cases驗證。三cases NOT_RUN，attempt NOT_CREATED；沒有任何code/import/tests/fixture/runtime/engine/network或source修改。只新增本 sibling JSON/MD。
