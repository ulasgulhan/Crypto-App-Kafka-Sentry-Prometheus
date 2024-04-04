from django import forms
from .models import CryptoMarketAPICredentials


class PassphraseForm(forms.ModelForm):
    access_key = forms.CharField(label='access_key', max_length=200, required=True)
    access_passphrase = forms.CharField(label='access_passphrase', max_length=200, required=True, widget=forms.PasswordInput)
    secret_key = forms.CharField(label='secret_key', max_length=200, required=True, widget=forms.PasswordInput)

    class Meta:
        model = CryptoMarketAPICredentials
        fields = ['access_key', 'access_passphrase', 'secret_key']


class NonePassphraseForm(forms.ModelForm):
    access_key = forms.CharField(label='access_key', max_length=200, required=True)
    secret_key = forms.CharField(label='secret_key', max_length=200, required=True, widget=forms.PasswordInput)

    class Meta:
        model = CryptoMarketAPICredentials
        fields = ['access_key', 'secret_key']


class FuturesForm(forms.Form):

    FUTURE_CHOICES = [
    ('Buy', 'Buy'),
    ('Sell', 'Sell')
    ]
    size = forms.FloatField(label='size', required=True)
    price = forms.FloatField(label='price', required=True)
    side = forms.ChoiceField(label='side', choices=FUTURE_CHOICES, required=True)

