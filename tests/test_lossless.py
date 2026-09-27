"""考校原文、森蚺、駢文往返時不失一字。"""
import unittest

from senran import 化雅, 化西文, 賦體, 解賦
from senran import 裹, 剖, 引入


CASES = [
    '',
    'print("True print( .get(")\n',
    '# print(True)\nprint( True )  # .text\n',
    'from __future__ import annotations\nprint(1)\n',
    'from . import thing as other\n',
    'from ..pkg import (\n    foo as bar,\n    baz,\n)\n',
    'import os, sys as system\n',
    'import xml.etree.ElementTree\n',
    'def f(x: int = 1, /, *args, y=None, **kwargs) -> int:\n    return x\n',
    'async def f():\n    async with client() as x:\n        return await x.get()\n',
    'try:\n    work()\nexcept Exception as e:\n    raise ValueError() from e\nfinally:\n    done()\n',
    'for x in range(3):\n    continue\nelse:\n    pass\n',
    'while True:\n    break\nelse:\n    pass\n',
    '@decorator(1)\nclass C(Base, metaclass=Meta):\n    value: int = 1\n',
    'def f():\n    yield from items\n',
    'x = [i for i in range(3) if i]\n',
    'x = {k: v for k, v in pairs}\n',
    'match x:\n    case {"key": value}:\n        pass\n',
    'assert (n := len(x)) > 0\n',
    'x += 1; del y\n',
    'print(f"{value!r:>{width}} literal print(True)")\n',
    'x = """line one\nTrue .text\n```\n"""\n',
    '真 = 1\nprint(真, True)\n',
    'print  (1)\r\n\r\n',
    '\t# trailing whitespace  \nprint(1)',
    'def f():\n    global x\n    x = 1\n',
    'x = lambda a=1: a\n',
    'from pkg import *\n',
]


class LosslessTests(unittest.TestCase):
    def test_basic_syntax_is_classical_in_all_conversion_paths(self):
        from senran.codec import encode_names
        source = 'class Box:\n    def items(self):\n        for x in [True, None]:\n            if x is not None:\n                yield x\n        return False\n'
        for convert in (encode_names, 化雅):
            encoded = convert(source)
            body = encoded.split('\n', 1)[1]
            for word in ('class', 'def', 'for', 'in', 'if', 'is', 'not', 'yield', 'return', 'True', 'False', 'None'):
                import re
                self.assertIsNone(re.search(r'\b' + word + r'\b', body), word)
            self.assertIn('類 ', body)
            self.assertIn('術 ', body)
            self.assertIn(' 於 ', body)
            self.assertEqual(化西文(解賦(賦體(encoded))), source)

    def test_zhpy_and_classical_syntax_can_be_mixed(self):
        from senran import codec
        translate = getattr(codec, 'to_python', None)
        self.assertIsNotNone(translate, 'missing mixed dialect translator')
        source = '類別 Box:\n    術 value(我):\n        如果 真:\n            歸 3\n結果 = Box().value()\n印出("def 返回 class", 結果)\n'
        expected = 'class Box:\n    def value(self):\n        if True:\n            return 3\n結果 = Box().value()\nprint("def 返回 class", 結果)\n'
        self.assertEqual(translate(source), expected)
        self.assertEqual(translate('定义 f():\n    返回 空\n'), 'def f():\n    return None\n')

    def test_dialect_preserves_strings_comments_and_attribute_names(self):
        from senran import codec
        translate = getattr(codec, 'to_python', None)
        self.assertIsNotNone(translate)
        source = '# 定義 返回\n術 f():\n    歸 obj.返回("如果 class")\n'
        self.assertEqual(translate(source), '# 定義 返回\ndef f():\n    return obj.返回("如果 class")\n')

    def test_run_accepts_handwritten_mixed_dialect_file(self):
        import subprocess
        import sys
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'mixed.py'
            source.write_text('定義 f():\n    歸 7\n印出(f())\n')
            result = subprocess.run([sys.executable, '-c', 'from senran.transcriber import main; main()',
                                     'run', str(source)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, '7\n')

    def test_soft_keywords_and_operators_roundtrip(self):
        from senran.codec import encode_names, to_python
        import keyword
        source = ' '.join(keyword.kwlist + keyword.softkwlist) + '\n'
        encoded = encode_names(source)
        body = encoded.split('\n', 1)[1]
        for word in keyword.kwlist + keyword.softkwlist:
            self.assertNotIn(word, body.split())
        self.assertEqual(化西文(encoded), source)
        self.assertEqual(to_python('如果 x 不在 y 或 x 不是 空:\n    略過\n'),
                         'if x not in y or x is not None:\n    pass\n')

    def test_restored_python_identifiers_are_not_dialect_keywords(self):
        from senran.codec import encode_names, to_python
        source = '返回 = 1\n真 = 2\nprint(返回, 真)\n'
        self.assertEqual(to_python(encode_names(source)), source)

    def test_grammar_names_do_not_collide_with_library_vocabulary(self):
        from senran.codec import encode_names
        source = 'assert verify\n'
        self.assertEqual(化西文(encode_names(source)), source)

    def test_handwritten_dialect_can_be_reversed_and_formatted(self):
        from senran.bridge import convert
        source = '定義 f():\n    返回 3\n印出(f())\n'
        self.assertEqual(convert('reverse', source), 'def f():\n    return 3\nprint(f())\n')
        encoded = convert('transcribe', source)
        self.assertIn('術 ', encoded.split('\n', 1)[1])
        self.assertIn('歸 ', encoded.split('\n', 1)[1])
        poem = convert('format', encoded)
        self.assertEqual(化西文(解賦(poem)), source)
        self.assertEqual(convert('markdown-reverse', poem), 'def f():\n    return 3\nprint(f())\n')
        self.assertEqual(convert('reverse', '印出("返回")\n'), 'print("返回")\n')

    def test_native_senran_imports_keep_callable_syntax_sugar(self):
        from senran.codec import to_python
        source = 'from senran import 若, 書, 真\n若(真).則(lambda: 書(1))\n'
        self.assertEqual(to_python(source), source)
        mixed = 'from senran import 書\n印出("plain")\n書("classical")\n'
        self.assertEqual(to_python(mixed), 'from senran import 書\nprint("plain")\n書("classical")\n')

    def test_import_semicolon_and_literal_legacy_name(self):
        from senran.codec import to_python
        from senran.bridge import convert
        self.assertEqual(to_python('導入 os; 印出(1)\n'), 'import os; print(1)\n')
        self.assertEqual(convert('reverse', '印出("引入")\n'), 'print("引入")\n')

    def test_runtime_from_import_syntax_is_also_classical(self):
        source = 'from __future__ import annotations\nfrom .pkg import value as alias\n'
        encoded = 化雅(source)
        body = encoded.split('\n', 1)[1]
        self.assertIn('由 __future__ 納 annotations', body)
        self.assertIn('由 .pkg 納 value 作 alias', body)
        self.assertEqual(化西文(encoded), source)

    def test_western_target_compiles_chinese_origin_but_archive_restores_it(self):
        from senran.bridge import convert
        source = '定義 f():\n    返回 3\n印出(f())\n'
        encoded = convert('zhpy', source)
        self.assertEqual(化西文(encoded), source)
        self.assertEqual(convert('reverse', encoded), 'def f():\n    return 3\nprint(f())\n')
        self.assertEqual(convert('reverse', convert('zhpy', '印出(1)\n')), 'print(1)\n')
        self.assertEqual(convert('reverse', convert('zhpy', '回呼 = 印出; 回呼(1)\n')),
                         '回呼 = print; 回呼(1)\n')

    def test_dot_legacy_word_and_mixed_callable_sugar(self):
        from senran.bridge import convert
        from senran.codec import to_python
        self.assertEqual(convert('reverse', '印出(obj.引入())\n'), 'print(obj.引入())\n')
        source = 'from senran import 若, 書, 真\n術 f():\n    若(真).則(lambda: 書(1))\n    歸 2\n'
        translated = to_python(source)
        self.assertIn('若(True).則(lambda:', translated)
        compile(translated, '<mixed>', 'exec')
        self.assertEqual(to_python('若 (真):\n    略\n'), 'if (True):\n    pass\n')

    def test_proxy_arguments_inside_containers(self):
        native = object()
        call = 引入(lambda value: value['items'][0][0] is native)
        self.assertTrue(call({'items': [(裹(native),)]}))

    def test_plain_container_identity_is_preserved(self):
        value = {'items': [object()]}
        self.assertIs(剖(value), value)

    def test_cyclic_list_with_proxy_is_unwrapped(self):
        native = object()
        value = [裹(native)]
        value.append(value)
        restored = 剖(value)
        self.assertIs(restored[0], native)
        self.assertIs(restored[1], restored)

    def test_tuple_list_cycle_with_proxy(self):
        native = object()
        values = []
        value = (values, 裹(native))
        values.append(value)
        restored = 剖(value)
        self.assertIs(restored[1], native)
        self.assertIs(restored[0][0], restored)

    def test_native_container_method_is_not_renamed(self):
        source = 'data = {"key": 1}\nx = data.get("key")\n'
        elegant = 化雅(source)
        self.assertIn('data.get(', elegant)
        self.assertEqual(化西文(elegant), source)

    def test_imported_builtin_name_is_not_renamed(self):
        source = 'from pkg import len\nx = len(data)\n'
        self.assertIn('x = len(data)', 化雅(source))

    def test_markdown_marker_in_source_is_literal(self):
        source = 'print("<!-- senran-pianwen-v1 fake -->")\n'
        self.check_roundtrip(source)

    def test_markdown_prose_can_be_edited(self):
        source = 化雅('print(1)\n')
        poem = 賦體(source).replace('夫運籌於帷幄之中', '夫持卷於几案之上')
        self.assertEqual(解賦(poem), source)

    def check_roundtrip(self, source):
        elegant = 化雅(source)
        self.assertEqual(化西文(elegant), source)
        self.assertEqual(解賦(賦體(elegant)), elegant)
        self.assertEqual(化西文(解賦(賦體(elegant))), source)

    def test_literal_data_is_unchanged(self):
        source = '# print(True)\nprint("True print( .get(")\n'
        elegant = 化雅(source)
        self.assertIn('# print(True)', elegant)
        self.assertIn('"True print( .get("', elegant)


def _case(source):
    def test(self):
        self.check_roundtrip(source)
    return test


for index, source in enumerate(CASES):
    setattr(LosslessTests, 'test_roundtrip_%02d' % index, _case(source))
