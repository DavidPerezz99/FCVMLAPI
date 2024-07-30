import asyncio
import httpx
import time

URL = "http://127.0.0.1:8000/predict"  

async def send_request(client, data):
    try:
        response = await client.post(URL, json=data)
        return response.status_code, response.json()
    except Exception as e:
        return None, str(e)

async def main(num_requests, data):
    async with httpx.AsyncClient() as client:
        tasks = [send_request(client, data) for _ in range(num_requests)]
        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        success_responses = [r for r in responses if r[0] == 200]
        failed_responses = [r for r in responses if r[0] is None or r[0] != 200]
        
        print(f"Total requests: {num_requests}")
        print(f"Successful responses: {len(success_responses)}")
        print(f"Failed responses: {len(failed_responses)}")
        print(f"Total time taken: {end_time - start_time} seconds")


test_data = {
    "feature1": "value1",
    "feature2": "value2",

}

num_requests = 1000

asyncio.run(main(num_requests, test_data))
