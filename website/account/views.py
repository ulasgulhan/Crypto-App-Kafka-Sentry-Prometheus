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
            account_endpoint = '/api/v2/mix/account/account?symbol=btcusdt&productType=USDT-FUTURES&marginCoin=usdt'
            personal_info_endpoint = '/api/v2/spot/account/info'
            account_message = timestamp + 'GET' + account_endpoint + ''
            personal_info_message = timestamp + 'GET' + personal_info_endpoint + ''
            account_signature = hmac.new(secret_key.encode(), account_message.encode(), hashlib.sha256).digest()
            info_signature = hmac.new(secret_key.encode(), personal_info_message.encode(), hashlib.sha256).digest()
            account_signature_b64 = base64.b64encode(account_signature).decode()
            info_signature_b64 = base64.b64encode(info_signature).decode()
            personal_info_headers = {
                'ACCESS-TIMESTAMP': timestamp,
                'ACCESS-KEY': access_key,
                'ACCESS-PASSPHRASE': access_passphrase,
                'ACCESS-SIGN': info_signature_b64,
            }
            account_headers = {
                'ACCESS-TIMESTAMP': timestamp,
                'ACCESS-KEY': access_key,
                'ACCESS-PASSPHRASE': access_passphrase,
                'ACCESS-SIGN': account_signature_b64,
            }
            personal_info = requests.get('https://api.bitget.com/api/v2/spot/account/info', headers=personal_info_headers)
            account_response = requests.get('https://api.bitget.com/api/v2/mix/account/account?symbol=btcusdt&productType=USDT-FUTURES&marginCoin=usdt', headers=account_headers)
            coin_response  = requests.get('https://api.bitget.com/api/v2/spot/market/tickers')
            info = account_response.json()
            coin = coin_response.json()
            user = request.user
            account = personal_info.json()
            context = {
                    'info': info,
                    'coins': coin,
                    'user': user,
                    'account': account,
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