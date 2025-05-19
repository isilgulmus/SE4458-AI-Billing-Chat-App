# api_gateway.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()  

BASE_URL = os.getenv("BASE_URL")
AUTH_ENDPOINT = f"{BASE_URL}/auth/login"
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def get_token():
    try:
        response = requests.post(AUTH_ENDPOINT, json={"username": USERNAME, "password": PASSWORD})
        response.raise_for_status()
        return response.json()["token"]
    except Exception as e:
        raise Exception(f"Failed to get token: {e}")

def call_api(intent: str, params: dict):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    try:
        if intent == "query_bill":
            response = requests.get(f"{BASE_URL}/Bill/QueryBill", params=params, headers=headers)
        elif intent == "query_detailed_bill":
            response = requests.get(f"{BASE_URL}/Bill/QueryDetailedBill", params=params, headers=headers)
        elif intent == "make_payment":
            response = requests.post(f"{BASE_URL}/Bill/PayBill", json=params, headers=headers)
        elif intent == "add_usage":
            response = requests.post(f"{BASE_URL}/usage", json=params, headers=headers)

        else:
            return f"Unknown intent: {intent}"

        return response.text
    except Exception as e:
        return f"[API Error] {e}"
