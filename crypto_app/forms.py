from django import forms

# creating a form
class AddCrypto(forms.Form):
    name = forms.CharField(max_length = 200)
    symbol = forms.CharField(max_length = 200)
