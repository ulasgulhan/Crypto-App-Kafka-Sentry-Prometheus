from . import CryptoMarketPlace
import time
from ..models import BybitAPI
from ..utilities import bybit_signature, decode


class Bybit(CryptoMarketPlace):
    def __init__(self, user):
        self.timestamp = str(int(time.time_ns() / 1000000))
        self.user = user
        self.db_model = BybitAPI
        self.domain = 'https://api.bybit.com'
    

    def generate_headers(self, params):
        api_info = BybitAPI.objects.get(user=self.user)
        api_info.api_key = decode(api_info.api_key)
        if params.startswith('/'):
            message = self.timestamp + api_info.api_key + str(5000)
        else:
            message = self.timestamp + api_info.api_key + str(5000) + params

        headers = {
            'X-BAPI-TIMESTAMP': self.timestamp,
            'X-BAPI-API-KEY': api_info.api_key,
            'X-BAPI-RECV-WINDOW': str(5000),
            'X-BAPI-SIGN': bybit_signature(decode(api_info.secret_key), message)
        }

        return headers
    
    def get_api_data(self):
        context = {}

        api_endpoints = self.get_api_endpoints('bybit')

        for endpoint in api_endpoints:
            context[endpoint.endpoint_name] = self.fetcher(endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method, params=endpoint.endpoint_params)

        return context


