from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_coin_data, name='coin_data')
]