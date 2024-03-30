from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from account.forms import PassphraseForm, NonePassphraseForm
from .models import CryptoMarketAPICredentials, CryptoMarkets
import asyncio

# Create your views here.


@login_required(login_url='/login')
def profile(request):
    user = request.user
    api_connection = {}

    crypto_markets = CryptoMarkets.objects.filter(is_active=True)
    api_info = CryptoMarketAPICredentials.objects.filter(user=request.user)


    context = {
        'user': user,
        'crypto_markets': crypto_markets,
    }
    
    for api in api_info:
        api_connection[api.crypto_market.slug] = True
    
    context['connection'] = api_connection
    
    return render(request, 'profile.html', context)


# region Access


@login_required(login_url='/login')
def access(request, market_id):
    crypto_market_class = CryptoMarkets.objects.get(id=market_id)
    if market_id == 2:
        if request.method == 'POST':
            form = NonePassphraseForm(request.POST)
        else:
            form = NonePassphraseForm()
    else:
        if request.method == 'POST':
            form = PassphraseForm(request.POST)
        else:
            form = PassphraseForm()
    if form.is_valid():
        api = form.save(commit=False)
        api.user = request.user
        api.crypto_market = crypto_market_class
        api.api_key = form.cleaned_data['access_key']
        api.save()
        return redirect('all_data')
    return render(request, 'access.html', {'form': form})

# endregion


# region Delete

@login_required(login_url='/login')
def delete(request, market_id):
    api_info = CryptoMarketAPICredentials.objects.filter(user=request.user, crypto_market=market_id)
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

        # print(context['bitget_demo_coin'])
        print(context['bitget_future_demo_trade'])

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
             


