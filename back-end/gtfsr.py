import requests
import os
from dotenv import load_dotenv

load_dotenv()


class GTFSR:
    base_url = "https://api.nationaltransport.ie/gtfsr/v2/"
    format_json = "?format=json"
    api_key = os.getenv("API_KEY", None)

    def __init__(self) -> None:
        pass

    @classmethod
    def fetch_vehicles(self) -> dict:
        return self.fetch_endpoint("Vehicles")

    @classmethod
    def fetch_trip_updates(self) -> dict:
        return self.fetch_endpoint("TripUpdates")

    @classmethod
    def fetch_gtfsr(self) -> dict:
        return self.fetch_endpoint("gtfsr")

    @classmethod
    def fetch_endpoint(self, endpoint: str) -> dict:
        url = self.base_url + endpoint + self.format_json
        headers = {
            'Cache-Control': 'no-cache',
            'x-api-key': self.api_key
        }

        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            return None
        return response.json()


if __name__ == "__main__":
    # quick debugging
    print(GTFSR.fetch_endpoint("TripUpdates"))
