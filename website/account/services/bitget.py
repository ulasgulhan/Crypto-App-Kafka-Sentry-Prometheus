from . import CryptoMarketPlace
import time
from ..utilities import generate_signature, decode
from asgiref.sync import sync_to_async
import aiohttp
import asyncio




class Bitget(CryptoMarketPlace):

    def __init__(self, user):
        super().__init__()
        self.timestamp = str(int(time.time_ns() / 1000000))
        self.user = user
        self.domain = "https://api.bitget.com"


    
    async def generate_headers(self, url=None, params=None):
        api_info = await sync_to_async(self.db_model.objects.get)(user=self.user, crypto_market=1)


        if url == '/api/v2/mix/order/place-order':
            message = self.timestamp + 'POST' + '/api/v2/mix/order/place-order' + str(params)
            print(message)
        else:
            message = self.timestamp + 'GET' + url


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

            api_endpoints = await self.get_api_endpoints(1)

            params = {
                "symbol": "ETHUSDT",
                "productType": "SUSDT-FUTURES",
                "marginMode": "isolated",
                "marginCoin": "USDT",
                "size": "0.1",
                "price": "2000",
                "side": "sell",
                "tradeSide": "open",
                "orderType": "limit",
                "force": "gtc",
                "clientOid": "121211212122"
            }

            tasks = []
            for endpoint in api_endpoints:
                if endpoint.endpoint_url == '/api/v2/mix/order/place-order':
                    tasks.append(self.fetcher(session, endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method, params=params))
                else:
                    tasks.append(self.fetcher(session, endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method))


            results = await asyncio.gather(*tasks)

            for i, endpoint in enumerate(api_endpoints):
                context[endpoint.endpoint_name] = results[i]

        return context