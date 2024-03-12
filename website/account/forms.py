from django import forms
from .models import BitGetAPI, BybitAPI


class BitGetAPIForm(forms.ModelForm):
    access_key = forms.CharField(label='access_key', max_length=200, required=True)
    access_passphrase = forms.CharField(label='access_passphrase', max_length=200, required=True, widget=forms.PasswordInput)
    secret_key = forms.CharField(label='secret_key', max_length=200, required=True, widget=forms.PasswordInput)

    class Meta:
        model = BitGetAPI
        fields = ['access_key', 'access_passphrase', 'secret_key']


class ByBitAPIForm(forms.ModelForm):
    access_key = forms.CharField(label='access_key', max_length=200, required=True)
    secret_key = forms.CharField(label='secret_key', max_length=200, required=True, widget=forms.PasswordInput)

    class Meta:
        model = BybitAPI
        fields = ['access_key', 'secret_key']
