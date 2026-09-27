import unittest
import os
import tempfile
from senran import 引入, 剖

class TestMLEcosystem(unittest.TestCase):
    def test_scikit_learn_linear_model(self):
        機算 = 引入("sklearn.linear_model")
        np = 引入("numpy")

        # 準備資料
        X = np.陣([[1.0], [2.0], [3.0], [4.0]])
        # y = 2 * x + 1
        y = np.陣([3.0, 5.0, 7.0, 9.0])

        模型 = 機算.LinearRegression()
        # 習 / 訓 / 擬合 -> fit
        模型.習(X, y)

        # 卜 / 推測 -> predict
        預測 = 模型.卜(np.陣([[5.0]]))
        self.assertAlmostEqual(預測[0], 11.0)

        # 考分 -> score
        得分 = 模型.考分(X, y)
        self.assertAlmostEqual(得分, 1.0)

    def test_matplotlib_visualization(self):
        plt = 引入("matplotlib.pyplot")
        np = 引入("numpy")

        x = np.linspace(0, 10, 20)
        y = np.sin(x)

        # 繪 -> plot
        plt.繪(x, y, label="正弦")
        # 標題 / 題 -> title
        plt.題("山水起伏圖")
        # 橫標 / 縱標 -> xlabel / ylabel
        plt.橫標("程途")
        plt.縱標("高低")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            tf_path = tf.name

        try:
            # 存圖 / 摹卷 -> savefig
            plt.存圖(tf_path)
            self.assertTrue(os.path.exists(tf_path))
            self.assertGreater(os.path.getsize(tf_path), 0)
        finally:
            plt.close()
            if os.path.exists(tf_path):
                os.remove(tf_path)

    def test_tqdm_progress(self):
        tqdm_mod = 引入("tqdm")
        items = [1, 2, 3]
        # 歷程 -> tqdm
        collected = []
        for x in tqdm_mod.歷程(items, disable=True):
            collected.append(x)
        self.assertEqual(collected, [1, 2, 3])

if __name__ == "__main__":
    unittest.main()
