<p align="center">
  <img src="assets/senran-icon.png" alt="森蚺圖徽" width="256">
</p>

# 🐍 森蚺 (Senran)

> **「昔者伏羲作八卦以通神明之德，周公制禮樂而布九數之規。漢有《九章算術》，窮幽索微，為百代算法之宗；近世有高士作《周蟒》，始使華夏文字驅策西土靈機。今作『森蚺』，遠追《九章》之遺法，近承《周蟒》之宏願，以古雅文言驅策萬象西邦庫卷，海納百川，有容乃大。」**

[![授權條款：MIT](https://img.shields.io/badge/授權-MIT-yellow.svg)](LICENSE)
[![版本：Python 3.12+](https://img.shields.io/badge/法度-Python%203.12+-blue.svg)](https://www.python.org/)
[![考校](https://img.shields.io/badge/考校-無損往返-brightgreen.svg)](#整庫無損轉錄)

---

## 📜 稽首前修（致敬）

本卷之作，不敢自專，謹稽首致敬於先賢巨帙：

* 🏛️ **《九章算術》**：成於兩漢，劉徽、李淳風為之注。以「方田、粟米、衰分、少廣、商功、均輸、盈不足、方程、勾股」列章，開萬算之法門。森蚺之思辨與章程，皆本乎九章之風骨。
* 🐍 **《周蟒》（zhpy）**：近人林哲正（gasolin）於丁亥歲（2007）所辟道統。開以華文撰寫 Python 之先河，破夷夏之隔，示後學以大道。今已併入其繁、簡詞表，承其白話之法，益以文言之律；源流與授權，詳見下章。
* 🖋️ **《文言》（wenyan-lang）**：黃令東先生所創之奇巧語言，極盡辭章文理之美，同為吾輩心儀之典範。

---

## 🌌 萬象森羅說（第一性原理）

今西邦有術名曰 **Python**，本蟒類也。其術縱橫四海，名庫千百，然皆操西土鳥篆，学者每有望洋之嘆。  
或曰：「天下庫卷何止億萬，欲盡譯之，非窮畢生之力不可為也，安能全備？」  
**答曰：非也。**

**術曰：**  
西邦之機，行法有常。察其動靜，不外乎名與物而已。  
客欲問物，機必有應；若所問之名未見，則遣「轉發客」司之。轉發客懷古今之典律，以「取」易 `get`，以「書」易 `write`，以「格」易 `status_code`。雖庫殊派異，其理則一。  
故森蚺不設萬千死格，但立**「萬象森羅代理客」**，逢山開道，遇水搭橋。凡西邦之庫，入我門來，皆隨手化為雅言。

---

## 🛠️ 置辦營造（安裝與引入）

### 1. 遙程直引（無需手動 Clone，一行即成正式庫）

任何學士皆可透過 `pip` 直自太虛倉庫（GitHub）銘刻入系統環境：

```bash
pip install git+https://github.com/sucryan/senran.git
```
*(若已刊印至 PyPI 平台，則直書 `pip install senran` 即可)*

### 2. 案台傳鈔（本機原始碼開發）

```bash
git clone https://github.com/sucryan/senran.git
cd senran
pip install -e .
```

---

## 📜 白話文言，同出一門（周蟒融入）

森蚺已將[周蟒](https://github.com/gasolin/zhpy)之繁、簡中文詞表改編併入，非止列名致敬。
使用者可兼用白話、文言與 Python 原語；變數之名，中西皆可，無須盡易為漢字。
森蚺之增益，在於文言語法、萬象代理與駢文往返；周蟒之白話根基，仍存其用。

```python
類別 Box:
    術 value(我):
        如果 真:
            歸 3

印出(Box().value())
```

此卷兼用周蟒之「類別、我、如果、印出」與森蚺之「術、歸」；可存為 `mixed.senran`，循下令而行：

```bash
senran run mixed.senran
```

欲由西文轉周蟒、由周蟒轉森蚺，或復歸原文，亦有專令：

```bash
senran zhpy input.py -o plain.senran
senran plain.senran -o classical.senran
senran 化西文 plain.senran -o original.py
```

由有封卷之周蟒或森蚺互轉，仍保最初來源之還原契；手寫未封之中文卷，化西文則依詞律譯為 Python，不冒稱曾有西文原稿。
右鍵之「西文」以 Python 為歸處：若原稿本為中文方言，則譯其語法；若原稿本為 Python，則逐字復之。
另 `化西文()`、`senran 化西文` 及整庫 `decode` 為原稿還原之契，封卷起於中文者，仍可取回原中文稿，不與編譯混同。

### 文言語法之律

| 部類 | Python 原語 | 森蚺文言 |
| :--- | :--- | :--- |
| 定術立類 | `def`、`class`、`lambda`、`return` | `術`、`類`、`匿名`、`歸` |
| 分途擇路 | `if`、`elif`、`else`、`match`、`case` | `若`、`若又`、`否則`、`配`、`案` |
| 巡覽進退 | `for`、`in`、`while`、`break`、`continue`、`pass` | `遍`、`於`、`當`、`止`、`續`、`略` |
| 驗算辨偽 | `try`、`except`、`finally`、`raise`、`assert` | `試`、`捕`、`終`、`擲`、`驗` |
| 引卷共事 | `from`、`import`、`as`、`with` | `由`、`納`、`作`、`偕` |
| 異步產值 | `async`、`await`、`yield` | `異步`、`候`、`產` |
| 判理取捨 | `and`、`or`、`not`、`is` | `且`、`或`、`非`、`乃` |
| 名域刪改 | `global`、`nonlocal`、`del`、`type`（型別宣告） | `全域`、`外域`、`刪`、`型別宣告` |
| 元常通配 | `True`、`False`、`None`、`_`（通配） | `真`、`假`、`空`、`任` |

周蟒白話亦可用「定義／定义、返回、取、在、嘗試／尝试、印出／打印」等詞；英語關鍵字亦無須禁絕。
詞與名須依 Python 之法分隔，如 `如果 真:`，不將 `如果真` 強拆為二詞。字串、註解與點號後之屬性不作語法改寫。
中文語法卷須經 `senran run` 翻譯而行，不可直接交付原生 `python mixed.senran`；中文語法詞及白話內建詞，在此入口視為保留之名。
整庫與右鍵轉錄時，引卷之句保留原生 `from/import/as`；外邦模組、屬性與未載之變數名亦存其舊，不強易漢字代號。
VS Code 轉為周蟒或森蚺後，語言模式隨之改為森蚺；按 **F5**，或由命令選單取「森蚺：吟詠當前文卷」，即可存檔而行。
Markdown 亦可由此命令吟詠。右鍵仍止四項轉換，不增編輯器頂端按鈕。

### 源流與授權

所併者為周蟒 `zhpy3/plugtw.py`、`plugcn.py` 之詞表，來源提交為
[`f4d932a`](https://github.com/gasolin/zhpy/tree/f4d932a5ab810158ef4e4113df337cbf7d83817a)。
其著作權歸 **Fred Lin and contributors（2007 起）**，遵 MIT 授權；完整聲明保留於
[`senran/zhpy_keywords.py`](senran/zhpy_keywords.py)。
本次併入語法及現行 Python 3 內建詞之轉譯，不攜周蟒舊執行器；不宣稱 Python 2 程式、插件、中文模組名與方法名皆可原樣運行。

---

## 🤖 天機神思・機巧使（三界無損互轉與外邦 Agent 調度）

森蚺專為「不會寫代碼之人」與「天機神思（AI Coding Agent）」立下宏願：  
以白話或文言策問，三界代碼一體同生；亦使任意專案之 AI（Cursor、Claude Code、Copilot、ChatGPT）即刻化身為「機巧使」！

### 1. 白話策問，三界同生（三界章程）

不會寫代碼之人，只需輸入白話意向，機巧使即刻鋪排「三界互轉代碼」：

1. **駢儷賦體 (.md)**：四六對仗、文言詩性，閱讀者無需閱讀繁複註解，閱文即明其意。
2. **森蚺文言 (.senran)**：端方古雅之文言代碼，經 `senran run` 譯為 Python 而行。
3. **西邦原碼 (.py)**：標準原生 Python 代碼，便於西文環境融會貫通。

```python
from senran import 機巧使

# 策問白話意向
成果 = 機巧使.策問("我想抓取網頁並解析內容")

print(成果["駢體賦"])  # 📜 .md 駢儷賦體文章（供人直觀閱讀）
print(成果["森蚺碼"])  # 🐍 森蚺文言代碼（以 senran run 執行）
print(成果["標準碼"])  # 💻 標準原生 Python 代碼
```

### 2. 三界無損雙向互轉

```python
from senran import 機巧使

# 西邦標準 Python ⇄ 森蚺文言
森蚺碼 = 機巧使.化森蚺("res = requests.get('https://example.com')")
標準碼 = 機巧使.化西文(森蚺碼)

# 代碼 ⇄ 四六駢儷賦體 (.md)
駢文 = 機巧使.化駢文(森蚺碼)
可執行碼 = 機巧使.解駢文(駢文)
```

### 3. 一鍵設壇（如何讓外部專案的 AI Agents 正常調用）

當學士在其他專案以 `pip install senran` 引入本庫時，如何讓 Cursor、Claude Code、GitHub Copilot 或 Antigravity 知道要化身為「機巧使」？

只需在專案目錄下敲一行指令：

```bash
senran 設壇
```
森蚺即刻於當前專案自動銘刻：

* `AGENTS.md` & `Agent.md`（通用 Agent 法典）
* `.cursorrules`（Cursor 專屬憲則）
* `CLAUDE.md`（Claude Code 專屬憲則）
* `.github/copilot-instructions.md`（GitHub Copilot 專屬憲則）

從此，該專案內的任何 AI 工具皆會自動以「機巧使」之身分發言，遵循《九章算術》之雅言，自動生成森蚺文言與 .md 駢體！

### 4. 網頁版 AI（ChatGPT / Claude / Gemini / DeepSeek）敕令

若使用瀏覽器網頁版 AI，只需在終端執行：

```bash
senran 敕令
```
複製輸出之「機巧使明詔」，貼入 AI 對話窗或自訂指令中，該 AI 即刻開悟化身為森蚺機巧使。

### 5. 終端開壇論道（REPL 互動）

```bash
# 終端交互式對話，直接向機巧使吩咐意向
senran 策問

# 或單次策問
senran 策問 "我想訓練神經網路計算梯度"
```

---

## 🧩 智囊伴侶（VS Code 擴充套件）

為使諸位學士操鍵如撫琴、落字皆雅言，專案隨附 **VSCode 專屬智囊套件**（位於 `vscode-extension/`）：

* 🔤 **西邦之言自動提雅**：凡檔案載入森蚺（`from senran import ...`），鍵入習慣之英文（如 `print`、`len`、`status_code`、`backward`），下拉選單即自動於首位推舉對應古雅文言（`書`、`計`、`格`、`反溯`）！
* ✨ **落字成章（智慧自動補全）**：輸入漢字或拼音（如鍵入 `shu` 提示 `書`、`fansu` 提示 `反溯`、`liang` 提示 `量`），自動帶出底層 Python 原語註釋。
* 📜 **懸停解經（Hover Tooltips）**：滑鼠移至任一文言字詞，即刻顯現古典註解、Python 原語對照與用法範例。
* ⚡ **通神符咒（Code Snippets）**：支援 `sr-init`（起手）、`sr-http`（雲端探訪）、`sr-torch`（深度神思）、`sr-file`（案牘卷宗）等一鍵展開。

**一鍵載入法**：

先入 `vscode-extension/`，行 `npx @vscode/vsce package` 以成安裝卷；Git 惟收原碼與圖徽。
於 VS Code 按 `Ctrl+Shift+P`，選 `Extensions: Install from VSIX...`，納入 `senran-vscode-0.1.7.vsix` 即可。
右鍵列四途：**周蟒（白話）、森蚺（文言）、Markdown（駢文）、西文（Python）**。
不置按鈕於編輯器頂端。四令共用轉錄之核，Markdown 亦可轉周蟒、森蚺或還原 Python。

---

## 🔄 化俗為雅（文言轉錄儀）

習於西邦法度者，不必強記文言符節。森蚺自帶**一鍵轉錄儀**，將尋常 Python 秒化為古雅文章：

* 🖱️ **VSCode 鼠標一鍵化雅**：於 Python 卷中按右鍵，選 **「🐍 森蚺：一鍵化俗為雅（轉錄為文言代碼）」**（或按 `Ctrl+Alt+W` / Mac `Cmd+Alt+W`），即可轉錄全卷；不取片段，以全還原之契。
* 💻 **終端命令列轉錄**：
  ```bash
  # 直接轉錄並存為新檔
  senran input.py -o refined.py
  ```

---

## 🔄 化雅為俗（原碼還原儀）

若需將森蚺文言代碼交予西邦無文言支援之同仁或舊式環境，可隨時一鍵逆轉為標準原生 Python：

* 🖱️ **VSCode 鼠標一鍵化俗**：於文言卷中按右鍵，選 **「💻 森蚺：一鍵化雅為俗（逆轉為標準西邦代碼）」**（或按 `Ctrl+Alt+E` / Mac `Cmd+Alt+E`），即可還原全卷；有封卷者，依其紀錄逐字復原。
* 💻 **終端命令列化西文**：
  ```bash
  # 將文言檔案逆轉為標準 Python 原碼
  senran 化西文 refined.py -o standard.py
  ```

---

## 🪶 聲律風骨（駢儷格式化儀）

森蚺之格式化，非僅縮排空格之小巧，乃**將代碼排版為四六對仗、聲律清朗之駢儷賦體 Markdown 文章（.md 卷帙）**！任何人使用 Markdown 預覽即可獲得極佳之閱讀體驗：

```markdown
# 📜【森蚺駢儷憲典 · 賦體卷】

> 夫運籌於帷幄之中，決勝於方寸之間。

置百家之珍，引「requests」入府，銘曰「求」；  
遣驛使以往訪，運籌「求.得('https://httpbin.org/get')」，定卷為「報」；  
若夫考校其理，審「報.格 == 200」符契而稱是：  
    几案展卷，落字有聲，明書其辭：'功成：', 報.文[:20]；  

---
*🪶【賦畢 · 算道咸吉】*
```

* 📜 **VSCode 一鍵排賦**：按右鍵點選 **「📜 森蚺：賦體排版（化為 Markdown 駢儷文章）」**（快捷鍵 `Ctrl+Alt+P` / Mac `Cmd+Alt+P`），即刻在側窗展卷朗閱 Markdown！
* 💻 **終端轉賦與吟詠執行**：
  ```bash
  # 1. 將 Python 排版為 .md 駢文
  senran format input.py -o poem.md

  # 2. 直接吟詠執行 .md 駢文卷帙！
  senran run poem.md
  ```

---

## 整庫無損轉錄

欲舉一庫而易其文，復循原路而歸其本，可依四令，次第行之：

```bash
senran repo encode 原庫 森蚺庫
senran repo format 森蚺庫 駢文庫
senran repo unformat 駢文庫 解賦庫
senran repo decode 解賦庫 還原庫
```

若欲舉庫轉為周蟒，首令改為 `senran repo encode-zhpy 原庫 周蟒庫`；其後排賦、解賦、還原之法皆同。

### 閱卷之法

整庫閱覽體，語法關鍵字易為文言，惟引卷之句保留原生；內建詞未遭遮蔽者取雅稱，其餘名稱存其舊。
字串、註解及檔名，皆存其舊；`.pyx`、C、圖像諸卷，亦原樣搬存。
此體為閱覽與還原而設，欲行其算，須先復為 Python；不可謂萬庫譯畢皆能直行。
Python 須為 3.12 以上，方能辨 f-string 中之名稱。

### 封卷之契

新庫之目錄須未存在，且不得與原庫相疊。每轉一界，留名稱、編碼之對照與校驗值，
不另暗藏原碼副本；駢文則附完整森蚺碼卷，以備解賦。碼卷或清冊不合，遂止而報異，不妄稱還原。

所存者，一般檔案之位元組、權限、連結與空目錄；Git 歷史、時間戳、硬連結關係及延伸屬性，不在此契。
舊有 `化雅()` 與 `senran input.py` 仍循代理體之法，兼存逐字還原紀錄；惟其詞律有界，不保任意外邦程式皆可直行。
新封之卷可無損往返；舊式純駢文若無完整碼卷，須重製而後解之。

### 諸庫考校

參考原庫置於 `examples/upstream/`，四界之卷置於 `examples/roundtrip/`；二者皆由 Git 忽略，不入本庫史冊。

```bash
python3 tools/verify_repositories.py --fetch
python3 tools/verify_repositories.py --style zhpy
```

考校先定各庫之 Git 提交，繼而逐檔比對位元組、權限、連結與目錄；不執行其程式，亦不鍛造或評估外邦機器學習之術。
十二庫、四千三百五十五份 Python 卷，往返皆無差異；詳見[考校與辨偽錄](docs/review-2026-09-28.md)。

---

## 📖 九章演算法（使用範例）

### 卷之一【方田】—— 啟蒙立基，度量名錄

> **今有門生四人，欲錄其名號，算其多寡，並列其序。問：何如調度？**  
> **答曰：得門生四位，整飭如禮。**

```python
from senran import 書, 計, 疇, 錄, 序, 若, 真

# 几案印出
書("問天地好在，四海安康！")

# 錄籍與度量
門生 = 錄(["顏回", "子路", "子貢", "冉有"])
書("門徒人數：", 計(門生))

# 劃定疆界巡覽 (range)
for 數 in 疇(1, 4):
    書(f"第 {數} 通鼓，起！")

# 依理排序
功名 = 錄([88, 92, 75, 99])
書("按等第排列：", 序(功名))
```

---

### 卷之二【均輸】—— 馳驛千里，雲端通訊（Requests）

> **今有驛使欲探太虛之境（HTTP API）。問：路途通暢否？所攜幾何？**  
> **答曰：得格二百，其途坦蕩。**

```python
from senran import 引入, 書

# 引入西邦 requests 庫
求 = 引入("requests")

# 遣驛使前往探問 (get)
報 = 求.得("https://httpbin.org/get")

書("驛使回報狀態格：", 報.格)         # status_code -> 200
書("此行順遂否：", "吉" if 報.格 == 200 else "凶")
書("驛報文章前段：", 報.文[:50])        # text
書("剖解為譜：", 報.譜().get("url"))   # json()
```

---

### 卷之三【勾股】—— 方陣運算，割圓量海（NumPy / Math）

> **今有八卦方陣，各布其數。欲考其形貌，求其總和，推其均平。問：法何出？**  
> **術曰：以陣布列，總其數，均其值。**

```python
from senran import 引入, 書

算術 = 引入("math")
算矩 = 引入("numpy")

# 開方測距 (sqrt)
書("開方八十一得：", 算術.開方(81))

# 八卦方陣 (array)
方陣 = 算矩.陣([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

書("方陣形貌：", 方陣.形)   # shape -> (3, 3)
書("全陣均值：", 方陣.均())  # mean() -> 5.0
書("全陣總和：", 方陣.總())  # sum()  -> 45
```

---

### 卷之四【商功】—— 案牘批閱，卷宗進退（檔案讀寫與 SQLite）

> **今有良銘欲刻於石碑，復有英雄榜欲定於公堂。問：何以銘之？何以存之？**  
> **答曰：開卷以筆銘，立堂以法判。**

```python
from senran import 引入, 啟, 書

# 1. 卷宗檔案上下文 (with 啟)
with 啟("銘刻.txt", "w", encoding="utf-8") as 牘:
    牘.書("天下大事，必作於細。")  # write

with 啟("銘刻.txt", "r", encoding="utf-8") as 牘:
    書("石碑銘文：", 牘.閱())      # read

# 2. 府衙案台 (SQLite3)
庫 = 引入("sqlite3")
連線 = 庫.通(":memory:")         # connect
案台 = 連線.案台()               # cursor

案台.判詞("CREATE TABLE 榜 (名 TEXT, 功 INT)") # execute
案台.判詞("INSERT INTO 榜 VALUES ('關雲長', 99), ('趙子龍', 98)")
案台.判詞("SELECT * FROM 榜")

書("英雄名冊：", 案台.盡攬())     # fetchall
連線.閉()                        # close
```

---

### 卷之五【盈不足】—— 天機神思，反溯知微（PyTorch 深度學習）

> **今有神經絡層，欲窮天機之理，初始權重或盈或不足。問：何以修為，使損耗歸無？**  
> **術曰：布列張量，前行推演，反溯求勢，精進步新。**

```python
from senran import 引入, 書, 疇

神算 = 引入("torch")
神兵 = 引入("torch.nn")
調律 = 引入("torch.optim")

# 1. 自動求導 (Autograd)
# 設權重 w=2.0, 求 f(w) = 3 * w^2 + 5 之梯度 (df/dw = 6*w = 12.0)
權 = 神算.量([2.0], requires_grad=True)
損 = 3 * (權 ** 2) + 5
損.反溯() # backward()
書("反溯求勢所得（梯度）：", 權.勢.析值()) # grad.item() -> 12.0

# 2. 神經網絡鍛造 (Neural Network Training)
絡 = 引入(神兵.Linear(1, 1))
優化客 = 引入(調律.SGD(絡.本.parameters(), lr=0.01))

x = 神算.量([[1.0], [2.0], [3.0]])
y = 神算.量([[2.0], [4.0], [6.0]])

for 輪 in 疇(1, 51):
    優化客.清勢()          # zero_grad()
    預測 = 絡(x)           # forward
    當前損 = ((預測 - y) ** 2).均()
    當前損.反溯()          # backward()
    優化客.步進()          # step()

書("歷練圓滿，推測 x=4 之數：", 絡(神算.量([[4.0]])).析值())
```

---

## 📑 典律總目（常用文言對照）

森蚺體察古今，定常用之符節如下：

| 部類 | 文言召喚 | 底層 Python 屬性 / 函式 | 常用庫示例 |
| :--- | :--- | :--- | :--- |
| **元常** | `真`、`假`、`空`、`無` | `True`、`False`、`None` | 內建 |
| **几案** | `書`、`問`、`審`、`係` | `print`、`input`、`type`、`isinstance` | 內建 |
| **度量** | `計`、`疇`、`總`、`極大`、`極小` | `len`、`range`、`sum`、`max`、`min` | 內建 |
| **收納** | `得`、`取`、`徵`、`索`、`尋` | `get`、`fetch`、`find`、`search` | requests, bs4, re |
| **傳遞** | `投`、`寄`、`發`、`置`、`設` | `post`、`send`、`put`、`set` | requests, httpx, socket |
| **驛報** | `格`、`態`、`文`、`實`、`譜` | `status_code`、`text`、`content`、`json` | requests, urllib |
| **矩陣** | `陣`、`形`、`均`、`和`、`塑`、`皆零` | `array`、`shape`、`mean`、`sum`、`reshape`、`zeros`| numpy, scipy |
| **卷帙** | `欄`、`冠`、`履`、`描述`、`依序` | `columns`、`head`、`tail`、`describe`、`sort_values`| pandas, polars |
| **天機** | `量`、`勢`、`反溯`、`清勢`、`步進`、`析值` | `tensor`、`grad`、`backward`、`zero_grad`、`step`、`item` | PyTorch, TensorFlow |
| **機心** | `習`、`訓`、`卜`、`斷`、`考分`、`習化` | `fit`、`train`、`predict`、`score`、`fit_transform` | scikit-learn, XGBoost |
| **丹青** | `繪`、`布星`、`立柱`、`題`、`存圖` | `plot`、`scatter`、`bar`、`title`、`savefig` | matplotlib, seaborn |
| **案牘** | `啟`、`閱`、`書`、`閉`、`通`、`判詞` | `open`、`read`、`write`、`close`、`connect`、`execute`| io, os, sqlite3 |
| **行者** | `歷程`、`行者`、`化規` | `tqdm`、`model_dump` | tqdm, pydantic |
| **律則** | `為_*`、`化_*`、`取_*`、`設_*` | `is_*`、`to_*`、`get_*`、`set_*` | 萬用前綴自動轉譯 |

> **注**：凡未及備載之冷僻西域名稱，森蚺皆直接放行相容。若誤筆求不可得之物，森蚺必自省其身，出古典之辭指引相近字，絕無窒礙。

---

## 🧪 考校明察（測試驗證）

本庫收轉錄、搬卷及編輯器之考校；不須另納外邦機器學習庫，亦不行其術：

```bash
python3 -m unittest discover -s tests -v
```

> 考校須報 `OK`，原碼往返四界，位元組須悉同。舊案台若留未入 Git 之考校，不屬本卷所載。

---

## 📜 牌記（LICENSE）

本卷遵行 **MIT 授權牌記**。  
天地無私，斯術同乘。天下學士，皆得傳鈔、講習、刊刻與興造，垂范後世。
