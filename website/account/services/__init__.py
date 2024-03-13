import requests
import time
from ..models import BitGetAPI, BybitAPI, APIEndpoints
from ..utilities import generate_signature


# yapılacaklar servis api endpointleri dbye kaydedilsin dbdn gelsin auth header required false true gelsin



class CryptoMarketPlace():
    def __init__(self):
        self.timestamp = None
        self.db_model = None
        self.domain = None
        self.api_model = APIEndpoints

    def generate_headers(self, url=None):
        return None
    

    def get_api_endpoints(self, website):
        return APIEndpoints.objects.filter(api_site_name=website)


    def fetcher(self, auth_header_required=False, url=None, method="GET"):
        if auth_header_required:
            headers = self.generate_headers(url)
            response = requests.request(method, self.domain + url, headers=headers)
        else:
            response = requests.request(method, self.domain + url)
        
        return response.json()
    


class Bitget(CryptoMarketPlace):

    def __init__(self, user):
        self.timestamp = str(int(time.time_ns() / 1000000))
        self.user = user
        self.db_model = BitGetAPI
        self.domain = "https://api.bitget.com"


    def generate_headers(self, endpoint_path):
        api_info = BitGetAPI.objects.get(user=self.user)

        message = self.timestamp + 'GET' + endpoint_path

        headers = {
            'ACCESS-TIMESTAMP': self.timestamp,
            'ACCESS-KEY': api_info.api_key,
            'ACCESS-PASSPHRASE': api_info.access_passphrase,
            'ACCESS-SIGN': generate_signature(api_info.secret_key, message)
        }

        return headers
    

    def get_api_data(self):
        context = {}

        api_endpoints = self.get_api_endpoints('bitget')
        
        for endpoint in api_endpoints:
            context[endpoint.endpoint_name] = self.fetcher(endpoint.auth_required, url=endpoint.endpoint_url)

        return context