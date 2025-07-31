import os
import requests
from dotenv import load_dotenv

class AlgoTestClient:
    def __init__(self, phone_number: str, main_url: str):
        load_dotenv()
        self.base_url = main_url
        self.phone_number = phone_number
        self.password = os.getenv("PASSWORD", "default_password")
        self.session = requests.Session()
        self.csrf_token = None
        self.jwt_token = None

        self.login()

    def login(self):
        login_payload = {
            "phoneNumber": self.phone_number,
            "password": self.password,
        }

        headers = {"Content-Type": "application/json"}
        response = self.session.post(f"{self.base_url}/login", json=login_payload, headers=headers)

        if response.status_code == 200:
            self.csrf_token = self.session.cookies.get("csrf_access_token")
            self.jwt_token = self.session.cookies.get("access_token_cookie")

            self.session.headers.update({
                "X-CSRF-TOKEN-ACCESS": self.csrf_token,
                "Authorization": self.jwt_token,
            })

            print("Login successful!")
        else:
            raise Exception(f"Login failed: {response.status_code}, {response.text}")

    def get_session(self):
        return self.session

    def get_tokens(self):
        return {
            "X-CSRF-TOKEN-ACCESS": self.csrf_token,
            "Authorization": self.jwt_token,
        }


