from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BaseAPI(models.Model):
    api_key     = models.CharField(max_length=200)
    secret_key  = models.CharField(max_length=200)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.user_id


class BitGetAPI(BaseAPI):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bitget_api')
    access_passphrase = models.CharField(max_length=200)


class BybitAPI(BaseAPI):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bybit_api')


