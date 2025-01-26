import requests
import os
import csv
import bus_model

from dotenv import load_dotenv


load_dotenv()


class GTFSR:
    """A class to make requests to the GTFSR API. All methods can be used without initialising the class."""
    base_url = "https://api.nationaltransport.ie/gtfsr/v2/"
    format_json = "?format=json"
    api_key = os.getenv("API_KEY", None)

    @classmethod
    def fetch_vehicles(self) -> dict:
        """
        Fetches the vehicles endpoint from the GTFSR API.

        Returns:
            dict: The response from the GTFSR API
        """
        return self.fetch_endpoint("Vehicles")

    @classmethod
    def fetch_trip_updates(self) -> dict:
        """
        Fetches the trip_updates endpoint from the GTFSR API.

        Returns:
            dict: The response from the GTFSR API
        """
        return self.fetch_endpoint("TripUpdates")

    @classmethod
    def fetch_gtfsr(self) -> dict:
        """
        Fetches the gtfsr endpoint from the GTFSR API.

        Returns:
            dict: The response from the GTFSR API
        """
        return self.fetch_endpoint("gtfsr")

    @classmethod
    def fetch_endpoint(self, endpoint: str) -> dict:
        """
        Makes a request to the GTFSR API at the specified endpoint.

        Returns:
            dict: A JSON formatted response from the GTFSR API
        """
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

class StaticGTFSR:
    """A class to parse the static csv-format GTFSR data."""
    static_folder = "back-end/static_gtfsr/"
    agency  = static_folder + "agency.txt"
    stops   = static_folder + "stops.txt"
    routes  = static_folder + "routes.txt"
    trips   = static_folder + "trips.txt"
    stop_times = static_folder + "stop_times.txt"
    calendar = static_folder + "calendar.txt"
    calendar_dates = static_folder + "calendar_dates.txt"
    shapes = static_folder + "shapes.txt"
    feed_info = static_folder + "feed_info.txt"

    @classmethod
    def read_routes(self, path=routes):
        with open(path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                bus_model.Route(row['route_id'], row['agency_id'], row['route_short_name'], row['route_long_name'], row['route_type'])

    @classmethod
    def read_stops(self, path=stops):
        with open(path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                bus_model.Stop(row['stop_id'], row['stop_code'] or None, row['stop_name'], row['stop_lat'], row['stop_lon'])        

if __name__ == "__main__":
    # quick debugging
    StaticGTFSR.read_routes()
