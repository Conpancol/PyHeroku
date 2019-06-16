from django import forms
from .models import Quote
from .models import QuotedMaterials
from common.FrontendTexts import FrontendTexts

view_texts = FrontendTexts('quotes')


class QuotesForm(forms.ModelForm):
    class Meta:
        model = Quote
        labels = view_texts.getComponent()['materials_upload']['labels']
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


class QuotedMaterialsForm(forms.ModelForm):
    class Meta:
        model = QuotedMaterials
        labels = view_texts.getComponent()['materials_upload']['labels']
        fields = ('providerId',
                  'providerName',
                  'revision',
                  'document')
