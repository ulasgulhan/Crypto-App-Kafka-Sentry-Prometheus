from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_big_data, name='all_data'),

    path('profile/', views.profile, name='profile'),

    path('bitget/', views.bitget, name='bitget'),
    path('bybit/', views.bybit, name='bybit'),
    path('okx/', views.okx, name='okx'),

    path('bitget/delete', views.delete_bitget_api, name='delete_bitget'),
    path('bybit/delete', views.delete_bybit_api, name='delete_bybit'),
    path('okx/delete', views.delete_okx_api, name='delete_okx'),
    path('dtest/<int:market_id>', views.delete_test, name='delete_test'),

    path('bitget/access', views.bitget_access, name='bitget_access'),
    path('bybit/access', views.bybit_access, name='bybit_access'),
    path('okx/access', views.okx_access, name='okx_access'),
    path('test/<int:market_id>', views.test, name='test'),
    
]