from django import forms
from .models import RFQ
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


class RFQInternalCode(forms.Form):
    internalcode = forms.CharField(max_length=50)
    incoterms = forms.ChoiceField(choices=INCOTERMS_CHOICES, label="Incoterms", initial='', widget=forms.Select(),
                                  required=True)
    port = forms.CharField(max_length=50)
