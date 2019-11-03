import csv
import datetime
import logging
import re

from .RequestForQuotes import *
from .RFQTools import RFQTools

from common.Materials import Material
from common.ExtMaterials import ExtMaterials

try:
    from ..choices import *
except FileNotFoundError:
    INCOTERMS_CHOICES = (
        (1, "FOB"),
        (2, "CFR"),
        (3, "CIF"),
        (4, "EXW"),
    )


class RFQCreator:
    """clase para crear RFQs"""
    def __init__(self):
        self.rfq = RequestForQuotes()
        self.rfq_list = []
        try:
            logging.basicConfig(filename='logs/rfqcreator.log', level=logging.DEBUG)
        except FileNotFoundError:
            print("logging disabled for RFQCreator")

    def setRFQInformation(self, internalCode, externalCode, sender, company, receivedDate):
        self.rfq.setIntenalCode(internalCode)
        self.rfq.setExternalCode(externalCode)
        self.rfq.setSender(sender)
        self.rfq.setCompany(company)
        self.rfq.setReceivedDate(receivedDate)
        dt = datetime.datetime.now()
        self.rfq.setProcessedDate(dt.strftime('%d/%m/%Y'))

    def addRFQNote(self, note):
        self.rfq.setNote(note)

    def createRFQfromCSV(self, csvfile):
        try:
            with open(csvfile, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, dialect="excel-tab")
                extmaterials = []
                for row in reader:
                    try:
                        orderNum = row[0]
                        itemCode = row[1]
                        quantity = float(row[2])
                        unit = row[3]
                        print(orderNum, itemCode, quantity, unit)
                        material = Material()
                        material.setItemCode(itemCode)
                        extendedMaterial = ExtMaterials(material)
                        extendedMaterial.setOrderNumber(orderNum)
                        extendedMaterial.setUnit(unit)
                        extendedMaterial.setQuantity(quantity)
                        extmaterials.append(extendedMaterial)

                    except ValueError:
                        print('There is a wrong data format entry. Please check')
                        logging.info('There is a wrong data format entry. Please check')
                        continue

                self.rfq.setMaterialList(extmaterials)

            rfq_json = self.rfq.__dict__
            rfq_json['materialList'] = self.rfq.to_json()

            total_materials = len(rfq_json['materialList'])
            logging.info('End of RFQ creation  \t' + str(total_materials))

            return rfq_json

        except IOError as error:
            logging.info(error)

    def exportRFQtoCSV(self, rfq, terms, port):

        labels = []
        labels.append('Id')
        labels.append('OrderId')
        labels.append('ItemId')
        labels.append('Description')
        labels.append('Type')
        labels.append('Quantity')
        labels.append('Unit')
        labels.append('# Plates')

        internal_code = str(rfq["internalCode" ])
        csvfile = 'RFQ-' + internal_code + '_Conpancol.csv'
        path = "media/export/" + csvfile

        try:

            with open(path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, dialect="excel", delimiter=';')
                header = 'RFQ internal code: ' + str(rfq["internalCode"])
                writer.writerow([header])
                details = 'Received date: ' + str(rfq["receivedDate"])
                writer.writerow([details])
                note = 'Note: ' + str(rfq["note"])

                writer.writerow([note])
                writer.writerow([''])
                writer.writerow(labels)

                items = rfq["materialList"]

                id = 1

                for item in items:
                    row = []
                    row.append(str(id))
                    row.append(item["orderNumber"])
                    row.append(item["itemcode"])
                    description = item["description"]
                    row.append(description)
                    row.append(item["type"])
                    row.append(str(item["quantity"]))
                    row.append(str(item["unit"]))

                    if item["category"] == "PLATE":
                        nplates = self.getNumberPlates(item["dimensions"], item["quantity"])
                        row.append(str(nplates))

                    writer.writerow(row)
                    id += 1

                for i in range(1, 3):
                    writer.writerow([' '])
                bottom_txt_file = open('./resources/inputs/Bottom_conditions_EN.txt', 'r')
                bottom_txt_rows = bottom_txt_file.readlines()
                incoterms = INCOTERMS_CHOICES[int(terms)-1][1]
                for line in bottom_txt_rows:
                    row = line.replace('\n', ' ')
                    row = row.replace('###INCOTERMS###', incoterms)
                    row = row.replace('###PORT###', port)
                    writer.writerow([row])
                bottom_txt_file.close()

            f.close()
            return path

        except IOError:
            logging.info('Problem with file creation')
            return path

        except Exception as e:
            logging.info('General exception' + str(e))
            return path

    def getNumberPlates(self, dimensions, total_area):
        nplates = 0.0
        all_dims = dimensions.split(',')
        try:
            for dm in all_dims:
                if re.search('MM', dm):
                    max_occurences = len(re.findall('MM', dm))
                    if max_occurences == 3:
                        dim_values = []
                        dims = dm.split('X')
                        if len(dims) == 3:
                            for dd in dims:
                                try:
                                    dim_values.append(float(dd.replace(' ', '').replace('MM', '')))
                                except ValueError:
                                    dim_values.append(0.0)
                                    logging.info('Got a Value conversion exception, please check')
                                    logging.info(dd.replace(' ', '').replace('MM', ''))

                            area = dim_values[0] * dim_values[1] * 0.000001
                            nplates = format(total_area / area, '.2f')
                            result = str(dim_values) + " " + str(total_area) + " " + str(nplates)
                            print(result)
        except Exception as e:
            print("There is problem with your dimensions")
            print(e)
            logging.info("There is a problem with your dimensions")
            logging.info(e)

        return nplates

    def findQuotesFromCSV(self, csvfile):
        try:
            with open(csvfile, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, dialect="excel-tab")
                extmaterials = []
                for row in reader:
                    try:
                        orderNum = row[0]
                        itemCode = row[1]
                        quantity = float(row[2])
                        unit = row[3]
                        material = Material()
                        material.setItemCode(itemCode)
                        extendedMaterial = ExtMaterials(material)
                        extendedMaterial.setOrderNumber(orderNum)
                        extendedMaterial.setUnit(unit)
                        extendedMaterial.setQuantity(quantity)
                        extmaterials.append(extendedMaterial)

                    except ValueError:
                        logging.info('There is a wrong data format entry. Please check')
                        continue

                self.rfq.setMaterialList(extmaterials)

            rfq_json = self.rfq.__dict__
            rfq_json['materialList'] = self.rfq.to_json()

            return rfq_json['materialList']

        except IOError as error:
            logging.info(error)

    def editRFQwithMaterials(self, form, material_formset, material_data):
        try:
            internalCode = form.cleaned_data['internalCode']
            externalCode = form.cleaned_data['externalCode']
            sender = form.cleaned_data['sender']
            company = form.cleaned_data['company']
            receivedDate = form.cleaned_data['receivedDate']
            note = form.cleaned_data['note']

            rfq = RequestForQuotes()
            rfq.setIntenalCode(internalCode)
            rfq.setExternalCode(externalCode)
            rfq.setSender(sender)
            rfq.setCompany(company)
            rfq.setReceivedDate(receivedDate)
            rfq.setNote(note)

            extmaterials = []

            try:
                idx = 0
                for material in material_formset:

                    itemcode_data = material_data[idx]['itemcode']
                    description_data = material_data[idx]['description']
                    type_data = material_data[idx]['type']
                    dimensions_data = material_data[idx]['dimensions']
                    category_data = material_data[idx]['category']

                    order_number_data = material_data[idx]['orderNumber']

                    temp_material = Material()
                    temp_material.setItemCode(itemcode_data)
                    temp_material.setDescription(description_data)
                    temp_material.setType(type_data)
                    temp_material.setDimensions(dimensions_data)
                    temp_material.setCategory(category_data)

                    mod_material = ExtMaterials(temp_material)
                    mod_material.setOrderNumber(order_number_data)
                    mod_material.setQuantity(material.cleaned_data['quantity'])
                    mod_material.setUnit(material.cleaned_data['unit'])
                    extmaterials.append(mod_material)
                    idx = idx + 1

            except Exception as ex:
                logging.info(ex)

            rfq.setMaterialList(extmaterials)

            rfq_json = rfq.__dict__
            rfq_json['materialList'] = rfq.to_json()

            self.rfq_list.append(rfq_json)

            return self.rfq_list

        except IOError as error:
            logging.info(error)
            return self.rfq_list

    def runBasicAnalysis(self, rfq):

        labels = []
        labels.append('Id')
        labels.append('OrderId')
        labels.append('ItemId')
        labels.append('Description')
        labels.append('Type')
        labels.append('Quantity')
        labels.append('Unit')
        labels.append('# Plates')
        labels.append('History')
        labels.append('Unit price')
        labels.append('Project')
        labels.append('Date')

        internal_code = str(rfq["internalCode"])
        csvfile = 'RFQ-WAnalysis-' + internal_code + '_Conpancol.csv'
        path = "media/export/" + csvfile

        try:

            with open(path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, dialect="excel", delimiter=';')
                header = 'RFQ internal code: ' + str(rfq["internalCode"])
                writer.writerow([header])
                details = 'Received date: ' + str(rfq["receivedDate"])
                writer.writerow([details])
                note = 'Note: ' + str(rfq["note"])

                writer.writerow([note])
                writer.writerow([''])
                writer.writerow(labels)

                items = rfq["materialList"]

                tools = RFQTools()
                item_history = tools.RFQMatcherContext(rfq["internalCode"])
                # print(item_history)
                provider_prices = tools.QuotedMaterialMatcher(rfq["internalCode"], 'MP10001')
                print(provider_prices)

                id = 1

                for item in items:
                    row = []
                    row.append(str(id))
                    row.append(item["orderNumber"])
                    row.append(item["itemcode"])
                    description = item["description"]
                    row.append(description)
                    row.append(item["type"])
                    row.append(str(item["quantity"]))
                    row.append(str(item["unit"]))

                    if item["category"] == "PLATE":
                        nplates = self.getNumberPlates(item["dimensions"], item["quantity"])
                        row.append(str(nplates))
                    else:
                        row.append("-")

                    if len(item_history) != 0:
                        row.append(item_history[item["itemcode"]])
                    else:
                        row.append("-")

                    if(len(provider_prices)) != 0:
                        row.append(provider_prices[item["itemcode"]][0])
                        row.append(provider_prices[item["itemcode"]][1])
                        row.append(provider_prices[item["itemcode"]][2])
                    else:
                        row.append('-')
                        row.append('-')
                        row.append('-')

                    writer.writerow(row)
                    id += 1

            f.close()
            return path

        except IOError:
            logging.info('Problem with file creation')
            return path

        except Exception as e:
            logging.info('General exception' + str(e))
            return path
