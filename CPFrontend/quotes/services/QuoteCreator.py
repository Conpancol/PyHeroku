import csv
import datetime
import logging

from .Quotes import *

from common.Materials import Material
from common.QuotedMaterials import QuotedMaterials


class QuoteCreator:
    """clase que crea QUOTES en el formator necesario para guardar en la DB"""
    def __init__(self):
        self.quote = Quotes()
        logging.basicConfig(filename='logs/qcreator.log', level=logging.DEBUG)

    def setQuoteInformation(self, internalCode, externalCode, providerCode, id, provider, contact, receivedDate, sentDate, user):
        self.quote.setIntenalCode(internalCode)
        self.quote.setExternalCode(externalCode)
        self.quote.setProviderCode(providerCode)
        self.quote.setContactName(contact)
        self.quote.setProviderId(id)
        self.quote.setProviderName(provider)
        self.quote.setReceivedDate(receivedDate)
        self.quote.setSentDate(sentDate)
        self.quote.setUser(user)
        dt = datetime.datetime.now()
        self.quote.setProcessedDate(dt.strftime('%d/%m/%Y'))

    def setQuoteNote(self, note):
        self.quote.setNote(note)

    def setQuoteIncoterms(self, incoterms):
        self.quote.setIncoterms(incoterms)

    def setQuoteEdt(self, edt):
        self.quote.setEdt(edt)

    def createQuotefromCSV(self, csvfile):
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
                        weight = float(row[4])
                        givenweight = float(row[5])
                        unitprice = float(row[6])
                        totalprice = float(row[7])
                        currency = row[8]
                        country = row[9]
                        note = row[10]

                        material = Material()
                        material.setItemCode(itemCode)
                        quoted_material = QuotedMaterials(material)
                        quoted_material.setOrderNumber(orderNum)
                        quoted_material.setUnit(unit)
                        quoted_material.setQuantity(quantity)
                        quoted_material.setTheoreticalWeight(weight)
                        quoted_material.setGivenWeight(givenweight)
                        quoted_material.setUnitPrice(unitprice)
                        quoted_material.setTotalPrice(totalprice)
                        quoted_material.setCurrency(currency)
                        quoted_material.setCountryOrigin(country)
                        quoted_material.setNote(note)
                        qtmaterials.append(quoted_material)
                    except ValueError as error:
                        print(itemCode)
                        print(error)
                        continue

                self.quote.setMaterialList(qtmaterials)

            quote_json = self.quote.__dict__
            quote_json['materialList'] = self.quote.to_json()

            total_materials = len(quote_json['materialList'])
            logging.info('End of Quote creation  \t' + str(total_materials))

            return quote_json

        except IOError as error:
            print("QuoteCreator")
            print(error)
