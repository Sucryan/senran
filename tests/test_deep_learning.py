import unittest
from senran import 引入, 剖

class TestDeepLearning(unittest.TestCase):
    def test_pytorch_tensor_and_grad(self):
        機心 = 引入("torch")
        
        # 量 -> tensor
        甲 = 機心.量([1.0, 2.0, 3.0, 4.0])
        # 均 -> mean
        self.assertEqual(甲.均().析值(), 2.5) # 析值 -> item
        # 總 -> sum
        self.assertEqual(甲.總().析值(), 10.0)
        # 形 -> shape
        self.assertEqual(甲.形, (4,))
        # 相 -> view
        重塑 = 甲.相((2, 2))
        self.assertEqual(重塑.形, (2, 2))

        # 皆零 -> zeros, 皆一 -> ones
        零量 = 機心.皆零((2, 3))
        self.assertEqual(零量.形, (2, 3))
        一量 = 機心.皆一((3, 2))
        self.assertEqual(一量.形, (3, 2))

        # 矩積 -> matmul
        乘積 = 機心.矩積(零量, 一量)
        self.assertEqual(乘積.形, (2, 2))

    def test_pytorch_autograd(self):
        機心 = 引入("torch")
        
        # 設定可求導之權重
        權 = 機心.量([3.0], requires_grad=True)
        # y = 權^2 + 2*權 + 1
        # dy/d權 = 2*權 + 2 = 2*3 + 2 = 8
        損 = 權 ** 2 + 2 * 權 + 1
        
        # 溯 / 反溯 / 反向傳播 -> backward()
        損.反溯()
        
        # 勢 / 梯度 -> grad
        self.assertIsNotNone(權.勢)
        self.assertAlmostEqual(權.勢.析值(), 8.0)

    def test_pytorch_nn_and_optim(self):
        機心 = 引入("torch")
        import torch.nn as nn
        import torch.optim as optim
        
        # 構建簡易線性層
        層 = 引入(nn.Linear(2, 1))
        # 構建精進器 (SGD)
        精進客 = 引入(optim.SGD(層.本.parameters(), lr=0.1))
        
        # 清勢 -> zero_grad()
        精進客.清勢()
        
        輸入 = 機心.量([[1.0, 2.0]])
        輸出 = 層(輸入)
        
        目標 = 機心.量([[5.0]])
        損 = (輸出 - 目標).總()
        損.反溯()
        
        # 步進 -> step()
        精進客.步進()
        self.assertEqual(輸出.形, (1, 1))

if __name__ == "__main__":
    unittest.main()
