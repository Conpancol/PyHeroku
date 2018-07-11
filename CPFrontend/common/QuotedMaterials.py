from common.ExtMaterials import ExtMaterials


class QuotedMaterials(ExtMaterials):
    """clase basica de materiales metalicos con cotizacion"""
    def __init__(self, material):
        super().__init__(material)
        self.theoreticalWeight = 0.00
        self.givenWeight = 0.00
        self.unitPrice = 0.00
        self.totalPrice = 0.00
        self.currency = "NA"
        self.countryOrigin = "NA"
        self.note = "NA"

    def setTheoreticalWeight(self, theoWeight):
        self.theoreticalWeight = theoWeight

    def setGivenWeight(self, givenWeight):
        self.givenWeight = givenWeight

    def setUnitPrice(self, unitPrice):
        self.unitPrice = unitPrice

    def setTotalPrice(self, total):
        self.totalPrice = total

    def setNote(self, note):
        self.note = note

    def setCountryOrigin(self, country):
        self.countryOrigin = country

    def setCurrency(self, currency):
        self.currency = currency
