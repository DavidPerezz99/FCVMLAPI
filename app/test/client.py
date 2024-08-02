import requests
import json

# Base URL of the local app
base_url = "http://127.0.0.1:8000"
predict_url = "http://127.0.0.1:8000"

# Load the input data for the predict endpoint
with open('input_test.json') as f:
    input_data = json.load(f)

# Authentication credentials
auth_data = {
    "username": "CPS_DAVID_PEREZ_DEV",
    "password": "UIS@123FCV"
}

def get_jwt_token(auth_url, auth_data):
    response = requests.post(auth_url, data=auth_data)
    print(response.json().get('access_token'))
    return response.json().get('access_token')
    #if response.status_code == 200:
    #    return response.json().get('access_token')
    #else:
    #    raise Exception("Authentication failed")

# Endpoints
endpoints = {
    "login": "/",
    "predict": "/predict"
}

# Test each endpoint
    # Get JWT token
token = get_jwt_token(base_url + "/auth/token", auth_data)
headers = {'token':token}
response = requests.post(predict_url+ "/predict", json=input_data, headers = headers)
#else:
    #response = requests.get(url)
    
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
print("="*50)

response_validate_user = requests.get(predict_url+ "/", json=headers)
print(f"Active User is: {response_validate_user.json()}")

