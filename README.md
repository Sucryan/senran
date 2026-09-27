# 🐍 森蚺 (Senran)

> **「蛇之巨者，有蟒與蚺。蟒者行於林野，蚺者吞象納百川。」**  
> **森蚺（Senran）** 是一套讓你可以**直接用文言文寫 Python**，並**無縫驅策無數現代第三方函式庫**的優雅動態代理模組。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

---

## 🌟 核心特色 (Highlights)

1. **萬象森羅（Universal Proxy）**：
   不需手動為幾萬個套件重寫 `def`。基於 Python 元編程動態代理機制，引入任何 PyPI 套件（`requests`、`numpy`、`pandas`、`torch` 等），皆可直接文言化調用！
2. **百家相容、永不拋錨**：
   支援常見動詞前後綴（如 `為_` $\to$ `is_`、`化_` $\to$ `to_`、`取_` $\to$ `get_`）。遇生僻屬性自動相容原庫英文名，並在找不到方法時提供文言智慧相近字提示。
3. **雅正凝練**：
   兼具文言韻味與現代編程邏輯，杜絕生硬字面對譯，追求古雅、純粹、簡短之文學意境。
4. **即插即用**：
   標準 Python 模組，無須自定義直譯器或修改解譯器，完美相容 VSCode、Jupyter Notebook 與現代虛擬環境。

---

## 📦 安裝方式 (Installation)

### 本地開發安裝
```bash
git clone https://github.com/sucryan/senran.git
cd senran
pip install -e .
```

---

## 🍵 快速體驗 (Quick Start)

### 1. 天下初開：基礎內建
```python
from senran import 書, 計, 疇, 總, 序, 錄, 若, 真

# 几案印出
書("問天地好在，四海安康！")

# 數算與度量
門徒 = 錄(["顏回", "子路", "子貢"])
書("門徒人數：", 計(門徒))

# 劃定疆界 (range)
for 數 in 疇(1, 4):
    書(f"第 {數} 聲：在！")

# 若則邏輯
功名 = 100
若(功名 >= 60).則(lambda: 書("明斷：及格矣，善哉！"))
```

### 2. 雲端探訪：驅策 Requests
```python
from senran import 引入, 書

# 引入任意第三方庫
求 = 引入("requests")
報 = 求.得("https://httpbin.org/get")

書("回報狀態格：", 報.格)         # status_code
書("驛使所帶之文：", 報.文[:60])     # text
書("剖析為譜：", 報.譜().get("url")) # json()
```

### 3. 格物算學：驅策 NumPy 與 Pandas
```python
from senran import 引入, 書

算矩 = 引入("numpy")
史冊 = 引入("pandas")

# 矩陣計算
陣 = 算矩.陣([[1, 2], [3, 4]])
書("矩陣形貌：", 陣.形)   # shape
書("各項均值：", 陣.均())  # mean()
書("各項總和：", 陣.總())  # sum()

# 資料卷帙
卷 = 史冊.DataFrame({"名": ["太白", "東坡"], "酒量": [100, 80]})
書("卷帙首列：\n", 卷.冠(1))  # head(1)
```

### 4. 府庫檔案與資料庫：File I/O & SQLite3
```python
from senran import 引入, 啟, 書

# 檔案上下文管理 (with)
with 啟("碑銘.txt", "w", encoding="utf-8") as 牘:
    牘.書("天下大事，必作於細。")  # write

with 啟("碑銘.txt", "r", encoding="utf-8") as 牘:
    書("讀得：", 牘.閱())         # read

# SQLite 資料庫操作
庫 = 引入("sqlite3")
連線 = 庫.通(":memory:")      # connect
案台 = 連線.案台()            # cursor
案台.判詞("CREATE TABLE 榜 (名 TEXT, 分 INT)") # execute
案台.判詞("INSERT INTO 榜 VALUES ('子淵', 100)")
案台.判詞("SELECT * FROM 榜")
書("案台得錄：", 案台.盡攬()) # fetchall
連線.閉()                    # close
```

---

## 📜 常用詞律對照 (Lexicon Reference)

| 類型 | 文言屬性 / 方法 | 原生 Python 對應 | 涵蓋範例函式庫 |
| :--- | :--- | :--- | :--- |
| **內建** | `書` / `問` / `計` / `疇` / `總` | `print`, `input`, `len`, `range`, `sum` | Python 核心 |
| **常數** | `真` / `假` / `空` | `True`, `False`, `None` | Python 核心 |
| **型別** | `整` / `浮` / `文` / `錄` / `譜` | `int`, `float`, `str`, `list`, `dict` | Python 核心 |
| **獲取** | `得` / `取` / `徵` / `索` / `尋` | `get`, `fetch`, `find`, `search` | `requests`, `bs4`, `re` |
| **發送** | `投` / `寄` / `置` / `設` | `post`, `send`, `put`, `set` | `requests`, `httpx`, `socket` |
| **傳輸** | `格` / `態` / `文` / `實` / `譜` | `status_code`, `text`, `content`, `json` | `requests`, `httpx`, `urllib` |
| **結構** | `附` / `綴` / `插` / `黜` / `析` / `合` | `append`, `extend`, `insert`, `remove`, `split`, `join` | 序列與容器庫 |
| **檔案** | `啟` / `閱` / `書` / `閉` / `存` | `open`, `read`, `write`, `close`, `exists` | `io`, `os`, `pathlib` |
| **算學** | `開方` / `正弦` / `陣` / `形` / `均` / `總` | `sqrt`, `sin`, `array`, `shape`, `mean`, `sum` | `math`, `numpy` |
| **卷帙** | `欄` / `冠` / `履` / `描述` / `依序` | `columns`, `head`, `tail`, `describe`, `sort_values` | `pandas`, `polars` |
| **判詞** | `通` / `判詞` / `盡攬` / `攬一` / `案台` | `connect`, `execute`, `fetchall`, `fetchone`, `cursor` | `sqlite3`, `sqlalchemy` |
| **前綴** | `為_*` / `化_*` / `取_*` / `設_*` | `is_*`, `to_*`, `get_*`, `set_*` | 萬用前綴自動轉譯 |

---

## 🧪 運行測試 (Running Tests)

專案具備完整之測試套件，涵蓋內建語意、元編程代理、容錯建議以及真實生態系套件支援：

```bash
python3 -m unittest discover -s tests -v
```

---

## 🤝 參與貢獻 (Contributing)

歡迎提交 Pull Request 為森蚺增添更多文言典籍或修飾詞律！
1. Fork 本倉庫
2. 建立你的分支 (`git checkout -b feature/suanjing-advance`)
3. 在 `senran/dictionary.py` 增添詞律或擴充 `senran/scrolls/`
4. 確保通過測試 (`python3 -m unittest discover -s tests`)
5. 提交並發起 Pull Request

---

## 📄 授權條款 (License)

本專案採用 [MIT License](LICENSE) 授權。
無論身處廟堂之高，或居江湖之遠，皆可自由研讀、揮灑與流傳。
