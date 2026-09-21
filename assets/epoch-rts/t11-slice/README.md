<!-- Purpose: Original T11 source, license and reproducible rig export. Created: 2026-09-21; Updated: 2026-09-22. -->
# T11 原創美術樣板

工人／長矛兵／房屋／三個HUD圖示的可編輯來源為 `slice.json` 與 `tools/epoch-rts/export-t11.py`。這是分段低面數原創樣板，並非正式發行人物或Blender檔案。完整結果與限制見 [T11驗收](../../../docs/empire-rts/evidence/t11-validation.md)。

## 作者、來源與授權

- 幾何、七骨架、動作、配色與圖示：Epoch RTS contributors，2026-09-21。原創參數化製作，無Empire Earth素材，無上游人物mesh／動畫複製。
- 本目錄 `slice.json` 及生成的模型／貼圖／圖示／動畫／骨架對照與actor：**CC BY-SA 3.0**，署名「Epoch RTS contributors — T11 art slice」，保留 [授權連結](https://creativecommons.org/licenses/by-sa/3.0/) 與本來源說明。
- 房屋幾何沿用本repo原創T10 exporter，使用T11尺寸／配色輸入；沒有覆寫T10輸出。
- exporter、測試、runner、地圖及simulation子模板：GPL-2.0-or-later。
- 上游R28材質 `player_trans.xml`／shader、地形、樹木、施工鷹架、音效、其餘HUD、M2父模板等仍依賴官方public。**Wildfire Games**，[原作者](https://www.wildfiregames.com/)、[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)。截圖包含上游素材，不得改署名為全部原創。字型沿用官方Source Han Sans，SIL OFL1.1。
- 沒有付費、套件安裝或新增外部美術下載；研究來源是格式／原始碼參考，不是模型拷貝。

## 官方R28流程與本機工具

實際runtime為官方0.28.0 ARM64；Python `/usr/bin/python3` 3.9.6與標準庫可用。PATH及/Applications未找到Blender、Assimp；不將此範圍說成全磁碟搜尋。未實測任何Blender版本。

查核官方固定tag，原始下載保留於忽略目錄 `work/t11-research/`，雜湊見 [runtime紀錄](../../../docs/empire-rts/evidence/t11-runtime-assets.json)：

- [CommonConvert.cpp v0.28.0](https://gitea.wildfiregames.com/0ad/0ad/src/tag/v0.28.0/source/collada/CommonConvert.cpp)：由controller的joint向上辨識骨架root，處理座標轉換。
- [StdSkeletons.cpp v0.28.0](https://gitea.wildfiregames.com/0ad/0ad/src/tag/v0.28.0/source/collada/StdSkeletons.cpp)：`standard_skeleton`、root identifier及bone target對照。
- [PMDConvert.cpp v0.28.0](https://gitea.wildfiregames.com/0ad/0ad/src/tag/v0.28.0/source/collada/PMDConvert.cpp)：skin／bind pose／weights → 原生PMD。
- [PSAConvert.cpp v0.28.0](https://gitea.wildfiregames.com/0ad/0ad/src/tag/v0.28.0/source/collada/PSAConvert.cpp)：動畫DAE仍需controller及骨架，依時間軸取樣到PSA。
- [官方社群動畫教學](https://wildfiregames.com/forum/topic/17842-how-to-export-animations-from-blender3d-to-0ad/)只提供歷史流程背景（mesh＋armature、動作、骨架XML、actor）；其2013年Blender版本建議不是2026年相容性結論。實際契約以R28原始碼、public.zip與原生匯入為準。

流程：可編輯JSON＋exporter → skinned DAE、各動作DAE、skeleton XML、PNG → actor綁定 → R28原生PMD／PSA／DDS cache → 遊戲內檢查。未改C++，未混用repo舊public。

## 匯出契約

| 項目 | 規格 |
| --- | --- |
| 格式／尺度 | COLLADA1.4.1、Y_UP、meter=1；模型原點在地面；頂點法線與單一UV明確輸出 |
| 骨架 | epoch_root、torso、head、兩arm、兩leg，共7；各肢體為root子節點，rigid每頂點1個權重=1；無肘／膝／手指，非完整人體rig |
| 變換 | bind pose固定；local matrix關鍵影格，X軸旋轉，LINEAR，無縮放／IK／外部約束 |
| 動作 | idle 2s、walk 0.8s、work 1s、attack 1s、death 1.2s；每骨5個source keys；原生30Hz取樣，實際59／23／29／29／35幀 |
| 共用 | 工人與兵共用rig與5組clip；walk也作run、work作Build／Gather_tree；其餘採集名稱是fallback而未驗收 |
| 人物 | 工人408頂點／204三角；兵438頂點／218三角；人物帽高4.3m、兵含矛6.2m，沿RTS誇張比例 |
| 房屋 | 162頂點／80三角，11.2×6.5×9.2m；保留16×16 footprint、14×14 obstruction，外圈留白 |
| 貼圖 | 人物128×16 RGBA 8色塊；房屋64×16；player色塊alpha0、其餘255，使用public player_trans材質 |
| 圖示 | 三個128×128 RGBA原創幾何輪廓；深藍灰底與青銅邊框 |

骨架與clip必须一起修改；不能把這7骨rig接到public biped動作。幾何尺寸在exporter中編輯，JSON提供骨架位置、角度、時長、色票與房屋參數。工具針對此固定樣板，不是任意外部DAE匯入器。改過來源後必須重跑匯出、測試與GUI，`--check`只證明位元一致，不證明姿勢合理。

## 重現

在repo根目錄，先正常關閉其他0 A.D.視窗，避免共用日誌競爭：

```sh
/usr/bin/python3 tools/epoch-rts/export-t11.py
/usr/bin/python3 tools/epoch-rts/export-t11.py --check
/usr/bin/python3 tools/epoch-rts/test-export-t11.py
/usr/bin/python3 tools/epoch-rts/t11-macos.py --app '../runtime/0 A.D..app' --mode validation --seed 42
/usr/bin/python3 tools/epoch-rts/t11-macos.py --app '../runtime/0 A.D..app' --mode validation --seed 7
/usr/bin/python3 tools/epoch-rts/t11-macos.py --app '../runtime/0 A.D..app' --mode validation --seed 42 --visual --timeout 600
```

一般視窗約126秒完成檢查，留場可點選；Cmd+Q正常退出才通過visual runner。可用Alt+F顯示FPS，滾輪縮放；這些操作不替代行為檢查。runner不自動認定畫面通過，`visual_verified:false`刻意保留，人工畫面紀錄另存。

輸出位於epoch_rts的 `art/meshes/{skeletal,structural}/epoch_rts/t11_*`、`art/animation/epoch_rts/t11_*`、`art/skeletons/epoch_t11.xml`、skins及portraits子目錄。不要提交runtime cache。

T11 worker僅把Builder清單中的M2 house替換成同規則的t11_house，故圖示、施工預覽及完工美術一致；成本50木／25秒／人口10沿用M2。其餘身份、能力、戰鬥、採集、碰撞與HP逐項比對。原M2模板與T05–T10檔案不變，獨立地圖不注入一般duel。
