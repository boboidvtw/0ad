<!-- Purpose: review route and parallel ownership. Created: 2026-10-25. -->
# Ownership / route

此資料夾只 DESIGN。Root 安排 fresh full CODE+Python design review，Node schema/Acorn/IPC另JS。Root讀回完整reports與當前manifest全match並明確授implementation後：

- save_graph_reader：NEW t17-save-five-mod-capture.py、NEW test-t17-save-five-mod-capture.py、NEW implementation-python evidence。Python owns all output、authreader、zipfile/runtime limits/protocol schema。
- save_admission_collector：NEW t17-save-five-mod-source-inventory-v2.cjs、NEW test-t17-save-five-mod-source-inventory-v2.cjs、NEW implementation-node evidence。OnlyAST+strictdecode+spawn/NDJSON，不改oldsource，不直接寫source/artifacts。
- Root：兩slice fullcurrentfreeze+完整獨立 CODE+Python+JS/API review，舊反例retained驗證，新真candidatecapture之授權/guard決策。不得以任何單片approval當consumer/export/native closure。

Node/Python schema以PROTOCOL.md/LIMITS.json為唯一接口；author若遇zipfile/dirfd平台差異或schema缺項先報root並保存gap，不私改limits/gates。正式工具不暴露測試fault-hook或任意archiveexpected，單元測試以import/privatefixture/harness注入；source implementation需審constructor/CLI public surface避免model-only proof。

Acceptance:所有原3核心場景archiveauthority/symlinkescape/concurrentoverwrite都有新真main/OScontrols；包括每返回chunk的immutabledata驗證與nooverwriteroot/allfiles；實際source/API/runtime依賴精確凍結。全部仍candidate sourcebytes/AST evidence；actualglobal unique export/reader containers/freshrealm/jobs/hotload/intrinsics/sourceguards/5mods profile remainOPEN，Admission unchangedbeforeprobeBLOCK。

Design-fix-v1 normative interface: ANALYSIS-SCHEMA.json plus SOURCE-RELATIONS.json plus LIMITS.json and PROTOCOL.md. Preserve vfs exactly and correlate with private selected[index]; do not strip/derive it as an undocumented normalization. Original CODE approval is historical design-only; fresh three-way full design review is required after this fix. New SPEC remains reference-only until those approvals and explicit implementation authority.

Design-fix-v2 NAME-PRODUCERS.json is part of sole shared interface. Node owns actual escaped/astral identifier producer controls; Python owns shape/unit/capture correlation, not an invented JSdecoder. Both must preserve these exact field meanings.
