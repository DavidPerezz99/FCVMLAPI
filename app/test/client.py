import requests
import json
from fastapi.security import OAuth2PasswordRequestForm  # type: ignore


base_url = "http://127.0.0.1:8000"
predict_url = "http://localhost:5000"


with open("app/test/input_test.json") as f:
    input_data = json.load(f)

# Authentication credentials
# form_data = OAuth2PasswordRequestForm(username="user", password="pass")
form_data = {"username": "user", "password": "pass"}


def get_jwt_token(auth_url, auth_data):
    try:
        response = requests.post(auth_url,
                                 data=auth_data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


token_data = get_jwt_token(base_url + "/auth/token", form_data)
print(token_data)

if token_data:
    token = token_data.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(base_url + "/predict",
                             json=input_data,
                             headers=headers)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
else:
    print("Failed to obtain JWT token.")
