from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from account.forms import BitGetAPIForm, ByBitAPIForm, OkxAPIFrom
from .models import BitGetAPI, BybitAPI, CryptoMarketAPICredentials, OkxAPI
import asyncio
from collections import defaultdict
from .services.okx import OKX
from .services.bitget import Bitget
from .services.bybit import Bybit

# Create your views here.


@login_required
def profile(request):
    user = request.user
    bybit_connected = False
    bitget_connected = False
    okx_connected = False

    bitget_api_info = BitGetAPI.objects.filter(user=request.user)
    bybit_api_info = BybitAPI.objects.filter(user=request.user)
    okx_api_info = OkxAPI.objects.filter(user=request.user)

    if bitget_api_info:
        bitget_connected = True
    
    if bybit_api_info:
        bybit_connected = True
    
    if okx_api_info:
        okx_connected = True

    context = {
        'user': user,
        'bitget_connected': bitget_connected,
        'bybit_connected': bybit_connected,
        'okx_connected': okx_connected,
    }
    return render(request, 'profile.html', context)


# region Access

@login_required
def bitget_access(request):
    if request.method == 'POST':
        form = BitGetAPIForm(request.POST)
        if form.is_valid():
            api = form.save(commit=False)
            api.user = request.user
            api.api_key = form.cleaned_data['access_key']
            api.save()
            return redirect('all_data')
    else:
        form = BitGetAPIForm()
    return render(request, 'access.html', {'bitget_form': form})


@login_required
def bybit_access(request):
    if request.method == 'POST':
        form = ByBitAPIForm(request.POST)
        if form.is_valid():
            api = form.save(commit=False)
            api.user = request.user
            api.api_key = form.cleaned_data['access_key']
            api.save()
            return redirect('all_data')
    else:
        form = ByBitAPIForm()
    return render(request, 'access.html', {'bybit_form': form})


@login_required
def okx_access(request):
    if request.method == 'POST':
        form = OkxAPIFrom(request.POST)
        if form.is_valid():
            api = form.save(commit=False)
            api.user = request.user
            api.api_key = form.cleaned_data['access_key']
            api.save()
            return redirect('all_data')
    else:
        form = OkxAPIFrom()
    return render(request, 'access.html', {'bybit_form': form})

# endregion


# region Delete

@login_required
def delete_bitget_api(request):
    api_info = BitGetAPI.objects.filter(user=request.user)
    api_info.delete()
    return redirect('profile')


@login_required
def delete_bybit_api(request):
    api_info = BybitAPI.objects.filter(user=request.user)
    api_info.delete()
    return redirect('profile')


@login_required
def delete_okx_api(request):
    api_info = OkxAPI.objects.filter(user=request.user)
    api_info.delete()
    return redirect('profile')

# endregion


# region Crypto Sites

@login_required
def bitget(request):
    try:
        from .services.bitget import Bitget
        api_class = Bitget(request.user)

        context = asyncio.run(api_class.get_api_data())

        return render(request, 'sites/bitget.html', context)
    except Exception as e:
        print(e)
        return render(request, 'sites/bitget.html')


@login_required
def bybit(request):
    try:
        from .services.bybit import Bybit

        api_class = Bybit(request.user)
        context = asyncio.run(api_class.get_api_data())

        return render(request, 'sites/bybit.html', context)
    except Exception as e:
        print(e)
        return render(request, 'sites/bybit.html')


@login_required
def okx(request):
    try:
        from .services.okx import OKX

        api_class = OKX(request.user)
        context = asyncio.run(api_class.get_api_data())

        return render(request, 'sites/okx.html', context)
    except Exception as e:
        print(e)
        return render(request, 'sites/okx.html')




def get_crypto_markets_by_user(request):
    crypto_markets = {
        "okx": OKX(request.user),
        "bitget": Bitget(request.user),
        "bybit": Bybit(request.user)
    }

    datas = CryptoMarketAPICredentials.objects.get(user=request.user)

    for data in datas:
        if data.cryptomarket.slug not in crypto_markets.keys():
            crypto_markets.delete(data)
    
    return crypto_markets




def get_api_data_of_markets(crypto_markets):
    context = {}

    for market_class in crypto_markets.values():
        context.update(asyncio.run(market_class.get_api_data())) 
    

       

"""
tokencı


access_token
pharase yoksa default none
secret key
crypto_market_id foreign key ile crypto markete bağlı

"""


"""
crypto markets

name
id
"""

"""
endpoints
crypto markets foreign key

"""




def get_big_data(request):
    try:

        okx_class = OKX(request.user)
        bitget_class = Bitget(request.user)
        bybit_class = Bybit(request.user)
        context = asyncio.run(okx_class.get_api_data())
        context.update(asyncio.run(bitget_class.get_api_data()))
        context.update(asyncio.run(bybit_class.get_api_data()))

                
        total_assets = defaultdict(lambda: {'total_amount': 0, 'available': 0, 'reserved': 0})


        if 'bybit_account_assets_fund' in context:
            bybit_assets = context['bybit_account_assets_fund'].get('result', {}).get('spot', {}).get('assets', [])
            for asset in bybit_assets:
                total_assets[asset['coin']]['total_amount'] += float(asset['free']) + float(asset['frozen'])
                total_assets[asset['coin']]['available'] += float(asset['free'])
                total_assets[asset['coin']]['reserved'] += float(asset['frozen'])


        if 'okx_account_assets' in context:
            okx_assets = context['okx_account_assets'].get('data', [])
            for asset in okx_assets:
                total_assets[asset['ccy']]['total_amount'] += float(asset['bal'])
                total_assets[asset['ccy']]['available'] += float(asset['availBal'])
                total_assets[asset['ccy']]['reserved'] += float(asset['frozenBal'])


        if 'account_assets' in context:
            bitget_assets = context['account_assets'].get('data', [])
            for asset in bitget_assets:
                total_assets[asset['coin']]['total_amount'] += float(asset['available']) + float(asset['frozen']) + float(asset['locked'])
                total_assets[asset['coin']]['available'] += float(asset['available'])
                total_assets[asset['coin']]['reserved'] += float(asset['frozen']) + float(asset['locked'])

        context['total_assets'] = total_assets.items()
        
        return render(request, 'home.html', context)
    except Exception as e:
        print(e)
        return render(request, 'home.html')
             


