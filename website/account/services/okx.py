import asyncio
import aiohttp
from . import CryptoMarketPlace
from ..utilities import okx_signature, decode
import datetime as dt
from asgiref.sync import sync_to_async



class OKX(CryptoMarketPlace):
    def __init__(self, user):
        super().__init__()
        self.timestamp = dt.datetime.utcnow().isoformat()[:-3]+'Z'
        self.user = user
        self.domain = 'https://www.okx.com'
    

    async def generate_headers(self, url=None, params=None, method=None):
        api_info = await sync_to_async(self.db_model.objects.get)(user=self.user, crypto_market=3)



        if params:
            endpoint = url + '?' + params
            print(endpoint)
            message = self.timestamp + method + url + '?' + params
        else:
            message = self.timestamp + method + url

        headers = {
            'OK-ACCESS-TIMESTAMP': self.timestamp,
            'OK-ACCESS-KEY': decode(api_info.api_key),
            'OK-ACCESS-PASSPHRASE': decode(api_info.access_passphrase),
            'OK-ACCESS-SIGN': okx_signature(decode(api_info.secret_key), message).decode('utf-8'),
            'Content-Type': 'application/json'
        }

        return headers
    

    async def get_api_data(self):
        context = {}
        async with aiohttp.ClientSession() as session:

            api_endpoints = await self.get_api_endpoints(crypto_market=3, method='GET')

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
                        
            api_endpoints = await self.get_api_endpoints(crypto_market=3, method='GET', endpoint_name='okx_single_coin')

            
            for endpoint in api_endpoints:
                context['coin'] = await self.fetcher(session, endpoint.auth_required, url=endpoint.endpoint_url + f'{symbol}', method=endpoint.method)  

              
        return context
    
    async def place_order(self, symbol=None, size=None, price=None, side=None):
        context = {}
        async with aiohttp.ClientSession() as session:

            api_endpoints = await self.get_api_endpoints(crypto_market=3, method='POST')

            # params = f'instId={str(symbol)}&tdMode=isolated&side={str(side)}&ordType=limit&sz={str(size)}&px={str(price)}'

            tasks = []
            for endpoint in api_endpoints:
                if endpoint.method == 'POST':
                    tasks.append(self.fetcher(session, endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method, params=endpoint.endpoint_params))

            results = await asyncio.gather(*tasks)

            for i, endpoint in enumerate(api_endpoints):
                context[endpoint.endpoint_name] = results[i]

        return context
            