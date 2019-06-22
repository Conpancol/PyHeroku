import csv
import json
import logging
import os

from pymongo import MongoClient


class RFQTools:
    def __init__(self):
        dburl = os.getenv('ATLAS_URL')
        if dburl is None:
            try:
                with open('./resources/config/dbconfig.json', 'r') as f:
                    config = json.load(f)
                    dburl = config['DEV']['DBURL']
                    dport = int(config['DEV']['DBPORT'])
                    self.client = MongoClient(dburl, dport)
            except FileNotFoundError:
                logging.info("RFQTools> Using default connection values")
                print("RFQTools> Using default connection values")
                dburl = 'localhost'
                dport = 27017
                self.client = MongoClient(dburl, dport)
        else:
            self.client = MongoClient(dburl)

        self.db = self.client.conpancol
        self.collection = self.db.rfquotes
        self.quoted_materials = self.db.qmaterials

        logging.basicConfig(filename='./logs/material_finder.log',
                            level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d-%y %H:%M')

        self.categories = {}
        self.types = {}

    def RFQMatcherContext(self, current_rfq):
        try:

            itemcodes = {}

            stages = [{'$match': {'internalCode': current_rfq}},
                      {'$project': {'_id': 0, 'materialList.itemcode': 1}}]

            items = self.collection.aggregate(stages).next()['materialList']

            for item in items:
                code = item['itemcode']
                itemcodes[code] = ''

            cursor = self.collection.find({})

            for rfq in cursor:
                internalCode = rfq['internalCode']
                materialList = rfq['materialList']

                if internalCode == current_rfq:
                    continue

                for item in materialList:
                    code = item['itemcode']
                    for key, value in itemcodes.items():
                        if key == code:
                            if itemcodes[key].find(str(internalCode)) < 0:
                                itemcodes[key] = value + str(internalCode) + ' '

            for key, value in itemcodes.items():
                row = str(key) + '\t' + value
                logging.debug(row)

            return itemcodes

        except StopIteration as error:
            logging.info("RFQMatcherContext> Cursor return no elements - RFQ not found " + error)
            return {}

        except Exception as error:
            logging.info("RFQMatcherContext> General exception found " + error)
            return {}

    def QuotedMaterialMatcher(self, current_rfq, providerId):
        try:

            itemcodes = {}

            stages = [{'$match': {'internalCode': current_rfq}},
                      {'$project': {'_id': 0, 'materialList.itemcode': 1}}]

            items = self.collection.aggregate(stages).next()['materialList']

            for item in items:
                code = item['itemcode']

                stages = [{'$match': {'providerId': providerId, 'itemcode': code, 'revision': 1}},
                          {'$project': {'_id': 0, 'unitPrice': 1, 'projectId': 1}}]

                try:
                    data = self.quoted_materials.aggregate(stages).next()
                    itemcodes[code] = [data['unitPrice'], data['projectId']]
                except StopIteration as nodata:
                    itemcodes[code] = ['-', '-']
                    print(code + ' ' + str(nodata.value))
                    continue

            return itemcodes

        except StopIteration as error:
            logging.info("QuotedMaterialMatcher> Cursor return no elements - RFQ not found " + error)
            return {}

        except Exception as error:
            logging.info("QuotedMaterialMatcher> General exception found " + error)
            return {}
