# 🐍 森蚺 (Senran)

> **「昔者伏羲作八卦以通神明之德，周公制禮樂而布九數之規。漢有《九章算術》，窮幽索微，為百代算法之宗；近世有高士作《周蟒》，始使華夏文字驅策西土靈機。今作『森蚺』，遠追《九章》之遺法，近承《周蟒》之宏願，以古雅文言驅策萬象西邦庫卷，海納百川，有容乃大。」**

[![授權條款：MIT](https://img.shields.io/badge/授權-MIT-yellow.svg)](LICENSE)
[![版本：Python 3.8+](https://img.shields.io/badge/法度-Python%203.8+-blue.svg)](https://www.python.org/)
[![考校：皆備](https://img.shields.io/badge/考校-三十四試咸吉-brightgreen.svg)]()

---

## 📜 稽首前修（致敬）

本卷之作，不敢自專，謹稽首致敬於先賢巨帙：

* 🏛️ **《九章算術》**：成於兩漢，劉徽、李淳風為之注。以「方田、粟米、衰分、少廣、商功、均輸、盈不足、方程、勾股」列章，開萬算之法門。森蚺之思辨與章程，皆本乎九章之風骨。
* 🐍 **《周蟒》（zhpy）**：近人林哲正（gasolin）於丁亥歲（2007）所辟道統。開以華文撰寫 Python 之先河，破夷夏之隔，示後學以大道。
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

## 🤖 天機神思・機巧使（三界無損互轉與外邦 Agent 調度）

森蚺專為「不會寫代碼之人」與「天機神思（AI Coding Agent）」立下宏願：  
以白話或文言策問，三界代碼一體同生；亦使任意專案之 AI（Cursor、Claude Code、Copilot、ChatGPT）即刻化身為「機巧使」！

### 1. 白話策問，三界同生（三界章程）
不會寫代碼之人，只需輸入白話意向，機巧使即刻鋪排「三界互轉代碼」：
1. **駢儷賦體 (.md)**：四六對仗、文言詩性，閱讀者無需閱讀繁複註解，閱文即明其意。
2. **森蚺文言 (.py)**：端方古雅之文言代碼，底層直通 Python 執行。
3. **西邦原碼 (.py)**：標準原生 Python 代碼，便於西文環境融會貫通。

```python
from senran import 機巧使

# 策問白話意向
成果 = 機巧使.策問("我想抓取網頁並解析內容")

print(成果["駢體賦"])  # 📜 .md 駢儷賦體文章（供人直觀閱讀）
print(成果["森蚺碼"])  # 🐍 森蚺文言代碼（可直接執行）
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

### 🧩 智囊伴侶：VSCode 專屬擴充套件（senran-vscode）

為使諸位學士操鍵如撫琴、落字皆雅言，專案隨附 **VSCode 專屬智囊套件**（位於 `vscode-extension/`）：

* 🔤 **西邦之言自動提雅**：凡檔案載入森蚺（`from senran import ...`），鍵入習慣之英文（如 `print`、`len`、`status_code`、`backward`），下拉選單即自動於首位推舉對應古雅文言（`書`、`計`、`格`、`反溯`）！
* ✨ **落字成章（智慧自動補全）**：輸入漢字或拼音（如鍵入 `shu` 提示 `書`、`fansu` 提示 `反溯`、`liang` 提示 `量`），自動帶出底層 Python 原語註釋。
* 📜 **懸停解經（Hover Tooltips）**：滑鼠移至任一文言字詞，即刻顯現古典註解、Python 原語對照與用法範例。
* ⚡ **通神符咒（Code Snippets）**：支援 `sr-init`（起手）、`sr-http`（雲端探訪）、`sr-torch`（深度神思）、`sr-file`（案牘卷宗）等一鍵展開。

**一鍵載入法**：
進入 VSCode 按下 `Ctrl+Shift+P` $\to$ 選取 `Extensions: Install from VSIX...` $\to$ 挑選 `vscode-extension/senran-vscode-0.1.5.vsix` 即可！

---

### 🔄 化俗為雅：一鍵文言轉錄儀（Transpiler）

習於西邦法度者，不必強記文言符節。森蚺自帶**一鍵轉錄儀**，將尋常 Python 秒化為古雅文章：

* 🖱️ **VSCode 鼠標一鍵化雅**：在編輯器中對任意 Python 檔案按滑鼠右鍵，點擊 **「🐍 森蚺：一鍵化俗為雅（轉錄為文言代碼）」**（或快捷鍵 `Ctrl+Alt+W` / Mac `Cmd+Alt+W`），選取之處或全篇代碼即刻轉為文言！
* 💻 **終端命令列轉錄**：
  ```bash
  # 直接轉錄並存為新檔
  senran input.py -o refined.py
  ```

---

### 🔄 化雅為俗：一鍵逆轉外邦代碼（Reverse Transpiler）

若需將森蚺文言代碼交予西邦無文言支援之同仁或舊式環境，可隨時一鍵逆轉為標準原生 Python：

* 🖱️ **VSCode 鼠標一鍵化俗**：在編輯器中對任意文言檔案按滑鼠右鍵，點擊 **「💻 森蚺：一鍵化雅為俗（逆轉為標準西邦代碼）」**（或快捷鍵 `Ctrl+Alt+E` / Mac `Cmd+Alt+E`），選取之處或全篇代碼即刻精準還原為原生 Python！
* 💻 **終端命令列化西文**：
  ```bash
  # 將文言檔案逆轉為標準 Python 原碼
  senran 化西文 refined.py -o standard.py
  ```

---

### 🪶 聲律風骨：四六駢儷格式化儀（Pianwen Formatter `.md`）

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

本卷內蘊三十四項法度考校，以驗算理之精微：

```bash
python3 -m unittest discover -s tests -v
```
> 報曰：`Ran 34 tests ... OK`，諸法咸吉。

---

## 📜 牌記（LICENSE）

本卷遵行 **MIT 授權牌記**。  
天地無私，斯術同乘。天下學士，皆得傳鈔、講習、刊刻與興造，垂范後世。
