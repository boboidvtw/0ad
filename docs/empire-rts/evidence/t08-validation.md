<!-- Purpose: R28 T08 feasibility evidence and bounded decision. Created: 2026-09-20. -->
# T08 潛艇可行性調查證據

**DONE，限定 T08 規則／可行性調查及範圍決策。完整潛艇功能未實作，T09維持TODO。**

## 基線與原生介面

起點 master `e956ac6`，工作樹原為 clean，無 pyrogenesis 進程。macOS 26.6.2 / arm64，官方 app 0.28.0，DMG SHA-256 與基線一致。使用者 Mod symlink 指向本 repo；public 資料來自官方 app 的 public.zip。見 [runtime manifest](t08-runtime-manifest.json)。未使用 repo 0.0.27 public、未改 C++。

官方 [R28 Position 文件](https://docs.wildfiregames.com/entity-docs/r28/components/position/) 說明 Floating／FloatDepth。下列具體介面來源為實際 runtime archive 的同名檔案，成員 SHA-256 已保存；腳本方法與 native binding 存在性另外由真實引擎確認，沒有拿舊 repo 介面替代。

| 介面／來源 | 實際結論 |
| --- | --- |
| template_unit_ship.xml；Position | Floating=true、FloatDepth；原生 ship 平面尋路。FloatDepth=4 在水位20、海床8的場景得到 y=16。 |
| 引擎 Position binding | SetHeightFixed、SetHeightOffset、SetHeightRelative、SetFloating 可見；沒有 SetFloatDepth setter。探針用 SetHeightFixed 在 y20／16 間切換。存在性不等於每個 setter 都驗收。 |
| Visibility.js | ActivateScriptedVisibility(entity,true) 啟用 IID_Visibility.GetVisibility(player,isVisible,isExplored) callback；回傳 0 隱藏／2 可見。独立 EpochT08Visibility 僅被測試模板引用。 |
| RangeManager native binding | RequestVisibilityUpdate(entity) 實測可更新狀態；本次偵測器移動／死亡／轉敵由探針顯式呼叫，不是完整自動偵測管理器。 |
| Attack.js CanAttack | 檢查位置、類別、外交、HP、部分高度條件；不是 LoS gate。 |
| UnitAI.js CheckTargetVisible | hidden 回傳 false，但不能據此宣稱所有攻擊入口或既有攻擊會停止。 |
| Fogging.js | fog/mirage 不是水下隱身；本探針不建立 Mirage，也不覆寫全域 Fogging。 |

## 測試設計与發現

深水場景固定水位20、海床8，x520以東為陸地。兩玩家敵對，沒有 reveal-all。原生 ship_scout 衍生暫用測試船，無彈道 Ranged／只准 Ship，HP2000。測試用 `none` stance 禁用自主逃跑及反擊，仍透過正常 ProcessCommand 發移動與攻擊指令。座標／距離固定；seed交叉驗證不是隨機海床測試。

- FloatDepth=4 不會自動隱形；普通 LoS 仍 visible。
- SetHeightFixed 可浮到 y20／潛到 y16；航行後仍維持 y16；向陸地發命令停在 x508.5，未穿越 x520。
- callback 在相同普通視野下對 owner 回傳 visible、對沒有偵測的敵方回傳 hidden；60公尺可見、61公尺隱藏；偵測器轉敵／摧毀後隱藏，歸還後重新可見，浮起後無需偵測器。
- **原生攻擊缺口**：隱藏目標仍被已知 entity ID 的正常 attack command 命中；既有攻擊在失去偵測後仍持續。這是測得的限制，不是潛艇需求驗收通過。
- PerformAttack 直接入口亦會對 hidden 目標造成傷害。候選實作必須在命令、選敵、每次發射與需要時的命中處理檢查狀態，不能只包 GUI 或 CanAttack。
- RestrictedClasses=!Ship 可排除有效陸上單位；外交拒絕友船。**尚未實作動態水面／水下類別或武器分層**；上述不代表普通艦砲已拒絕已偵測水下目標。

## 範圍決策

T08交付是規則、隔離原生探針及決策。保留最小 Mod 研究切片，不加入 M2 訓練／建造，也不將測試元件當可玩的潛艇 controller。

後續最小候選：同一實體的兩態 controller＋逐玩家 visibility＋範圍偵測更新＋專用攻擊 gate＋無彈道直接傷害。可先在 Mod 層實作驗證；現有證據沒有要求先改 C++。

完整可玩潛艇延後到 T09 決策後的新任務：2秒切換／停火、所有權／非法命令、淺水安全路徑、獨立武器矩陣、正在進行與延遲傷害撤銷、非同步視野更新、GUI按鈕／選取／小地圖與盟友共享均需另驗。精確魚雷、水下與水面独立碰撞層、3D尋路、性能／多人／存讀檔未驗證。當 Mod 方案有可重現無法解決的正確性或性能限制，才在 T09 考慮匹配 R28 的 C++ 基線。

T07原有精確空中彈道、寬鬆降落區／無精準停機位、建築避碰、移動目標只驗追蹤等限制完整保留。T05–T07本次不重跑，T09不標DONE。

## 調查過程的修正

首次地圖把 rmgen 水位當相對高度，得到海床8、水位0而非深水；更正為水位20並增加實際12公尺水深斷言。第二次目標使用 passive stance，受攻擊自主逃離，使固定60／61公尺測量失效；改為原生 none stance並保存每階段實際座標。失敗場次留在本機 work，未算最終通過結果。

## 最終驗收結果

| 項目 | 實際結果 |
| --- | --- |
| seed42／7 原生探針 | 各30項通過，0錯誤／0警告；含確認原生攻擊缺口的斷言 |
| seed42／7 重播 | 各30項，suite／來源／runner一致，自然EOF與exit0；hash_checks_ok=0，不宣稱全狀態hash或多人同步 |
| 深度／移動 | y20→16；15秒後x441.010且y16；陸地邊界x508.5 |
| 隱藏時新攻擊 | HP2000→1956.26，3秒；原生缺口已重現 |
| 失去偵測後既有攻擊 | HP1897.94→1854.20，3秒；原生缺口已重現 |
| GUI | 四狀態8項API檢查、四張人工檢視截圖；正常Cmd+Q退出exit0，0錯誤／0警告 |
| 必要回歸 | 原M1地圖載入／模擬PASS，0錯誤／0警告；T05–T07不重做 |
| 靜態／審查 | Python語法、模板XML、地圖JSON、diff空白檢查通過；唯讀審查及runner修正複查無阻擋項 |

[引擎與重播結果](t08-engine-results.json) · [GUI紀錄](t08-visual-validation.json) · [回歸結果](t08-regression-results.json) · [最終全部Mod／runner來源](t08-source-manifest.json)。原始logs／replays在本機忽略的work及遊戲replay目錄；公開證據JSON不含私人絕對路徑。

探針與M1取得完整結果後受控停止（exit−15）；非GUI重播自然EOF。GUI runner的visual_verified仍為false，因程式不能自動證明渲染；独立GUI紀錄保存人工檢視與截圖。首場GUI來源相同但runner尚未隔離重播profile輸出；最終場次已固定runner並重拍四圖，所有最終場次fullMod manifest相同且結束核對未變。

### 畫面證據

- [水面](t08-surface.png)：中間紅色敵船可見。
- [未偵測下潛](t08-hidden.png)：中間敵船消失。
- [已偵測水下](t08-detected.png)：偵測船移到右方後敵船重新可見，船體位置較低。
- [重新浮起](t08-resurfaced.png)：敵船回到水面高度。

暫用船的桅杆突出水面是美術限制；同一固定camera的顯示／隱藏證據不涵蓋滑鼠選取、小地圖洩漏、owner／盟友GUI、真實潛艇外观或動畫。

### 重現

```sh
/usr/bin/python3 tools/epoch-rts/t08-macos.py --app '../runtime/0 A.D..app' --mode probe --seed 42
/usr/bin/python3 tools/epoch-rts/t08-macos.py --app '../runtime/0 A.D..app' --mode probe --seed 7
/usr/bin/python3 tools/epoch-rts/t08-macos.py --app '../runtime/0 A.D..app' --mode visual --visual --timeout 180
```

GUI約2秒水面、33秒隱藏、64秒偵測、95秒重新浮起；四階段後正常關閉。重播對應原場次的local-replays.json及result.json，傳入`--replay PATH --baseline PATH --seed 42`（或7），保持相同mode。所有引擎場次串行，不與其他0 A.D.進程共用logs。
