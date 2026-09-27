"""
森蚺駢文賦體格式化儀 (Senran Pianwen Formatter)
將代碼化為四六對仗、聲律清朗之文言駢體文章（.sr 卷帙），
兼具古典文學美感與嚴謹邏輯，並可雙向還原與吟詠執行。
"""

import ast
import re
import sys
from typing import List, Tuple, Optional


class PianwenFormatter(ast.NodeVisitor):
    """將 Python AST 節點轉化為四六駢儷體章句"""

    def __init__(self):
        self.lines: List[str] = []
        self.indent_level: int = 0

    def emit(self, text: str):
        indent = "    " * self.indent_level
        self.lines.append(f"{indent}{text}")

    def format(self, source_code: str) -> str:
        self.lines = [
            "# 📜【森蚺駢儷憲典 · 賦體卷】",
            "",
            "> 夫運籌於帷幄之中，決勝於方寸之間。",
            ""
        ]
        tree = ast.parse(source_code)
        for node in tree.body:
            self.visit(node)
        self.lines.append("")
        self.lines.append("---")
        self.lines.append("*🪶【賦畢 · 算道咸吉】*")
        return "\n".join(self.lines)

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            asname = alias.asname or alias.name
            self.emit(f"夫機巧初動，引外邦「{alias.name}」之庫，役使為「{asname}」；")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module or ""
        names = "、".join([a.name for a in node.names])
        if module == "senran":
            self.emit(f"先啟森蚺道統，恭請符節「{names}」入列几案；")
        else:
            self.emit(f"引「{module}」之籍，恭請名品「{names}」登堂；")

    def visit_Assign(self, node: ast.Assign):
        targets = "、".join([ast.unparse(t) for t in node.targets])
        value_str = ast.unparse(node.value)
        
        # 針對常見模式進行詩意對仗
        if "引入" in value_str:
            mod_match = re.search(r'引入\(["\'](.+?)["\']\)', value_str)
            mod_name = mod_match.group(1) if mod_match else value_str
            self.emit(f"置百家之珍，引「{mod_name}」入府，銘曰「{targets}」；")
        elif ".得(" in value_str or ".get(" in value_str:
            self.emit(f"遣驛使以往訪，運籌「{value_str}」，定卷為「{targets}」；")
        elif "量(" in value_str or "tensor(" in value_str:
            self.emit(f"布列玄機張量，化萬物之精，鑄「{targets}」之形；")
        elif targets.startswith("self.") or targets.startswith("己."):
            self.emit(f"賦物之秉性，定「{targets}」之值為「{value_str}」；")
        elif isinstance(node.value, ast.Call):
            self.emit(f"鑄就實例，以「{value_str}」化生「{targets}」；")
        else:
            self.emit(f"設符節曰「{targets}」，權衡其理，賦其值曰「{value_str}」；")

    def visit_Expr(self, node: ast.Expr):
        val_str = ast.unparse(node.value)
        if val_str.startswith("書(") or val_str.startswith("print("):
            args_str = val_str[val_str.index("(") + 1 : -1]
            self.emit(f"几案展卷，落字有聲，明書其辭：{args_str}；")
        elif ".反溯(" in val_str or ".backward(" in val_str:
            self.emit("反溯求勢，洞燭幽微，萬千梯度皆通於指掌；")
        elif ".清勢(" in val_str or ".zero_grad(" in val_str:
            self.emit("蕩滌前勢，澄澈靈台，重開造化新天；")
        elif ".步進(" in val_str or ".step(" in val_str:
            self.emit("循梯度而步進，隨機變而精微，功德又添一重；")
        else:
            self.emit(f"操持法印，施號發令：「{val_str}」；")

    def visit_If(self, node: ast.If):
        test_str = ast.unparse(node.test)
        self.emit(f"若夫考校其理，審「{test_str}」符契而稱是：")
        self.indent_level += 1
        for sub_node in node.body:
            self.visit(sub_node)
        self.indent_level -= 1
        if node.orelse:
            self.emit("如其不然，背道相左：")
            self.indent_level += 1
            for sub_node in node.orelse:
                self.visit(sub_node)
            self.indent_level -= 1

    def visit_For(self, node: ast.For):
        target_str = ast.unparse(node.target)
        iter_str = ast.unparse(node.iter)
        self.emit(f"循序週流，以「{target_str}」度「{iter_str}」，往復而行：")
        self.indent_level += 1
        for sub_node in node.body:
            self.visit(sub_node)
        self.indent_level -= 1

    def visit_ClassDef(self, node: ast.ClassDef):
        bases_str = "、".join([ast.unparse(b) for b in node.bases])
        if bases_str:
            self.emit(f"立宗為門類，號曰「{node.name}」，承襲「{bases_str}」之道統：")
        else:
            self.emit(f"立宗為門類，號曰「{node.name}」，自成一家：")
        self.indent_level += 1
        for sub_node in node.body:
            self.visit(sub_node)
        self.indent_level -= 1
        self.emit(f"「{node.name}」門類大成，立基完備。")
        self.emit("")

    def visit_FunctionDef(self, node: ast.FunctionDef):
        for dec in node.decorator_list:
            self.emit(f"冠以靈飾，受令於「{ast.unparse(dec)}」：")
        args = [a.arg for a in node.args.args]
        if args and args[0] in ("self", "己"):
            other_args = ", ".join(args[1:])
            if node.name == "__init__":
                self.emit(f"夫門類初立，溯源鑄形（初始化），納諸數「{other_args}」：")
            else:
                self.emit(f"賦物之能，立此法度曰「{node.name}」，納客數「{other_args}」：")
        else:
            args_str = ", ".join(args)
            self.emit(f"立宗定法，名曰「{node.name}」，納客數「{args_str}」：")
        self.indent_level += 1
        for sub_node in node.body:
            self.visit(sub_node)
        self.indent_level -= 1

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        for dec in node.decorator_list:
            self.emit(f"冠以靈飾，受令於「{ast.unparse(dec)}」：")
        args_str = ", ".join([a.arg for a in node.args.args])
        self.emit(f"立非同步玄機之法，名曰「{node.name}」，納客數「{args_str}」：")
        self.indent_level += 1
        for sub_node in node.body:
            self.visit(sub_node)
        self.indent_level -= 1

    def visit_Return(self, node: ast.Return):
        val = ast.unparse(node.value) if node.value else "空"
        self.emit(f"全功奏凱，以「{val}」歸報；")


def 賦體(代碼: str) -> str:
    """將常規代碼轉化為駢儷賦體文（.sr）"""
    return PianwenFormatter().format(代碼)


def 解賦(駢文: str) -> str:
    """
    從駢儷賦體文章（.md / .sr）中還原出可執行之森蚺 Python 代碼。
    """
    py_lines = [
        "from senran import 引入, 書, 計, 疇, 總, 序, 錄, 譜, 若, 真, 假, 啟, 定",
        ""
    ]
    lines = 駢文.split("\n")
    indent = ""

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith(">") or line.startswith("---") or line.startswith("*"):
            continue

        # 計算原本縮排
        current_indent = raw_line[: len(raw_line) - len(raw_line.lstrip())]

        # 1. 庫引入
        m = re.search(r'引外邦「(.+?)」之庫，役使為「(.+?)」', line)
        if m:
            py_lines.append(f"{current_indent}{m.group(2)} = 引入('{m.group(1)}')")
            continue

        # 2. 引入森蚺或單一庫
        m = re.search(r'引「(.+?)」之籍，恭請名品「(.+?)」', line)
        if m:
            py_lines.append(f"{current_indent}{m.group(2)} = 引入('{m.group(1)}')")
            continue

        # 3. 門類與方法定義
        m = re.search(r'立宗為門類，號曰「(.+?)」', line)
        if m:
            py_lines.append(f"{current_indent}class {m.group(1)}:")
            continue

        if "門類大成，立基完備" in line:
            continue

        m = re.search(r'夫門類初立，溯源鑄形（初始化），納諸數「(.*?)」', line)
        if m:
            args = f"己, {m.group(1)}" if m.group(1).strip() else "己"
            py_lines.append(f"{current_indent}def __init__({args}):")
            continue

        m = re.search(r'賦物之能，立此法度曰「(.+?)」，納客數「(.*?)」', line)
        if m:
            args = f"己, {m.group(2)}" if m.group(2).strip() else "己"
            py_lines.append(f"{current_indent}def {m.group(1)}({args}):")
            continue

        m = re.search(r'立宗定法，名曰「(.+?)」，納客數「(.*?)」', line)
        if m:
            py_lines.append(f"{current_indent}def {m.group(1)}({m.group(2)}):")
            continue

        m = re.search(r'全功奏凱，以「(.+?)」歸報', line)
        if m:
            py_lines.append(f"{current_indent}return {m.group(1)}")
            continue

        # 4. 賦值與實例化
        m = re.search(r'賦物之秉性，定「(.+?)」之值為「(.+?)」', line)
        if m:
            py_lines.append(f"{current_indent}{m.group(1)} = {m.group(2)}")
            continue

        m = re.search(r'鑄就實例，以「(.+?)」化生「(.+?)」', line)
        if m:
            py_lines.append(f"{current_indent}{m.group(2)} = {m.group(1)}")
            continue

        m = re.search(r'設符節曰「(.+?)」，權衡其理，賦其值曰「(.+?)」', line)
        if m:
            py_lines.append(f"{current_indent}{m.group(1)} = {m.group(2)}")
            continue

        m = re.search(r'遣驛使以往訪，運籌「(.+?)」，定卷為「(.+?)」', line)
        if m:
            py_lines.append(f"{current_indent}{m.group(2)} = {m.group(1)}")
            continue

        m = re.search(r'置百家之珍，引「(.+?)」入府，銘曰「(.+?)」', line)
        if m:
            py_lines.append(f"{current_indent}{m.group(2)} = 引入('{m.group(1)}')")
            continue

        # 5. 印出
        m = re.search(r'几案展卷，落字有聲，明書其辭：(.+?)；', line)
        if m:
            py_lines.append(f"{current_indent}書({m.group(1)})")
            continue

        # 6. 反溯 / 清勢 / 步進
        if "反溯求勢" in line:
            py_lines.append(f"{current_indent}損.反溯()")
            continue
        if "蕩滌前勢" in line:
            py_lines.append(f"{current_indent}優化客.清勢()")
            continue
        if "循梯度而步進" in line:
            py_lines.append(f"{current_indent}優化客.步進()")
            continue

        # 7. 條件若則
        m = re.search(r'若夫考校其理，審「(.+?)」符契而稱是：', line)
        if m:
            py_lines.append(f"{current_indent}if {m.group(1)}:")
            continue
        if "如其不然" in line:
            py_lines.append(f"{current_indent}else:")
            continue

        # 8. 迴圈
        m = re.search(r'循序週流，以「(.+?)」度「(.+?)」，往復而行：', line)
        if m:
            py_lines.append(f"{current_indent}for {m.group(1)} in {m.group(2)}:")
            continue

        # 9. 一般表達式調用
        m = re.search(r'操持法印，施號發令：「(.+?)」；', line)
        if m:
            py_lines.append(f"{current_indent}{m.group(1)}")
            continue

    return "\n".join(py_lines)
