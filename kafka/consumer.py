import django
import os
import sys
from asgiref.sync import sync_to_async

PROJE_DIZINI = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'website'))

os.chdir(PROJE_DIZINI)

sys.path.insert(0, PROJE_DIZINI)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

# http://127.0.0.1:8000/account/copy-trade-subscribers/{int(sub)}/{str(symbol)}/{int(size)}/{int(price)}/{str(side)}/{str(site)}

""" params = {
            'sub': int(sub),
            'symbol': str(symbol),
            "size": int(size),
            "price": int(price),
            "side": str(side),
            'site': str(site)
        } """

from django.template.defaulttags import csrf_token
from kafka import KafkaConsumer
import json
import asyncio
import aiohttp
from account.models import Membership


async def get_csrf_token(session):  # Helper function to fetch CSRF token
    async with session.get('http://127.0.0.1:8000/account/csrf_token/') as response:
        return await response.text()

async def send_request(session, sub, symbol, size, price, side, site):
    try:
        csrf_token = await get_csrf_token(session)  # Fetch token before sending request
        headers = {'X-CSRFToken': csrf_token}
        print('before url')
        url = f"http://127.0.0.1:8000/account/copy-trade-subscribers/{int(sub)}/{str(symbol)}/{int(size)}/{int(price)}/{str(side)}/{str(site)}"

        async with session.request('POST', url, headers=headers) as response:
            print('in session')
            if response.status == 200:
                data = await response.json()
                print(data)
                return await response.json()
            else:
                print(f"Error sending request: {response.status}")
    except Exception as e:
        print(e)


async def consume():
    consumer = KafkaConsumer('copy-trade', bootstrap_servers='localhost:9092')

    async with aiohttp.ClientSession() as session:
        for message_value in consumer:
            message = json.loads(message_value.value.decode('utf-8'))
            print(message['trader_id'])
            print(message)

            trader = await sync_to_async(Membership.objects.get)(user=message['trader_id'])
            subscribers = await sync_to_async(list)(trader.subscribers.values_list('id', flat=True))
            tasks = []
            for sub in subscribers:
                print('for loop subscribers')
                tasks.append(send_request(session, sub, message['symbol'], message['size'], message['price'], message['side'], message['site']))

            response = await asyncio.gather(*tasks)
            print(response)


async def main():
    await consume()

if __name__ == "__main__":
    asyncio.run(main())