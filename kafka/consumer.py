import django
import os
import sys
from asgiref.sync import sync_to_async

PROJE_DIZINI = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'website'))

os.chdir(PROJE_DIZINI)

sys.path.insert(0, PROJE_DIZINI)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()



from django.template.defaulttags import csrf_token
from kafka import KafkaConsumer
import json
import asyncio
import aiohttp
from account.models import Membership


async def send_request(sub, symbol, size, price, side, site):
    try:
        async with aiohttp.ClientSession() as session:
            print('before url')
            url = f"http://127.0.0.1:8000/account/copy-trade-subscribers/{int(sub)}/{str(symbol)}/{int(size)}/{int(price)}/{str(side)}/{str(site)}"
            headers = {'X-CSRFToken': csrf_token}
            async with session.post(url, headers=headers) as response:
                print('in session')
                return await response.json()
    except Exception as e:
        print(e)


async def consume():
    consumer = KafkaConsumer('copy-trade', bootstrap_servers='localhost:9092')

    for message_value in consumer:
        message = json.loads(message_value.value.decode('utf-8'))
        print(message['trader_id'])
        print(message)

        trader = await sync_to_async(Membership.objects.get)(user=message['trader_id'])
        subscribers = await sync_to_async(list)(trader.subscribers.values_list('id', flat=True))
        tasks = []
        for sub in subscribers:
            print('for loop subscribers')
            tasks.append(send_request(sub, message['symbol'], message['size'], message['price'], message['side'], message['site']))

        print('before response')
        response = await asyncio.gather(*tasks)

        print(response)


async def main():
    await consume()

if __name__ == "__main__":
    asyncio.run(main())