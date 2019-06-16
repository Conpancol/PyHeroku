import csv
import logging

from common.Materials import Material
from common.ExtMaterials import ExtMaterials
from common.QuotedMaterials import QuotedMaterials
from common.ExtQuotedMaterials import ExtQuotedMaterials


class ExtQuotedMaterialCreator:
    """clase que crea EXTENDED QUOTED MATERIALS en el formator necesario para guardar en la DB"""
    def __init__(self):
        logging.basicConfig(filename='logs/qcreator.log', level=logging.DEBUG)
        self.providerId = ''
        self.providerName = ''
        self.revision = 0

    def setExtendedInformation(self, providerId, providerName, revision):
        self.providerId = providerId
        self.providerName = providerName
        self.revision = revision

    def createExtQuotedMaterialsfromCSV(self, csvfile):
        try:
            with open(csvfile, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, dialect="excel-tab")
                qtmaterials = []
                for row in reader:
                    try:
                        orderNum = row[0]
                        itemCode = row[1]
                        quantity = float(row[2])
                        unit = row[3]
                        unitprice = float(row[4])
                        totalprice = float(row[5])
                        currency = row[6]
                        country = row[7]
                        projectId = row[8]
                        updateDate = row[9]

                        material = Material()
                        material.setItemCode(itemCode)
                        material.setDescription("")

                        ext_material = ExtMaterials(material)
                        ext_material.setOrderNumber(orderNum)
                        ext_material.setUnit(unit)
                        ext_material.setQuantity(quantity)

                        quoted_material = QuotedMaterials(ext_material)
                        quoted_material.setTheoreticalWeight(0.0)
                        quoted_material.setGivenWeight(0.0)
                        quoted_material.setUnitPrice(unitprice)
                        quoted_material.setTotalPrice(totalprice)
                        quoted_material.setCurrency(currency)
                        quoted_material.setCountryOrigin(country)
                        quoted_material.setNote("NA")

                        ext_quoted_material = ExtQuotedMaterials(quoted_material)
                        ext_quoted_material.setProjectId(projectId)
                        ext_quoted_material.setUpdateDate(updateDate)
                        ext_quoted_material.setProviderId(self.providerId)
                        ext_quoted_material.setProviderName(self.providerName)
                        ext_quoted_material.setRevision(self.revision)

                        qtmaterials.append(ext_quoted_material)

                    except ValueError as error:
                        print(itemCode)
                        print(error)
                        continue

            quote_json = [ob.__dict__ for ob in qtmaterials]
            logging.info('End of Quote creation  \t' + str(len(qtmaterials)))

            return quote_json

        except IOError as error:
            print("ExtendedQuotedMaterialsCreator")
            print(error)
