from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_big_data, name='coin_data'),
    # path('home/', views.home, name='home')
]