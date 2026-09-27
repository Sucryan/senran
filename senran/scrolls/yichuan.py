"""
典籍：驛傳 (Yichuan Scroll)
專門收攬千里通訊、雲端互通之典籍（HTTP / 通訊協議）。
"""

from senran.core import 引入

try:
    驛傳 = 引入("requests")
except Exception:
    try:
        驛傳 = 引入("urllib.request")
    except Exception:
        驛傳 = None
