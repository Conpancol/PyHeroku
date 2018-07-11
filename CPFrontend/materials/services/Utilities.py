import re

types = ['CS',
         'SS',
         'ALLOY',
         'PPL',
         'TITANIUM',
         'HASTELLOY',
         'STEEL',
         'ALUMINUM',
         'COPPER',
         'BRONZE',
         'IRON',
         'GS',
         'BURNING BARS',
         'SX',
         'COAL']

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
