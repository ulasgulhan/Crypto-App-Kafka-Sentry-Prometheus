from . import CryptoMarketPlace
import time
from ..models import OkxAPI
from ..utilities import okx_signature
from pprint import pprint
import datetime as dt



class OKX(CryptoMarketPlace):
    def __init__(self, user):
        self.timestamp = dt.datetime.utcnow().isoformat()[:-3]+'Z'
        self.user = user
        self.db_model = OkxAPI
        self.domain = 'https://www.okx.com'
    

    def generate_headers(self, endpoint_path):
        api_info = OkxAPI.objects.get(user=self.user)

        message = self.timestamp + 'GET' + endpoint_path

        headers = {
            'OK-ACCESS-TIMESTAMP': self.timestamp,
            'OK-ACCESS-KEY': api_info.api_key,
            'OK-ACCESS-PASSPHRASE': api_info.access_passphrase,
            'OK-ACCESS-SIGN': okx_signature(api_info.secret_key, message)
        }

        return headers
    

    def get_api_data(self):
        context = {}

        api_endpoints = self.get_api_endpoints('okx')

        for endpoint in api_endpoints:
            context[endpoint.endpoint_name] = self.fetcher(endpoint.auth_required, url=endpoint.endpoint_url, method=endpoint.method)

        return context
