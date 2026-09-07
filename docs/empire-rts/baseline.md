<!-- Purpose: Reproducible M1 runtime baseline and launch instructions; Created: 2026-09-06. -->
# 第一階段基線與啟動方式

## 版本決策

M1 使用 **官方 0 A.D. Release 28 / 0.28.0，macOS ARM64 發行包**執行獨立 Mod。repo 原始引擎程式維持不動。這不是宣稱 repo 的 C++ 已升級或建置成 Release 28。

| 項目 | 固定值 |
| --- | --- |
| 專案文件／原始碼起點 | `f03b7d7173abea8bd05120cabb6f2f1a1e25ea96` |
| 先前上游來源快照 | `a2b5838b181e1c3b770ae4e665811a87bd436fac` |
| 實際遊戲與 public Mod | 官方 Release 28，`0.28.0` |
| 平台 | macOS 26.6.2（25G83），Apple Silicon / arm64 |
| 本 Mod | `epoch_rts`，`0.1.0`；依賴 `0ad=0.28.0` |
| 測試地圖 | `random/epoch_frontier`；192 tiles、2 players、seed 42、兩方雅典、Nomad 關閉 |

repo 中較早的 `public/mod.json` 仍是 `0.0.27`。請不要把這個 public 與 Release 28 引擎混合使用，也不要直接把此 repo 視為已驗證的 R28 全套原始碼。此階段只將 `epoch_rts` 載入官方 R28 自帶的 public；未驗證其他版本及平台。

選擇理由：官方提供 Apple Silicon 原生遊戲及匹配資料，可直接驗證 Mod；從此 repo 建置需另處理舊基線與依賴，並非 M1 的必要前提。將來需要 C++ 修改時，須先選定與 runtime 相符的原始碼版本，再新增建置與回歸任務。

## 取得官方遊戲

- [官方 macOS 下載頁](https://play0ad.com/download/mac/)
- [Release 28 ARM64 DMG](https://releases.wildfiregames.com/0ad-0.28.0-macos-aarch64.dmg)
- [官方 SHA-256](https://releases.wildfiregames.com/0ad-0.28.0-macos-aarch64.dmg.sha256sum)
- 固定 SHA-256：`8c53566123fed9a79766c364e543d6e9dc7c84f642c78d2bb5892eeea9c4c052`

取得 DMG 後先核對 SHA-256，再按官方方式將 app 複製到自行選擇的資料夾。不必改動系統安全設定。遊戲執行時會建立正常的 `~/Library/Application Support/0ad` 設定、日誌與 replay，以及 `~/Library/Caches/0ad` 快取。

## 啟動本 Mod

在 repo 根目錄執行（app 路徑請依實際位置調整）：

```bash
EPOCH_RTS_0AD_APP='/path/to/0 A.D..app' tools/epoch-rts/launch-macos.sh
```

預設直接開啟 Frontier 01 測試地圖。另一位玩家不配置 AI，讓操作驗證不受進攻干擾；這不是兩時代 AI 驗收。

若要查看 Mod 已載入並從選單選地圖：

```bash
EPOCH_RTS_0AD_APP='/path/to/0 A.D..app' tools/epoch-rts/launch-macos.sh --menu
```

啟動器會檢查 app 版本，並在 `~/Library/Application Support/0ad/mods/epoch_rts` 建立指向此 repo 的連結；既有不同目標的連結或資料夾會保留並停止，不覆寫使用者內容。搬動 repo 後需檢查該連結。本腳本不下載遊戲、不修改 app，也不將引擎或快取提交至 Git。

手動進入地圖時使用 Random maps，選擇 Epoch RTS — Frontier 01，兩位雅典玩家，192 tiles，Nomad 關閉；M1 尚不支援其他模式。地圖直接限制兩位玩家與最小尺寸。

存檔與其他遊戲功能沿用上游，未在 M1 宣稱已完成其專案級驗收。實際結果以 [M1 驗收](evidence/m1-validation.md) 為準。


## 無畫面引擎測試

先以啟動器登錄 Mod，再關閉所有 0 A.D. 視窗。需要 Python 3（測試環境為 3.14.6）：

```bash
python3 tools/epoch-rts/smoke-macos.py --app '/path/to/0 A.D..app' --seed 42
python3 tools/epoch-rts/smoke-macos.py --app '/path/to/0 A.D..app' --seed 7
```

測試使用官方引擎實際生成地圖、載入自訂模板及運行模擬；偵測到至少 100 個回合後，以 SIGTERM 結束測試程序。引擎跑得很快，實際停止時通常已超過 100 回合；這不是效能基準。30 秒未達條件則失敗，最終只終止該測試自己啟動的程序。

每次結果會保存在新的 `work/epoch-rts-smoke/時間-seed/` 目錄。`result.json` 區分引擎測試與畫面驗證；`visual_verified` 永遠為 false。若已有遊戲程序，測試會停止，避免日誌互相覆寫。詳細日誌只留本機；提交證據前需排除使用者路徑與設定。

## T04 經濟原型（epoch_rts 0.2.0）

沿用上述官方 R28 runtime 與 Mod 安裝方式。進入新的 Frontier Duel：

```bash
EPOCH_RTS_0AD_APP='/path/to/0 A.D..app' tools/epoch-rts/launch-macos.sh duel
```

兩位 Frontier Union 玩家，192 tiles；正常開局有 6 工人、2 長矛兵與唯一市中心。可採集、建造、訓練；鐵器研究入口與科技 HUD 尚待 T05。畫面暫用可讀英文名稱，中文支援待字型驗收。

關閉所有 0 A.D. 實例後執行整合檢查：

```bash
python3 tools/epoch-rts/smoke-macos.py --app '/path/to/0 A.D..app' --scenario t04 --seed 42
python3 tools/epoch-rts/smoke-macos.py --app '/path/to/0 A.D..app' --scenario t04 --seed 7
```

`--scenario duel` 只檢查正常地圖載入及運行；預設 `--scenario m1` 保留 M1 地圖回歸。`t04` 使用專用驗收地圖，會建立測試實體、設定資源並檢查邊界，不能當作無作弊完整對局。測試最長 60 秒，收到完整結果後停止自己的引擎程序；報告中的 SIGTERM 不代表遊戲正常退出，正常退出另由 GUI 測試驗證。
