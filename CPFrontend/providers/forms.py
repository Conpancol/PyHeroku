from django import forms
from .choices import *
from common.FrontendTexts import FrontendTexts

view_texts = FrontendTexts('providers')


class ProviderForm(forms.Form):
    labels = view_texts.getComponent()['creator']['labels']
    name = forms.CharField(max_length=255, label=labels['name'])
    category = forms.ChoiceField(choices=CATEGORY_CHOICES,
                                 label=labels['category'],
                                 initial='',
                                 widget=forms.Select(),
                                 required=True)
    specialty = forms.CharField(max_length=255, label=labels['specialty'])
    webpage = forms.CharField(max_length=255, label=labels['webpage'])
    contactNames = forms.CharField(max_length=255, label=labels['contactNames'])
    emailAddresses = forms.EmailField(label=labels['emailAddresses'])
    address = forms.CharField(max_length=255, label=labels['address'])
    country = forms.CharField(max_length=255, label=labels['country'])
    city = forms.CharField(max_length=255, label=labels['city'])
    phone = forms.CharField(max_length=255, label=labels['phone'])
    taxId = forms.CharField(max_length=255, label=labels['taxId'])
    coordinates = forms.CharField(max_length=255, label=labels['coordinates'])


class ProviderFinderForm(forms.Form):
    labels = view_texts.getComponent()['finder']['labels']
    code = forms.CharField(max_length=255)


class SelectorForm(forms.Form):
    labels = view_texts.getComponent()['selector']['labels']
    code = forms.CharField(max_length=255, label=labels['code'])
    action = forms.ChoiceField(choices=ACTION_CHOICES,
                               label=labels['action'],
                               initial='',
                               widget=forms.Select(),
                               required=True)


class CommentForm(forms.Form):
    labels = view_texts.getComponent()['comment']['labels']
    date = forms.CharField(max_length=255, label=labels['date'])
    issuer = forms.CharField(max_length=255, label=labels['issuer'])
    text = forms.CharField(max_length=500, label=labels['text'])

