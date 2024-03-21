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
        api_secret_key = decode(api_info.secret_key)
        message = self.timestamp + api_key + str(5000) + params
        signature = bybit_signature(api_secret_key, message)

        headers = {
            'X-BAPI-TIMESTAMP': self.timestamp,
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-RECV-WINDOW': str(5000),
            'X-BAPI-SIGN': signature
        }

        return headers
    
    async def get_api_data(self):
        context = {}

        api_endpoints = await self.get_api_endpoints('bybit')

        for endpoint in api_endpoints:
            context[endpoint.endpoint_name] = await self.fetcher(endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method, params=endpoint.endpoint_params)

        return context