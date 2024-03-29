from django import forms
from django.contrib import admin
from .models import APIEndpoints, CryptoMarketAPICredentials, CryptoMarkets


# Register your models here.



class APIEndpointsAdmin(admin.ModelAdmin):
    list_display    = ('endpoint_name', 'method', 'auth_required', 'crypto_market', 'is_active')
    list_editable   = ('is_active',)


class CryptoMarketAPICredentialsAdmin(admin.ModelAdmin):
    list_display    = ('user', 'crypto_market')


class CryptoMarketsAdmin(admin.ModelAdmin):
    list_display        = ('name',)
    prepopulated_fields = {'slug':('name',)}

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'slug':
            kwargs['widget'] = forms.TextInput(attrs={'readonly': 'readonly'})
        return super().formfield_for_dbfield(db_field, **kwargs)
 



admin.site.register(APIEndpoints, APIEndpointsAdmin)
admin.site.register(CryptoMarketAPICredentials, CryptoMarketAPICredentialsAdmin)
admin.site.register(CryptoMarkets, CryptoMarketsAdmin)

