import unittest
from unittest.mock import MagicMock, patch
from senran import 引入, 剖

class TestPopularEcosystem(unittest.TestCase):
    def test_numpy_support(self):
        np = 引入("numpy")
        
        # 陣 -> array
        數組 = np.陣([10, 20, 30])
        # 均 -> mean
        self.assertEqual(數組.均(), 20.0)
        # 和 / 總 -> sum
        self.assertEqual(數組.總(), 60)
        # 形 -> shape
        self.assertEqual(數組.形, (3,))
        # 皆零 -> zeros
        零陣 = np.皆零((2, 3))
        self.assertEqual(零陣.形, (2, 3))
        # 塑 -> reshape
        重塑 = 數組.塑((3, 1))
        self.assertEqual(重塑.形, (3, 1))

    def test_pandas_support(self):
        pd = 引入("pandas")
        資料 = {"名號": ["子路", "顏回", "子貢"], "智勇": [85, 99, 90]}
        表 = pd.DataFrame(資料)

        # 欄 -> columns
        self.assertIn("名號", list(表.欄))
        # 冠 -> head
        首部 = 表.冠(2)
        self.assertEqual(len(首部), 2)
        # 描述 -> describe
        摘要 = 表.描述()
        self.assertTrue(hasattr(摘要, "loc"))

    @patch("requests.get")
    def test_requests_mock(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "天行健，君子以自強不息。"
        mock_resp.json.return_value = {"天地": "玄黃"}
        mock_get.return_value = mock_resp

        求 = 引入("requests")
        報 = 求.得("https://example.com/api")

        # 格 / 態 -> status_code
        self.assertEqual(報.格, 200)
        # 文 -> text
        self.assertEqual(報.文, "天行健，君子以自強不息。")
        # 析文 / 譜 -> json()
        self.assertEqual(報.譜()["天地"], "玄黃")

    @patch("httpx.Client.get")
    def test_httpx_mock(self, mock_client_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "地勢坤，君子以厚德載物。"
        mock_client_get.return_value = mock_resp

        客戶 = 引入("httpx").Client()
        報 = 客戶.得("https://example.com/api")
        self.assertEqual(報.態, 200)
        self.assertEqual(報.文, "地勢坤，君子以厚德載物。")

if __name__ == "__main__":
    unittest.main()
