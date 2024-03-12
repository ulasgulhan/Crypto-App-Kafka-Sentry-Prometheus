from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_big_data, name='all_data'),
    path('profile/', views.profile, name='profile'),
    path('bitget', views.bitget, name='bitget'),
    path('bitget/delete', views.delete_bitget_api, name='delete_bitget'),
    path('bybit/delete', views.delete_bybit_api, name='delete_bybit'),
    path('bitget/access', views.bitget_access, name='bitget_access'),
    path('bybit/access', views.bybit_access, name='bybit_access'),
    
]