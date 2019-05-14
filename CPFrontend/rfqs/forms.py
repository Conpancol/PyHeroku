from django import forms
from .models import RFQ
from .choices import *
from common.FrontendTexts import FrontendTexts

view_texts = FrontendTexts('rfqs')


class RFQForm(forms.ModelForm):
    class Meta:
        model = RFQ
        labels = view_texts.getComponent()['simple_upload']['labels']
        fields = ('internalCode',
                  'externalCode',
                  'sender',
                  'company',
                  'receivedDate',
                  'note',
                  'document')


class RFQFormOnlyinfo(forms.ModelForm):
    class Meta:
        model = RFQ
        labels = view_texts.getComponent()['simple_upload']['labels']
        fields = ('internalCode',
                  'externalCode',
                  'sender',
                  'company',
                  'receivedDate',
                  'note')


class ExtMaterialForm(forms.Form):
    orderNumber = forms.CharField(max_length=255)
    itemcode = forms.CharField(max_length=255)
    quantity = forms.FloatField()
    unit = forms.CharField(max_length=255)


class RFQInternalCode(forms.Form):
    labels = view_texts.getComponent()['simple_upload']['labels']
    internalcode = forms.CharField(max_length=50)
    incoterms = forms.ChoiceField(choices=INCOTERMS_CHOICES,
                                  label="Incoterms",
                                  initial='',
                                  widget=forms.Select(),
                                  required=True)
    port = forms.CharField(max_length=50)


class SelectorForm(forms.Form):
    labels = view_texts.getComponent()['selector']['labels']
    code = forms.CharField(max_length=255,
                           label=labels['internalCode'])
    action = forms.ChoiceField(choices=ACTION_CHOICES,
                               label=labels['action'],
                               initial='',
                               widget=forms.Select(),
                               required=True)
