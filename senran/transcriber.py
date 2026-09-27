"""
森蚺轉錄儀（化俗為雅 / Transpiler）
將西邦庸俗之標準 Python 代碼，一鍵轉錄為古雅端方之森蚺文言。
"""

import re
import sys
import argparse
from typing import Optional

# 核心轉譯詞律對照
TRANSCRIPTION_RULES = [
    # 1. 內建函式
    (r"\bprint\s*\(", "書("),
    (r"\blen\s*\(", "計("),
    (r"\brange\s*\(", "疇("),
    (r"\bsum\s*\(", "總("),
    (r"\bopen\s*\(", "啟("),
    (r"\binput\s*\(", "問("),
    (r"\bsorted\s*\(", "序("),
    (r"\breversed\s*\(", "反("),
    (r"\btype\s*\(", "審("),
    (r"\bisinstance\s*\(", "係("),

    # 2. 常數
    (r"\bTrue\b", "真"),
    (r"\bFalse\b", "假"),
    (r"\bNone\b", "空"),

    # 3. 網絡通訊 (requests, httpx, urllib)
    (r"\.status_code\b", ".格"),
    (r"\.text\b", ".文"),
    (r"\.content\b", ".實"),
    (r"\.json\s*\(\s*\)", ".譜()"),
    (r"\.get\s*\(", ".得("),
    (r"\.post\s*\(", ".投("),

    # 4. 深度學習與機器學習 (PyTorch / Sklearn)
    (r"\.backward\s*\(\s*\)", ".反溯()"),
    (r"\.grad\b", ".勢"),
    (r"\.zero_grad\s*\(\s*\)", ".清勢()"),
    (r"\.step\s*\(\s*\)", ".步進()"),
    (r"\.item\s*\(\s*\)", ".析值()"),
    (r"\.tensor\s*\(", ".量("),
    (r"\.matmul\s*\(", ".矩積("),
    (r"\.fit\s*\(", ".習("),
    (r"\.predict\s*\(", ".卜("),
    (r"\.score\s*\(", ".考分("),

    # 5. 數據分析與矩陣 (NumPy / Pandas)
    (r"\.array\s*\(", ".陣("),
    (r"\.shape\b", ".形"),
    (r"\.mean\s*\(\s*\)", ".均()"),
    (r"\.zeros\s*\(", ".皆零("),
    (r"\.ones\s*\(", ".皆一("),
    (r"\.reshape\s*\(", ".塑("),
    (r"\.columns\b", ".欄"),
    (r"\.head\s*\(", ".冠("),
    (r"\.tail\s*\(", ".履("),
    (r"\.describe\s*\(\s*\)", ".描述()"),

    # 6. 檔案與資料庫 (File I/O / SQLite)
    (r"\.read\s*\(\s*\)", ".閱()"),
    (r"\.write\s*\(", ".書("),
    (r"\.close\s*\(\s*\)", ".閉()"),
    (r"\.cursor\s*\(\s*\)", ".案台()"),
    (r"\.execute\s*\(", ".判詞("),
    (r"\.fetchall\s*\(\s*\)", ".盡攬()"),
    (r"\.fetchone\s*\(\s*\)", ".攬一()"),
    (r"\.commit\s*\(\s*\)", ".立契()"),

    # 7. 繪圖 (Matplotlib)
    (r"\.plot\s*\(", ".繪("),
    (r"\.scatter\s*\(", ".布星("),
    (r"\.title\s*\(", ".題("),
    (r"\.xlabel\s*\(", ".橫標("),
    (r"\.ylabel\s*\(", ".縱標("),
    (r"\.savefig\s*\(", ".存圖("),
    (r"\.show\s*\(\s*\)", ".展現()"),

    # 8. 物件導向、門類與自指 (OOP, Classes, Methods, self)
    (r"\bself\.", "己."),
    (r"\bself\b", "己"),
    (r"\bclass\s+Dog\b", "class 犬"),
    (r"\bDog\b", "犬"),
    (r"\bdog1\b", "犬一"),
    (r"\bdog2\b", "犬二"),
    (r"\bclass\s+Cat\b", "class 貓"),
    (r"\bCat\b", "貓"),
    (r"\bcat1\b", "貓一"),
    (r"\bcat2\b", "貓二"),
    (r"\bclass\s+User\b", "class 客"),
    (r"\bUser\b", "客"),
    (r"\buser1\b", "客一"),
    (r"\bdef\s+bark\b", "def 吠"),
    (r"\.bark\s*\(", ".吠("),
    (r"\bdef\s+meow\b", "def 喵"),
    (r"\.meow\s*\(", ".喵("),
    (r"\bdef\s+get_info\b", "def 取_身世"),
    (r"\.get_info\s*\(", ".取_身世("),
    (r"\bdef\s+get_name\b", "def 取_名"),
    (r"\.get_name\s*\(", ".取_名("),
    (r"\bdef\s+get_age\b", "def 取_歲"),
    (r"\.get_age\s*\(", ".取_歲("),
    (r"\bdef\s+forward\b", "def 前向"),
    (r"\.forward\s*\(", ".前向("),
    (r"\bdef\s+reset\b", "def 重開"),
    (r"\.reset\s*\(", ".重開("),
    (r"def\s+__init__\s*\(\s*己\s*,\s*name\s*,\s*age\s*\)", "def __init__(己, 名, 歲)"),
    (r"己\.name\b", "己.名"),
    (r"己\.age\b", "己.歲"),
    (r"\b己\.名\s*=\s*name\b", "己.名 = 名"),
    (r"\b己\.歲\s*=\s*age\b", "己.歲 = 歲"),
    (r"\{己\.name\}", "{己.名}"),
    (r"\{己\.age\}", "{己.歲}"),
]

# 常用函式庫引進替換規則
IMPORT_RULES = [
    (r"import\s+([\w\.]+)\s+as\s+(\w+)", r"\2 = 引入('\1')"),
    (r"from\s+dataclasses\s+import\s+dataclass", "from dataclasses import dataclass as 定品"),
    (r"@dataclass\b", "@定品"),
    (r"import\s+requests\b(?!\.)", "求 = 引入('requests')"),
    (r"import\s+httpx\b(?!\.)", "求 = 引入('httpx')"),
    (r"import\s+flask\b(?!\.)", "法宴 = 引入('flask')"),
    (r"import\s+fastapi\b(?!\.)", "急驛 = 引入('fastapi')"),
    (r"import\s+click\b(?!\.)", "號令 = 引入('click')"),
    (r"import\s+numpy\b(?!\.)", "算矩 = 引入('numpy')"),
    (r"import\s+pandas\b(?!\.)", "史冊 = 引入('pandas')"),
    (r"import\s+torch\b(?!\.)", "神算 = 引入('torch')"),
    (r"import\s+sqlite3\b(?!\.)", "庫 = 引入('sqlite3')"),
    (r"import\s+json\b(?!\.)", "法書 = 引入('json')"),
    (r"import\s+math\b(?!\.)", "算術 = 引入('math')"),
    (r"import\s+([\w\.]+)\b", r"\1 = 引入('\1')"),
]

HEADER = "from senran import 引入, 書, 計, 疇, 總, 序, 錄, 譜, 若, 真, 假, 啟, 定\n\n"


def 化雅(代碼: str) -> str:
    """
    將標準 Python 代碼字串，一鍵轉錄為森蚺文言。
    """
    結果 = 代碼

    # 1. 替換 import 語句為 引入(...)
    lines = 結果.split("\n")
    new_lines = []
    
    # 紀錄是否替換了 requests 等變數名，以便後續調用替換
    alias_map = {}

    for line in lines:
        stripped = line.strip()
        matched = False
        for pattern, repl in IMPORT_RULES:
            if re.match(pattern, stripped):
                # 記錄預設替換 (使用單詞邊界檢測 as，避免如 flask / fastapi 誤判)
                has_as = bool(re.search(r"\bas\b", stripped))
                if re.search(r"import\s+requests\b(?!\.)", stripped) and not has_as:
                    alias_map["requests"] = "求"
                elif re.search(r"import\s+httpx\b(?!\.)", stripped) and not has_as:
                    alias_map["httpx"] = "求"
                elif re.search(r"import\s+flask\b(?!\.)", stripped) and not has_as:
                    alias_map["flask"] = "法宴"
                elif re.search(r"import\s+fastapi\b(?!\.)", stripped) and not has_as:
                    alias_map["fastapi"] = "急驛"
                elif re.search(r"import\s+click\b(?!\.)", stripped) and not has_as:
                    alias_map["click"] = "號令"
                elif re.search(r"import\s+torch\b(?!\.)", stripped) and not has_as:
                    alias_map["torch"] = "神算"
                elif re.search(r"import\s+numpy\b(?!\.)", stripped) and not has_as:
                    alias_map["numpy"] = "算矩"
                elif re.search(r"import\s+pandas\b(?!\.)", stripped) and not has_as:
                    alias_map["pandas"] = "史冊"
                elif re.search(r"import\s+sqlite3\b(?!\.)", stripped) and not has_as:
                    alias_map["sqlite3"] = "庫"
                elif re.search(r"import\s+json\b(?!\.)", stripped) and not has_as:
                    alias_map["json"] = "法書"
                elif re.search(r"import\s+math\b(?!\.)", stripped) and not has_as:
                    alias_map["math"] = "算術"

                indent = line[: len(line) - len(line.lstrip())]
                trans = re.sub(pattern, repl, stripped)
                new_lines.append(indent + trans)
                matched = True
                break
        if not matched:
            new_lines.append(line)

    # 2. 替換預設變數名稱 (如 requests.get -> 求.get)，但跳過引進語句與包含 引入() 的行
    replaced_lines = []
    for line in new_lines:
        stripped = line.strip()
        if "引入(" in line or stripped.startswith(("import ", "from ")):
            replaced_lines.append(line)
        else:
            for orig_var, new_var in alias_map.items():
                line = re.sub(r"\b" + orig_var + r"\.", new_var + ".", line)
            replaced_lines.append(line)

    結果 = "\n".join(replaced_lines)

    # 3. 替換核心詞律與屬性
    for pattern, repl in TRANSCRIPTION_RULES:
        結果 = re.sub(pattern, repl, 結果)

    # 4. 若無 senran 引入，則自動冠上起手引入
    if "from senran import" not in 結果 and "import senran" not in 結果:
        結果 = HEADER + 結果

    return 結果


def 轉錄(來源檔路徑: str, 輸出檔路徑: Optional[str] = None) -> str:
    """
    讀取檔案並轉錄為森蚺文言文，若指定輸出檔則儲存之。
    """
    with open(來源檔路徑, "r", encoding="utf-8") as f:
        原碼 = f.read()

    轉文 = 化雅(原碼)

    if 輸出檔路徑:
        with open(輸出檔路徑, "w", encoding="utf-8") as f:
            f.write(轉文)

    return 轉文


def main():
    from senran.formatter import 賦體, 解賦
    from senran.agent import 機巧使

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        # 1. 策問 / 機巧使 (Agent REPL 或 單次問道)
        if cmd in ("策問", "agent", "ask", "機巧使"):
            if len(sys.argv) > 2:
                意向 = " ".join(sys.argv[2:])
                成果 = 機巧使.策問(意向)
                print("=" * 60)
                print("📜【駢儷賦體 · 人讀卷帙 (.md)】")
                print("=" * 60)
                print(成果["駢體賦"])
                print("\n" + "=" * 60)
                print("🐍【森蚺文言 · 雅正代碼 (.py)】")
                print("=" * 60)
                print(成果["森蚺碼"])
                print("\n" + "=" * 60)
                print("💻【標準西文 · 原生代碼 (.py)】")
                print("=" * 60)
                print(成果["標準碼"])
            else:
                機巧使.開壇()
            return

        # 2. 設壇 (布施 AGENTS.md, .cursorrules, CLAUDE.md 等)
        if cmd in ("設壇", "init-agent", "init"):
            target_dir = sys.argv[2] if len(sys.argv) > 2 else "."
            文卷們 = 機巧使.設壇(target_dir)
            print("=" * 60)
            print("🏛️【森蚺 · 機巧使設壇大成】")
            print(f"壇場地址：{target_dir}")
            for v in 文卷們:
                print(f"  ✓ 已敕令明卷：{v}")
            print("凡天下天機神思（Cursor, Claude, Copilot, Antigravity）入此界者，皆當恪遵森蚺之法度！")
            print("=" * 60)
            return

        # 3. 敕令 (印出 System Prompt 供網頁版 ChatGPT / Claude / Gemini 複製)
        if cmd in ("敕令", "prompt", "system-prompt"):
            print(機巧使.天機敕令())
            return

        # 4. 化西文 (森蚺文言代碼 -> 標準西邦 Python)
        if cmd in ("化西文", "to-py", "transpile-to-py"):
            parser = argparse.ArgumentParser(description="森蚺化西文——將古雅文言轉為標準西邦 Python")
            parser.add_argument("cmd", help="化西文")
            parser.add_argument("file", help="森蚺文言檔案路徑")
            parser.add_argument("-o", "--output", help="輸出之標準 Python 檔案路徑")
            args = parser.parse_args()

            with open(args.file, "r", encoding="utf-8") as f:
                code = f.read()
            py_code = 機巧使.化西文(code)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(py_code)
                print(f"【森蚺化西文】西文卷帙銘刻大成：{args.output}")
            else:
                print(py_code)
            return

        # 5. 賦體排版 (.md)
        if cmd in ("format", "賦", "駢文"):
            parser = argparse.ArgumentParser(description="森蚺駢文儀——將代碼排版為四六駢儷體 Markdown 文章 (.md)")
            parser.add_argument("cmd", help="format / 賦")
            parser.add_argument("file", help="Python 原始腳本路徑")
            parser.add_argument("-o", "--output", help="輸出之 .md 賦體檔案路徑")
            args = parser.parse_args()

            with open(args.file, "r", encoding="utf-8") as f:
                code = f.read()
            sr = 賦體(code)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(sr)
                print(f"【森蚺駢文儀】賦體卷帙銘刻大成：{args.output}")
            else:
                print(sr)
            return

        # 6. 吟詠執行 (.md / .sr)
        if cmd in ("run", "吟", "行"):
            parser = argparse.ArgumentParser(description="森蚺吟詠儀——執行 .md 駢儷賦體文卷")
            parser.add_argument("cmd", help="run / 吟")
            parser.add_argument("file", help="欲執行之 .md 賦體檔案路徑")
            args = parser.parse_args()

            with open(args.file, "r", encoding="utf-8") as f:
                sr_text = f.read()
            py_code = 解賦(sr_text)
            exec(py_code, {"__name__": "__main__"})
            return

    # 預設轉錄模式 (化俗為雅)
    parser = argparse.ArgumentParser(
        description="森蚺轉錄儀（化俗為雅）—— 將庸俗西邦 Python 代碼轉為古雅森蚺文言"
    )
    parser.add_argument("file", help="欲轉錄之 Python 原始腳本路徑")
    parser.add_argument("-o", "--output", help="輸出之文言檔案路徑（若未指定則印於几案）")
    args = parser.parse_args()

    成果 = 轉錄(args.file, args.output)
    if not args.output:
        print(成果)
    else:
        print(f"【森蚺轉錄儀】化俗為雅大成！文卷已銘刻於：{args.output}")


if __name__ == "__main__":
    main()
