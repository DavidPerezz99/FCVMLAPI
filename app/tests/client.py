import requests
import json

# Base URL of the local app
base_url = "http://172.30.19.97:5001"
predict_url = "http://172.30.19.97:5001"

# Load the input data for the predict endpoint
with open('input_test.json') as f:
    input_data = json.load(f)

# Authentication credentials
auth_data = {
    "username": "user",
    "password": "pass"
}

def get_jwt_token(auth_url, auth_data):
    response = requests.post(auth_url, json=auth_data)
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
response = requests.post(predict_url+ "/predict", json=input_data)
#else:
    #response = requests.get(url)
    
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
print("="*50)
