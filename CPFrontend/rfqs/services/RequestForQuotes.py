class RequestForQuotes:
    """clase para RFQs - debe ser igual a la que tiene el Backend"""
    def __init__(self):
        self.internalCode = 0
        self.externalCode = 0
        self.receivedDate = '1900'
        self.processedDate = '1900'
        self.user = "aosorio"
        self.sender = "X"
        self.company = "X"
        self.note = "NA"
        self.materialList = []

    def setIntenalCode(self, code):
        self.internalCode = code

    def setExternalCode(self,code):
        self.externalCode = code

    def setUser(self,user):
        self.user = user

    def setSender(self,sender):
        self.sender = sender

    def setCompany(self,company):
        self.company = company

    def setMaterialList(self, materials):
        for mt in materials:
            self.materialList.append(mt)

    def setReceivedDate(self,date):
        self.receivedDate = date

    def setProcessedDate(self,date):
        self.processedDate = date

    def setNote(self,note):
        self.note = note

    def to_json(self):
        obj_list = [ob.__dict__ for ob in self.materialList]
        return obj_list
