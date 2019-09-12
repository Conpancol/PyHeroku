from django import forms
from .models import Quote
from .models import QuotedMaterials
from .choices import *
from common.FrontendTexts import FrontendTexts

view_texts = FrontendTexts('quotes')


class QuotesForm(forms.ModelForm):
    class Meta:
        model = Quote
        labels = view_texts.getComponent()['simple_upload']['labels']
        fields = ('internalCode',
                  'externalCode',
                  'providerCode',
                  'receivedDate',
                  'sentDate',
                  'user',
                  'providerId',
                  'providerName',
                  'contactName',
                  'incoterms',
                  'note',
                  'edt',
                  'document')


class QuotesFormOnlyinfo(forms.ModelForm):
    class Meta:
        model = Quote
        labels = view_texts.getComponent()['simple_upload']['labels']
        fields = ('internalCode',
                  'externalCode',
                  'providerCode',
                  'receivedDate',
                  'sentDate',
                  'user',
                  'providerId',
                  'providerName',
                  'contactName',
                  'incoterms',
                  'note',
                  'edt')


class QuotedMaterialForm(forms.Form):
    orderNumber = forms.CharField(max_length=255)
    itemcode = forms.CharField(max_length=255)
    quantity = forms.FloatField()
    unit = forms.CharField(max_length=255)
    unitPrice = forms.FloatField()
    totalPrice = forms.FloatField()
    revision = forms.IntegerField()


class QuotedMaterialsForm(forms.ModelForm):
    class Meta:
        model = QuotedMaterials
        labels = view_texts.getComponent()['materials_upload']['labels']
        fields = ('providerId',
                  'providerName',
                  'revision')


class SelectorForm(forms.Form):
    labels = view_texts.getComponent()['selector']['labels']
    code = forms.CharField(max_length=255,
                           label=labels['internalCode'])
    action = forms.ChoiceField(choices=ACTION_CHOICES,
                               label=labels['action'],
                               initial='',
                               widget=forms.Select(),
                               required=True)


class SmartQuotesForm(forms.Form):

    def __init__(self, data, *args, **kwargs):
        super(SmartQuotesForm, self).__init__(*args, **kwargs)

        self.labels = view_texts.getComponent()['simple_upload']['labels']

        self.fields['internalCode'] = forms.IntegerField(label=self.labels['internalCode'])
        self.fields['externalCode'] = forms.IntegerField(label=self.labels['externalCode'])
        self.fields['providerCode'] = forms.CharField(max_length=255, label=self.labels['providerCode'])
        self.fields['receivedDate'] = forms.CharField(max_length=255, label=self.labels['receivedDate'])
        self.fields['sentDate'] = forms.CharField(max_length=255, label=self.labels['sentDate'])

        self.provider_info = []
        counter = 1
        for provider in data:
            choice = (counter, provider['providerId'] + " | " + provider['name'])
            self.provider_info.append(choice)
            counter += 1

        self.fields['providerId'] = forms.ChoiceField(label=self.labels['providerId'],
                                                      choices=self.provider_info)

        self.fields['user'] = forms.CharField(max_length=255, label=self.labels['user'])
        self.fields['contactName'] = forms.CharField(max_length=255, label=self.labels['contactName'])
        self.fields['incoterms'] = forms.CharField(max_length=255, label=self.labels['incoterms'])
        self.fields['note'] = forms.CharField(max_length=255, label=self.labels['note'])
        self.fields['edt'] = forms.CharField(max_length=255, label=self.labels['edt'])
        self.fields['document'] = forms.FileField(label=self.labels['document'])

    def getProviderInfo(self):
        return self.provider_info

