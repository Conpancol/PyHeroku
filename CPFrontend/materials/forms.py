from django import forms
from .choices import *
from common.FrontendTexts import FrontendTexts

view_texts = FrontendTexts('materials')


class xcheckForm(forms.Form):
    labels = view_texts.getComponent()['singlexcheck']['labels']
    itemcode = forms.CharField(max_length=30,
                               label=labels['code'])


class SelectorForm(forms.Form):
    labels = view_texts.getComponent()['selector']['labels']
    code = forms.CharField(max_length=255,
                           label=labels['code'])
    action = forms.ChoiceField(choices=ACTION_CHOICES,
                               label=labels['action'],
                               initial='',
                               widget=forms.Select(),
                               required=True)


class MaterialForm(forms.Form):
    labels = view_texts.getComponent()['editor']['labels']
    itemcode = forms.CharField(max_length=255, label=labels['itemcode'])
    description = forms.CharField(max_length=500, label=labels['description'])
    type = forms.CharField(max_length=255, label=labels['type'])
    category = forms.CharField(max_length=255, label=labels['category'])
    dimensions = forms.CharField(max_length=255, label=labels['dimensions'])


class WeightCalculatorForm(forms.Form):
    labels = view_texts.getComponent()['weightcalc']['labels']
    value = forms.FloatField(label=labels['value'])
    units = forms.ChoiceField(choices=UNIT_CHOICES,
                              label=labels['units'],
                              initial='',
                              widget=forms.Select(),
                              required=True)
