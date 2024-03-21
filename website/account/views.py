from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from account.forms import BitGetAPIForm, ByBitAPIForm, OkxAPIFrom
from .models import BitGetAPI, BybitAPI, OkxAPI
from pprint import pprint
from django.contrib import messages

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
        
        context = api_class.get_api_data()

        return render(request, 'sites/bitget.html', context)
    except Exception as e:
        print(e)
        return render(request, 'sites/bitget.html')


@login_required
def bybit(request):
    try:
        from .services.bybit import Bybit

        api_class = Bybit(request.user)
        context = api_class.get_api_data()

        print(context['bybit_info'])

        return render(request, 'sites/bybit.html', context)
    except Exception as e:
        print(e)
        return render(request, 'sites/bybit.html')


@login_required
def okx(request):
    try:
        from .services.okx import OKX

        api_class = OKX(request.user)
        context = api_class.get_api_data()
        return render(request, 'sites/okx.html', context)
    except Exception as e:
        print(e)
        return render(request, 'sites/okx.html')



def get_big_data(request):
    if request.method == 'POST':
        form = BitGetAPIForm(request.POST)
        if form.is_valid():
            return render(request, 'home.html')
    else:
        form = BitGetAPIForm()
    return render(request, 'access.html', {'bitget_form': form})
             
# e

