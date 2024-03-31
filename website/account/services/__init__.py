from ..models import APIEndpoints, CryptoMarketAPICredentials
from asgiref.sync import sync_to_async
import json



# yapılacaklar servis api endpointleri dbye kaydedilsin dbdn gelsin auth header required false true gelsin



class CryptoMarketPlace():
    def __init__(self):
        self.timestamp = None
        self.db_model = CryptoMarketAPICredentials
        self.domain = None
        self.api_model = APIEndpoints
        

    def generate_headers(self, url=None, params=None, method=None):
        return None
    

    @sync_to_async
    def get_api_endpoints(self, crypto_market):
        return list(APIEndpoints.objects.filter(crypto_market=crypto_market))


    
    async def fetcher(self, session, auth_header_required=False, url=None, method=None, params=None):
        if params:
            if auth_header_required and method == 'POST':
                headers = await self.generate_headers(url=url, params=params, method=method)
            elif auth_header_required:
                headers = await self.generate_headers(params=params)
            else:
                headers = None
            
            if url == '/api/v2/mix/order/place-order':
                async with session.request(method, self.domain + url, headers=headers, json=params) as response:
                    return await response.json()
            else:
                async with session.request(method, self.domain + url + '?' + params, headers=headers) as response:
                    return await response.json()
        else:
            if auth_header_required:
                headers = await self.generate_headers(url=url)
            else:
                headers = None
            async with session.request(method, self.domain + url, headers=headers) as response:
                return await response.json()
    


