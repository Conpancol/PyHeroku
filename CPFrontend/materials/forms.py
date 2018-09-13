from django import forms
from .choices import *


class xcheckForm(forms.Form):
    itemcode = forms.CharField(max_length=30)


class SelectorForm(forms.Form):
    code = forms.CharField(max_length=255)
    action = forms.ChoiceField(choices=ACTION_CHOICES,
                               label="Action",
                               initial='',
                               widget=forms.Select(),
                               required=True)


class MaterialForm(forms.Form):
    itemcode = forms.CharField(max_length=255)
    description = forms.CharField(max_length=500)
    type = forms.CharField(max_length=255)
    category = forms.CharField(max_length=255)
    dimensions = forms.CharField(max_length=255)

