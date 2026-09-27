"""
森蚺轉錄儀（化俗為雅 / Transpiler）
將西邦庸俗之標準 Python 代碼，一鍵轉錄為古雅端方之森蚺文言。
"""

import re
import sys
import argparse
from typing import Optional



def 化雅(代碼: str) -> str:
    """將標準 Python 轉為有校驗封卷的森蚺代理體。"""
    from senran.codec import encode_runtime, decode_source
    from senran.bridge import is_packet
    if is_packet(代碼):
        代碼 = decode_source(代碼)
    return encode_runtime(代碼)


def 轉錄(來源檔路徑: str, 輸出檔路徑: Optional[str] = None) -> str:
    """
    讀取檔案並轉錄為森蚺文言文，若指定輸出檔則儲存之。
    """
    with open(來源檔路徑, "r", encoding="utf-8", newline="") as f:
        原碼 = f.read()

    轉文 = 化雅(原碼)

    if 輸出檔路徑:
        with open(輸出檔路徑, "w", encoding="utf-8", newline="") as f:
            f.write(轉文)

    return 轉文


def main():
    from senran.formatter import 賦體, 解賦
    from senran.agent import 機巧使

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == 'repo':
            from senran.repository import main as repo_main
            del sys.argv[1]
            repo_main()
            return
        if cmd in ('zhpy', '周蟒'):
            parser = argparse.ArgumentParser(description='轉為周蟒白話中文卷')
            parser.add_argument('cmd')
            parser.add_argument('file')
            parser.add_argument('-o', '--output')
            args = parser.parse_args()
            from senran.bridge import convert
            with open(args.file, encoding='utf-8', newline='') as stream:
                source = stream.read()
            result = convert('zhpy', 解賦(source) if args.file.lower().endswith('.md') else source)
            if args.output:
                with open(args.output, 'w', encoding='utf-8', newline='') as stream:
                    stream.write(result)
            else:
                sys.stdout.write(result)
            return
        if cmd in ('unformat', '解賦'):
            parser = argparse.ArgumentParser(description='駢文還原完整森蚺碼卷')
            parser.add_argument('cmd')
            parser.add_argument('file')
            parser.add_argument('-o', '--output')
            args = parser.parse_args()
            with open(args.file, encoding='utf-8', newline='') as stream:
                code = 解賦(stream.read())
            if args.output:
                with open(args.output, 'w', encoding='utf-8', newline='') as stream:
                    stream.write(code)
            else:
                sys.stdout.write(code)
            return

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

            with open(args.file, "r", encoding="utf-8", newline="") as f:
                code = f.read()
            py_code = 機巧使.化西文(code)
            if args.output:
                with open(args.output, "w", encoding="utf-8", newline="") as f:
                    f.write(py_code)
                print(f"【森蚺化西文】西文卷帙銘刻大成：{args.output}")
            else:
                sys.stdout.write(py_code)
            return

        # 5. 賦體排版 (.md)
        if cmd in ("format", "賦", "駢文"):
            parser = argparse.ArgumentParser(description="森蚺駢文儀——將代碼排版為四六駢儷體 Markdown 文章 (.md)")
            parser.add_argument("cmd", help="format / 賦")
            parser.add_argument("file", help="Python 原始腳本路徑")
            parser.add_argument("-o", "--output", help="輸出之 .md 賦體檔案路徑")
            args = parser.parse_args()

            with open(args.file, "r", encoding="utf-8", newline="") as f:
                code = f.read()
            from senran.bridge import convert
            sr = convert('format', code)
            if args.output:
                with open(args.output, "w", encoding="utf-8", newline="") as f:
                    f.write(sr)
                print(f"【森蚺駢文儀】賦體卷帙銘刻大成：{args.output}")
            else:
                sys.stdout.write(sr)
            return

        # 6. 吟詠執行 (.md / .sr)
        if cmd in ("run", "吟", "行"):
            parser = argparse.ArgumentParser(description="森蚺吟詠儀——執行 .md 駢儷賦體文卷")
            parser.add_argument("cmd", help="run / 吟")
            parser.add_argument("file", help="欲執行之 .md 賦體檔案路徑")
            args = parser.parse_args()

            with open(args.file, "r", encoding="utf-8", newline="") as f:
                sr_text = f.read()
            py_code = 解賦(sr_text) if args.file.lower().endswith('.md') else sr_text
            from senran.codec import to_python
            exec(compile(to_python(py_code), args.file, 'exec'),
                 {"__name__": "__main__", "__file__": args.file})
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
        sys.stdout.write(成果)
    else:
        print(f"【森蚺轉錄儀】化俗為雅大成！文卷已銘刻於：{args.output}")


if __name__ == "__main__":
    main()
