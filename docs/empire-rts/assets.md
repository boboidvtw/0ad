<!-- Purpose: M1 temporary asset provenance; Created: 2026-09-06. -->
# M1 暫用素材登錄

本階段沒有製作正式模型，也沒有購買素材。下列項目由官方 0 A.D. Release 28 的 `public` Mod 提供，Epoch RTS 透過模板或名稱引用，未複製素材二進位檔。

| ID | 用途／引用路徑（public 內） | 狀態 | 作者與來源 | 授權證據 |
| --- | --- | --- | --- | --- |
| M1-A01 | `units/athen/support_female_citizen` 模板及其模型、圖示與動畫依賴；Pioneer 沿用 | 暫用 | Wildfire Games／各素材作者；官方 Release 28 | repo 根 LICENSE.txt、runtime 的 art/LICENSE.txt 與個別素材說明 |
| M1-A02 | `medit_grass_field_a`、`medit_city_tile` 地形 | 暫用 | 同上 | art/LICENSE.txt 與個別素材說明 |
| M1-A03 | `gaia/fruit/berry_01`、`gaia/tree/aleppo_pine` | 暫用 | 同上 | 模板及其 art 依賴的授權 |
| M1-A04 | `gaia/ore/mediterranean_large`、`gaia/rock/mediterranean_large` | 暫用 | 同上 | 模板及其 art 依賴的授權 |
| M1-A05 | `placePlayerBases` 產生的雅典市中心與起始單位 | 暫用 | 同上 | `simulation/data/civs/athen.json` 與其模板／art 依賴 |
| M1-A06 | `cirrus` 天空與預設 public HUD、音效 | 暫用 | 同上 | runtime 的 art/LICENSE.txt、audio/LICENSE.txt 及各子目錄授權 |

取得日期：2026-09-06。來源下載網址與 SHA-256 見 [基線與執行方式](baseline.md)。原始圖像／模型的作者不得統一改署名為 Epoch RTS。這是原型的依賴登錄，不是完整發行用逐檔授權清單；發行前仍須枚舉傳遞依賴與全部所需署名。

自訂內容：`epoch_frontier.js`、對應地圖設定與 `pioneer.xml` 為本專案新增程式／設定，GPL-2.0-or-later。沒有新增模型、貼圖、圖示、音樂或原作 Empire Earth 素材。

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
