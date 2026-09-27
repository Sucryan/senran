import unittest
from senran.formatter import 賦體, 解賦

class TestFormatter(unittest.TestCase):
    def test_pianwen_formatting_and_roundtrip(self):
        code = """
求 = 引入('requests')
報 = 求.得('https://httpbin.org/get')
if 報.格 == 200:
    書('功成：', 報.文[:20])
"""
        sr = 賦體(code)
        self.assertIn("置百家之珍，引「requests」入府，銘曰「求」；", sr)
        self.assertIn("遣驛使以往訪", sr)
        self.assertIn("若夫考校其理", sr)
        self.assertIn("几案展卷，落字有聲", sr)

        # 解賦還原
        reconstructed = 解賦(sr)
        self.assertIn("求 = 引入('requests')", reconstructed)
        self.assertIn("報 = 求.得('https://httpbin.org/get')", reconstructed)
        self.assertIn("if 報.格 == 200:", reconstructed)
        self.assertIn("書('功成：', 報.文[:20])", reconstructed)

if __name__ == "__main__":
    unittest.main()
