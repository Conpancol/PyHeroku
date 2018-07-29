from django import forms


class xcheckForm(forms.Form):
    itemcode = forms.CharField(max_length=30)
