import unittest
from senran.transcriber import 化雅

class TestTranscriber(unittest.TestCase):
    def test_transcribe_basic_builtins(self):
        code = """
print("hello world")
n = len([1, 2, 3])
for i in range(10):
    pass
total = sum([1, 2])
flag = True
"""
        converted = 化雅(code)
        self.assertIn('書("hello world")', converted)
        self.assertIn("計([1, 2, 3])", converted)
        self.assertIn("疇(10)", converted)
        self.assertIn("總([1, 2])", converted)
        self.assertIn("flag = 真", converted)
        self.assertIn("from senran import", converted)

    def test_transcribe_requests(self):
        code = """
import requests

res = requests.get("https://example.com")
print(res.status_code)
print(res.text)
data = res.json()
"""
        converted = 化雅(code)
        self.assertIn("求 = 引入('requests')", converted)
        self.assertIn("求.得(", converted)
        self.assertIn("res.格", converted)
        self.assertIn("res.文", converted)
        self.assertIn("res.譜()", converted)
        self.assertIn("書(", converted)

    def test_transcribe_pytorch(self):
        code = """
import torch

x = torch.tensor([1.0, 2.0])
x.backward()
print(x.grad)
optimizer.zero_grad()
optimizer.step()
"""
        converted = 化雅(code)
        self.assertIn("神算 = 引入('torch')", converted)
        self.assertIn(".量(", converted)
        self.assertIn(".反溯()", converted)
        self.assertIn(".勢", converted)
        # 未能證明 optimizer 為代理時，保留原方法，免傷自訂物件。
        self.assertIn("optimizer.zero_grad()", converted)
        self.assertIn("optimizer.step()", converted)

if __name__ == "__main__":
    unittest.main()
