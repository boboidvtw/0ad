<!-- Purpose: M1 temporary asset provenance; Created: 2026-09-06. -->
# 素材登錄

M1階段沒有製作正式模型，也沒有購買素材。下列項目由官方 0 A.D. Release 28 的 `public` Mod 提供，Epoch RTS 透過模板或名稱引用，未複製素材二進位檔。

| ID | 用途／引用路徑（public 內） | 狀態 | 作者與來源 | 授權證據 |
| --- | --- | --- | --- | --- |
| M1-A01 | `units/athen/support_female_citizen` 模板及其模型、圖示與動畫依賴；Pioneer 沿用 | 暫用 | Wildfire Games／各素材作者；官方 Release 28 | repo 根 LICENSE.txt、runtime 的 art/LICENSE.txt 與個別素材說明 |
| M1-A02 | `medit_grass_field_a`、`medit_city_tile` 地形 | 暫用 | 同上 | art/LICENSE.txt 與個別素材說明 |
| M1-A03 | `gaia/fruit/berry_01`、`gaia/tree/aleppo_pine` | 暫用 | 同上 | 模板及其 art 依賴的授權 |
| M1-A04 | `gaia/ore/mediterranean_large`、`gaia/rock/mediterranean_large` | 暫用 | 同上 | 模板及其 art 依賴的授權 |
| M1-A05 | `placePlayerBases` 產生的雅典市中心與起始單位 | 暫用 | 同上 | `simulation/data/civs/athen.json` 與其模板／art 依賴 |
| M1-A06 | `cirrus` 天空與預設 public HUD、音效 | 暫用 | 同上 | runtime 的 art/LICENSE.txt、audio/LICENSE.txt 及各子目錄授權 |

取得日期：2026-09-06。來源下載網址與 SHA-256 見 [基線與執行方式](baseline.md)。原始圖像／模型的作者不得統一改署名為 Epoch RTS。這是原型的依賴登錄，不是完整發行用逐檔授權清單；發行前仍須枚舉傳遞依賴與全部所需署名。

自訂內容：`epoch_frontier.js`、對應地圖設定與 `pioneer.xml` 為本專案新增程式／設定，GPL-2.0-or-later。M1當時沒有新增模型、貼圖、圖示、音樂或原作 Empire Earth 素材。

資產替換時在此表新增新來源、作者、授權、原始檔、匯出設定與遊戲內證據；不得把暫用狀態直接改成正式而省略驗收。

已讀取 Release 28 實際 public.zip 的 `art/LICENSE.txt`：要求署名 Wildfire Games、連結 https://www.wildfiregames.com/ 與 https://creativecommons.org/licenses/by-sa/3.0/；素材按 CC BY-SA 3.0 條件使用。本次遊戲截圖包含這些暫用美術，亦保留上述署名與來源。

## T04 新增暫用引用（2026-09-07～2026-09-08）

- 長矛兵、投石兵與鐵刃步兵分別引用 R28 雅典長矛兵、雅典投石兵、羅馬基礎劍士的模型、動畫與圖示。
- 六棟建築引用 R28 雅典市中心、房屋、倉庫、兵營、農田、鍛造所；玩法由 epoch_rts 模板覆寫。
- Frontier Union 暫用雅典徽章、音樂清單與小地圖邊框，尚未製作正式文明識別。MiniMapPanel.js 取自固定 R28，新增 epoch 的暫用邊框映射；程式沿用 GPL-2.0-or-later。
- 本次仍只透過路徑引用素材，沒有複製 public 素材二進位檔或購買資產。來源、作者與 CC BY-SA 3.0 署名條件同上；新增驗收截圖包含上述暫用素材。

## T05 字型與介面引用（2026-09-08～09）

- 官方 R28 基礎 mod.zip 已包含 `fonts/SourceHanSansTW-Regular.otf` 與 Bold；default.cfg 的 `fonts.zh_TW.sans` 指向它們。以 `zh_TW` 啟動即可，不新增下載或付費。
- 已讀取同包 `fonts/source-han-sans -LICENSE.txt`：Adobe 2014–2021，SIL Open Font License 1.1。只依賴官方 runtime，未將字型二進位複製進 repo。
- 新增研究圖示引用 public 的 `town_phase.png`、`sword_01.png`；音效引用 `interface/alarm/alarm_phase.xml`。上游美術署名同上。
- Researcher.js、BuildLabel.js/XML 與 selection_details.js 取自官方 R28 並作局部修改，保留 GPL-2.0-or-later 出處。尚未製作正式 HUD 美術。

## T07 飛行原型引用（2026-09-13）

- `units/plane`、`art/actors/units/global/plane.xml` 及其飛機模型、mustang貼圖／圖示、projectile依賴由官方R28提供；機場沿用epoch兵營的雅典兵營，防空引用 `structures/hellenes/wooden_tower.xml`。無新增美術二進位檔、付費素材或Empire Earth素材。
- 作者／來源：Wildfire Games及各素材作者，官方Release28；美術按前述CC BY-SA3.0署名。驗收截圖同樣包含這些暫用素材，不是正式美術交付。
- `EpochAircraftMotion.js` 衍生自官方R28 `simulation/components/UnitMotionFlying.js`，保留Wildfire Games及GPL-2.0-or-later出處；沒有修改public或C++。

## T08 調查探針引用（2026-09-20）

- 原生 `units/athen/ship_scout` 衍生測試船；模型為 `art/actors/structures/athenians/pentekonter_scout.xml`，圖示 `units/athen/ship_scout.png`，以及繼承的船舶音效。水域使用 `medit_sand_wet` 與官方 ocean 水面、cirrus 天空。
- 僅引用固定 R28 public，沒有複製美術二進位、購買素材或加入 Empire Earth 素材。作者 Wildfire Games／各素材作者，CC BY-SA 3.0 及來源署名沿用上文；T08截圖同樣含上述美術。
- 船模型高桅杆不適合作正式潛艇，偵測後即使 y16 仍可能有桅杆露水；只用於可見性與位置探針，不代表完成水下美術。

## T10 原創暫用靜態樣板（2026-09-21）

| 欄位 | T10-A01 房屋 |
| --- | --- |
| 用途／狀態 | A04靜態匯入樣板，暫用；獨立T10地圖，未替換M2房屋 |
| 作者／來源 | Epoch RTS contributors；原創參數幾何與色塊貼圖，非上游模型改作 |
| 授權 | 新美術CC BY-SA3.0；產生工具GPL-2.0-or-later；[來源、署名與授權](../../assets/epoch-rts/t10-house/README.md) |
| 可編輯來源／工具 | assets/epoch-rts/t10-house/house.json；tools/epoch-rts/export-house.py；Python3.9.6標準庫 |
| 輸出 | epoch_rts/art/下t10_house.dae、t10_house.png與actor；精確路徑見手冊 |
| 規格 | COLLADA1.4.1、Y_UP、1單位1公尺、11×6×9公尺；80三角形／162頂點、1組UV、64×16RGBA；無骨架／動畫 |
| 上游依賴 | R28 player_trans.xml／model shader；M2房屋繼承的圖示、音效等仍引用public，未複製；Wildfire Games署名沿用上文 |
| 驗收 | [T10報告](evidence/t10-validation.md)：兩seed各13項、重播、GUI玩家色／選取、M1回歸與確定性匯出 |
| 未完成 | 正式美術、Blender、LOD、人物動畫、建造／毀滅、效能；沒有逐檔發行授權清單 |

## T11 原創低面數樣板（2026-09-21～22）

| ID | 資產／狀態 | 可編輯来源及產出 | 規格／驗收 |
| --- | --- | --- | --- |
| T11-A02 | 工人／已驗樣板 | slice.json＋export-t11.py；t11_worker.dae／actor／PNG | 408頂點、204三角、7骨；idle／walk／採木／建造修理／death |
| T11-A03 | 長矛兵／已驗樣板 | 同上，t11_soldier.dae／actor／PNG | 438頂點、218三角、共用rig；idle／walk／近戰／death |
| T11-A04 | 房屋／已驗樣板 | slice.json house＋原T10 exporter；t11_house.dae／actor／PNG | 80三角、11.2×6.5×9.2m；施工／完工／玩家色；public鷹架仍暫用 |
| T11-A08 | 3個HUD圖示／已驗樣板 | export-t11.py內原創幾何輪廓，portraits/epoch_rts/t11_*.png | 128×128；工人／兵／房屋選取及建造按鈕；非整套HUD重製 |

作者Epoch RTS contributors，幾何／骨架／5clip／貼圖／圖示為原創CC BY-SA3.0，沒有複製上游人物或Empire Earth素材。房屋衍生本repo原創T10參數幾何。工具／simulation採GPL-2.0-or-later。來源、完整署名與重現契約見[手冊](../../assets/epoch-rts/t11-slice/README.md)。上游player_trans材質、shader、鷹架、樹、地形、其餘HUD、音效與字型仍按前述Wildfire Games／OFL條件引用。

Python3.9.6標準庫，未用Blender／Assimp／付費工具。兩seed各126項、兩事件重播、GUI及5項工具測試見[T11驗收](evidence/t11-validation.md)；來源及native cache雜湊存evidence/t11-*。骨架不含肘膝／手指，原M2未全量換皮，其他動作／材質／LOD／效能及發行授權清單未完成，不將樣板標為正式量產資產。
