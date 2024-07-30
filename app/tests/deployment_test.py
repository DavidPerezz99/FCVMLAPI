import asyncio
import httpx
import time
from app.tests.client import get_jwt_token
import json 


URL = "http://127.0.0.1:8000" 
auth_data = {
    "username": "CPS_DAVID_PEREZ_DEV",
    "password": "UIS@123FCV"
}
with open('input_test.json') as f:
    data = json.load(f)
token = get_jwt_token(URL + "/auth/token", auth_data)
headers = {'Authorization': f'Bearer {token}'}


async def send_request(client, data, headers):
    try:
        response = await client.post(URL + "/predict", json=data, headers = headers)
        return response.status_code, response.json()
    except Exception as e:
        return None, str(e)

async def main(num_requests, data, headers):
    async with httpx.AsyncClient() as client:
        tasks = [send_request(client, data, headers) for _ in range(num_requests)]
        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        success_responses = [r for r in responses if r[0] == 200]
        failed_responses = [r for r in responses if r[0] is None or r[0] != 200]
        
        print(f"Total requests: {num_requests}")
        print(f"Successful responses: {len(success_responses)}")
        print(f"Failed responses: {len(failed_responses)}")
        print(f"Total time taken: {end_time - start_time} seconds")

num_requests = 1000
asyncio.run(main(num_requests, data, headers))
