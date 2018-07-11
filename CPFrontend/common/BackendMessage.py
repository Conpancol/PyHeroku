class BackendMessage:
    def __init__(self, json):
        self.errorInd = json["errorInd"]
        self.value = json["value"]

    def setErrorInd(self,flag):
        self.errorInd = flag

    def setValue(self,value):
        self.value = value

    def getErrorInd(self):
        return self.errorInd

    def getValue(self):
        return self.value

    def __str__(self):
        return str(self.getErrorInd()) + " " + str(self.getValue())

