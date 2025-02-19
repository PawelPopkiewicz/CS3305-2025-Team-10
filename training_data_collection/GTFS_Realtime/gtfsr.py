"""
Provides a class to query GTFSR API
"""

import os
import urllib.request
import json
import requests
from dotenv import load_dotenv
from .get_root import get_root


class GTFSR:
    """
    Queries the GTFSR API
    """

    def __init__(self):
        self.configure()
        self.base_url = "https://api.nationaltransport.ie/gtfsr/v2/"
        self.json_format = "?format=json"
        self.api_key = os.environ.get("api_key")
        print(self.api_key)

    def configure(self):
        """Configure the setup by loading the env which contains api_key"""
        load_dotenv()

    def fetch_gtfsr(self):
        """Fetches the gtfsr endpoint which is the same as tripUpdates"""
        return self.fetch_endpoint("gtfsr")

    def fetch_vehicles(self):
        """Fetches the vehicle updates"""
        return self.fetch_endpoint("Vehicles")

    def fetch_tripUpdates(self):
        """Fetches the tripUpdates"""
        return self.fetch_endpoint("TripUpdates")

    def fetch_endpoint(self, endpoint):
        """Fetches the json data from the provided endpoint"""
        try:
            url = self.base_url+endpoint+self.json_format
            hdr = {
                'Cache-Control': 'no-cache',
                'x-api-key': self.api_key,
            }

            response = requests.get(url, headers=hdr, timeout=10)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"Error occured when connecting to and endpoint{e}")
            return None

    def print_json(self, json_data):
        """prints the provided json data"""
        print(json.dumps(json_data, indent=4))

    def create_json_file(self, filename, json_data):
        """creates a json file in the directory from the given json data"""
        try:
            root = get_root()
            with open(root / "training_data_collection" / "GTFS_Realtime" / "json_files" / filename, "w+", encoding="utf-8") as json_file:
                json.dump(json_data, json_file)
        except Exception as e:
            print(f"Error occured when creating a json file: {e}")


if __name__ == "__main__":
    gtfsr = GTFSR()
    json_vehicle_data = gtfsr.fetch_vehicles()
    gtfsr.create_json_file("vehicles.json", json_vehicle_data)
#     json_trip_data = gtfsr.fetch_tripUpdates()
#     gtfsr.create_json_file("tripUpdates.json", json_trip_data)
