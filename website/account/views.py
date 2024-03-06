import requests
from django.shortcuts import render

# Create your views here.


def get_coin_data(request):
    user = request.user
    url = "https://api.bitget.com/api/v2/spot/market/tickers"
    response = requests.get(url)
    # print(response.json())
    change24h = []
    for coin in response.json()['data']:
            try:
                percentage_change=((float(coin['high24h']) - float(coin['low24h'])) / float(coin['low24h'])) * 100
                change24h.append(percentage_change)
            except ZeroDivisionError:
                change24h.append(0)
    

    context = {
        'coins': response.json(),
        'user': user,
        'percentage': change24h,
    }
    
    return render(request, 'home.html', context)