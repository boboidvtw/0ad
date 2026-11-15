<!-- Purpose: T10 closeout and T11 continuation. Created: 2026-09-21. -->
# T10收尾／T11交接

T10 DONE限靜態房屋匯入，M4 IN_PROGRESS、T11 TODO。起點master 6221d74；本批提交由Git歷史查實際HEAD。唯一repo為既有0ad checkout，只本機工作、未push。

先核對Git、progress、實際runtime，再讀[t10驗收](evidence/t10-validation.md)、[匯入手冊](../../assets/epoch-rts/t10-house/README.md)、assets／art-direction。官方R28 0.28.0 ARM64在`../runtime/0 A.D..app`，Mod在`binaries/data/mods/epoch_rts`；repo舊public不可混用。原始日誌／重播留work，公開結果與來源manifest在evidence/t10-*。

已完成：JSON→DAE／PNG→原生PMD／DDS→GUI；兩seed各13項、兩重播、GUI三圖、M1及工具4測試通過。玩家色／選取實測；無hash行，不聲稱完整狀態同步。工具未使用Blender，房屋是80三角形暫用簡模；人物、正式材質／圖示、建造／損壞動畫、LOD與效能尚未驗收。

下一個完整工作單元T11：

1. 定義最小工人、戰鬥單位、建築與HUD樣板的風格、輪廓、玩家色與必要動作驗收；先讀既有M2模板，保持玩法。
2. 調查本機製作工具與官方R28骨架／動畫格式；靜態T10可重用，不能假定動畫匯入已可用。不新增付費服務。
3. 先做可獨立驗收的美術切片；如人物流程受阻，記錄PARTIAL與可重現問題，不以建築完成替代T11全部驗收。
4. 引擎場次串行，保存GUI證據及來源雜湊，按影響回歸；同步progress、assets、journal與交接。

T05–T07限定驗收不重做。T07仍即時防空、90公尺落地區；精確彈道／停機位／建築避碰未完成。T08僅調查，hidden與失去偵測仍受原生攻擊，T16專用攻擊gate、T17潛艇、T18精確空戰均TODO。T09維持Mod-first，不预設改C++；詳見[前次交接](SESSION-HANDOFF-2026-09-21.md)與[t09決策](t09-engine-decision.md)。沒有背景任務或排程。
