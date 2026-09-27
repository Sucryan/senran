import unittest
import os
import tempfile
from senran import 引入, 啟, 書, 譜, 錄, 剖

class TestLibraries(unittest.TestCase):
    def test_math_library(self):
        算術 = 引入("math")
        # 開方 -> sqrt
        self.assertEqual(算術.開方(16), 4.0)
        # 正弦 -> sin
        self.assertAlmostEqual(算術.正弦(0), 0.0)
        # 英文原名直接兼容
        self.assertEqual(算術.floor(3.9), 3)

    def test_json_library(self):
        典籍 = 引入("json")
        資料 = {"君子": "務本", "本立": "道生"}
        # 化字 -> dumps
        字串 = 典籍.化字(資料, ensure_ascii=False)
        self.assertIn("務本", 字串)
        # 析字 -> loads
        復原 = 典籍.析字(字串)
        self.assertEqual(復原["君子"], "務本")

    def test_os_and_pathlib(self):
        府衙 = 引入("os")
        # 存在 -> path.exists / exists
        當前處 = 府衙.getcwd()
        self.assertTrue(府衙.path.exists(當前處))

    def test_sqlite3_database(self):
        庫 = 引入("sqlite3")
        # 通 -> connect
        連接 = 庫.通(":memory:")
        案台 = 連接.案台()  # cursor
        # 判詞 -> execute
        案台.判詞("CREATE TABLE 門生 (名 TEXT, 功名 INT)")
        案台.判詞("INSERT INTO 門生 VALUES ('顏回', 100)")
        案台.判詞("SELECT 名, 功名 FROM 門生")
        # 攬一 -> fetchone
        所得 = 案台.攬一()
        self.assertEqual(剖(所得), ("顏回", 100))
        連接.閉()

    def test_random_library(self):
        機運 = 引入("random")
        # 拈號 -> randint
        號 = 機運.拈號(1, 10)
        self.assertTrue(1 <= 號 <= 10)
        # 隨選 -> choice
        選 = 機運.隨選(["仁", "義", "禮", "智", "信"])
        self.assertIn(選, ["仁", "義", "禮", "智", "信"])

    def test_file_io_context_manager(self):
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as tf:
            tf_path = tf.name

        try:
            # 啟 -> open
            with 啟(tf_path, "w", encoding="utf-8") as 牘:
                牘.書("落霞與孤齊飛，秋水共長天一色。") # 書 -> write

            with 啟(tf_path, "r", encoding="utf-8") as 牘:
                得文 = 牘.閱() # 閱 -> read
                self.assertEqual(得文, "落霞與孤齊飛，秋水共長天一色。")
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)

if __name__ == "__main__":
    unittest.main()
