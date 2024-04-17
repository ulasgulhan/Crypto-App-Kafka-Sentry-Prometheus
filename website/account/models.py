from django.db import models
from django.contrib.auth.models import User
import base64

# Create your models here.

METHODS_CHOICES = [
    ('GET', 'GET'),
    ('POST', 'POST')
]


FUTURE_CHOICES = [
    ('Buy', 'Buy'),
    ('Sell', 'Sell')
]


class CryptoMarkets(models.Model):
    name            = models.CharField(max_length=200)
    slug            = models.SlugField(max_length=200, unique=True)
    is_active       = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Crypto Market'
        verbose_name_plural = 'Crypto Markets'

    def __str__(self) -> str:
        return self.name


class APIEndpoints(models.Model):
    endpoint_name   = models.CharField(max_length=200)
    endpoint_url    = models.CharField(max_length=200)
    endpoint_params = models.CharField(max_length=200, blank=True, null=True)
    auth_required   = models.BooleanField()
    method          = models.CharField(max_length=200, choices=METHODS_CHOICES)
    crypto_market   = models.ForeignKey(CryptoMarkets, on_delete=models.CASCADE)
    is_active       = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'API Endpoint'
        verbose_name_plural = 'API Endpoints'


class CryptoMarketAPICredentials(models.Model):
    api_key             = models.CharField(max_length=200)
    secret_key          = models.CharField(max_length=200)
    access_passphrase   = models.CharField(max_length=200, default=None, blank=True, null=True)
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_market       = models.ForeignKey(CryptoMarkets, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Crypto Market API Credantial'
        verbose_name_plural = 'Crypto Market API Credantials'

    def encode(self, value):
        return base64.b64encode(value.encode()).decode()

    def save(self, *args, **kwargs):
        if not self.id:
            self.api_key = self.encode(self.api_key)
            self.secret_key = self.encode(self.secret_key)
            if self.access_passphrase:
                self.access_passphrase = self.encode(self.access_passphrase)
        super().save(*args, **kwargs)


class Membership(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships', verbose_name="User")
    subscriber  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers', verbose_name="Subscribed User")


    class Meta:
        verbose_name = "Membership"
        verbose_name_plural = "Memberships"
    
    def __str__(self) -> str:
        return self.user



