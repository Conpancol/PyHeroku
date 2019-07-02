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


class QuotedMaterialsForm(forms.ModelForm):
    class Meta:
        model = QuotedMaterials
        labels = view_texts.getComponent()['materials_upload']['labels']
        fields = ('providerId',
                  'providerName',
                  'revision',
                  'document')


class SelectorForm(forms.Form):
    labels = view_texts.getComponent()['selector']['labels']
    code = forms.CharField(max_length=255,
                           label=labels['internalCode'])
    action = forms.ChoiceField(choices=ACTION_CHOICES,
                               label=labels['action'],
                               initial='',
                               widget=forms.Select(),
                               required=True)
