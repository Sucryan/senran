"""
森蚺經書 (Senran Core)
定義 Python 核心內建常數、型別、內建函式及模組引入之文言體系。
"""

import importlib
import sys
from typing import Any, Callable
from senran.proxy import 裹, 剖, SenranProxy


# ==========================================
# 1. 核心常數 (Constants)
# ==========================================
真 = True
假 = False
空 = None
無 = None


# ==========================================
# 2. 核心內建型別 (Types)
# ==========================================
整 = int
浮 = float
文 = str
字 = str
節 = bytes
錄 = list
列 = list
譜 = dict
集 = set
偶 = tuple


# ==========================================
# 3. 核心內建函式 (Built-in Functions)
# ==========================================
def 書(*args, **kwargs):
    """印出內容於几案之上 (print)"""
    unwrapped_args = [剖(a) for a in args]
    unwrapped_kwargs = {k: 剖(v) for k, v in kwargs.items()}
    return print(*unwrapped_args, **unwrapped_kwargs)


def 問(提示: str = "") -> str:
    """垂詢使用者，收納應對 (input)"""
    return input(提示)


def 計(物: Any) -> int:
    """度量事物長度或容量 (len)"""
    return len(剖(物))


def 疇(*args) -> Any:
    """劃定數之疆界 (range)"""
    unwrapped_args = [剖(a) for a in args]
    return 裹(range(*unwrapped_args))


def 總(序列: Any, 起始: Any = 0) -> Any:
    """薈萃總和 (sum)"""
    return sum(剖(序列), 剖(起始))


求和 = 總


def 極大(*args, **kwargs) -> Any:
    """取其最巨者 (max)"""
    return 裹(max(*[剖(a) for a in args], **{k: 剖(v) for k, v in kwargs.items()}))


def 極小(*args, **kwargs) -> Any:
    """取其最微者 (min)"""
    return 裹(min(*[剖(a) for a in args], **{k: 剖(v) for k, v in kwargs.items()}))


def 審(物: Any) -> Any:
    """審視其根底門類 (type)"""
    return type(剖(物))


def 係(物: Any, 類: Any) -> bool:
    """查核此物是否屬某類 (isinstance)"""
    return isinstance(剖(物), 剖(類))


def 枚(可枚舉物: Any, 始: int = 0):
    """逐一條列數算 (enumerate)"""
    for idx, val in enumerate(剖(可枚舉物), 始):
        yield 裹(idx), 裹(val)


def 並(*可迭代物):
    """兩兩齊行，並轡前馳 (zip)"""
    unwrapped = [剖(item) for item in 可迭代物]
    for row in zip(*unwrapped):
        yield tuple(裹(x) for x in row)


def 序(序列: Any, 逆序: bool = False, 準則: Any = None):
    """依理排序 (sorted)"""
    kw = {}
    if 準則 is not None:
        kw["key"] = 剖(準則)
    kw["reverse"] = 剖(逆序)
    return 裹(sorted(剖(序列), **kw))


def 反(序列: Any):
    """溯源反轉 (reversed)"""
    return 裹(reversed(剖(序列)))


def 啟(*args, **kwargs) -> SenranProxy:
    """啟開卷宗檔案 (open)"""
    unwrapped_args = [剖(a) for a in args]
    unwrapped_kwargs = {k: 剖(v) for k, v in kwargs.items()}
    f = open(*unwrapped_args, **unwrapped_kwargs)
    return 裹(f)


def 定(條件: Any, 告誡: str = "明斷有誤"):
    """明斷理則，若背道而馳則鳴警 (assert)"""
    if not bool(剖(條件)):
        raise AssertionError(f"【森蚺明斷】{告誡}")


# ==========================================
# 4. 萬邦通譯：引入外邦典籍 (Module Importer)
# ==========================================
class _ModuleImporter:
    """支援 引入('requests') 亦支援 引入.requests 的萬能引進器"""
    
    def __call__(self, 模組名: str) -> SenranProxy:
        try:
            mod = importlib.import_module(模組名)
            return 裹(mod)
        except ImportError as e:
            raise ImportError(f"森蚺通譯未能在行囊中尋得庫【{模組名}】。請先以 pip 置辦之：{e}")

    def __getattr__(self, name: str) -> SenranProxy:
        return self(name)


引入 = _ModuleImporter()
載 = 引入


# ==========================================
# 5. 語法流 DSL：若 / 則 / 否則 (Conditional Sugar)
# ==========================================
class 若:
    """提供仿文言若則控制語義"""
    def __init__(self, 斷言: Any):
        self._cond = bool(剖(斷言))

    def 則(self, 動作: Any, *args, **kwargs) -> "若":
        if self._cond:
            if callable(動作):
                動作(*args, **kwargs)
        return self

    def 否則(self, 動作: Any, *args, **kwargs):
        if not self._cond:
            if callable(動作):
                動作(*args, **kwargs)
        return self
