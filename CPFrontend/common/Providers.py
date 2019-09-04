class Providers:
    """clase base de proveedores"""
    def __init__(self):
        self.providerId = ''
        self.countryCode = ''
        self.coordinates = ''

        self.name = ''
        self.category = ''
        self.country = ''
        self.city = ''
        self.webpage = ''
        self.address = ''
        self.phone = ''
        self.emailAddresses = ''
        self.contactNames = ''
        self.specialty = ''
        self.taxId = ''
        self.bank = ''
        self.iban = ''
        self.comments = []
        self.hasDataProtection = False
        self.procurementCodes = []

    def setProviderId(self, id):
        self.providerId = id

    def setName(self, name):
        self.name = name

    def setCategory(self, category):
        self.category = category

    def setCountry(self, country):
        self.country = country

    def setCountryCode(self, code):
        self.countryCode = code

    def setCity(self, city):
        self.city = city

    def setCoordinates(self, coordinates):
        self.coordinates = coordinates

    def setAddress(self, address):
        self.address = address

    def setPhone(self, phone):
        self.phone = phone

    def setWebpage(self, web):
        self.webpage = web

    def setEmailAddresses(self, emails):
        self.emailAddresses = emails

    def setContactNames(self, names):
        self.contactNames = names

    def setSpecialty(self, specialty):
        self.specialty = specialty

    def setTaxId(self, taxid):
        self.taxId = taxid

    def setHasDataProtection(self, flag):
        self.hasDataProtection = flag

    def setBank(self, bank):
        self.bank = bank

    def setIban(self, iban):
        self.iban = iban

    def setComments(self, comments):
        self.comments = comments

    def setProcurementCodes(self, procurementCodes):
        self.comments = procurementCodes

    def to_json_comments(self):
        obj_list = [ob.__dict__ for ob in self.comments]
        return obj_list

    def to_json_procurement(self):
        obj_list = [ob.__dict__ for ob in self.comments]
        return obj_list
