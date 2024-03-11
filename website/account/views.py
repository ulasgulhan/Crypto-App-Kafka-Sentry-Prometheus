import requests
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import APIForm
import time
import hashlib
import hmac
import base64
from django.contrib.auth.models import User
from .models import BitGetAPI

# Create your views here.


@login_required
def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)


def bitget_access(request):
    if request.method == 'POST':
        form = APIForm(request.POST)
        if form.is_valid():
            api = form.save(commit=False)
            api.user = request.user
            api.api_key = form.cleaned_data['access_key']
            api.save()
            return redirect('coin_data')
    else:
        form = APIForm()
    return render(request, 'access.html', {'form': form})


def bitget(request):
    api_info = BitGetAPI.objects.filter(user=request.user)
    timestamp = str(int(time.time_ns() / 1000000))
    for api in api_info:
        access_key = api.api_key
        access_passphrase = api.access_passphrase
        secret_key = api.secret_key
    

    # API request URI
    account_endpoint = '/api/v2/mix/account/account?symbol=btcusdt&productType=USDT-FUTURES&marginCoin=usdt'
    personal_info_endpoint = '/api/v2/spot/account/info'
    account_assets = '/api/v2/spot/account/assets?assetType=all'

    # Sigmature Message
    account_message = timestamp + 'GET' + account_endpoint + ''
    personal_info_message = timestamp + 'GET' + personal_info_endpoint + ''
    account_assets_message = timestamp + 'GET' + account_assets + ''

    # Signature Encode
    account_signature = hmac.new(secret_key.encode(), account_message.encode(), hashlib.sha256).digest()
    info_signature = hmac.new(secret_key.encode(), personal_info_message.encode(), hashlib.sha256).digest()
    assets_signature = hmac.new(secret_key.encode(), account_assets_message.encode(), hashlib.sha256).digest()


    # Signature Decode
    account_signature_b64 = base64.b64encode(account_signature).decode()
    info_signature_b64 = base64.b64encode(info_signature).decode()
    assets_signature_b64 = base64.b64encode(assets_signature).decode()


    # API Headers
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
    assets_headers = {
        'ACCESS-TIMESTAMP': timestamp,
        'ACCESS-KEY': access_key,
        'ACCESS-PASSPHRASE': access_passphrase,
        'ACCESS-SIGN': assets_signature_b64,
    }


    # API Requests
    personal_info = requests.get('https://api.bitget.com/api/v2/spot/account/info', headers=personal_info_headers)
    account_response = requests.get('https://api.bitget.com/api/v2/mix/account/account?symbol=btcusdt&productType=USDT-FUTURES&marginCoin=usdt', headers=account_headers)
    coin_response  = requests.get('https://api.bitget.com/api/v2/spot/market/tickers')
    assets_response  = requests.get('https://api.bitget.com/api/v2/spot/account/assets?assetType=all', headers=assets_headers)


    info = account_response.json()
    coin = coin_response.json()
    user = request.user
    account = personal_info.json()
    assets = assets_response.json()
    context = {
            'info': info,
            'coins': coin,
            'user': user,
            'account': account,
            'assets': assets
        }
    return render(request, 'sites/bitget.html', context)

def get_big_data(request):
    if request.method == 'POST':
        form = APIForm(request.POST)
        if form.is_valid():
            access_key = form.cleaned_data['access_key']
            access_passphrase = form.cleaned_data['access_passphrase']
            secret_key = form.cleaned_data['secret_key']
            timestamp = str(int(time.time_ns() / 1000000))


            # API request URI
            account_endpoint = '/api/v2/mix/account/account?symbol=btcusdt&productType=USDT-FUTURES&marginCoin=usdt'
            personal_info_endpoint = '/api/v2/spot/account/info'
            account_assets = '/api/v2/spot/account/assets?assetType=all'


            # Sigmature Message
            account_message = timestamp + 'GET' + account_endpoint + ''
            personal_info_message = timestamp + 'GET' + personal_info_endpoint + ''
            account_assets_message = timestamp + 'GET' + account_assets + ''


            # Signature Encode
            account_signature = hmac.new(secret_key.encode(), account_message.encode(), hashlib.sha256).digest()
            info_signature = hmac.new(secret_key.encode(), personal_info_message.encode(), hashlib.sha256).digest()
            assets_signature = hmac.new(secret_key.encode(), account_assets_message.encode(), hashlib.sha256).digest()


            # Signature Decode
            account_signature_b64 = base64.b64encode(account_signature).decode()
            info_signature_b64 = base64.b64encode(info_signature).decode()
            assets_signature_b64 = base64.b64encode(assets_signature).decode()


            # API Headers
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
            assets_headers = {
                'ACCESS-TIMESTAMP': timestamp,
                'ACCESS-KEY': access_key,
                'ACCESS-PASSPHRASE': access_passphrase,
                'ACCESS-SIGN': assets_signature_b64,
            }


            # API Requests
            personal_info = requests.get('https://api.bitget.com/api/v2/spot/account/info', headers=personal_info_headers)
            account_response = requests.get('https://api.bitget.com/api/v2/mix/account/account?symbol=btcusdt&productType=USDT-FUTURES&marginCoin=usdt', headers=account_headers)
            coin_response  = requests.get('https://api.bitget.com/api/v2/spot/market/tickers')
            assets_response  = requests.get('https://api.bitget.com/api/v2/spot/account/assets?assetType=all', headers=assets_headers)


            info = account_response.json()
            coin = coin_response.json()
            user = request.user
            account = personal_info.json()
            assets = assets_response.json()
            context = {
                    'info': info,
                    'coins': coin,
                    'user': user,
                    'account': account,
                    'assets': assets
                }
            return render(request, 'home.html', context)
    else:
        form = APIForm()
    return render(request, 'access.html', {'form': form})
            
