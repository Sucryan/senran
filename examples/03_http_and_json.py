"""
範例三：雲端驛傳（網絡通訊與 JSON 序列化）
示範以文言驅策 json 與 requests (或 urllib)。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from senran import 引入, 書

# 1. 典籍序列化 (json)
法書 = 引入("json")
文房 = {"筆": "狼毫", "墨": "松煙", "紙": "宣紙", "硯": "端硯"}

# 化字 -> dumps
字串 = 法書.化字(文房, ensure_ascii=False)
書("化文入字：", 字串)

# 析字 -> loads
復原本 = 法書.析字(字串)
書("由字析物：", 復原本["筆"])

# 2. 雲端傳訊 (requests)
try:
    求 = 引入("requests")
    書("\n--- 雲端探訪 (Requests) ---")
    
    # 得 -> get
    報 = 求.得("https://httpbin.org/get")
    書("驛使回報狀態格：", 報.格)
    若合度 = (報.格 == 200)
    書("此行是否平順：", "吉" if 若合度 else "凶")
    
    # 析文 / 譜 -> json()
    內容譜 = 報.譜()
    書("驛使所訪之源址：", 內容譜.get("url"))

except Exception as e:
    書(f"（聯網探訪略過：{e}）")
