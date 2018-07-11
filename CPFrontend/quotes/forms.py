from django import forms
from .models import Quote


class QuotesForm(forms.ModelForm):
    class Meta:
        model = Quote
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
                  'document')
