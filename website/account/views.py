from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from account.forms import PassphraseForm, NonePassphraseForm
from .models import CryptoMarketAPICredentials, CryptoMarkets, User, Membership
import asyncio
from kafka import KafkaProducer
from .utilities import kafka_producer_serializer


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


@login_required(login_url='/login')
def copy_trader(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_copy_trader:
        user.is_copy_trader = False
    else:
        user.is_copy_trader = True
    user.save()
    return redirect('profile')


@login_required(login_url='/login')
def copy_trader_list(request):
    users = User.objects.filter(is_copy_trader=True).exclude(id=request.user.id)
    subscriber = request.user
    subscription_status = {}
    
    for user in users:
        is_subscribed = Membership.objects.filter(user=user, subscribers=subscriber).exists()
        if is_subscribed:
            subscription_status[user.id] = is_subscribed

    context = {
        'users': users,
        'subscription_status': subscription_status
    }

    return render(request, 'membership.html', context)


@login_required(login_url='/login')
def subscribe(request, user_id):
    copy_trader = User.objects.get(id=user_id)
    subscriber = request.user

    is_subscribed = Membership.objects.filter(user=copy_trader, subscribers=subscriber).exists()

    if is_subscribed:
        membership_instance = Membership.objects.get(user=copy_trader)
        membership_instance.subscribers.remove(subscriber)
    else:
        membership_instance, _ = Membership.objects.get_or_create(user=copy_trader)
        membership_instance.subscribers.add(subscriber)

    return redirect('copy_trader_list')
    


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

        print(context['okx_account_assets'])

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


@login_required(login_url='/login')
def bitget_coin_detail(request, symbol):
    try:
        from .services.bitget import Bitget
        from .forms import FuturesForm

        producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=kafka_producer_serializer)
        api_class = Bitget(request.user)
        context = asyncio.run(api_class.get_coin_data(symbol))

        if request.method == 'POST':
            form = FuturesForm(request.POST)
            if form.is_valid():
                size = form.cleaned_data['size']
                price = form.cleaned_data['price']
                side = form.cleaned_data['side']
                result = asyncio.run(api_class.place_order(symbol, size, price, side))
                if result['bitget_place_order']['msg'] == 'success':
                    message = {'symbol': symbol, 'size': size, 'side': side, 'price': price}
                    producer.send('copy-trade', message)
                    producer.flush()
                    producer.close()
                print(result)
                return redirect('bitget')
        else:
            form = FuturesForm()
        
        context['form'] = form

        return render(request, 'coin_details/bitget_coin.html', context)
    except Exception as e:
        print(e)
        return render(request, 'coin_details/bitget_coin.html')


@login_required(login_url='/login')
def bybit_coin_detail(request, symbol):
    try:
        from .services.bybit import Bybit
        from .forms import FuturesForm


        producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=kafka_producer_serializer)
        api_class = Bybit(request.user)
        context = asyncio.run(api_class.get_coin_data(symbol))
        if request.method == 'POST':
            form = FuturesForm(request.POST)
            if form.is_valid():
                qty = form.cleaned_data['size']
                price = form.cleaned_data['price']
                side = form.cleaned_data['side']
                result = asyncio.run(api_class.place_order(symbol, side, qty, price))
                producer.send('copy-trade', result)
                producer.flush()
                producer.close()
                print(result)
                return redirect('bybit')
        else:
            form = FuturesForm()
        
        context['form'] = form


        return render(request, 'coin_details/bybit_coin.html', context)
    except Exception as e:
        print(e)
        return render(request, 'coin_details/bybit_coin.html')


@login_required(login_url='/login')
def okx_coin_detail(request, symbol):
    try:
        from .services.okx import OKX
        from .forms import FuturesForm

        producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=kafka_producer_serializer)
        api_class = OKX(request.user)
        context = asyncio.run(api_class.get_coin_data(symbol))
        if request.method == 'POST':
            form = FuturesForm(request.POST)
            if form.is_valid():
                size = form.cleaned_data['size']
                price = form.cleaned_data['price']
                side = form.cleaned_data['side']
                result = asyncio.run(api_class.place_order(symbol, size, price, side))
                if result['okx_place_order']['code'] == '0':
                    producer.send('copy-trade', result)
                    producer.flush()
                    producer.close()
                print(result)
                return redirect('okx')
        else:
            form = FuturesForm()
        
        context['form'] = form

        return render(request, 'coin_details/okx_coin.html', context)
    except Exception as e:
        print(e)
        return render(request, 'coin_details/okx_coin.html')


             


