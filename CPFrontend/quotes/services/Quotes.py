class Quotes:
    def __init__(self):
        """clase basica de materiales cotizados"""
        self.internalCode = 0
        self.externalCode = 0
        self.providerCode = "X"
        self.receivedDate = "X"
        self.processedDate = "X"
        self.sentDate = "X"
        self.user = "X"
        self.providerId = "X"
        self.providerName = "X"
        self.contactName = "X"
        self.incoterms = "X"
        self.materialList = []
        self.note = "NA"

    def setIntenalCode(self, code):
        self.internalCode = code

    def setExternalCode(self,code):
        self.externalCode = code

    def setProviderCode(self,code):
        self.providerCode = code

    def setUser(self,user):
        self.user = user

    def setProviderId(self,id):
        self.providerId = id

    def setProviderName(self,provider):
        self.providerName = provider

    def setContactName(self,contact):
        self.contactName = contact

    def setMaterialList(self, materials):
        for mt in materials:
            self.materialList.append(mt)

    def setReceivedDate(self,date):
        self.receivedDate = date

    def setProcessedDate(self,date):
        self.processedDate = date

    def setSentDate(self,date):
        self.sentDate = date

    def setUser(self,user):
        self.user = user

    def setIncoterms(self,incoterms):
        self.incoterms = incoterms

    def setNote(self,note):
        self.note = note

    def to_json(self):
        obj_list = [ ob.__dict__ for ob in self.materialList]
        return obj_list
