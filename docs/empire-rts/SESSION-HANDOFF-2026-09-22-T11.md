<!-- Purpose: T11 closeout and next-session entrypoint. Created: 2026-09-22. -->
# T11 收尾／後續交接

T11及M4 DONE **僅限原創低面數美術樣板**：工人1、長矛兵1、房屋1、圖示3；不是完整人物、全套美術或發行品質。起點master `9d36013`，本批提交請以實際Git log核對。既有0ad repo、官方R28與Mod架構不變，只本機工作、未push。

先核對Git、[progress](progress.md)與runtime，再讀[T11驗收](evidence/t11-validation.md)、[原始檔／工具手冊](../../assets/epoch-rts/t11-slice/README.md)。官方app在`../runtime/0 A.D..app`，Mod在`binaries/data/mods/epoch_rts`；不要混用repo舊public。T10之前82個Mod檔保持相同，不重做T05–T10已完成的限定驗收。

已完成：原創7骨rig、5clip→COLLADA→原生PMD／PSA；原創人物／房屋／HUD、普通採木／修理／建造／近戰與死亡顯示。兩seed各126項、兩事件重播、兩GUI、5項工具測試通過；最終6場fullMod＋asset／exporter／runner來源相同。原始日誌／重播與中間圖片在work，公開結果／manifest／GUI截圖在evidence/t11-*。

局限：rigid分段肢體，無肘膝／手指；其他採集／run／動作過渡、斜坡、隊形、LOD、正式材質、完整HUD、原創建築鷹架／毀滅尚未完成。原M2未全量換皮。未安裝或驗證Blender／Assimp。小場景57–60 FPS只是觀察，不能當T14效能驗收；無完整狀態hash／多人／存讀檔驗收。

主線下一個完整單元T12（TODO）：

1. 先定義限定青銅→鐵器、標準資源下的AI經營／建造／升級／進攻與可觀察驗收。
2. 檢查實際R28 public.zip的Petra與epoch civ／模板差異；先查相容性，不預設重寫AI或修改C++。
3. 先做小型runtime探針再決定接入方法；記錄失敗局與限制，使用兩seed與固定來源。
4. T11美術擴充可獨立安排，不需要重做已完成樣板。必要時先補完整rig／專用動作，再決定整套M2換皮。

T07仍即時防空、90m落地區，精確彈道／停機位／避碰未完成。T08仍只有調查：hidden及失去偵測後仍受原生攻擊；T16專用攻擊檢查、T17潛艇、T18精確空戰全部TODO。T12–T15亦未宣稱完成。沒有背景任務或排程。
