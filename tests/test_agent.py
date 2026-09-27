"""
森蚺機巧使（Agent 中樞與三界互轉）單元考校
"""

import os
import shutil
import tempfile
import unittest
from senran.agent import 機巧使, MachineEnvoy, 策問, 設壇, 天機敕令, 化森蚺, 化西文, 化駢文, 解駢文


class TestMachineEnvoy(unittest.TestCase):
    """考校機巧使之神思、設壇與三界代碼互轉"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_ce_wen_intents(self):
        """考校白話/文言策問三界產出"""
        # 1. 爬蟲網絡
        成果 = 機巧使.策問("我想抓取網頁")
        self.assertIn("駢體賦", 成果)
        self.assertIn("森蚺碼", 成果)
        self.assertIn("標準碼", 成果)
        self.assertIn("requests", 成果["森蚺碼"])
        self.assertIn("httpbin.org", 成果["標準碼"])

        # 2. 矩陣計算
        成果_數 = 機巧使.策問("幫我算矩陣平均值")
        self.assertIn("numpy", 成果_數["森蚺碼"])
        self.assertIn("array", 成果_數["標準碼"])

        # 3. 深度學習
        成果_道 = 機巧使.策問("我想訓練神經網路計算梯度")
        self.assertIn("torch", 成果_道["森蚺碼"])
        self.assertIn("backward", 成果_道["標準碼"])

        # 4. 任意意向回退
        成果_奇 = 機巧使.策問("我想巡查泰山諸峰")
        self.assertIn("泰山諸峰", 成果_奇["森蚺碼"])

    def test_tri_directional_conversion(self):
        """考校三界代碼互轉"""
        標準碼 = (
            "import requests\n"
            "res = requests.get('https://example.com')\n"
            "if res.status_code == 200:\n"
            "    print(res.text)\n"
        )
        # 1. 標準 -> 森蚺
        森蚺碼 = 化森蚺(標準碼)
        self.assertIn("引入('requests')", 森蚺碼)
        self.assertIn(".得(", 森蚺碼)
        self.assertIn(".格", 森蚺碼)
        self.assertIn("書(", 森蚺碼)

        # 2. 森蚺 -> 駢文 (.sr)
        駢文 = 化駢文(森蚺碼)
        self.assertIn("📜【森蚺駢儷憲典", 駢文)
        self.assertIn("几案展卷，落字有聲", 駢文)

        # 3. 駢文 -> 可執行 Python
        復原碼 = 解駢文(駢文)
        self.assertIn("引入('requests')", 復原碼)

        # 4. 森蚺 -> 標準 Python
        逆轉碼 = 化西文(森蚺碼)
        self.assertIn("import requests", 逆轉碼)
        self.assertIn(".get(", 逆轉碼)
        self.assertIn(".status_code", 逆轉碼)
        self.assertIn("print(", 逆轉碼)

    def test_she_tan_and_chi_ling(self):
        """考校一鍵設壇與敕令明詔"""
        文卷清單 = 設壇(self.temp_dir)
        self.assertTrue(any("AGENTS.md" in f for f in 文卷清單))
        self.assertTrue(any(".cursorrules" in f for f in 文卷清單))
        self.assertTrue(any("CLAUDE.md" in f for f in 文卷清單))
        self.assertTrue(any("copilot-instructions.md" in f for f in 文卷清單))

        for f in 文卷清單:
            self.assertTrue(os.path.exists(f))

        敕令文 = 天機敕令()
        self.assertIn("機巧使明詔", 敕令文)
        self.assertIn("衍文鐵律", 敕令文)


if __name__ == "__main__":
    unittest.main()
