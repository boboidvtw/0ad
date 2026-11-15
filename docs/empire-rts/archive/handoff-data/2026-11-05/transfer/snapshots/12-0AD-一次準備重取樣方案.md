<!-- Purpose: reviewable one-time readiness refresh decision. Date: 2026-11-05. -->
# 0AD：一次準備檢查重取樣方案（待核准）

三方 SOURCE-v2 已核可；三個正式案例均 NOT_RUN。第一次獨立檢查完成後，根端因生成長工具呼叫耗時約79秒，超過原60秒有效期，已正確停止。這是本次編排失誤；原 guard、失敗工具紀錄與 STOP 都完整保留。

## 本次申請的具體範圍

只核准一次新的獨立準備檢查，以及一次替換固定動態檔案 `freshguard-v1.json`。替換前保留原檔完整 bytes、SHA、版本與失敗紀錄；不得刪除原證據。新取樣使用同一位已授權的獨立 Python reviewer，不新增角色或切換模型。

通過後立即使用已寫好且經獨立審查的 root sampler v5；再次核實原來源、runtime、資源、owner 與原執行目錄不存在。只有全部原門檻通過，才在另一個明確工具呼叫中，以 wrapper v2 啟動原 controller，單次依原順序執行既定三個案例。任何檢查失敗、逾時、寫入不完整或 UNKNOWN 都停止，不自動再取樣或重試。

固定檔案位於實際 repo：
`work/t17-save-five-mod-inventory-repair-preparation/required-fault-controls-implementation-v1/execution-preparation-v1/freshguard-v1.json`。
原 SHA：`afb3339b0471f8ecd857957c18752dafc291854e6cd4d54f9c5b6baf4d6257f5`。
原檔備份與 STOP 位於 `work/t14-t18-resume-20261104-current/`。

## 保持不變的限制

- 同一 execution-v1 根目錄、原案例 ID、順序、caps、retry0；不換名、不新增案例、不重跑24個 helpers。
- 有效期仍為 age≤60秒、到期剩餘≥120秒、TTL120–600秒；不放寬門檻。
- SOURCE manifest d69d3456、controller fd1948 與三方 SOURCE 報告不變。
- 三案例僅 injected-errno／手寫協定 model 範圍；不執行 engine，不代表 native、GUI、官方封包或完整覆蓋驗收。
- 無 C++、commit、push、delete、發布、外部訊息、付費、reset 或新排程。

已審查 root sampler v5 SHA：`12824cbc5ee18a22c5a626eaab00e3fb763e90e9c95f462f25bb6b37ed41e65a`。
wrapper v2 SHA：`4fae31d809b3609d66888d65923a55dddd21dbfac84a5242323fcb407973d031`。
獨立審查 JSON SHA：`1670aec9b86d5cbb9ce1780de84e240d8051b073012590694a75886a2c8eb2fb`，結論 APPROVE_LIMITED_ORCHESTRATION_SOURCE_ONLY、零 confirmed findings；未執行這兩支程式。

## 為何需要這一次決策

原 `required-fault-controls-preparation-v1/CONTRACT-v1.md` Stage C 與 SOURCE interface 規定 preflight/setup failure「grants no retry/reuse」。該規則沒有明文給予過期 guard 自動更新例外；根端與獨立 reviewer 採保守解釋，不能把案例尚未執行當作可自行覆寫準備證據的授權。故提出這一份具體例外，僅處理尚未進入 campaign 的一次重取樣，不修改既有案例 retry0。

既有0ad-t14每5小時排程保留；決策待回覆期間安靜保持，不因排程喚醒自行重取樣。
