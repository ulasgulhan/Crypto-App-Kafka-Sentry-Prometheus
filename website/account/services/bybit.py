import asyncio
import aiohttp
from . import CryptoMarketPlace
import time
from ..models import BybitAPI
from ..utilities import bybit_signature, decode
from asgiref.sync import sync_to_async


class Bybit(CryptoMarketPlace):
    def __init__(self, user):
        self.timestamp = str(int(time.time_ns() / 1000000))
        self.user = user
        self.db_model = BybitAPI
        self.domain = 'https://api.bybit.com'
    

    
    async def generate_headers(self, url=None, params=''):
        api_info = await sync_to_async(BybitAPI.objects.get)(user=self.user)
        api_key = decode(api_info.api_key)
        message = self.timestamp + api_key + str(5000) + params

        headers = {
            'X-BAPI-TIMESTAMP': self.timestamp,
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-RECV-WINDOW': str(5000),
            'X-BAPI-SIGN': bybit_signature(decode(api_info.secret_key), message)
        }

        return headers
    
    async def get_api_data(self):
        context = {}
        async with aiohttp.ClientSession() as session:

            api_endpoints = await self.get_api_endpoints('bybit')

            tasks = []
            for endpoint in api_endpoints:
                tasks.append(self.fetcher(session, endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method, params=endpoint.endpoint_params))

            results = await asyncio.gather(*tasks)

            for i, endpoint in enumerate(api_endpoints):
                context[endpoint.endpoint_name] = results[i]

        return context