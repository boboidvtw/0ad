<!-- Purpose: GitHub-readable checkpoint and evidence index. Date: 2026-11-12 Asia/Taipei. -->
# T14–T18：2026-11-12 交接與 metadata DESIGN 閱讀進度

整體 **PARTIAL**。本包是文件與原樣文字證據歸檔，沒有新遊戲功能或原生驗收。

- [目前狀態](STATUS.json)／[最新 checkpoint v12](metadata/current-checkpoint-v12.json)／[閱讀歸屬 v6](metadata/root-independent-read-progress-v6.json)／[逐檔 bytes 與 SHA256](FILES.json)。
- [85-binding 原 manifest](metadata/design-manifest-v1.json)，SHA `e73e6c48bd2a7ea31742aef7ad4b1744e6f28dbed799c39b28b25a3f9079b93a`，1,447,275 bytes。85 原檔與 freeze 的170檢查 MATCH；原樣資料在 `metadata/freeze/`，一律加 `.txt`，原路徑與 bindingIndex 由 FILES 映射。原始 manifest 的相對路徑仍指向原機 checkout，沒有改寫凍結內容。
- 根端歷次合計完整閱讀71/85、尚缺14；本 chat 本人完整24、部分1、未讀60。歷史閱讀不能借作新根端親讀。CODE v10／Python v6／JSAPI v13 僅 IN_PROGRESS；三方正式 JSON/MD 均不存在，沒有代簽核可。
- [DESIGN](metadata/DESIGN-v1.md)／[raw-stage 候選](metadata/RAW-STAGE-v1.json)／[未執行測試計劃](metadata/FUTURE-TEST-PLAN-v1.json)。controls 由 source 在 Save 前因果建立；host 保存 controls 與獨立 expected 後，才首次語意讀取當次 actual metadata。這是待審設計，11技術義務仍全部 OPEN。
- [交接 anchor](transfer/current-state.json)／[child MATCH receipt](transfer/child-readback.json)／[父 chat 排程移轉收據](transfer/migration-readback.json)。15 originals＋15 snapshots MATCH。只歸檔既有 `0ad-t14` 移轉證據，沒有新增或修改排程。

後續先補根端未讀及必要原契約，再由原三 reviewer 完成 exact manifest 的正式 DESIGN 報告，根端獨立核對後仍需另作 source-scope 准入。此包不允許 import/compile/tests/helpers/producer/fixture/guard/attempt/engine；未執行任何這類工作。SaveGame void 返回與 SAVE_RETURN 標記不能取代 archive 證據。

原 guard `afb3339b` 與過期 STOP 不變，一次刷新仍待具體決策；三正式案例 NOT_RUN、24 helpers 已耗用、全部 FAIL/STOP/UNKNOWN/raw/seals/T14 PARTIAL/SQLite Insufficient data 均保留。SOURCE-v2及sampler/wrapper既有限定來源核可不重做、不升為native核可。

原機的完整 work/raw/seals、未提交實作、runtime binaries、private profiles 及 automation TOML 不在本包；不可據此刪除原工作目錄或聲稱可執行備份。歷史 checkpoint 裡的較早狀態與錯誤原樣保留，現況以 STATUS/v12 及原始正式報告為準。[先前評估資料](../2026-11-05/README.md)與 repo 原授權仍適用。
