from . import CryptoMarketPlace
import time
from ..models import BitGetAPI
from ..utilities import generate_signature, decode


class Bitget(CryptoMarketPlace):

    def __init__(self, user):
        self.timestamp = str(int(time.time_ns() / 1000000))
        self.user = user
        self.db_model = BitGetAPI
        self.domain = "https://api.bitget.com"


    def generate_headers(self, url=None, params=None):
        api_info = BitGetAPI.objects.get(user=self.user)

        message = self.timestamp + 'GET' + url
        
        headers = {
            'ACCESS-TIMESTAMP': self.timestamp,
            'ACCESS-KEY': decode(api_info.api_key),
            'ACCESS-PASSPHRASE': decode(api_info.access_passphrase),
            'ACCESS-SIGN': generate_signature(decode(api_info.secret_key), message)
        }

        return headers
    

    def get_api_data(self):
        context = {}

        api_endpoints = self.get_api_endpoints('bitget')
        
        for endpoint in api_endpoints:
            context[endpoint.endpoint_name] = self.fetcher(endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method)

        return context