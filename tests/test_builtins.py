import io
import sys
import unittest
from senran import (
    書, 計, 疇, 總, 整, 浮, 文, 錄, 譜, 集, 偶,
    真, 假, 空, 審, 係, 枚, 並, 序, 反, 定, 若
)

class TestBuiltins(unittest.TestCase):
    def test_constants(self):
        self.assertIs(真, True)
        self.assertIs(假, False)
        self.assertIs(空, None)

    def test_types(self):
        self.assertEqual(整("42"), 42)
        self.assertEqual(浮("3.14"), 3.14)
        self.assertEqual(文(100), "100")
        self.assertEqual(錄((1, 2)), [1, 2])
        self.assertEqual(譜([("甲", 1)]), {"甲": 1})

    def test_calculations(self):
        self.assertEqual(計([1, 2, 3, 4]), 4)
        self.assertEqual(總([10, 20, 30]), 60)
        self.assertEqual(list(疇(3)), [0, 1, 2])
        self.assertEqual(序([3, 1, 2]), [1, 2, 3])
        self.assertEqual(list(反([1, 2, 3])), [3, 2, 1])

    def test_print(self):
        captured = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = captured
            書("天地玄黃", "宇宙洪荒")
            self.assertEqual(captured.getvalue().strip(), "天地玄黃 宇宙洪荒")
        finally:
            sys.stdout = old_stdout

    def test_enumeration_and_zip(self):
        pairs = list(枚(["甲", "乙"]))
        self.assertEqual(pairs, [(0, "甲"), (1, "乙")])

        zipped = list(並([1, 2], ["甲", "乙"]))
        self.assertEqual(zipped, [(1, "甲"), (2, "乙")])

    def test_assertion(self):
        定(1 + 1 == 2, "一加一當為二")
        with self.assertRaises(AssertionError):
            定(1 == 2, "妄言")

    def test_conditional_sugar(self):
        result = []
        若(真).則(lambda: result.append("成")).否則(lambda: result.append("敗"))
        self.assertEqual(result, ["成"])

        result.clear()
        若(假).則(lambda: result.append("成")).否則(lambda: result.append("敗"))
        self.assertEqual(result, ["敗"])

if __name__ == "__main__":
    unittest.main()
