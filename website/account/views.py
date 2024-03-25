from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from account.forms import PassphraseForm, NonePassphraseForm
from .models import CryptoMarketAPICredentials, CryptoMarkets
import asyncio
from collections import defaultdict
from .services.okx import OKX
from .services.bitget import Bitget
from .services.bybit import Bybit

# Create your views here.


@login_required(login_url='/login')
def profile(request):
    user = request.user
    bybit_connected = False
    bitget_connected = False
    okx_connected = False

    bitget_api_info = CryptoMarketAPICredentials.objects.filter(user=request.user, crypto_market=1)
    bybit_api_info = CryptoMarketAPICredentials.objects.filter(user=request.user, crypto_market=2)
    okx_api_info = CryptoMarketAPICredentials.objects.filter(user=request.user, crypto_market=3)

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

@login_required(login_url='/login')
def bitget_access(request):
    crypto_market_class = CryptoMarkets.objects.get(id=1)
    if request.method == 'POST':
        form = PassphraseForm(request.POST)
        if form.is_valid():
            api = form.save(commit=False)
            api.user = request.user
            api.crypto_market = crypto_market_class
            api.api_key = form.cleaned_data['access_key']
            api.save()
            return redirect('all_data')
    else:
        form = PassphraseForm()
    return render(request, 'access.html', {'bitget_form': form})


@login_required(login_url='/login')
def bybit_access(request):
    crypto_market_class = CryptoMarkets.objects.get(id=2)
    if request.method == 'POST':
        form = NonePassphraseForm(request.POST)
        if form.is_valid():
            api = form.save(commit=False)
            api.user = request.user
            api.crypto_market = crypto_market_class
            api.api_key = form.cleaned_data['access_key']
            api.save()
            return redirect('all_data')
    else:
        form = NonePassphraseForm()
    return render(request, 'access.html', {'bybit_form': form})


@login_required(login_url='/login')
def okx_access(request):
    crypto_market_class = CryptoMarkets.objects.get(id=3)
    if request.method == 'POST':
        form = PassphraseForm(request.POST)
        if form.is_valid():
            api = form.save(commit=False)
            api.user = request.user
            api.crypto_market = crypto_market_class
            api.api_key = form.cleaned_data['access_key']
            api.save()
            return redirect('all_data')
    else:
        form = PassphraseForm()
    return render(request, 'access.html', {'bybit_form': form})

# endregion


# region Delete

@login_required(login_url='/login')
def delete_bitget_api(request):
    api_info = CryptoMarketAPICredentials.objects.filter(user=request.user, crypto_market=1)
    api_info.delete()
    return redirect('profile')


@login_required(login_url='/login')
def delete_bybit_api(request):
    api_info = CryptoMarketAPICredentials.objects.filter(user=request.user, crypto_market=2)
    api_info.delete()
    return redirect('profile')


@login_required(login_url='/login')
def delete_okx_api(request):
    api_info = CryptoMarketAPICredentials.objects.filter(user=request.user, crypto_market=3)
    api_info.delete()
    return redirect('profile')

# endregion


# region Crypto Sites

@login_required(login_url='/login')
def bitget(request):
    try:
        from .services.bitget import Bitget
        api_class = Bitget(request.user)

        context = asyncio.run(api_class.get_api_data())

        return render(request, 'sites/bitget.html', context)
    except Exception as e:
        print(e)
        return render(request, 'sites/bitget.html')


@login_required(login_url='/login')
def bybit(request):
    try:
        from .services.bybit import Bybit

        api_class = Bybit(request.user)
        context = asyncio.run(api_class.get_api_data())

        return render(request, 'sites/bybit.html', context)
    except Exception as e:
        print(e)
        return render(request, 'sites/bybit.html')


@login_required(login_url='/login')
def okx(request):
    try:
        from .services.okx import OKX

        api_class = OKX(request.user)
        context = asyncio.run(api_class.get_api_data())

        return render(request, 'sites/okx.html', context)
    except Exception as e:
        print(e)
        return render(request, 'sites/okx.html')


@login_required(login_url='/login')
def get_big_data(request):
    try:
        from .services.all_api_data import AllData

        api_class = AllData()
        context = api_class.get_all_data(request)
        
        return render(request, 'home.html', context)
    except Exception as e:
        print(e)
        return render(request, 'home.html')
             


