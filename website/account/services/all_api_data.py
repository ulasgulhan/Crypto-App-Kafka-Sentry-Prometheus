from ..models import CryptoMarketAPICredentials
from .okx import OKX
from .bitget import Bitget
from .bybit import Bybit
import asyncio
from collections import defaultdict



class AllData():
    def get_crypto_markets_by_user(self, request):
        crypto_markets = {
            "okx": OKX(request.user),
            "bitget": Bitget(request.user),
            "bybit": Bybit(request.user)
        }

        datas = CryptoMarketAPICredentials.objects.filter(user=request.user)

        for data in datas:
            if data.crypto_market.slug not in crypto_markets.keys():
                crypto_markets.delete(data)
        
        return crypto_markets




    def get_api_data_of_markets(self, crypto_markets):
        context = {}
        
        for market_class in crypto_markets.values():
            context.update(asyncio.run(market_class.get_api_data()))

        return context
    
    def get_all_data(self, request):
        context = self.get_api_data_of_markets(self.get_crypto_markets_by_user(request))
                
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

        return context