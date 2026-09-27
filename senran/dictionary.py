"""
森蚺典律 (Senran Lexicon)
收錄文言與 Python 常見動詞、名詞、前後綴規則之映射表，
以支援百家函式庫（requests, numpy, pandas, os, sys, math, torch 等）。
"""

from typing import Dict, List, Optional, Set

# ==========================================
# 1. 核心動詞辭典 (Universal Verbs)
# ==========================================
VERBS: Dict[str, str] = {
    # 存取與獲取
    "得": "get",
    "取": "get",
    "收": "receive",
    "受": "recv",
    "徵": "fetch",
    "攬": "fetch",
    "搜": "search",
    "索": "find",
    "尋": "find",
    "查": "find",
    "考": "check",
    "驗": "verify",
    "證": "validate",

    # 發送與放置
    "投": "post",
    "寄": "send",
    "發": "send",
    "傳": "transmit",
    "置": "put",
    "設": "set",
    "易": "update",
    "更": "update",
    "補": "patch",

    # 容器與結構操作
    "附": "append",
    "綴": "extend",
    "插": "insert",
    "黜": "remove",
    "刪": "delete",
    "除": "delete",
    "截": "pop",
    "棄": "discard",
    "滌": "clear",
    "空": "empty",
    "模": "copy",
    "仿": "copy",

    # 字串與序列操作
    "析": "split",
    "剖": "split",
    "合": "join",
    "結": "join",
    "排": "sort",
    "序": "sort",
    "逆": "reverse",
    "反": "reverse",
    "數": "count",
    "點": "count",
    "替": "replace",
    "換": "replace",
    "削": "strip",

    # 檔案與系統操作
    "啟": "open",
    "閱": "read",
    "讀": "read",
    "書": "write",
    "錄": "write",
    "記": "log",
    "閉": "close",
    "封": "close",
    "闢": "mkdir",
    "立": "create",
    "通": "connect",
    "斷": "disconnect",
    "遷": "move",
    "更名": "rename",

    # 執行與生命週期
    "行": "run",
    "作": "execute",
    "施": "execute",
    "起": "start",
    "始": "start",
    "止": "stop",
    "終": "terminate",
    "歇": "sleep",
    "憩": "sleep",
    "候": "wait",
    "待": "wait",
    "聚": "gather",

    # 數學、科學與機器學習
    "算": "calculate",
    "積": "dot",
    "塑": "reshape",
    "合並": "concat",
    "訓": "fit",
    "習": "train",
    "卜": "predict",
    "斷定": "predict",
    "評": "evaluate",
    "生": "generate",
    "編": "encode",
    "解": "decode",
    "載": "load",
    "卸": "dump",
    "傾": "dump",
}

# ==========================================
# 2. 核心名詞辭典 (Universal Nouns & Attributes)
# ==========================================
NOUNS: Dict[str, str] = {
    # 網絡與通訊 (requests, httpx, urllib...)
    "文": "text",
    "實": "content",
    "質": "content",
    "格": "status_code",
    "態": "status_code",
    "品": "status_code",
    "題": "headers",
    "首": "headers",
    "章": "headers",
    "址": "url",
    "源": "url",
    "譜": "json",
    "由": "reason",
    "誤": "error",
    "信": "message",
    "訊": "info",
    "告": "warning",

    # 數據科學與結構 (numpy, pandas, torch...)
    "形": "shape",
    "貌": "shape",
    "容": "size",
    "維": "ndim",
    "量": "size",
    "型": "dtype",
    "欄": "columns",
    "行名": "index",
    "標": "index",
    "目": "index",
    "值": "values",
    "均": "mean",
    "差": "std",
    "方差": "var",
    "極大": "max",
    "極小": "min",
    "中值": "median",
    "總": "sum",
    "和": "sum",
    "冠": "head",
    "履": "tail",
    "陣": "array",
    "表": "dataframe",

    # 檔案與路徑
    "名": "name",
    "徑": "path",
    "父": "parent",
    "根": "root",
    "基": "stem",
    "尾": "suffix",
    "處": "cwd",

    # 時間與隨機
    "時": "time",
    "刻": "now",
    "今": "now",
    "年": "year",
    "月": "month",
    "日": "day",
    "宿": "date",

    # 字典與容器屬性
    "鍵": "keys",
    "物": "values",
    "項": "items",
}

# ==========================================
# 3. 複合常用語 (Idiomatic Multi-word Expressions)
# ==========================================
COMPOUNDS: Dict[str, str] = {
    # 網絡與傳輸
    "析文": "json",
    "化譜": "json",
    "解譜": "json",
    "狀態": "status_code",
    "標頭": "headers",
    "網址": "url",

    # 檔案與系統
    "存在": "exists",
    "列案": "listdir",
    "行令": "system",
    "行命": "run",

    # 數據分析 (pandas / numpy)
    "皆零": "zeros",
    "皆一": "ones",
    "階梯": "arange",
    "等距": "linspace",
    "眼": "eye",
    "轉置": "T",
    "首五": "head",
    "尾五": "tail",
    "描述": "describe",
    "閱譜": "read_csv",
    "書譜": "to_csv",
    "閱卷": "read_excel",
    "書卷": "to_excel",
    "棄空": "dropna",
    "補空": "fillna",
    "分群": "groupby",
    "依序": "sort_values",

    # 序列化
    "化字": "dumps",
    "析字": "loads",
    "入卷": "dump",
    "出卷": "load",

    # 數學運算
    "開方": "sqrt",
    "絕對": "abs",
    "指數": "exp",
    "對數": "log",
    "正弦": "sin",
    "餘弦": "cos",
    "正切": "tan",

    # 資料庫
    "判詞": "execute",
    "盡攬": "fetchall",
    "攬一": "fetchone",
    "立契": "commit",
    "悔契": "rollback",
    "案台": "cursor",

    # 隨機
    "隨機數": "random",
    "隨選": "choice",
    "拈號": "randint",
    "洗牌": "shuffle",
}

# ==========================================
# 4. 常見前後綴規則 (Prefix / Suffix Rules)
# ==========================================
PREFIX_RULES: List[tuple] = [
    ("為_", "is_"),
    ("乃_", "is_"),
    ("係_", "is_"),
    ("化_", "to_"),
    ("致_", "to_"),
    ("取_", "get_"),
    ("求_", "get_"),
    ("設_", "set_"),
    ("閱_", "read_"),
    ("書_", "write_"),
    ("錄_", "write_"),
    ("存_", "has_"),
    ("有_", "has_"),
]

# 合併所有單詞與複合詞
ALL_LEXICON: Dict[str, str] = {}
ALL_LEXICON.update(VERBS)
ALL_LEXICON.update(NOUNS)
ALL_LEXICON.update(COMPOUNDS)

# 反向查詢表 (用於偵錯與提示：English -> [Chinese aliases])
REVERSE_LEXICON: Dict[str, List[str]] = {}
for zh, en in ALL_LEXICON.items():
    REVERSE_LEXICON.setdefault(en.lower(), []).append(zh)
