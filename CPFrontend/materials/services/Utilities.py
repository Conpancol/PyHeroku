import re
import csv


types = ['CS',
         'SS',
         'ALLOY',
         'PPL',
         'TITANIUM',
         'HASTELLOY',
         'CORTEN',
         'ALUMINUM',
         'COPPER',
         'BRONZE',
         'IRON',
         'GS',
         'BURNING BARS',
         'SX',
         'COAL',
         'BRICK',
         'CEMENT',
         'MORTAR',
         'AL203',
         'STEEL']

dimdesc = ['MM', '\"', '/', 'SCH']


def find_type(description):
    for tp in types:
        if any(tp in s for s in description):
            return tp
    return 'NA'


def find_dimensions(description):
    dimensions = []
    for lm in description:
        if re.search('\d', lm):
            for dm in dimdesc:
                if any( dm in lm for dm in dimdesc):
                    dimensions.append(lm)
                    break
    if len(dimensions) > 0:
        return ','.join(dimensions).strip()
    else:
        return 'NA'


def fileFilter(csvfile):
    try:
        with open(csvfile, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, dialect="excel-tab")
            for row in reader:
                print(row)

    except UnicodeDecodeError as exception:
        print(exception)
        input_file = open(csvfile, "rb")
        s = input_file.read()
        input_file.close()
        s = s.replace(b'\xb0', bytes(b'\xc2\xb0'))
        output_file = open(csvfile, "wb")
        output_file.write(s)
        output_file.close()
        print('input file corrected')
