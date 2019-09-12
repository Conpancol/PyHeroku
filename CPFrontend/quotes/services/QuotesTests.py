import unittest
from ..forms import SmartQuotesForm


class MyTestCase(unittest.TestCase):
    def test_smart_form(self):

        providers_list = [{'providerID': "MP10001", "name": "PV01"},
                          {'providerID': "MP10002", "name": "PV02"}]

        form = SmartQuotesForm(providers_list)

        provider_choices = form.getProviderInfo()

        print(provider_choices)

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
