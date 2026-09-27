# 🐍 森蚺 VSCode 智囊擴充套件 (Senran Extension)

> **「操鍵如撫琴，落字皆雅言。」**  
> 本擴充套件專為 **森蚺（Senran）** 設計，讓你在 VSCode 中撰寫 Python 時，能像母語般流暢補全文言指令、獲得懸停典籍註解，並一鍵展開常用演算法片段。

---

右鍵保留三項轉換指令，編輯器頂端不放按鈕。轉換共用 Python 核心，
請先以 Python 3.12 以上安裝此專案；若執行檔不叫 `python3`，在設定中填入
`senran.pythonPath`。須取消局部選取，以完整文卷轉換並保留還原封卷。

化俗為雅採整庫閱覽模式：已知名稱依詞典更名，未知名稱用可逆漢字代號，
保留 Python 保留字、字串與註解。此模式須還原後執行，不宣稱直接執行任意文言化專案。
在森蚺 Markdown 文卷上使用「化俗為雅」可解賦，使用「化雅為俗」可直接還原 Python。
駢文中的完整碼卷是還原來源；修改碼卷時會拒絕無損還原，正文修辭不影響單卷解賦。

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
即可產出 `senran-vscode-0.1.6.vsix`，內含與 README 相同的專案圖示。

### 2. 在 VSCode 中載入
* 開啟 VSCode，按下 `Ctrl+Shift+P`（Mac 鍵為 `Cmd+Shift+P`）
* 輸入並選擇：`Extensions: Install from VSIX...`
* 挑選剛產出的 `.vsix` 檔案，即可啟動森蚺智囊！
