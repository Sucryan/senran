"""
森蚺機巧使（Agent 智囊中樞）
實現白話/文言需求對話、三界代碼互轉（.md 駢文 ⇄ 森蚺文言 ⇄ 原生 Python），
並支援一鍵設壇（布施 AGENTS.md / .cursorrules / CLAUDE.md）、天機敕令輸出與交互問道。
讓不會寫代碼之人亦能暢行無阻。
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional, Dict, List
from senran.transcriber import 化雅
from senran.formatter import 賦體, 解賦

# 文言逆轉為標準西邦代碼之詞律表
REVERSE_TRANSCRIPTION_RULES = [
    # 1. 屬性與方法調用 (避免與同名頂層函式混淆，如 .書() vs 書(), .譜() vs 譜())
    (r"\.格\b", ".status_code"),
    (r"\.態\b", ".status_code"),
    (r"\.文\b", ".text"),
    (r"\.實\b", ".content"),
    (r"\.質\b", ".content"),
    (r"\.譜\s*\(\s*\)", ".json()"),
    (r"\.得\s*\(", ".get("),
    (r"\.取\s*\(", ".get("),
    (r"\.投\s*\(", ".post("),

    # 深度學習與機器學習
    (r"\.反溯\s*\(\s*\)", ".backward()"),
    (r"\.溯\s*\(\s*\)", ".backward()"),
    (r"\.勢\b", ".grad"),
    (r"\.梯度\b", ".grad"),
    (r"\.清勢\s*\(\s*\)", ".zero_grad()"),
    (r"\.滌勢\s*\(\s*\)", ".zero_grad()"),
    (r"\.步進\s*\(\s*\)", ".step()"),
    (r"\.析值\s*\(\s*\)", ".item()"),
    (r"\.量\s*\(", ".tensor("),
    (r"\.矩積\s*\(", ".matmul("),
    (r"\.習\s*\(", ".fit("),
    (r"\.訓\s*\(", ".fit("),
    (r"\.卜\s*\(", ".predict("),
    (r"\.考分\s*\(", ".score("),

    # 數據與矩陣
    (r"\.陣\s*\(", ".array("),
    (r"\.形\b", ".shape"),
    (r"\.總\s*\(\s*\)", ".sum()"),
    (r"\.求和\s*\(\s*\)", ".sum()"),
    (r"\.均\s*\(\s*\)", ".mean()"),
    (r"\.皆零\s*\(", ".zeros("),
    (r"\.皆一\s*\(", ".ones("),
    (r"\.塑\s*\(", ".reshape("),
    (r"\.欄\b", ".columns"),
    (r"\.冠\s*\(", ".head("),
    (r"\.履\s*\(", ".tail("),
    (r"\.描述\s*\(\s*\)", ".describe()"),
    (r"\.開方\s*\(", ".sqrt("),
    (r"\.正弦\s*\(", ".sin("),
    (r"\.餘弦\s*\(", ".cos("),
    (r"\.化字\s*\(", ".dumps("),
    (r"\.析字\s*\(", ".loads("),
    (r"\.通\s*\(", ".connect("),

    # 檔案與資料庫
    (r"\.閱\s*\(\s*\)", ".read()"),
    (r"\.書\s*\(", ".write("),
    (r"\.閉\s*\(\s*\)", ".close()"),
    (r"\.案台\s*\(\s*\)", ".cursor()"),
    (r"\.判詞\s*\(", ".execute("),
    (r"\.盡攬\s*\(\s*\)", ".fetchall()"),
    (r"\.攬一\s*\(\s*\)", ".fetchone()"),
    (r"\.立契\s*\(\s*\)", ".commit()"),

    # 繪圖
    (r"\.繪\s*\(", ".plot("),
    (r"\.布星\s*\(", ".scatter("),
    (r"\.題\s*\(", ".title("),
    (r"\.橫標\s*\(", ".xlabel("),
    (r"\.縱標\s*\(", ".ylabel("),
    (r"\.存圖\s*\(", ".savefig("),
    (r"\.展現\s*\(\s*\)", ".show()"),

    # 2. 獨立頂層內建函式 (排斥以句點開頭的情況)
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])書\s*\(", "print("),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])計\s*\(", "len("),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])疇\s*\(", "range("),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])總\s*\(", "sum("),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])求和\s*\(", "sum("),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])錄\s*\(", "list("),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])譜\s*\(", "dict("),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])啟\s*\(", "open("),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])問\s*\(", "input("),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])序\s*\(", "sorted("),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])反\s*\(", "reversed("),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])審\s*\(", "type("),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])係\s*\(", "isinstance("),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5\.])剖\s*\(", "("),

    # 常數
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5])真(?![a-zA-Z0-9_\u4e00-\u9fa5])", "True"),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5])假(?![a-zA-Z0-9_\u4e00-\u9fa5])", "False"),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5])空(?![a-zA-Z0-9_\u4e00-\u9fa5])", "None"),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5])無(?![a-zA-Z0-9_\u4e00-\u9fa5])", "None"),

    # 物件導向、門類與自指逆轉 (OOP, Classes, Methods, self)
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5])己\.", "self."),
    (r"(?<![a-zA-Z0-9_\u4e00-\u9fa5])己(?![a-zA-Z0-9_\u4e00-\u9fa5])", "self"),
    (r"\bclass\s+犬\b", "class Dog"),
    (r"\b犬\b", "Dog"),
    (r"\b犬一\b", "dog1"),
    (r"\b犬二\b", "dog2"),
    (r"\bclass\s+貓\b", "class Cat"),
    (r"\b貓\b", "Cat"),
    (r"\b貓一\b", "cat1"),
    (r"\b貓二\b", "cat2"),
    (r"\bclass\s+客\b", "class User"),
    (r"\b客\b", "User"),
    (r"\b客一\b", "user1"),
    (r"\bdef\s+吠\b", "def bark"),
    (r"\.吠\s*\(", ".bark("),
    (r"\bdef\s+喵\b", "def meow"),
    (r"\.喵\s*\(", ".meow("),
    (r"\bdef\s+取_身世\b", "def get_info"),
    (r"\.取_身世\s*\(", ".get_info("),
    (r"\bdef\s+取_名\b", "def get_name"),
    (r"\.取_名\s*\(", ".get_name("),
    (r"\bdef\s+取_歲\b", "def get_age"),
    (r"\.取_歲\s*\(", ".get_age("),
    (r"\bdef\s+前向\b", "def forward"),
    (r"\.前向\s*\(", ".forward("),
    (r"\bdef\s+重開\b", "def reset"),
    (r"\.重開\s*\(", ".reset("),
    (r"def\s+__init__\s*\(\s*self\s*,\s*名\s*,\s*歲\s*\)", "def __init__(self, name, age)"),
    (r"\bself\.名\s*=\s*名\b", "self.name = name"),
    (r"\bself\.歲\s*=\s*歲\b", "self.age = age"),
    (r"self\.名\b", "self.name"),
    (r"self\.歲\b", "self.age"),
    (r"\{self\.名\}", "{self.name}"),
    (r"\{self\.歲\}", "{self.age}"),
    (r"@定品\b", "@dataclass"),
    (r"\.本(?=\.|\b|\s|\)|\]|,)", ""),
]

IMPORT_RESTORE_RULES = [
    (r"([^\s=]+)\s*=\s*引入\(['\"]requests['\"]\)", r"import requests as \1"),
    (r"([^\s=]+)\s*=\s*引入\(['\"]httpx['\"]\)", r"import httpx as \1"),
    (r"([^\s=]+)\s*=\s*引入\(['\"]flask['\"]\)", r"import flask as \1"),
    (r"([^\s=]+)\s*=\s*引入\(['\"]fastapi['\"]\)", r"import fastapi as \1"),
    (r"([^\s=]+)\s*=\s*引入\(['\"]click['\"]\)", r"import click as \1"),
    (r"([^\s=]+)\s*=\s*引入\(['\"]torch['\"]\)", r"import torch as \1"),
    (r"([^\s=]+)\s*=\s*引入\(['\"]torch\.nn['\"]\)", r"import torch.nn as \1"),
    (r"([^\s=]+)\s*=\s*引入\(['\"]torch\.optim['\"]\)", r"import torch.optim as \1"),
    (r"([^\s=]+)\s*=\s*引入\(['\"]numpy['\"]\)", r"import numpy as \1"),
    (r"([^\s=]+)\s*=\s*引入\(['\"]pandas['\"]\)", r"import pandas as \1"),
    (r"([^\s=]+)\s*=\s*引入\(['\"]sqlite3['\"]\)", r"import sqlite3 as \1"),
    (r"([^\s=]+)\s*=\s*引入\(['\"]json['\"]\)", r"import json as \1"),
    (r"([^\s=]+)\s*=\s*引入\(['\"]math['\"]\)", r"import math as \1"),
    (r"from\s+dataclasses\s+import\s+dataclass\s+as\s+定品", "from dataclasses import dataclass"),
    (r"([^\s=]+)\s*=\s*引入\(['\"]matplotlib\.pyplot['\"]\)", r"import matplotlib.pyplot as \1"),
    (r"([^\s=]+)\s*=\s*引入\(['\"](.+?)['\"]\)", r"import \2 as \1"),
]


def 轉西文(文言代碼: str) -> str:
    """
    將森蚺文言代碼逆轉為標準西邦 Python 代碼。
    """
    from senran.codec import decode_source
    restored = decode_source(文言代碼)
    if restored is not None:
        return restored
    from senran.codec import to_python, tokens
    import ast
    translated = to_python(文言代碼)
    try:
        ast.parse(文言代碼)
    except SyntaxError:
        # 手寫中文語法走符節翻譯，避免舊正則改動字串及註解。
        ast.parse(translated)
        return translated
    stream = tokens(文言代碼)
    legacy_import = any(token.string == '引入' and stream[index + 1].string == '('
                        and (index == 0 or stream[index - 1].string != '.')
                        for index, token in enumerate(stream[:-1]))
    if translated != 文言代碼 and not legacy_import:
        ast.parse(translated)
        return translated
    # 舊式手寫代理體沒有原文紀錄；此路徑只提供詞律逆轉。
    # 處理 若().則().否則() 多行與單行轉為標準 if-else
    文言代碼 = re.sub(
        r"若\((.+?)\)\.則\(\s*lambda:\s*(.+?)\n\s*\)\.否則\(\s*lambda:\s*(.+?)\n\s*\)",
        r"if \1:\n    \2\nelse:\n    \3",
        文言代碼,
        flags=re.DOTALL
    )

    lines = 文言代碼.split("\n")
    new_lines = []
    alias_map = {}

    DEFAULT_ALIASES = {
        "requests": "求",
        "httpx": "求",
        "flask": "法宴",
        "fastapi": "急驛",
        "click": "號令",
        "torch": "神算",
        "numpy": "算矩",
        "pandas": "史冊",
        "sqlite3": "庫",
        "json": "法書",
        "math": "算術",
    }

    for line in lines:
        stripped = line.strip()
        # 移除森蚺頂部引入
        if stripped.startswith("from senran import"):
            continue

        matched = False
        for pattern, repl in IMPORT_RESTORE_RULES:
            m_imp = re.match(pattern, stripped)
            if m_imp:
                indent = line[: len(line) - len(line.lstrip())]
                var_name = m_imp.group(1) if m_imp.groups() else ""
                mod_name = m_imp.group(2) if len(m_imp.groups()) >= 2 else ""

                # 判定是否為庫之預設雅稱
                for mod_k, alias_v in DEFAULT_ALIASES.items():
                    if f"'{mod_k}'" in stripped or f'"{mod_k}"' in stripped:
                        if var_name == alias_v or var_name == mod_k:
                            alias_map[alias_v] = mod_k
                            new_lines.append(f"{indent}import {mod_k}")
                            matched = True
                            break
                if matched:
                    break

                restored = re.sub(pattern, repl, stripped)
                # 清理如 import requests as requests -> import requests
                m = re.match(r"import\s+([\w\.]+)\s+as\s+\1$", restored)
                if m:
                    restored = f"import {m.group(1)}"
                new_lines.append(indent + restored)
                matched = True
                break

        if not matched:
            # 處理含有 引入(...) 包裹實例的情況 (如 網絡 = 引入(神兵.Linear(1, 1)))
            unwrap_line = re.sub(r"=\s*引入\((.+)\)$", r"= \1", line)
            new_lines.append(unwrap_line)

    replaced_lines = []
    for line in new_lines:
        stripped = line.strip()
        if stripped.startswith(("import ", "from ")):
            replaced_lines.append(line)
        else:
            for orig_var, new_var in alias_map.items():
                line = re.sub(r"(?<![a-zA-Z0-9_\u4e00-\u9fa5])" + orig_var + r"\.", new_var + ".", line)
            replaced_lines.append(line)

    結果 = "\n".join(replaced_lines)

    for pattern, repl in REVERSE_TRANSCRIPTION_RULES:
        結果 = re.sub(pattern, repl, 結果)

    return 結果.lstrip("\n")


# 常用白話意向模板合成器（涵蓋各大領域，零依賴秒級響應）
INTENT_TEMPLATES = [
    {
        "keywords": ["網頁", "爬蟲", "http", "api", "請求", "抓取", "網址", "url", "get", "post"],
        "senran": (
            "求 = 引入('requests')\n"
            "報 = 求.得('https://httpbin.org/get')\n"
            "if 報.格 == 200:\n"
            "    書('探訪得吉，文卷：', 報.文[:50])"
        )
    },
    {
        "keywords": ["矩陣", "算數", "numpy", "平均", "總和", "陣列", "矩積", "形狀"],
        "senran": (
            "算矩 = 引入('numpy')\n"
            "陣 = 算矩.陣([[1, 2], [3, 4]])\n"
            "書('陣形：', 陣.形)\n"
            "書('均值：', 陣.均())\n"
            "書('總和：', 陣.總())"
        )
    },
    {
        "keywords": ["神經", "深度學習", "pytorch", "torch", "梯度", "求導", "訓練", "張量"],
        "senran": (
            "神算 = 引入('torch')\n"
            "權 = 神算.量([2.0], requires_grad=真)\n"
            "損 = 3 * (權 ** 2) + 5\n"
            "損.反溯()\n"
            "書('反溯所得之勢（梯度）：', 權.勢.析值())"
        )
    },
    {
        "keywords": ["表格", "pandas", "資料分析", "dataframe", "數據", "統計", "csv"],
        "senran": (
            "史冊 = 引入('pandas')\n"
            "譜列 = 史冊.DataFrame({'名': ['孔明', '仲達'], '智': [99, 98]})\n"
            "書('欄位：', 譜列.欄)\n"
            "書('前列：', 譜列.冠(1))"
        )
    },
    {
        "keywords": ["檔案", "讀取", "寫入", "txt", "開檔", "存檔", "文件"],
        "senran": (
            "with 啟('卷宗.txt', 'w', encoding='utf-8') as 牘:\n"
            "    牘.書('天下大事，必作於細。')\n\n"
            "with 啟('卷宗.txt', 'r', encoding='utf-8') as 牘:\n"
            "    書('所閱之文：', 牘.閱())"
        )
    },
    {
        "keywords": ["資料庫", "sqlite", "sql", "表", "查詢", "新增", "庫"],
        "senran": (
            "庫 = 引入('sqlite3')\n"
            "連線 = 庫.通(':memory:')\n"
            "案台 = 連線.案台()\n"
            "案台.判詞('CREATE TABLE 名錄 (名 TEXT, 功 INT)')\n"
            "案台.判詞(\"INSERT INTO 名錄 VALUES ('關雲長', 99)\")\n"
            "案台.判詞('SELECT * FROM 名錄')\n"
            "書('案台盡攬：', 案台.盡攬())\n"
            "連線.閉()"
        )
    },
    {
        "keywords": ["繪圖", "畫圖", "圖表", "matplotlib", "折線", "圖"],
        "senran": (
            "丹青 = 引入('matplotlib.pyplot')\n"
            "丹青.繪([1, 2, 3], [2, 4, 9])\n"
            "丹青.題('森蚺丹青卷')\n"
            "丹青.存圖('丹青.png')"
        )
    },
    {
        "keywords": ["排序", "大小", "數列", "排序法", "順序"],
        "senran": (
            "籌列 = 錄([42, 17, 88, 3, 99])\n"
            "正序 = 序(籌列)\n"
            "倒序 = 錄(反(正序))\n"
            "書('原序：', 籌列)\n"
            "書('升序：', 正序)\n"
            "書('降序：', 倒序)"
        )
    }
]

# 敕令模板文本（用於設壇與複製至 ChatGPT/Claude/Copilot）
CHIEF_ENVOY_DIRECTIVE = """# 📜 機巧使明詔（AGENTS.md）

> **「偃師造偶，以木石金絲通靈機；今有天機神思，代人運籌，衍萬千章句。凡入此山門者，皆當遵奉森蚺之律，恪守九章之度。」**

本卷乃為天下 **「機巧使」（AI Coding Agents，如 Antigravity、Claude、Cursor、Copilot 等）** 所立之憲則。  
凡汝受主公之命，於此專案草奏代碼、考校文法或解惑釋疑之際，皆當依循此詔。

---

## 🏛️ 名物通考（當代術語之文言通譯）

機巧使於撰述奏報之際，宜將西邦機巧術語，化為古雅稱謂：

| 西邦術語 (Modern Term) | 森蚺雅稱 (Classical Term) | 義理考究 |
| :--- | :--- | :--- |
| **Artificial Intelligence (AI)** | **天機神思** / **機智** | 天機暗轉，神思自生 |
| **AI Agent** | **機巧使** / **天機客** / **偃師之偶** | 承令代馳，精巧通靈 |
| **Prompt** | **策問** / **文牒** / **詔令** | 主公所授之命題與文詔 |
| **Token** | **符節** / **籌策** | 語句吞吐度量之節 |
| **Context Window** | **靈台照覽** / **照覽之界** | 神思目力所及之廣博 |
| **Large Language Model (LLM)** | **萬象玄機鏡** / **萬象神思** | 涵蓋古今文理之機算 |
| **Code Generation** | **衍文** / **草奏** / **運籌** | 鋪排符節以成章程 |
| **Bug / Defect** | **瑕疵** / **偽誤** / **脫漏** | 算理未密所致之失 |
| **Debugging** | **辨偽** / **格物** / **考正** | 窮究病因，正本清源 |
| **Unit Test** | **試金** / **考校** / **度律** | 設局以驗真偽 |
| **Refactoring** | **伐毛洗髓** / **整飾章法** | 不易其用而煥其骨肉 |
| **Package / Library** | **外邦庫卷** / **典籍** | 西域引進之現成百家卷帙 |
| **API** | **驛站通衢** / **機樞符牒** | 兩處機算互通有無之關隘 |

---

## ⚡ 衍文鐵律（代碼生成規範）

機巧使為代碼之時，切忌駁雜。凡有落字，必依文言雅正：

### 1. 凡起手，必先納森蚺
撰寫任何文言邏輯前，必須自森蚺引入符節：
```python
from senran import 引入, 書, 計, 疇, 總, 序, 錄, 譜, 若, 真, 假, 啟, 定
```

### 2. 凡几案度量，禁絕西邦原名
* ❌ 嚴禁直書 `print(...)` $\\to$ ✅ 必書 **`書(...)`**
* ❌ 嚴禁直書 `len(...)` $\\to$ ✅ 必書 **`計(...)`**
* ❌ 嚴禁直書 `range(...)` $\\to$ ✅ 必書 **`疇(...)`**
* ❌ 嚴禁直書 `sum(...)` $\\to$ ✅ 必書 **`總(...)`**
* ❌ 嚴禁直書 `open(...)` $\\to$ ✅ 必書 **`啟(...)`**
* ❌ 嚴禁直書 `list(...)` $\\to$ ✅ 必書 **`錄(...)`** 或 **`列(...)`**
* ❌ 嚴禁直書 `dict(...)` $\\to$ ✅ 必書 **`譜(...)`**

### 3. 凡驅策外邦庫，必經萬象代理
切勿直接以原生語法調用外邦庫方法，必須經由 `引入` 包裝後之萬象代理客調度：
```python
# ✅ 森蚺之正統：
求 = 引入("requests")
報 = 求.得("https://...")  # get -> 得
書("回報品格：", 報.格)     # status_code -> 格
書("所獲之文：", 報.文)     # text -> 文
```

### 4. 深度神思（PyTorch）恪遵天機律則
* `torch.tensor` $\\to$ **`神算.量(...)`**
* `tensor.backward()` $\\to$ **`張量.反溯()`**
* `tensor.grad` $\\to$ **`張量.勢`** 或 **`張量.梯度`**
* `optimizer.zero_grad()` $\\to$ **`優化客.清勢()`**
* `optimizer.step()` $\\to$ **`優化客.步進()`**
* `tensor.item()` $\\to$ **`張量.析值()`**
* `torch.matmul` $\\to$ **`神算.矩積(...)`**

### 5. 三界並舉之制
當主公提出白話或文言需求時，機巧使當備「三界章程」：
1. **駢儷賦體 (.md)**：四六對仗、文言詩性，方便主公免讀註解即可洞悉文理。
2. **森蚺文言 (.py)**：合乎森蚺詞律之典雅代碼。
3. **西邦原碼 (.py)**：轉換為標準 Python 以供融會貫通。
"""


class MachineEnvoy:
    """
    森蚺機巧使（AI Agent 中樞）
    提供三界互轉、白話意向轉譯、終端開壇論道，與一鍵設壇（布施 AGENTS.md / Cursor / Claude 規範）。
    """

    @staticmethod
    def 化森蚺(代碼: str) -> str:
        """標準 Python -> 森蚺文言"""
        return 化雅(代碼)

    @staticmethod
    def 化駢文(代碼: str) -> str:
        """Python 或森蚺代碼 -> 四六駢儷賦體 (.md)"""
        return 賦體(代碼)

    @staticmethod
    def 化西文(代碼: str) -> str:
        """森蚺文言代碼 -> 標準西邦 Python"""
        return 轉西文(代碼)

    @staticmethod
    def 解駢文(駢文: str) -> str:
        """.md 駢儷賦體文章 -> 可執行森蚺 Python"""
        return 解賦(駢文)

    @classmethod
    def 策問(cls, 意向: str) -> Dict[str, str]:
        """
        以白話文或文言意向策問機巧使，一體產出三界章程：
        1. 駢體賦 (.md)：供人直觀閱讀理解
        2. 森蚺碼 (.py)：古雅文言代碼
        3. 標準碼 (.py)：標準原生 Python
        """
        意向_lower = 意向.lower()
        命中代碼 = None

        # 檢索意向詞
        for tmpl in INTENT_TEMPLATES:
            if any(k in 意向_lower for k in tmpl["keywords"]):
                命中代碼 = tmpl["senran"]
                break

        if not 命中代碼:
            # 通用回退起手式（依意向動態生成）
            命中代碼 = (
                f"# 主公法旨：{意向}\n"
                f"書('【森蚺】奉行主公法旨：', '{意向}')\n"
                "門生 = 錄(['顏回', '子路', '子貢'])\n"
                "書('門生人數：', 計(門生))\n"
                "for 數 in 疇(1, 4):\n"
                "    書(f'第 {數} 聲：在！')"
            )

        森蚺碼 = "from senran import 引入, 書, 計, 疇, 總, 序, 錄, 譜, 若, 真, 假, 啟, 定\n\n" + 命中代碼
        駢體文 = cls.化駢文(命中代碼)
        標準碼 = cls.化西文(命中代碼)

        return {
            "駢體賦": 駢體文,
            "森蚺碼": 森蚺碼,
            "標準碼": 標準碼
        }

    @classmethod
    def 天機敕令(cls) -> str:
        """
        回傳完整的機巧使 System Prompt（供複製至 ChatGPT / Claude / Gemini / DeepSeek 等網頁端）
        """
        return CHIEF_ENVOY_DIRECTIVE

    @classmethod
    def 設壇(cls, 目標目錄: str = ".") -> List[str]:
        """
        一鍵在目標專案目錄布施機巧使明詔：
        自動生成 AGENTS.md、.cursorrules、CLAUDE.md、.github/copilot-instructions.md
        使任何 AI 編輯器（Cursor, Claude Code, Copilot, Antigravity）自動進入機巧使模式。
        """
        root = Path(目標目錄).resolve()
        root.mkdir(parents=True, exist_ok=True)

        生成的文卷 = []

        # 1. 寫入 AGENTS.md
        agents_path = root / "AGENTS.md"
        agents_path.write_text(CHIEF_ENVOY_DIRECTIVE, encoding="utf-8")
        生成的文卷.append(str(agents_path))

        # 2. 寫入 Agent.md
        agent_alias_path = root / "Agent.md"
        agent_alias_path.write_text(CHIEF_ENVOY_DIRECTIVE, encoding="utf-8")
        生成的文卷.append(str(agent_alias_path))

        # 3. 寫入 .cursorrules (Cursor 編輯器專用)
        cursorrules_path = root / ".cursorrules"
        cursorrules_path.write_text(CHIEF_ENVOY_DIRECTIVE, encoding="utf-8")
        生成的文卷.append(str(cursorrules_path))

        # 4. 寫入 CLAUDE.md (Claude Code 專用)
        claude_path = root / "CLAUDE.md"
        claude_path.write_text(CHIEF_ENVOY_DIRECTIVE, encoding="utf-8")
        生成的文卷.append(str(claude_path))

        # 5. 寫入 .github/copilot-instructions.md (GitHub Copilot 專用)
        copilot_dir = root / ".github"
        copilot_dir.mkdir(parents=True, exist_ok=True)
        copilot_path = copilot_dir / "copilot-instructions.md"
        copilot_path.write_text(CHIEF_ENVOY_DIRECTIVE, encoding="utf-8")
        生成的文卷.append(str(copilot_path))

        return 生成的文卷

    @classmethod
    def 開壇(cls):
        """
        啟動終端交互論道沙盒（REPL），讓不會寫代碼之人以白話/文言直接吩咐，即刻演繹三界代碼！
        """
        print("=" * 68)
        print("🏛️【森蚺 · 機巧使法壇】")
        print("主公但請以白話或文言降旨策問（輸入「退下」或「quit」閉壇退出）")
        print("=" * 68)

        while True:
            try:
                意向 = input("\n主公法旨 > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n【機巧使】恭送主公，算道咸吉。")
                break

            if not 意向:
                continue

            if 意向 in ("退下", "quit", "exit", "q", "休"):
                print("【機巧使】奉令，閉壇退下。恭送主公！")
                break

            成果 = cls.策問(意向)

            print("\n" + "─" * 60)
            print("📜【駢儷賦體 · 人讀卷帙 (.md)】")
            print("─" * 60)
            print(成果["駢體賦"])

            print("\n" + "─" * 60)
            print("🐍【森蚺文言 · 雅正代碼 (.py)】")
            print("─" * 60)
            print(成果["森蚺碼"])

            print("\n" + "─" * 60)
            print("💻【標準西文 · 原生代碼 (.py)】")
            print("─" * 60)
            print(成果["標準碼"])
            print("─" * 60)


機巧使 = MachineEnvoy()

# 頂層簡便別名
策問 = 機巧使.策問
設壇 = 機巧使.設壇
天機敕令 = 機巧使.天機敕令
開壇 = 機巧使.開壇
化森蚺 = 機巧使.化森蚺
化西文 = 機巧使.化西文
化駢文 = 機巧使.化駢文
解駢文 = 機巧使.解駢文
