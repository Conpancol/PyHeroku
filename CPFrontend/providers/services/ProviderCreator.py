import logging
import csv

from common.Providers import Providers
from common.Comments import Comments
from ..choices import *


class ProviderCreator:

    def __init__(self):
        """clase que crea PROVIDERS en el formator necesario para guardar en la DB"""
        self.provider_list = []
        logging.basicConfig(filename='logs/mtcreator.log',
                            level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d-%y %H:%M')

    def createProvidersfromCSV(self, csvfile):
        try:
            with open(csvfile, 'r', encoding='ISO-8859-1', newline='') as f:
                reader = csv.reader(f, dialect="excel-tab")
                filename = csvfile.split('/')[-1]
                logging.info('Opened file: ' + filename)
                for row in reader:
                    if row[0] == '':
                        continue
                    name = row[0]
                    category = row[1]
                    country = row[2]
                    city = row[3]
                    address = row[4]
                    phone = row[5]
                    providerWeb = row[6]
                    emailAddresses = row[7]
                    contactNames = row[8]
                    specialty = row[9]
                    taxid = row[10]
                    bank = row[11]
                    iban = row[12]
                    comments = [].append(row[13])
                    hasDataProtection = False
                    if row[14] == "True" or row[14] == "true":
                        hasDataProtection = True
                    procurementCodes = [].append(row[15])

                    provider = Providers()
                    provider.setProviderId('NA')
                    provider.setName(name)
                    provider.setCategory(category)
                    provider.setCountry(country)
                    provider.setCountryCode('NA')
                    provider.setCity(city)
                    provider.setCoordinates('0.000, 0.000')
                    provider.setWebpage(providerWeb)
                    provider.setAddress(address)
                    provider.setPhone(phone)
                    provider.setEmailAddresses(emailAddresses)
                    provider.setContactNames(contactNames)
                    provider.setSpecialty(specialty)
                    provider.setTaxId(taxid)
                    provider.setComments(comments)
                    provider.setHasDataProtection(hasDataProtection)
                    provider.setBank(bank)
                    provider.setIban(iban)
                    provider.setProcurementCodes(procurementCodes)

                    obj_id = provider.__dict__
                    self.provider_list.append(obj_id)

            return self.provider_list

        except IOError as error:
            print(error)
            return self.provider_list

    def createProvider(self, form):
        try:
            name = form.cleaned_data['name']
            category = CATEGORY_CHOICES[int(form.cleaned_data['category'])-1][1]
            specialty = form.cleaned_data['specialty']
            webpage = form.cleaned_data['webpage']
            contacts = form.cleaned_data['contactNames']
            emails = form.cleaned_data['emailAddresses']
            address = form.cleaned_data['address']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            phone = form.cleaned_data['phone']
            taxid = form.cleaned_data['taxId']
            coordinates = form.cleaned_data['coordinates']

            provider = Providers()
            provider.setProviderId('NA')
            provider.setName(name)
            provider.setCategory(category)
            provider.setCountry(country)
            provider.setCountryCode('NA')
            provider.setCity(city)
            provider.setCoordinates(coordinates)
            provider.setWebpage(webpage)
            provider.setAddress(address)
            provider.setPhone(phone)
            provider.setEmailAddresses(emails)
            provider.setContactNames(contacts)
            provider.setSpecialty(specialty)
            provider.setTaxId(taxid)

            obj_id = provider.__dict__
            self.provider_list.append(obj_id)

            return self.provider_list

        except Exception as error:
            print(error)
            return self.provider_list

    def createComment(self, form):
        try:
            date = form.cleaned_data['date']
            issuer = form.cleaned_data['issuer']
            text = form.cleaned_data['text']

            comment = Comments()
            comment.setDate(date)
            comment.setIssuer(issuer)
            comment.setText(text)

            obj_id = comment.__dict__

            return obj_id

        except Exception as error:
            print(error)
            return {}
