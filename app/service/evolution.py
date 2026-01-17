import os
import requests

EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")
EVOLUTION_API_INSTANCE = os.getenv("EVOLUTION_API_INSTANCE")


class EvolutionService:

    def send_message(self, phone_number: str, message: str):
        url = f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_API_INSTANCE}"
        headers = {
            "Content-Type": "application/json",
            "apikey": EVOLUTION_API_KEY
        }
        data = {
            "number": phone_number,
            "text": message
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
