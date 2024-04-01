from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_big_data, name='all_data'),

    path('profile/', views.profile, name='profile'),

    path('bitget/', views.bitget, name='bitget'),
    path('bybit/', views.bybit, name='bybit'),
    path('okx/', views.okx, name='okx'),

    path('<str:symbol>', views.coin_detail, name='coin_detail'),
    
    path('delete/<int:market_id>', views.delete, name='delete'),

    path('access/<int:market_id>', views.access, name='access'),
    
]