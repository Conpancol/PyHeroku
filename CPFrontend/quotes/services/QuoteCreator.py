import csv
import datetime
import logging

from .Quotes import *

from common.Materials import Material
from common.ExtMaterials import ExtMaterials
from common.QuotedMaterials import QuotedMaterials
from common.ExtQuotedMaterials import ExtQuotedMaterials


class QuoteCreator:
    """clase que crea QUOTES en el formator necesario para guardar en la DB"""
    def __init__(self):
        self.quote = Quotes()
        self.quote_list = []
        logging.basicConfig(filename='logs/qcreator.log', level=logging.DEBUG)

    def setQuoteInformation(self,
                            internalCode,
                            externalCode,
                            providerCode,
                            id,
                            provider,
                            contact,
                            receivedDate,
                            sentDate,
                            user,
                            edt):
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
        self.quote.setEdt(edt)

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

                        extended_material = ExtMaterials(material)
                        extended_material.setOrderNumber(orderNum)
                        extended_material.setUnit(unit)
                        extended_material.setQuantity(quantity)

                        quoted_material = QuotedMaterials(extended_material)
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

    def editQuotewithMaterials(self, quote_form, material_formset, material_data):
        try:

            quote = Quotes()
            quote.setIntenalCode(quote_form.cleaned_data['internalCode'])
            quote.setExternalCode(quote_form.cleaned_data['externalCode'])
            quote.setProviderCode(quote_form.cleaned_data['providerCode'])
            quote.setReceivedDate(quote_form.cleaned_data['receivedDate'])
            quote.setSentDate(quote_form.cleaned_data['sentDate'])
            quote.setUser(quote_form.cleaned_data['user'])
            quote.setProviderId(quote_form.cleaned_data['providerId'])
            quote.setProviderName(quote_form.cleaned_data['providerName'])
            quote.setContactName(quote_form.cleaned_data['contactName'])
            quote.setIncoterms(quote_form.cleaned_data['incoterms'])
            quote.setNote(quote_form.cleaned_data['note'])
            quote.setEdt(quote_form.cleaned_data['edt'])

            extmaterials = []

            try:
                idx = 0
                for tmp_data in material_formset:

                    itemcode_data = material_data[idx]['itemcode']
                    order_number_data = material_data[idx]['orderNumber']
                    quantity_data = material_data[idx]['quantity']
                    unit_data = material_data[idx]['unit']

                    material = Material()
                    material.setItemCode(itemcode_data)
                    material.setDescription(material_data[idx]['description'])
                    material.setType(material_data[idx]['type'])
                    material.setCategory(material_data[idx]['category'])
                    material.setDimensions(material_data[idx]['dimensions'])

                    ext_material = ExtMaterials(material)
                    ext_material.setOrderNumber(order_number_data)
                    ext_material.setQuantity(quantity_data)
                    ext_material.setUnit(unit_data)

                    mod_material = QuotedMaterials(ext_material)
                    mod_material.setOrderNumber(order_number_data)
                    mod_material.setQuantity(tmp_data.cleaned_data['quantity'])
                    mod_material.setUnit(tmp_data.cleaned_data['unit'])
                    mod_material.setUnitPrice(tmp_data.cleaned_data['unitPrice'])
                    mod_material.setTotalPrice(tmp_data.cleaned_data['totalPrice'])

                    mod_material.setCountryOrigin(material_data[idx]['countryOrigin'])
                    mod_material.setCurrency(material_data[idx]['currency'])
                    mod_material.setTheoreticalWeight(material_data[idx]['theoreticalWeight'])
                    mod_material.setGivenWeight(material_data[idx]['givenWeight'])

                    extmaterials.append(mod_material)

                    idx = idx + 1

            except Exception as ex:
                logging.info(ex)

            quote.setMaterialList(extmaterials)

            quote_json = quote.__dict__
            quote_json['materialList'] = quote.to_json()

            self.quote_list.append(quote_json)

            return self.quote_list

        except IOError as error:
            logging.info(error)
            return self.quote_list

    def editQuotedMaterials(self, quote_form, material_data):
        try:

            material = Material()
            material.setItemCode(material_data['itemcode'])
            material.setDescription(material_data['description'])
            material.setType(material_data['type'])
            material.setCategory(material_data['category'])
            material.setDimensions(material_data['dimensions'])

            ext_material = ExtMaterials(material)
            ext_material.setOrderNumber(material_data['orderNumber'])
            ext_material.setQuantity(material_data['quantity'])
            ext_material.setUnit(material_data['unit'])

            quoted_material = QuotedMaterials(ext_material)
            quoted_material.setUnitPrice(quote_form.cleaned_data['unitPrice'])
            quoted_material.setTotalPrice(quote_form.cleaned_data['totalPrice'])

            quote = ExtQuotedMaterials(quoted_material)
            quote.setRevision(quote_form.cleaned_data['revision'])

            quote_json = quote.__dict__

            self.quote_list.append(quote_json)

            return self.quote_list

        except IOError as error:
            logging.info(error)
            return self.quote_list
