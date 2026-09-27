import unittest
from senran import 裹, 剖, SenranProxy

class DummyTarget:
    def __init__(self):
        self.status_code = 200
        self.text = "君子不器"
        self._secret = "隱"

    def get_info(self):
        return "大智若愚"

    def to_dict(self):
        return {"道": 1}

    def is_valid(self):
        return True


class TestProxy(unittest.TestCase):
    def test_proxy_basic_attributes(self):
        obj = DummyTarget()
        p = 裹(obj)
        # 文 -> text
        self.assertEqual(p.文, "君子不器")
        # 格 -> status_code
        self.assertEqual(p.格, 200)
        # 英文直接兼容
        self.assertEqual(p.status_code, 200)

    def test_smart_prefix_resolution(self):
        obj = DummyTarget()
        p = 裹(obj)
        # 取_info -> get_info
        self.assertEqual(p.取_info(), "大智若愚")
        # 化_dict -> to_dict
        self.assertEqual(p.化_dict()["道"], 1)
        # 為_valid -> is_valid
        self.assertTrue(p.為_valid())

    def test_unwrapping(self):
        obj = DummyTarget()
        p = 裹(obj)
        self.assertIs(p.本, obj)
        self.assertIs(剖(p), obj)

    def test_helpful_error_suggestions(self):
        obj = DummyTarget()
        p = 裹(obj)
        with self.assertRaises(AttributeError) as ctx:
            _ = p.莫名其妙之物
        # 確保報錯有森蚺提示
        self.assertIn("森蚺未能在【DummyTarget】中尋得「莫名其妙之物」", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
