import uuid

import aiohttp
import asyncio

import requests
from pprint import pprint

json = {
    "number": "batch-11",
    "qty": 10,
    "sku": "СТУЛ"
}
response = requests.post('http://localhost:5000/batch/add', json=json)
pprint(response.json())


def random_suffix():
    return uuid.uuid4().hex[:6]


async def allocate():
    url = 'http://localhost:5000/allocate'
    json = {
        "order_id": 1,
        "sku": "СТУЛ",
        "qty": 6
    }
    async with aiohttp.ClientSession() as session:
        for i in range(0, 20):
            json["order_id"] = random_suffix()
            async with session.post(url, json=json) as response:
                print(await response.json())

asyncio.run(allocate())

# json['order_id'] = "order-001"
# response = requests.post(url, json=json)
# pprint(response.json())

# json['order_id'] = "order-002"
# response = requests.post(url, json=json)
# pprint(response.json())

# curl --location --request POST 'http://localhost:5000/allocate' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "order_id": "order-003",
#     "sku": "СТУЛ",
#     "qty": 6
# }
# ';

# curl --location --request POST 'http://localhost:5000/allocate' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "order_id": "order-003",
#     "sku": "СТУЛ",
#     "qty": 6
# }
# ';

