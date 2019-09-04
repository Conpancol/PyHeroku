import csv


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
        print(s)
        input_file.close()
        s = s.replace(b'\xb0', bytes(b'\xc2\xb0'))
        s = s.replace(b'\xd1', bytes(b'\xc3\x91'))
        s = s.replace(b'\xba', bytes(b'\xc2\xb0'))
        output_file = open(csvfile, "wb")
        output_file.write(s)
        output_file.close()
        print('input file corrected')

