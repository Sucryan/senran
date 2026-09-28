import unittest
from senran.transcriber import 化雅

class TestTranscriber(unittest.TestCase):
    def test_real_hello_world_runs_natively_and_after_every_conversion(self):
        import itertools
        import subprocess
        import sys
        import tempfile
        from pathlib import Path
        from senran.bridge import convert
        root = Path(__file__).resolve().parents[1]
        file = root / 'examples' / '01_hello_world.py'
        expected = ('【森蚺】問天地好在，四海安康！\n門徒人數： 4\n'
                    '--- 報數三聲 ---\n第 1 聲：在！\n第 2 聲：在！\n第 3 聲：在！\n'
                    '依理整飭： [1, 1, 2, 3, 4, 5, 6, 9]\n'
                    '逆序而行： [6, 2, 9, 5, 1, 4, 1, 3]\n'
                    '明斷：及格矣，善哉！\n')
        baseline = subprocess.run([sys.executable, str(file)], cwd=root, capture_output=True, text=True)
        self.assertEqual((baseline.returncode, baseline.stdout), (0, expected), baseline.stderr)
        source = file.read_text()
        with tempfile.TemporaryDirectory() as temp:
            for order in itertools.permutations(('transcribe', 'zhpy', 'format', 'reverse')):
                text, previous = source, None
                for target in order:
                    if previous == 'format':
                        text = convert('unformat', text)
                    text = convert(target, text)
                    path = Path(temp) / ('hello.md' if target == 'format' else 'hello.py')
                    path.write_text(text)
                    result = subprocess.run([sys.executable, '-m', 'senran', 'run', str(path)],
                                            cwd=root, capture_output=True, text=True)
                    self.assertEqual((result.returncode, result.stdout), (0, expected), (order, target, result.stderr))
                    previous = target
                if previous == 'format':
                    text = convert('unformat', text)
                self.assertEqual(convert('reverse', text), source)
            packet = convert('transcribe', source)
            edited = packet + '\n書("編輯後仍可執行")\n'
            for target in ('transcribe', 'zhpy', 'format', 'reverse'):
                text = convert(target, edited)
                path = Path(temp) / ('edited.md' if target == 'format' else 'edited.py')
                path.write_text(text)
                result = subprocess.run([sys.executable, '-m', 'senran', 'run', str(path)],
                                        cwd=root, capture_output=True, text=True)
                self.assertEqual((result.returncode, result.stdout),
                                 (0, expected + '編輯後仍可執行\n'), (target, result.stderr))

    def test_all_real_examples_compile_and_restore_exactly(self):
        from pathlib import Path
        from senran.bridge import convert
        from senran.codec import to_python
        examples = Path(__file__).resolve().parents[1] / 'examples'
        for file in sorted(examples.glob('0[1-5]_*.py')):
            source = file.read_text()
            compile(source, str(file), 'exec')
            for mode in ('transcribe', 'zhpy'):
                packet = convert(mode, source)
                compile(to_python(packet), str(file), 'exec')
                restored = convert('markdown-reverse', convert('format', packet))
                self.assertEqual(restored, source)
                compile(to_python(packet + '\n# edited revision\n', editable=True), str(file), 'exec')


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
        self.assertIn("由 senran 納", converted)

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
