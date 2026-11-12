<!-- Purpose: durable R07 full-design review continuation and quota recovery. Date: 2026-11-06 Asia/Taipei. -->
# T14–T18：R07 metadata新設計完整三方審查中，整體PARTIAL

Actual repo /Users/liyungchih/Documents/Codex/2026-09-06/new-chat/work/0ad。原canonical與Nov5移轉anchor不改；新工作先讀 work/t17-metadata-controls-design-20261105/ 最新 current-checkpoint-vN.json、三個design-review-ROLE-progress-vN.json及其後續正式report，完整DESIGN-v1/RAW-STAGE-v1/FUTURE-TEST-PLAN與85-binding design-manifest-v1。既有Nov5成果評估/18工作包仍適用；R06文件對照DONE，5主功能任務/17工作包未完成。

使用者要求繼續完成計劃，額度不足等恢復後自動接著做。先live get_usage_limits，沿相同三review tasks/settings續未完，不能以新role/model繞quota。原native/host調查兩task先前usage-limit errors保留在checkpoint-v2；Nov6 02:57台北heartbeat後live ordinaryAllowed true/primary0%/weekly77%/credits0/reset0，這是歷史不是後續保證。兩調查已各自落盤JSON/MD與完整親讀/部分/未讀位置，非三方DESIGN核可。

R06較強文字「host必Save前落盤」不是原HOST-API:10/FUTURE:12明文，已保preimage更正。可審候選是同callback真getter capture/immutable encode先唯一Save，host保存controls與固定expected後才讀actual metadata；不新增wait/turn/flush/Save、不延5秒。新stdout raw stage與host evidence檔名僅prospective設計，尚未部署。來源/realm/body/prototype/serializer/mutation/順序/原D與所有R08義務仍必證；十一技術義務關閉0。

新freeze 85bindings/1,447,275bytes，manifest SHA e73e6c48bd2a7ea31742aef7ad4b1744e6f28dbed799c39b28b25a3f9079b93a。三fresh必要獨立review：/root/r07_design_code_review、/root/r07_design_python_review、/root/r07_design_jsapi_review；固定design-review-CODE/Python/JSAPI-v1.json與MD。每個都需全文85 contents、current+snapshot逐SHA/bytes、exact role/inputManifestSHA、完整functional reasoning/findings/coverage；hash MATCH不等全文核可。任何source/design改動需新exact packet及必要fresh完整review，舊BLOCK不覆寫。三DESIGN核可且root實讀後還需另root source-scope assignment才實作；此時不import/compile/tests/helper/producer/fixture/engine/guard/attempt。

原fault controllerfd1948/SOURCE d69d三核可與sampler/wrapper限定SOURCE核可保留，原fixedguard afb3339b及過期STOP不變；R01一次guard刷新/替換仍待人類同一具體決策，不反覆追問、不因heartbeat或一般接續授權自行刷新。rootreport/capsule/EXEC與3cases仍NOT_CREATED/NOT_RUN。24helpers及所有DONE cases不重跑；原T14 PARTIAL/SQLite Insufficient data、全部FAIL/STOP/UNKNOWN/raw/seals保持。兩種R07不要混淆：舊tiny bridge R07已耗用DONE；本R07是Nov5計劃work package metadata design。

既有同id0ad-t14 ACTIVE每5h、target本chat；只prompt/updated_at改，readback在此新work目錄。沒有新排程。只通知有意義進展/完成/失敗/必要決策，其餘保持安靜。排程需要機器開機/app運作，不能保證額度恢復瞬間開始。最新GitHub fb4564363僅上次已核准文件資料更新；本輪本機source設計，不再commit/push。無C++/刪除/外部訊息/發布遊戲/新付費/credits/reset/換model。原機dirty/work/raw與74早期調查snapshot、85新freeze都保留。
