"""
萬象森羅：森蚺動態代理器 (Universal Dynamic Proxy)
包裝任意 Python 模組、物件、類別或函式，自動將文言屬性與方法請求轉發至底層物件。
"""

from typing import Any, Callable
from senran.resolver import resolve_attribute_name, suggest_available_attributes


# 不強制重新包裝的原始基礎型別，保證 Python 原生運算（如 == 200, 浮點計算, 字串操作）完全相容
PRIMITIVE_TYPES = (int, float, bool, type(None), bytes, str)


def 剖(obj: Any) -> Any:
    """解開森蚺代理，取得底層原生 Python 物件"""
    if isinstance(obj, SenranProxy):
        return obj._target
    return obj


def 裹(obj: Any) -> Any:
    """將原生 Python 物件裹入森蚺代理（基礎型別除外）"""
    if isinstance(obj, SenranProxy):
        return obj
    if isinstance(obj, PRIMITIVE_TYPES):
        return obj
    return SenranProxy(obj)


class SenranProxy:
    """
    森蚺萬象代理客。
    攔截所有屬性存取與調用，實現文言文對任意 Python 生態系之無縫驅策。
    """

    __slots__ = ("_target",)

    def __init__(self, target: Any):
        # 避免遞迴調用 __setattr__
        object.__setattr__(self, "_target", 剖(target))

    @property
    def 本(self) -> Any:
        """獲取底層原生 Python 物件"""
        return self._target

    @property
    def 原物(self) -> Any:
        """獲取底層原生 Python 物件之別名"""
        return self._target

    def __getattr__(self, name: str) -> Any:
        # 特殊內部欄位直接放行
        if name in ("_target", "本", "原物"):
            return object.__getattribute__(self, name)

        target = self._target
        resolved_name = resolve_attribute_name(target, name)

        if resolved_name is not None:
            attr = getattr(target, resolved_name)
            # 若為可調用之函數/方法，包裝並轉發
            if callable(attr):
                return self._wrap_callable(attr)
            return 裹(attr)

        # 查無此屬性，給予文雅之錯誤提示與相近字建議
        suggestions = suggest_available_attributes(target, name)
        msg = f"森蚺未能在【{type(target).__name__}】中尋得「{name}」。"
        if suggestions:
            msg += f" 或當為：{', '.join(suggestions)}？"
        else:
            msg += " 請考校字義或原庫屬性名。"
        raise AttributeError(msg)

    def __setattr__(self, name: str, value: Any):
        if name == "_target":
            object.__setattr__(self, name, value)
            return

        target = self._target
        resolved_name = resolve_attribute_name(target, name) or name
        setattr(target, resolved_name, 剖(value))

    def _wrap_callable(self, func: Callable) -> Callable:
        """包裝方法調用，自動解包傳入參數並將回傳值包裝為代理"""
        def _wrapped(*args, **kwargs):
            unwrapped_args = [剖(arg) for arg in args]
            unwrapped_kwargs = {k: 剖(v) for k, v in kwargs.items()}
            result = func(*unwrapped_args, **unwrapped_kwargs)
            return 裹(result)
        return _wrapped

    def __call__(self, *args, **kwargs):
        """若代理的目標本身是可調用對象（函數或類）"""
        target = self._target
        if not callable(target):
            raise TypeError(f"【{type(target).__name__}】非可施號令之物（不可調用）。")
        unwrapped_args = [剖(arg) for arg in args]
        unwrapped_kwargs = {k: 剖(v) for k, v in kwargs.items()}
        result = target(*unwrapped_args, **unwrapped_kwargs)
        return 裹(result)

    # ---------------- 運算符與容器行為 ----------------
    def __getitem__(self, item: Any) -> Any:
        res = self._target[剖(item)]
        return 裹(res)

    def __setitem__(self, key: Any, value: Any):
        self._target[剖(key)] = 剖(value)

    def __delitem__(self, key: Any):
        del self._target[剖(key)]

    def __iter__(self):
        for item in self._target:
            yield 裹(item)

    def __len__(self) -> int:
        return len(self._target)

    def __contains__(self, item: Any) -> bool:
        return 剖(item) in self._target

    def __bool__(self) -> bool:
        return bool(self._target)

    # 上下文管理器 (with 語句支援)
    def __enter__(self):
        res = self._target.__enter__()
        return 裹(res)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._target.__exit__(exc_type, exc_val, exc_tb)

    # 印出與字串展示
    def __repr__(self) -> str:
        return f"<森蚺客 護持: {repr(self._target)}>"

    def __str__(self) -> str:
        return str(self._target)

    # 比較運算子
    def __eq__(self, other: Any) -> bool:
        return self._target == 剖(other)

    def __ne__(self, other: Any) -> bool:
        return self._target != 剖(other)

    def __lt__(self, other: Any) -> bool:
        return self._target < 剖(other)

    def __le__(self, other: Any) -> bool:
        return self._target <= 剖(other)

    def __gt__(self, other: Any) -> bool:
        return self._target > 剖(other)

    def __ge__(self, other: Any) -> bool:
        return self._target >= 剖(other)

    # 算術運算子
    def __add__(self, other: Any) -> Any:
        return 裹(self._target + 剖(other))

    def __sub__(self, other: Any) -> Any:
        return 裹(self._target - 剖(other))

    def __mul__(self, other: Any) -> Any:
        return 裹(self._target * 剖(other))

    def __truediv__(self, other: Any) -> Any:
        return 裹(self._target / 剖(other))

    def __floordiv__(self, other: Any) -> Any:
        return 裹(self._target // 剖(other))

    def __mod__(self, other: Any) -> Any:
        return 裹(self._target % 剖(other))

    def __pow__(self, other: Any) -> Any:
        return 裹(self._target ** 剖(other))

    # 反向運算子 (Reflected / Right-hand operators)
    def __radd__(self, other: Any) -> Any:
        return 裹(剖(other) + self._target)

    def __rsub__(self, other: Any) -> Any:
        return 裹(剖(other) - self._target)

    def __rmul__(self, other: Any) -> Any:
        return 裹(剖(other) * self._target)

    def __rtruediv__(self, other: Any) -> Any:
        return 裹(剖(other) / self._target)

    def __rfloordiv__(self, other: Any) -> Any:
        return 裹(剖(other) // self._target)

    def __rmod__(self, other: Any) -> Any:
        return 裹(剖(other) % self._target)

    def __rpow__(self, other: Any) -> Any:
        return 裹(剖(other) ** self._target)

    # 矩陣乘法運算子 (@ / matmul)
    def __matmul__(self, other: Any) -> Any:
        return 裹(self._target @ 剖(other))

    def __rmatmul__(self, other: Any) -> Any:
        return 裹(剖(other) @ self._target)
