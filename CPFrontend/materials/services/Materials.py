class Material:
    def __init__(self):
        """clase basica de materiales metalicos"""
        self.itemcode = "1"
        self.description = "X"
        self.type = "X"
        self.category = "X"
        self.dimensions = "X"

    def setItemCode(self,code):
        self.itemcode = code

    def setDescription(self,description):
        self.description = description

    def setType(self, type):
        self.type = type

    def setCategory(self, category):
        self.category = category

    def setDimensions(self, dimensions):
        self.dimensions = dimensions

    def getItemCode(self):
        return self.itemcode

    def getDescription(self):
        return self.description

    def getType(self):
        return self.type

    def getCategory(self):
        return self.category

    def getDimensions(self):
        return self.dimensions

    def __str__(self):
        return self.getItemCode() + ' ' + self.getDescription()

