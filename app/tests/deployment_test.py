import asyncio
import httpx
import time
from client import get_jwt_token
import json


# URL = "http://127.0.0.1:8000"
base_url = "http://172.30.19.97:5000"
# predict_url = "http://127.0.0.1:5001"
predict_url = "http://172.30.19.97:5001"

auth_data = {"username": "CPS_DAVID_PEREZ_DEV", "password": "UIS@123FCV"}
with open("input_test.json") as f:
    data = json.load(f)
token = get_jwt_token(base_url + "/auth/token", auth_data)
# headers = {"Authorization": f"Bearer {token}"}
headers = {"token": token}


async def send_request(client, data, headers, timeout):
    try:
        response = await client.post(predict_url + "/models", json=data,
                                     headers=headers, timeout=timeout)
        return response.status_code, response.json()
    except Exception as e:
        return None, str(e)


async def main(num_requests, data, headers, timeout):
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        tasks = [send_request(client, data, headers, timeout) for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        success_responses = [r for r in responses if r[0] == 200]
        failed_responses = [r for r in responses if r[0] is None or r[0] != 200]
        
        print(f"Total requests: {num_requests}")
        print(f"Successful responses: {len(success_responses)}")
        print(f"Failed responses: {len(failed_responses)}")
        print(f"Total time taken: {end_time - start_time} seconds")
    return responses

num_requests = 1000
timeout = 300;
responses = asyncio.run(main(num_requests, data, headers, timeout))

# Extract the JSON parts of the successful responses
json_responses = [r[1] for r in responses]

# Save to a JSON file
with open('responses.json', 'w') as f:
    json.dump(json_responses, f, indent=4)

print("Responses have been saved to 'responses.json'")
