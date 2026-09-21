<!-- Purpose: Reproducible static art source and import recipe. Created: 2026-09-21. -->
# T10 靜態房屋匯入樣板

狀態：**暫用簡模**。本樣板驗證可編輯參數 → COLLADA／PNG → 獨立actor → R28原生匯入 → 遊戲顯示，不是正式房屋美術或Blender流程。

## 來源與授權

- 原創幾何／色塊貼圖：Epoch RTS contributors，2026-09-21，本repo參數化生成，沒有複製上游house模型、貼圖或Empire Earth素材。
- `house.json`及產生的`t10_house.dae`、`t10_house.png`、自訂`t10_house.xml` actor採 **CC BY-SA 3.0**：[授權](https://creativecommons.org/licenses/by-sa/3.0/)。署名「Epoch RTS contributors — T10 temporary house」，保留本來源說明與授權連結；不把上游作者署名替換為本專案。
- exporter、測試、地圖腳本、simulation模板採GPL-2.0-or-later。
- 原生材質`player_trans.xml`與`model` shader、參考房屋和地形來自固定官方R28 runtime；依其各目錄授權使用。官方art署名 **Wildfire Games**，[原作者](https://www.wildfiregames.com/)、[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)。本樣板不複製其材質／shader二進位。
- 發行包內public.zip沒有DAE來源；官方原始DAE的格式參考為 [v0.28.0 crate](https://gitea.wildfiregames.com/0ad/0ad/media/tag/v0.28.0/binaries/data/mods/public/art/meshes/props/wrld_crate_a.dae)。只查格式，未挪用幾何。

## 可編輯來源與工具

`house.json`是可編輯尺寸／RGBA palette；`tools/epoch-rts/export-house.py`是可編輯幾何產生器。沒有`.blend`、骨架、動畫或外部貼圖依賴。本機使用`/usr/bin/python3` 3.9.6、標準庫；沒有安裝Blender或新套件。

從repo根目錄：

```sh
/usr/bin/python3 tools/epoch-rts/export-house.py
/usr/bin/python3 tools/epoch-rts/export-house.py --check
/usr/bin/python3 tools/epoch-rts/test-export-house.py
/usr/bin/python3 tools/epoch-rts/t10-macos.py --app '../runtime/0 A.D..app' --mode validation --seed 42 --visual --timeout 180
```

第一個指令覆寫本樣板的兩個生成檔，修改前先保留所需差異；不要直接改生成檔。`--check`只在記憶體重建並比對，不寫入，任何不同以非零狀態結束。所有尺寸必須為有限正數且≤100，拒絕bool；屋簷≤min(width,depth)/4。門／色帶随尺寸縮放。只有已提交的預設尺寸做過GUI驗收；修改尺寸後要重新評估選取／阻擋範圍與視覺。

## 匯出契約

| 項目 | 固定樣板 |
| --- | --- |
| 格式／座標 | COLLADA1.4.1，meter=1，Y_UP，地面中心為原點，+Z為正面 |
| 尺寸 | 牆10×8×4m、屋頂高2m、屋簷0.5m；總bounds 11×6×9m |
| 幾何 | 80三角面、162輸出頂點；face分開法線，已三角化；單一mesh／identity scene node |
| UV／材質 | 1組UV，各面指向色塊中心；actor指定baseTex及player_trans.xml，不依賴DAE material binding |
| 貼圖 | 原創64×16 RGBA PNG；牆／屋頂／木色alpha255，玩家色alpha0；沒有normal/spec/AO |
| 動畫 | 靜態，0骨架／0動畫；不作人物匯入教學 |
| 規則 | 子模板只更換Identity名稱與VisualActor；M2 Cost／Health／Footprint／Obstruction／Population／BuildRestrictions完整繼承 |
| 碰撞／選取 | 原有14×14m obstruction、16×16m footprint；簡模11×9m留空間，未縮小玩法阻擋範圍 |

輸出位於`binaries/data/mods/epoch_rts/art/meshes/structural/epoch_rts/t10_house.dae`與`art/textures/skins/structural/epoch_rts/t10_house.png`。actor位於`art/actors/structures/epoch_rts/t10_house.xml`；simulation模板位於`simulation/templates/structures/epoch_rts/t10_house.xml`。

啟動固定R28後，引擎會把DAE／PNG轉成使用者cache內PMD／DDS；不要手動把cache當原始檔或提交repo。首度以全新檔名載入已產生實際cache並顯示；畫面驗收比只檢查檔案存在更重要。`t10-macos.py`在啟動／結束比對全部Mod、runner與參數／exporter來源，GUI要正常退出才通過。

## 依賴與驗收邊界

獨立actor只有本地mesh＋PNG＋public材質；材質要求baseTex，並引用public`shaders/effects/model.xml`及引擎所選渲染路徑。參考房屋仍是上游多變體模型，音效／圖示／人口及碰撞繼承原M2模板，沒有重新封裝整個public。

驗收地圖左為藍方樣板、中為紅方樣板、右為原M2參考房屋；一名工人以普通移動指令繞過樣板。可點選左右陣營樣板查看玩家色、選取圈和HP300。約21秒完成自動檢查，之後Cmd+Q正常退出。

[完整T10證據](../../../docs/empire-rts/evidence/t10-validation.md)包含來源、重播、GUI與限制。只驗靜態mesh匯入；沒有Blender匯出／重匯入、骨架、動畫、建造／毀壞美術、完整LOD或性能驗收。正式T11素材需逐項補齊，不可由本樣板推定全部格式均可用。
