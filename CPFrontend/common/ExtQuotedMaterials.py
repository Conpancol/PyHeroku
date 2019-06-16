from common.QuotedMaterials import QuotedMaterials


class ExtQuotedMaterials(QuotedMaterials):
    """clase basica de materiales metalicos con cotizacion"""
    def __init__(self, material):
        super().__init__(material)
        self.providerId = ''
        self.providerName = ''
        self.updateDate = ''
        self.projectId = 0
        self.revision = 0
        self.usdTRM = 0.0
        self.setTheoreticalWeight(material.getTheoreticalWeight())
        self.setGivenWeight(material.getGivenWeight())
        self.setUnitPrice(material.getUnitPrice())
        self.setTotalPrice(material.getTotalPrice())
        self.setCurrency(material.getCurrency())
        self.setCountryOrigin(material.getCountryOrigin())
        self.setNote(material.getNote())

    def setProviderId(self, providerId):
        self.providerId = providerId

    def setProviderName(self, providerName):
        self.providerName = providerName

    def setUpdateDate(self, updateDate):
        self.updateDate = updateDate

    def setProjectId(self, projectId):
        self.projectId = projectId

    def setRevision(self, revision):
        self.revision = revision

    def setUsdTRM(self, usdTRM):
        self.usdTRM = usdTRM

