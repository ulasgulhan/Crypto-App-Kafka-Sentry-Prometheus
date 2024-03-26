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
    slug            = models.SlugField(max_length=200, unique=True)
    is_active       = models.BooleanField(default=True)


class APIEndpoints(models.Model):
    endpoint_name   = models.CharField(max_length=200)
    endpoint_url    = models.CharField(max_length=200)
    endpoint_params = models.CharField(max_length=200, blank=True, null=True)
    auth_required   = models.BooleanField()
    method          = models.CharField(max_length=200, choices=METHODS_CHOICES)
    crypto_market   = models.ForeignKey(CryptoMarkets, on_delete=models.CASCADE)
    is_active       = models.BooleanField(default=True)


class CryptoMarketAPICredentials(models.Model):
    api_key             = models.CharField(max_length=200)
    secret_key          = models.CharField(max_length=200)
    access_passphrase   = models.CharField(max_length=200, default=None, blank=True, null=True)
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_market       = models.ForeignKey(CryptoMarkets, on_delete=models.CASCADE)

    def encode(self, value):
        return base64.b64encode(value.encode()).decode()

    def save(self, *args, **kwargs):
        if not self.id:
            self.api_key = self.encode(self.api_key)
            self.secret_key = self.encode(self.secret_key)
            if self.access_passphrase:
                self.access_passphrase = self.encode(self.access_passphrase)
        super().save(*args, **kwargs)

