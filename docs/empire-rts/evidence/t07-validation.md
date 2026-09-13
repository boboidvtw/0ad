<!-- Purpose: T07 actual engine and GUI acceptance evidence. Created: 2026-09-13. -->
# T07 飛機／機場／防空驗收

**DONE，限定獨立空戰沙盒原型。** [規格與限制](../t07-air-prototype.md) 的 F00–F07 已完成。M3仍有T08潛艇與T09引擎決策，不等於整個空戰系統完成。

## 環境與來源

- 起點 `cdcbffc`，Git原為clean；官方R28 0.28.0 macOS ARM64，epoch_rts 0.3.0；沿用既有Mod架構，未改C++、public或T05。
- 原runtime目錄消失後，重新下載相同官方DMG並核對SHA-256 `8c53566123fed9a79766c364e543d6e9dc7c84f642c78d2bb5892eeea9c4c052`，與[基線](../baseline.md)相符。官方包中的UnitMotionFlying和plane模板與保留reference一致。
- [最終來源manifest](t07-source-manifest.json)含全部Mod及T07 runner。最終T07執行均在啟動前取manifest，結束再核對未變。回歸時只差mod.json描述文字，玩法程式相同。
- 原始日誌／replay留於本機忽略的work與遊戲replays；公開JSON保留run ID、結果及雜湊，不提交本機私人路徑。

## 實際結果

| 範圍 | 結果 |
| --- | --- |
| 原生probe seed42 | 2項PASS；Stop連按使landing true→false；MoveToTargetRange未解除landing |
| T07 seed42／7 | 各36項PASS，0錯誤／0警告 |
| T07重播 seed42／7 | 各36項、事件／結果／來源一致；自然EOF、exit0；無hash行，不宣稱全狀態同步 |
| 機場訓練 | W200/M100正確扣款、20秒模板時間、21秒取樣只有1架、HP200地面待命 |
| 飛行／返航 | 25公尺高度、重複移動、新命令取代、落點距機場5.534公尺、再起飛 |
| 邊界／錯誤目標 | 越界目標限制於有效地圖、非法他人指令及敵方機場被拒、毀機場後就地落地 |
| 機場轉敵 | 重新尋找己方機場，並落入替代機場90公尺區域 |
| 滑跑停止 | 400ms取樣確認仍在地面且speed>0，停止後1秒速度0且無移動請求 |
| 對地／防空 | 固定房屋實際扣血；空中與友軍拒絕；防空10秒HP200→42.5，拒絕有效地面及友方目標 |
| M2回歸 | T06戰鬥81項，兩seed完整對局各15項（649.8／621秒勝利）；T04經濟183項；M1 smoke PASS |
| GUI | 滑鼠選取／起飛／攻擊，房屋受損及毀滅；飛機HP110/200、返航、再起飛、H連按後落地；兩場正常exit0、0錯誤／0警告 |

機器結果：[T07引擎](t07-engine-results.json)、[M2回歸](t07-regression-results.json)、[GUI紀錄](t07-visual-validation.json)。無畫面測試取得完整suite後受控停止（exit−15）；完整M2及無畫面replay自然exit0。兩seed固定沙盒座標相同，地圖種子不同；不是隨機機場配置測試。

## GUI證據

- [地面選取](t07-ground-selected.jpg)、[飛行中](t07-airborne.jpg)、[對地傷害](t07-ground-damage.jpg)。
- [受損返航](t07-return-landed.jpg)、[受損再次起飛](t07-damaged-relaunch.jpg)、[H連按返航落地](t07-stop-return.jpg)。
- [最終固定來源：敵房屋毀滅、飛機110/200、返航至機場](t07-final-combat-return.jpg)。

前六張來自第一次手動demo；期間只擴充validation測試函式，產品程式與demo未變。舊runner把結束時script hash記為source，不能當作整份初始script來源證明，因此另以最終manifest固定場次確認。最終demo的自動suite僅檢查fixture，不把它冒充GUI或36項引擎驗收。

## 修正與未驗證邊界

1. 獨立EpochAircraftMotion衍生R28飛行元件：冪等Land、移動解除降落、邊界收斂，EstimateFuturePosition把秒換成毫秒。只有本原型飛機使用。
2. 原生AA彈道在兩seed失敗。放大footprint至6公尺只讓seed42通過，已撤回；時間換算及高速彈丸嘗試仍有約6公尺取樣落差。最終AA採native non-projectile Ranged即時傷害，未改全域Attack或DelayedDamage。精確空中彈道仍未完成。
3. 對移動目標只驗證追蹤座標更新，未驗證實際命中移動目標；無重複controller計時器為程式審查結論（controller只用OnUpdate），不是全引擎timer負載測試。
4. 空戰沙盒不加入M2經濟建造白名單；無精準跑道／停機位、燃油、補給、空對空、命令佇列完整支援、AI、存讀檔、多人或效能驗收。GUI可見落地與兵營暫用模型重疊；正式素材另屬T10/T11。
5. 唯讀審查發現的地面取消返航、移動目標快照、無效ground fixture及滑跑回歸缺口均已修正並複查。最終無未解HIGH/MEDIUM審查項。

## 重現與下一步

在repo執行（先關閉現有遊戲）：

```sh
python3 tools/epoch-rts/t07-macos.py --app '../runtime/0 A.D..app' --mode probe --seed 42
python3 tools/epoch-rts/t07-macos.py --app '../runtime/0 A.D..app' --mode validation --seed 42
python3 tools/epoch-rts/t07-macos.py --app '../runtime/0 A.D..app' --mode validation --seed 7
python3 tools/epoch-rts/t07-macos.py --app '../runtime/0 A.D..app' --mode demo --visual --timeout 600
```

Demo機場約(300,300)、飛機(335,310)，點小地圖中央偏左下；右鍵地面飛行、右鍵敵房屋攻擊，H停止返航。GUI timeout只是安全上限，正常用Cmd+Q退出。

下一步T08先定義水面／水下可見性、浮潛切換、目標篩選及魚雷需求，再用同一R28原生介面取得可行性證據；T09之後彙整飛行限制與潛艇結果，才決定是否需要引擎修改。未執行push。
