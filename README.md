# Star Citizen 4.10.2 台灣繁體中文｜保留英文物品與地名

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/翻譯授權-CC_BY--NC--SA_4.0-blue)](LICENSE)
![Game](https://img.shields.io/badge/Star_Citizen-4.10.2-444)
![Status](https://img.shields.io/badge/狀態-待遊戲內測試-yellow)

將 **42Kit／星際公民漢化組 4.10.2 半漢化 V2** 轉成臺灣繁體中文，保留原本的**物品、載具、地點英文名稱**，方便搜尋裝備、航線及對照英文攻略。適用於 Star Citizen 遊戲本體的 `global.ini` 文字在地化機制。

**目前是初版。** 以 OpenCC 轉換為主，另外局部人工校訂；尚未在遊戲中逐一確認字型、UI 換行、任務文字及所有翻譯品質。

## 下載

- **快速安裝**：[下載完整 ZIP 語言包](dist/StarCitizen-zh-TW-4.10.2-CNE-V2.zip)（約 2.5 MB）
- **單檔下載**：[global.ini](global.ini)（約 9.7 MB；UTF-8 with BOM）
- [翻譯來源與授權聲明](ATTRIBUTION.md)｜[自動轉換方式](#自行重建與校對)

## 安裝至 Star Citizen

1. **關閉遊戲。** 建議先備份已有的 `user.cfg` 與語言檔，避免覆蓋其他個人設定。
2. 將本專案的 `global.ini` 複製到遊戲根目錄下：

   ```text
   StarCitizen/LIVE/data/Localization/chinese_(traditional)/global.ini
   ```

3. 在同一遊戲根目錄建立或編輯 `user.cfg`，加入：

   ```ini
   g_language = chinese_(traditional)
   g_languageAudio = english
   ```

4. 正常啟動遊戲，確認主選單、mobiGlas、物品庫存、任務文字是否顯示繁體中文。

**Fedora／Wine 例子：**

```text
~/SC/StarCitizen/LIVE/user.cfg
~/SC/StarCitizen/LIVE/data/Localization/chinese_(traditional)/global.ini
```

這種方法**只增添文字檔與語言設定**，不替換 `StarCitizen.exe`、`Data.p4k`、DLL 或反作弊元件。請確認語言檔與目前遊戲版本相容，若更新遊戲後顯示異常，可先還原原有設定。

### 如何還原？

關閉遊戲後移走 `chinese_(traditional)/global.ini`，並從 `user.cfg` 移除上述語言設定，或還原安裝前的備份；不需要修改或重新下載遊戲本體。

## 翻譯策略

| 部分 | 處理方式 |
|---|---|
| 物品、船艦、地點等專有名稱 | 沿用 42Kit 半漢化原版的**英文**，例如 `Hurston`、`Lorville`、`Drake Corsair` |
| 一般文字與選單 | OpenCC `s2twp`（簡體 → 臺灣繁體／常用詞） |
| 台灣用語 | 例如「滑鼠」、「伺服器」、「太空站」、「取得」，另針對購物和庫存提示修訂 |
| 遊戲動態標記 | 保留 `~mission(...)`、`<EM4>`、`%s`、`\\n` 等格式與變數 |

目前保留 **90,946 筆 Key**；**57,301 筆**內容經過字詞轉換或修訂，**20 筆**提示重新撰寫。上述數字不等於 57,301 筆人工翻譯；詳見 [build-report.json](build-report.json)。

## 自行重建與校對

此儲存庫**不重新發布上游簡體原始檔**；重建時請向原作者取得同版本檔案。

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-build.txt
mkdir -p sources
curl -L 'https://ini.42kit.com/half/global.ini' -o sources/42kit-half.ini
python3 scripts/build_tw.py
sha256sum output/global.ini
```

下載來源可能持續更新；只有 `sources/42kit-half.ini` 的 SHA-256 與 [build-report.json](build-report.json) 記載的來源相同時，才應期待輸出內容完全一致。重建會輸出 `output/global.ini`，不會自動修改遊戲目錄。

提供翻譯錯誤回報時，請附上**遊戲版本、對應的字串 Key、錯誤文字、建議台灣譯法**，有遊戲畫面更好；請不要上傳個人帳號、完整遊戲日誌或含個資的截圖。

## 翻譯來源與授權

本翻譯衍生自 **42Kit／星際公民漢化組**的非商業社群語言包，使用 **CC BY-NC-SA 4.0**，轉載、修改或再發布請標註來源與改作並遵守**非商業、相同方式分享**規定。臺灣詞彙方向參考 [StarCitizen-TCTP](https://github.com/Orbit-Startech/StarCitizen-TCTP)，但**未直接合併其 GPL 授權的完整譯文**。

- [完整署名與授權範圍](ATTRIBUTION.md)
- [CC BY-NC-SA 4.0 正式英文授權全文](LICENSE)
- [42Kit 上游漢化說明](https://citizenwiki.cn/Localization)

本專案**非官方**，與 Cloud Imperium Games／Roberts Space Industries 無關。
