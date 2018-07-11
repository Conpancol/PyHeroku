from common.Materials import Material


class ExtMaterials(Material):
    """Extended material class"""
    def __init__(self, material):
        super().__init__()
        self.orderNumber = "1"
        self.unit = "EA"
        self.quantity = 1.0
        self.setItemCode(material.getItemCode())

    def setOrderNumber(self, orderNum):
        self.orderNumber = orderNum

    def setUnit(self, unit):
        self.unit = unit

    def setQuantity(self, quantity):
        self.quantity = quantity

