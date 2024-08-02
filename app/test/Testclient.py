import sys
import os
import requests
import json
from fastapi.security import OAuth2PasswordRequestForm  # type: ignore
from fastapi.testclient import TestClient  # type: ignore


# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
client = TestClient(app)

# Base URL of the local app
# base_url = "http://172.30.19.97:5001"
# predict_url = "http://172.30.19.97:5001"

base_url = "http://127.0.0.1:8000"
predict_url = "http://localhost:5000"


# Load the input data for the predict endpoint
with open("app/test/input_test.json") as f:
    input_data = json.load(f)

# Authentication credentials
form_data = OAuth2PasswordRequestForm(username="user", password="pass")


def get_jwt_token(auth_url, auth_data):
    response = client.post(
        "/auth/token",
        data={"username": form_data.username, "password": form_data.password},
    )
    print(response.json())
    assert response.status_code == 200
    return response.json().get("access_token")


# Endpoints
endpoints = {"login": "/", "predict": "/predict"}

# Test each endpoint
# Get JWT token
token = get_jwt_token(base_url + "/auth/token", form_data)
headers = {"token": token}
response = requests.post(predict_url + "/models", json=input_data, headers=headers)
# else:
# response = requests.get(url)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
print("=" * 50)
