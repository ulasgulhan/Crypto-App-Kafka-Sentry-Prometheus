from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class APIEndpoints(models.Model):
    api_site_name   = models.CharField(max_length=200)
    endpoint_name   = models.CharField(max_length=200)
    endpoint_url    = models.CharField(max_length=200)
    endpoint_params = models.CharField(max_length=200, blank=True, null=True)
    auth_required   = models.BooleanField()
    method          = models.CharField(max_length=200)


class BaseAPI(models.Model):
    api_key     = models.CharField(max_length=200)
    secret_key  = models.CharField(max_length=200)

    class Meta:
        abstract = True
    


class BitGetAPI(BaseAPI):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bitget_api')
    access_passphrase = models.CharField(max_length=200)


class BybitAPI(BaseAPI):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bybit_api')


class OkxAPI(BaseAPI):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='okx_api')
    


