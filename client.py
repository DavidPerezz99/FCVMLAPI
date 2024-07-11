import requests
import json

# Base URL of the local app
base_url = "http://127.0.0.1:5000"

# Load the input data for the predict endpoint
with open('input_test.json') as f:
    input_data = json.load(f)

# Authentication credentials
auth_data = {
    "username": "your_username",
    "password": "your_password"
}

def get_jwt_token(auth_url, auth_data):
    response = requests.post(auth_url, json=auth_data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception("Authentication failed")

# Endpoints
endpoints = {
    "home": "/",
    "status": "/status",
    "predict": "/predict"
}

# Test each endpoint
for endpoint_name, endpoint_path in endpoints.items():
    url = base_url + endpoint_path
    if endpoint_name == "predict":
        # Get JWT token
        token = get_jwt_token(base_url + "/auth", auth_data)
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(url, json=input_data, headers=headers)
    else:
        response = requests.get(url)
    
    print(f"Endpoint: {endpoint_name}")
    print(f"URL: {url}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print("="*50)

if __name__ == "__main__":
    print("Testing all endpoints...")
    # Authentication URL
    auth_url = base_url + "/auth"
    # Get JWT token for authenticated endpoints
    token = get_jwt_token(auth_url, auth_data)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    # Test home endpoint
    home_response = requests.get(base_url + endpoints["home"])
    print("Home Endpoint Response:")
    print(home_response.json())
    
    # Test status endpoint
    status_response = requests.get(base_url + endpoints["status"])
    print("Status Endpoint Response:")
    print(status_response.json())
    
    # Test predict endpoint
    predict_response = requests.post(base_url + endpoints["predict"], headers=headers, json=input_data)
    print("Predict Endpoint Response:")
    print(predict_response.json())
