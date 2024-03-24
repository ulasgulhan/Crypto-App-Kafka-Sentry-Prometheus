from django.contrib import admin
from .models import APIEndpoints, CryptoMarketAPICredentials, CryptoMarkets

# Register your models here.



class APIEndpointsAdmin(admin.ModelAdmin):
    list_display    = ('endpoint_name', 'method')


class CryptoMarketAPICredentialsAdmin(admin.ModelAdmin):
    list_display    = ('user', 'crypto_market')


class CryptoMarketsAdmin(admin.ModelAdmin):
    list_display    = ('name',)



admin.site.register(APIEndpoints, APIEndpointsAdmin)
admin.site.register(CryptoMarketAPICredentials, CryptoMarketAPICredentialsAdmin)
admin.site.register(CryptoMarkets, CryptoMarketsAdmin)

