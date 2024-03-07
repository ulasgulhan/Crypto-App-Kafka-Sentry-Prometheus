import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import APIForm
import time
import hashlib
import hmac
import base64

# Create your views here.



def get_big_data(request):
    if request.method == 'POST':
        form = APIForm(request.POST)
        if form.is_valid():
            access_key = form.cleaned_data['access_key']
            access_passphrase = form.cleaned_data['access_passphrase']
            secret_key = form.cleaned_data['secret_key']
            timestamp = str(int(time.time_ns() / 1000000))
            endpoint = '/api/v2/spot/account/info'
            message = timestamp + 'GET' + endpoint + ''
            signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
            signature_b64 = base64.b64encode(signature).decode()
            headers = {
                'ACCESS-TIMESTAMP': timestamp,
                'ACCESS-KEY': access_key,
                'ACCESS-PASSPHRASE': access_passphrase,
                'ACCESS-SIGN': signature_b64,
            }
            account_response = requests.get('https://api.bitget.com/api/v2/spot/account/info', headers=headers)
            coin_response  = requests.get('https://api.bitget.com/api/v2/spot/market/tickers')
            info = account_response.json()
            coin = coin_response.json()
            user = request.user
            context = {
                    'info': info,
                    'coins': coin,
                    'user': user
                }
            return render(request, 'home.html', context)
    else:
        form = APIForm()
    return render(request, 'access.html', {'form': form})
            



""" @login_required
def get_coin_data(request):
    user = request.user
    url = "https://api.bitget.com/api/v2/spot/market/tickers"
    response = requests.get(url)
    

    context = {
        'coins': response.json(),
        'user': user,
    }
    
    return render(request, 'home.html', context) """