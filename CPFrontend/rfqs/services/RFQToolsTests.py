import unittest
from .RFQTools import RFQTools


class MyTestCase(unittest.TestCase):

    def test_initialization(self):

        tools = RFQTools()
        tools.RFQMatcherContext(3410)
        self.assertEqual(True, True)

    def test_qmaterial_matcher(self):

        tools = RFQTools()
        result = tools.QuotedMaterialMatcher(3412, 'MP10001')
        print(result["10400002011"][0])
        print(result["10400002011"][1])
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
