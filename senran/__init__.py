"""
森蚺 (Senran) — 文言驅策萬象 Python 庫
"""

from senran.core import (
    # 常數
    真,
    假,
    空,
    無,
    # 型別
    整,
    浮,
    文,
    字,
    節,
    錄,
    列,
    譜,
    集,
    偶,
    # 內建函式
    書,
    問,
    計,
    疇,
    總,
    求和,
    極大,
    極小,
    審,
    係,
    枚,
    並,
    序,
    反,
    啟,
    定,
    # 引進器
    引入,
    載,
    # 邏輯糖
    若,
)
from senran.proxy import 裹, 剖, SenranProxy
from senran.transcriber import 化雅, 轉錄
from senran.formatter import 賦體, 解賦

__version__ = "0.1.0"
__all__ = [
    "真",
    "假",
    "空",
    "無",
    "整",
    "浮",
    "文",
    "字",
    "節",
    "錄",
    "列",
    "譜",
    "集",
    "偶",
    "書",
    "問",
    "計",
    "疇",
    "總",
    "求和",
    "極大",
    "極小",
    "審",
    "係",
    "枚",
    "並",
    "序",
    "反",
    "啟",
    "定",
    "引入",
    "載",
    "若",
    "裹",
    "剖",
    "SenranProxy",
]
