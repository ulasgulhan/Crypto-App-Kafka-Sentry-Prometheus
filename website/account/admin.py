from django.contrib import admin
from .models import APIEndpoints

# Register your models here.



class APIEndpointsAdmin(admin.ModelAdmin):
    list_display    = ('api_site_name', 'endpoint_name', 'method')



admin.site.register(APIEndpoints, APIEndpointsAdmin)
