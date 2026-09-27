"""
典籍：算經 (Suanjing Scroll)
專門收攬算術、代數與數值計算之典籍。
"""

from senran.core import 引入

# 引入標準 math 庫並賦予古風別名
算術 = 引入("math")

# 引入常見科學計算庫（若環境有安裝則立取，未裝則延遲提示）
try:
    算矩 = 引入("numpy")
except Exception:
    算矩 = None
