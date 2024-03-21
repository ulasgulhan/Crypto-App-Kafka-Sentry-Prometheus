import requests
from ..models import APIEndpoints
from ..utilities import decode
from asgiref.sync import sync_to_async
import asyncio


# yapılacaklar servis api endpointleri dbye kaydedilsin dbdn gelsin auth header required false true gelsin



class CryptoMarketPlace():
    def __init__(self):
        self.timestamp = None
        self.db_model = None
        self.domain = None
        self.api_model = APIEndpoints
        

    def generate_headers(self, url=None, params=None):
        return None
    

    @sync_to_async
    def get_api_endpoints(self, website):
        return list(APIEndpoints.objects.filter(api_site_name=website))


    
    async def fetcher(self, auth_header_required=False, url=None, method=None, params=None):
        if params:
            if auth_header_required:
                headers = await self.generate_headers(params=params)
                response = requests.request(method, self.domain + url + '?' + params, headers=headers)
            else:
                response = requests.request(method, self.domain + url)
        else:
            if auth_header_required:
                headers = await self.generate_headers(url=url)
                response = requests.request(method, self.domain + url, headers=headers)
            else:
                response = requests.request(method, self.domain + url)
        
        return response.json()
    


