from django import forms
from .choices import *


class ProviderForm(forms.Form):
    name = forms.CharField(max_length=255)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES,
                                 label="Categories",
                                 initial='',
                                 widget=forms.Select(),
                                 required=True)
    specialty = forms.CharField(max_length=255)
    webpage = forms.CharField(max_length=255)
    contactNames = forms.CharField(max_length=255)
    emailAddresses = forms.EmailField()
    address = forms.CharField(max_length=255)
    country = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=255)
    taxId = forms.CharField(max_length=255)
    coordinates = forms.CharField(max_length=255)


class ProviderFinderForm(forms.Form):
    code = forms.CharField(max_length=255)


class SelectorForm(forms.Form):
    code = forms.CharField(max_length=255)
    action = forms.ChoiceField(choices=ACTION_CHOICES,
                               label="Action",
                               initial='',
                               widget=forms.Select(),
                               required=True)


class CommentForm(forms.Form):
    date = forms.CharField(max_length=255)
    issuer = forms.CharField(max_length=255)
    text = forms.CharField(max_length=500)

