from . import CryptoMarketPlace
import time
from ..utilities import generate_signature, decode
from asgiref.sync import sync_to_async
import aiohttp
import asyncio
import json




class Bitget(CryptoMarketPlace):

    def __init__(self, user):
        super().__init__()
        self.timestamp = str(int(time.time_ns() / 1000000))
        self.user = user
        self.domain = "https://api.bitget.com"


    
    async def generate_headers(self, url=None, params=None, method=None):
        api_info = await sync_to_async(self.db_model.objects.get)(user=self.user, crypto_market=1)

        if method == 'POST':
            body = json.dumps(params)
            message = self.timestamp + method + url + str(body)
        else:
            message = self.timestamp + method + url


        headers = {
            'ACCESS-TIMESTAMP': self.timestamp,
            'ACCESS-KEY': decode(api_info.api_key),
            'ACCESS-PASSPHRASE': decode(api_info.access_passphrase),
            'ACCESS-SIGN': generate_signature(decode(api_info.secret_key), message),
            'Content-Type': 'application/json'
        }


        return headers
    

    async def get_api_data(self):
        context = {}
        async with aiohttp.ClientSession() as session:

            api_endpoints = await self.get_api_endpoints(crypto_market=1, method='GET')



            tasks = []
            for endpoint in api_endpoints:
                tasks.append(self.fetcher(session, endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method))


            results = await asyncio.gather(*tasks)

            for i, endpoint in enumerate(api_endpoints):
                context[endpoint.endpoint_name] = results[i]

        return context
            
    
    async def get_coin_data(self, symbol):
        context = {}
        async with aiohttp.ClientSession() as session:
                        
            api_endpoints = await self.get_api_endpoints(crypto_market=1, method='GET')

            
            for endpoint in api_endpoints:
                if endpoint.endpoint_name == 'coins':
                    coins_response = await self.fetcher(session, endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method)
                    coins_data = coins_response.get('data', [])            
                    for coin in coins_data:
                        if coin['symbol'] == symbol:
                            context['coin'] = coin
                            break
        return context


    async def place_order(self, symbol=None, size=None, price = None, side=None):
        context = {}
        async with aiohttp.ClientSession() as session:

            api_endpoints = await self.get_api_endpoints(crypto_market=1, method='POST')

            params = {
                "symbol": 'SBTCSUSDT',
                "productType": "SUSDT-FUTURES",
                "marginMode": "isolated",
                "marginCoin": "SUSDT",
                "size": str(size),
                "price": str(price),
                "side": str(side),
                "tradeSide": "open",
                "orderType": "limit",
                "force": "gtc",
            }

            tasks = []
            for endpoint in api_endpoints:
                if endpoint.method == 'POST':
                    tasks.append(self.fetcher(session, endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method, params=params))

            results = await asyncio.gather(*tasks)

            for i, endpoint in enumerate(api_endpoints):
                context[endpoint.endpoint_name] = results[i]

        return context
            
