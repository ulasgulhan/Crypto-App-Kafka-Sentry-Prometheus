from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_big_data, name='all_data'),

    path('profile/', views.profile, name='profile'),

    path('bitget/', views.bitget, name='bitget'),
    path('bybit/', views.bybit, name='bybit'),
    path('okx/', views.okx, name='okx'),

    path('<int:user_id>', views.copy_trader, name='copy_trade'),


    path('bitget/<str:symbol>', views.bitget_coin_detail, name='bitget_coin_detail'),
    path('bybit/<str:symbol>', views.bybit_coin_detail, name='bybit_coin_detail'),
    path('okx/<str:symbol>', views.okx_coin_detail, name='okx_coin_detail'),
    
    path('delete/<int:market_id>', views.delete, name='delete'),

    path('access/<int:market_id>', views.access, name='access'),
    
]