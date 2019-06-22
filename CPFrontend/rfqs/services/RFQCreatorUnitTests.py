import unittest, os
from .RFQCreator import RFQCreator
from .RFQTestFile import rfq


class MyTestCase(unittest.TestCase):
    def test_getNumberPlates(self):

        good_dimensions = "4' X 8' X 3/4\",8000.0MM X 2000.0MM X 10.0MM"
        bad_dimensions = "4' X 8' X 10.00MM,8000.0MM X 2000.0MM X 10.0MM"

        rfq_service = RFQCreator()
        nplates = rfq_service.getNumberPlates(good_dimensions,32)
        self.assertEqual('2.00', str(nplates))
        nplates = rfq_service.getNumberPlates(bad_dimensions, 32)
        self.assertEqual('0.0', str(nplates))

    def test_runBasicAnalysis(self):

        rfq_service = RFQCreator()
        output_file = rfq_service.runBasicAnalysis(rfq)

        if os.path.exists(output_file):
            try:
                # os.remove('.' + output_file)
                print("removed file: " + output_file)
            except Exception as error:
                print(error)


if __name__ == '__main__':
    unittest.main()
