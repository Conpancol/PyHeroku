import unittest
from .RFQTools import RFQTools


class MyTestCase(unittest.TestCase):

    def test_initialization(self):

        tools = RFQTools()
        tools.RFQMatcherContext(3410)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
