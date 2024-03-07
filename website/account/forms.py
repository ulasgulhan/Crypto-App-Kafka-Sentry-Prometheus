from django import forms


class APIForm(forms.Form):
    access_key = forms.CharField(label='access_key', max_length=200, required=True)
    access_passphrase = forms.CharField(label='access_passphrase', max_length=200, required=True, widget=forms.PasswordInput)
    secret_key = forms.CharField(label='secret_key', max_length=200, required=True, widget=forms.PasswordInput)
