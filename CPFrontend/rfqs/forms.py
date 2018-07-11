from django import forms
from .models import RFQ


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
