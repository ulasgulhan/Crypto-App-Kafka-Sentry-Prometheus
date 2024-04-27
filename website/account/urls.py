from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_big_data, name='all_data'),
    path('csrf_token/', views.get_csrf_token, name='csrf_token'),

    path('profile/', views.profile, name='profile'),

    path('bitget/', views.bitget, name='bitget'),
    path('bybit/', views.bybit, name='bybit'),
    path('okx/', views.okx, name='okx'),
    path('copy-traders/', views.copy_trader_list, name='copy_trader_list'),
    path('copy-trade-subscribers/<int:sub>/<str:symbol>/<int:size>/<int:price>/<str:side>/<str:site>', views.copy_trade_all_subscribers, name='copy_trader_subscribers'),

    path('<int:user_id>', views.copy_trader, name='copy_trader'),
    path('copy-traders/<int:user_id>', views.subscribe, name='subscribe' ),

    path('bitget/<str:symbol>', views.bitget_coin_detail, name='bitget_coin_detail'),
    path('bybit/<str:symbol>', views.bybit_coin_detail, name='bybit_coin_detail'),
    path('okx/<str:symbol>', views.okx_coin_detail, name='okx_coin_detail'),
    
    path('delete/<int:market_id>', views.delete, name='delete'),

    path('access/<int:market_id>', views.access, name='access'),
    
]