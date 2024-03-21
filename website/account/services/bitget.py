from . import CryptoMarketPlace
import time
from ..models import BitGetAPI
from ..utilities import generate_signature, decode
from asgiref.sync import sync_to_async
import aiohttp
import asyncio




class Bitget(CryptoMarketPlace):

    def __init__(self, user):
        self.timestamp = str(int(time.time_ns() / 1000000))
        self.user = user
        self.db_model = BitGetAPI
        self.domain = "https://api.bitget.com"


    
    async def generate_headers(self, url=None, params=None):
        api_info = await sync_to_async(BitGetAPI.objects.get)(user=self.user)

        message = self.timestamp + 'GET' + url
        
        headers = {
            'ACCESS-TIMESTAMP': self.timestamp,
            'ACCESS-KEY': decode(api_info.api_key),
            'ACCESS-PASSPHRASE': decode(api_info.access_passphrase),
            'ACCESS-SIGN': generate_signature(decode(api_info.secret_key), message)
        }

        return headers
    

    async def get_api_data(self):
        context = {}
        async with aiohttp.ClientSession() as session:

            api_endpoints = await self.get_api_endpoints('bitget')

            tasks = []
            for endpoint in api_endpoints:
                tasks.append(self.fetcher(session, endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method))

            results = await asyncio.gather(*tasks)

            for i, endpoint in enumerate(api_endpoints):
                context[endpoint.endpoint_name] = results[i]

        return context