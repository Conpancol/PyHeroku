from django import forms
from .models import RFQ
from .models import RFQMaterial
from .choices import *


class RFQForm(forms.ModelForm):
    class Meta:
        model = RFQ
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
        fields = ('internalCode',
                  'externalCode',
                  'sender',
                  'company',
                  'receivedDate',
                  'note')


class RFQMaterialForm(forms.ModelForm):
    class Meta:
        model = RFQMaterial
        fields = ('orderNumber',
                  'itemCode',
                  'quantity',
                  'unit')


class RFQInternalCode(forms.Form):
    internalcode = forms.CharField(max_length=50)
    incoterms = forms.ChoiceField(choices=INCOTERMS_CHOICES, label="Incoterms", initial='', widget=forms.Select(),
                                  required=True)
    port = forms.CharField(max_length=50)


class SelectorForm(forms.Form):
    code = forms.CharField(max_length=255, label="Internal code")
    action = forms.ChoiceField(choices=ACTION_CHOICES,
                               label="Action",
                               initial='',
                               widget=forms.Select(),
                               required=True)
