from django.db import models
from django.contrib.auth.models import User
import base64

# Create your models here.

METHODS_CHOICES = [
    ('GET', 'GET'),
    ('POST', 'POST')
]


class CryptoMarkets(models.Model):
    name            = models.CharField(max_length=200)
    slug            = models.CharField(max_length=200)


class APIEndpoints(models.Model):
    api_site_name   = models.CharField(max_length=200)
    endpoint_name   = models.CharField(max_length=200)
    endpoint_url    = models.CharField(max_length=200)
    endpoint_params = models.CharField(max_length=200, blank=True, null=True)
    auth_required   = models.BooleanField()
    method          = models.CharField(max_length=200, choices=METHODS_CHOICES)
    crypto_market = models.ForeignKey(CryptoMarkets, on_delete=models.CASCADE)


class CryptoMarketAPICredentials(models.Model):
    api_key     = models.CharField(max_length=200)
    secret_key  = models.CharField(max_length=200)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    access_passphrase = models.CharField(max_length=200, default=None)
    crypto_market = models.ForeignKey(CryptoMarkets, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def encode(self, value):
        return base64.b64encode(value.encode()).decode()

    def save(self, *args, **kwargs):
        if not self.id:
            self.api_key = self.encode(self.api_key)
            self.secret_key = self.encode(self.secret_key)
            if self.access_passphrase:
                self.access_passphrase = self.encode(self.access_passphrase)
        super().save(*args, **kwargs)


""" 
class BaseAPI(models.Model):
    api_key     = models.CharField(max_length=200)
    secret_key  = models.CharField(max_length=200)

    class Meta:
        abstract = True
    

    def encode(self, value):
        return base64.b64encode(value.encode()).decode()

    def save(self, *args, **kwargs):
        if not self.id:
            self.api_key = self.encode(self.api_key)
            self.secret_key = self.encode(self.secret_key)
        super().save(*args, **kwargs)



class BitGetAPI(BaseAPI):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bitget_api')
    access_passphrase = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.id:
            self.access_passphrase = self.encode(self.access_passphrase)
        super().save(*args, **kwargs)


class BybitAPI(BaseAPI):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bybit_api')


class OkxAPI(BaseAPI):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='okx_api')
    access_passphrase = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.id:
            self.access_passphrase = self.encode(self.access_passphrase)
        super().save(*args, **kwargs)


    


 """