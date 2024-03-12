import requests
import time
from ..models import BitGetAPI, BybitAPI
from ..utilities import generate_signature


# yapılacaklar servis api endpointleri dbye kaydedilsin dbdn gelsin auth header required false true gelsin



class CryptoMarketPlace():
    def __init__(self):
        self.timestamp = None
        self.db_model = None
        self.domain = None

    def generate_headers(self, url=None):
        return None


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


    def get_api_endpoints(self):
        return {
            'account': {'url': '/api/v2/mix/account/account?symbol=btcusdt&productType=USDT-FUTURES&marginCoin=usdt', "auth_required": True, "method": "GET"},
            'personal_info': {'url': '/api/v2/spot/account/info', "auth_required": True, "method": "GET" },
            'account_assets':{'url': '/api/v2/spot/account/assets?assetType=all', "auth_required": True, "method": "GET" }, 
            'coins': {"url":"/api/v2/spot/market/tickers", "auth_required": False, "method": "GET" } 
        }

    def generate_headers(self, endpoint_path):
        api_info = BitGetAPI.objects.filter(user=self.user)

        message = self.timestamp + 'GET' + endpoint_path


        for api in api_info:
            access_key = api.api_key
            access_passphrase = api.access_passphrase
            secret_key = api.secret_key

        headers = {
            'ACCESS-TIMESTAMP': self.timestamp,
            'ACCESS-KEY': access_key,
            'ACCESS-PASSPHRASE': access_passphrase,
        }

        signature = generate_signature(secret_key, message)

        headers['ACCESS-SIGN'] = signature

        return headers
    

    def get_api_data(self):
        context = {}

        api_endpoints = self.get_api_endpoints()
        
        for endpoint_name, endpoint_data in api_endpoints.items():
            context[endpoint_name] = self.fetcher(endpoint_data.get("auth_required"), url=endpoint_data.get("url"))

        return context