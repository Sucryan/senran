"""
範例二：格物算學（數學與數據分析）
示範以文言驅策 math、numpy 與 pandas。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from senran import 引入, 書

# 1. 驅策標準庫 math
算術 = 引入("math")
書("九九之根（開方 81）：", 算術.開方(81))
書("圓周率之半徑正弦（sin(0)）：", 算術.正弦(0))

# 2. 驅策矩陣計算庫 numpy
try:
    算矩 = 引入("numpy")
    書("\n--- 矩陣運算 (NumPy) ---")
    
    # 陣 -> array
    八卦陣 = 算矩.陣([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])
    書("八卦陣形貌：", 八卦陣.形)
    書("八卦陣各項總和：", 八卦陣.總())
    書("八卦陣均值：", 八卦陣.均())
    
    # 皆零 -> zeros
    平湖 = 算矩.皆零((2, 2))
    書("平湖（全零矩陣）：\n", 平湖)

except ImportError:
    書("（未裝載 numpy，略過矩陣範例）")

# 3. 驅策數據表庫 pandas
try:
    史冊 = 引入("pandas")
    書("\n--- 卷帙統計 (Pandas) ---")
    
    卷 = 史冊.DataFrame({
        "名氏": ["陶淵明", "李太白", "蘇東坡"],
        "佳作數": [142, 1010, 2700],
        "醉意值": [92, 100, 88]
    })
    書("名錄欄位：", 卷.欄)
    書("先覽首二位文豪：\n", 卷.冠(2))
    
except ImportError:
    書("（未裝載 pandas，略過卷帙範例）")
