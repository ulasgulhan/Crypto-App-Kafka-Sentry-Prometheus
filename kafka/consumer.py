import django
import os
import sys
from asgiref.sync import sync_to_async


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'website'))

os.chdir(PROJECT_DIR)

sys.path.insert(0, PROJECT_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from kafka import KafkaConsumer
import json
import asyncio
import aiohttp
from account.models import Membership
from dotenv import load_dotenv


load_dotenv()

async def get_csrf_token(session):
    async with session.get(os.getenv('GET_CSRF_TOKEN')) as response:
        return await response.text()

async def send_request(session, sub, symbol, size, price, side, site):
    try:
        csrf_token = await get_csrf_token(session)
        headers = {'X-CSRFToken': csrf_token}
        base_url = os.getenv('BASE_URL_COPY_TRADE')
        url = f"{base_url}/{int(sub)}/{str(symbol)}/{int(size)}/{int(price)}/{str(side)}/{str(site)}"
        async with session.request('POST', url, headers=headers) as response:
            data = await response.json()
            return await response.json()
    except Exception as e:
        print(e)


async def consume():
    consumer = KafkaConsumer('copy-trade', bootstrap_servers='localhost:9092')

    async with aiohttp.ClientSession() as session:
        for message_value in consumer:
            message = json.loads(message_value.value.decode('utf-8'))
            print(message)

            trader = await sync_to_async(Membership.objects.get)(user=message['trader_id'])
            subscribers = await sync_to_async(list)(trader.subscribers.values_list('id', flat=True))
            tasks = []
            for sub in subscribers:
                tasks.append(send_request(session, sub, message['symbol'], message['size'], message['price'], message['side'], message['site']))

            response = await asyncio.gather(*tasks)
            print(response)


async def main():
    await consume()

if __name__ == "__main__":
    asyncio.run(main())