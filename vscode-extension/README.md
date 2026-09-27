# 🐍 森蚺 VSCode 智囊擴充套件 (Senran Extension)

> **「操鍵如撫琴，落字皆雅言。」**  
> 本擴充套件專為 **森蚺（Senran）** 設計，讓你在 VSCode 中撰寫 Python 時，能像母語般流暢補全文言指令、獲得懸停典籍註解，並一鍵展開常用演算法片段。

---

右鍵有四項轉換：周蟒（白話）、森蚺（文言）、Markdown（駢文）、西文（Python）；編輯器頂端不放按鈕。轉換共用 Python 核心，
請先以 Python 3.12 以上安裝此專案；若執行檔不叫 `python3`，在設定中填入
`senran.pythonPath`。須取消局部選取，以完整文卷轉換並保留還原封卷。

化俗為雅採整庫閱覽模式：未遮蔽之內建詞與語法轉為中文，未知變數、外部名稱及點號屬性保留，
`from/import/as` 引卷句亦存其舊，字串與註解不動；併入周蟒繁、簡詞表，可混用白話與文言語法。
此模式由 `senran run` 還原並執行，不宣稱直接交給原生 Python 即可執行任意文言化專案。
在 Markdown 文卷上可轉周蟒、森蚺，或直接還原 Python。周蟒與森蚺互轉保留最初來源的還原契。
右鍵「西文」對中文原稿翻譯語法，對 Python 原稿逐字還原；原稿還原 API 與整庫 decode 另保留中文原稿本身。
中文封卷修改後仍可吟詠與互轉，採目前正文重新封卷；未改封卷才保證逐字回到最初原稿。
嚴格原稿還原 API／整庫 decode 仍驗校原卷。駢文碼塊的外層校驗亦保留，須先解賦成代碼後再編輯；正文修辭不影響單卷解賦。
轉為中文後自動切至森蚺語言模式，還原西文則切回 Python。
存檔後按 F5（僅森蚺模式），或由命令選單取「森蚺：吟詠當前文卷」，即由 `senran run` 編譯而行；Markdown 亦可用命令選單吟詠。
勿用原生 Python 的執行按鈕直行中文卷。腳本引數可於終端傳入：`senran run file.senran argument`。

## 🌟 核心功能

1. **智慧補全 (IntelliSense Auto-Completion)**：
   * 在 `.py` 或 `.sr` 檔案中輸入漢字或拼音（如輸入 `shu` 提示 `書`、輸入 `liang` 提示 `量`），即可自動補全為標準森蚺指令。
   * 補全項目包含完整原語提示（如 `[森蚺] print`、`[森蚺] requests.get`、`[森蚺] torch.tensor`）。
2. **懸停解經 (Hover Tooltips)**：
   * 滑鼠移至任何文言符節（如 `書`、`得`、`反溯`、`陣`、`清勢`）上方，即刻彈出古典註解卡片、底層對應之 Python 原生函式，以及標準調用範例。
3. **百家代碼片段 (Code Snippets)**：
   * `sr-init`：森蚺起手引用
   * `sr-http`：Requests 雲端探訪模板
   * `sr-torch` / `sr-nn`：PyTorch 深度求導與神經網絡訓練模板
   * `sr-numpy`：NumPy 矩陣算學模板
   * `sr-pandas`：Pandas 卷帙統計模板
   * `sr-file-read` / `sr-file-write`：檔案批閱上下文模板
   * `sr-sqlite`：SQLite 公堂案台資料庫模板

---

## 📦 安裝與打包方式

### 1. 本地打包為 `.vsix` 安裝檔
在 `vscode-extension` 目錄下執行：
```bash
npx @vscode/vsce package
```
即可產出 `senran-vscode-0.1.9.vsix`，內含與 README 相同的專案圖示。

### 2. 在 VSCode 中載入
* 開啟 VSCode，按下 `Ctrl+Shift+P`（Mac 鍵為 `Cmd+Shift+P`）
* 輸入並選擇：`Extensions: Install from VSIX...`
* 挑選剛產出的 `.vsix` 檔案，即可啟動森蚺智囊！
