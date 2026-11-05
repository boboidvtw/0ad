<!-- Purpose: complete absence obligation for six expected metadata fields; no implementation. Created: 2026-10-26. -->
# Future schedules absence: separate source + full-value obligation

85f93比較器只證actual與caller-suppliedexpected完整值相等。兩者同帶futureSchedule仍會MATCH_METADATA_VALUES_ONLY；status不會變native/runtimeproof。因此不能用fullcompare成功、JSONkey blacklist、frozen/hash或shape自己推出absence。

後續controls必同時處理：

1. **完整producer／mutator closure**：source-ownedGUI boot與initialAttrs factory、nativeReplay新增三key、simulation init/settings/mapstartup/trigger/load/rejoin writers、官方 getSavedGameData/g_Groups constructors/restore/update/controlgroup input、native structuredclone與Save camera／description、GetInitAttributes/GetEngineInfo/getter hooks/prototypes/toJSON/JSON.stringify／customSerialize路徑。Unknown writer/callback/input/native clone/serialization effect一律OPEN/BLOCK；不能以沒搜尋到名字代替正向資料來源。
2. **排程只留externalclosure**：GUI schedules、下一command/checkpoint、cursor/sendOrdinal、caseNonce、transactionArms/armNonce/hostD、ACK與witness counters/ledger等不掛g_Groups、getSavedGameData返回值、InitAttributes/settings、component/controller/Scenario或Timer作未來行動。既有必要Timer的合法遊戲timer與native eventprefix仍全保，不能為absence刪真正gameplay欄位。
3. **metadata完整資料邊界**：actual top-level exact7key、expected exact6key（只有最外time例外）；完整initattrs/settings、mods array四欄、GUI groups10items與camera6keys、description原string皆不投影。Unexpectednestedfuturefield、非空group、hiddennested schedule或counter皆FAIL/BLOCK，不能actual→expected自bootstrap或兩邊同新增救MATCH。
4. **合法native欄位不誤刪**：Replay加的initAttributes.timestamp/engine_version/mods是真nativeproducer，不是應排除的future schedule；它們全部留在expected並來源綁定。只有metadata.time走既有epochinterval，不把規則遞迴套到nestedtimestamp。
5. **origin/load lineages**：origin每Save之前control independentlyprecommitted；load以已核originexpectedcontrol+本次freshnativeproducer作完整新expected，不復原origin未來commands、不放loadbranch排程進savedstate/metadata。原nativecontroller pendingtimer自然保留並由fullgraph/nativecounts等另gate，不能當future-schedule缺陷清除。
6. **actual驗證與不可變性**：actualarchive原bytes/metadata原entry、獨立controls原raw/時間／caller／source原件、完整值comparison、serializedgraph/nativequeue/fullsourceguards均需jointintegration。此sourceplan沒有執行上述runtime步驟，未宣告absencePASS。

以上不是新增engine操作或新門檻，而是既有d334「無future schedule/counters」完整義務的producer分解。Scope仍只有metadata expected-controls來源計畫。
