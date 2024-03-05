import requests
from django.shortcuts import render

# Create your views here.


def get_coin_data(request):
    user = request.user
    url = "https://api.bitget.com/api/v2/spot/public/coins"
    response = requests.get(url)

    context = {
        'coins': response.json(),
        'user': user
    }
    
    return render(request, 'home.html', context)