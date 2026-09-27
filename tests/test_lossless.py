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
