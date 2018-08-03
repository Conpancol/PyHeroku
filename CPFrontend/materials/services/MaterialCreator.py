import logging

from .Utilities import *

from common.Materials import Material


class MaterialCreator:

    def __init__(self):
        """clase que crea MATERIALS en el formator necesario para guardar en la DB"""
        self.material_list = []
        logging.basicConfig(filename='logs/mtcreator.log',
                            level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d-%y %H:%M')

    def createMaterialfromCSV(self, csvfile):
        try:
            fileFilter(csvfile)
            with open(csvfile, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, dialect="excel-tab")
                filename = csvfile.split('/')[-1]
                logging.info('Opened file: ' + filename)
                for row in reader:
                    if row[0] == '':
                        continue
                    item = row[1]
                    dsc = row[2].rstrip().split(',')
                    cat = dsc[0]
                    material = Material()
                    material.setItemCode(item)
                    material.setDescription(','.join(dsc))
                    material.setCategory(cat)
                    result = find_type(dsc)
                    material.setType(result)

                    if result == 'NA':
                        logging.info('No type for  \t' + str(material))
                    result = find_dimensions(dsc)
                    material.setDimensions(result)

                    obj_id = material.__dict__
                    self.material_list.append(obj_id)

                    if result == 'NA':
                        logging.info('No dimensions for  \t' + str(material))

            return self.material_list

        except IOError as error:
            print(error)
            return self.material_list

    def createMaterial(self, csvfile):
        try:
            with open(csvfile, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, dialect="excel-tab")
                filename = csvfile.split('/')[ -1 ]
                logging.info('Opened file: ' + filename)
                for row in reader:
                    item = row[0]
                    material = Material()
                    material.setItemCode(item)

                    obj_id = material.__dict__
                    self.material_list.append(obj_id)

            return self.material_list

        except IOError as error:
            print(error)
            return self.material_list

