"""
範例四：府庫案卷（資料庫與檔案讀寫）
示範以文言驅策 sqlite3 與 啟/閱/書 檔案上下文管理。
"""

import sys
import tempfile
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from senran import 引入, 啟, 書, 剖

# 1. 府庫檔案 (File I/O with Context Manager)
書("--- 卷宗批閱 (File I/O) ---")
tmp_file = tempfile.mktemp(suffix=".txt")

# 啟 -> open, 牘.書 -> write
with 啟(tmp_file, "w", encoding="utf-8") as 牘:
    牘.書("天下大事，必作於細；天下難事，必作於易。")

# 牘.閱 -> read
with 啟(tmp_file, "r", encoding="utf-8") as 牘:
    全文 = 牘.閱()
    書("自卷宗所得：", 全文)

if os.path.exists(tmp_file):
    os.remove(tmp_file)

# 2. 帳籍銘刻 (SQLite Database)
書("\n--- 銘刻石碑 (SQLite3) ---")
庫 = 引入("sqlite3")

# 通 -> connect
連線 = 庫.通(":memory:")
台 = 連線.案台() # cursor

# 判詞 -> execute
台.判詞("CREATE TABLE 英雄榜 (名號 TEXT, 戰功 INT)")
台.判詞("INSERT INTO 英雄榜 VALUES ('關雲長', 99), ('趙子龍', 98), ('張翼德', 95)")

台.判詞("SELECT 名號, 戰功 FROM 英雄榜 ORDER BY 戰功 DESC")

# 盡攬 -> fetchall
榜單 = 台.盡攬()
書("英雄榜全錄：")
for 名, 功 in 榜單:
    書(f"  英雄：{名}，立功：{功}")

連線.閉() # close
