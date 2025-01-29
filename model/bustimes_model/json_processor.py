"""
Filters the response json data
"""

import os
import json
from gtfsr import GTFSR


class JsonProcessor():
    """Processes json data"""

    def __init__(self):
        self.gtfsr = GTFSR()
        self.route_id_to_name = {}
        self.populate_route_id_to_name("route_id_to_name.txt")

    def populate_route_id_to_name(self, filename):
        """populate dict which maps route_id to its name"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            route_file = os.path.join(base_dir, filename)
            with open(route_file, "r", encoding="utf-8") as routes:
                for line in routes:
                    route_id, route_name = line.strip("\n").split(",")
                    self.route_id_to_name[route_id] = route_name
            print(self.route_id_to_name)
        except FileNotFoundError as e:
            print(f"Route file not found: {e}")
        except Exception as e: 
            print(f"Error initializing JsonProcessor: {e}")

    def filter_cork_city_routes(self, json_data):
        """filters the vehicles.json to only cork city"""
        filtered_json = {route_name: [] for route_name in self.route_id_to_name.values()}
        for vehicle in json_data.get('entity', []):
            route_id = vehicle['vehicle']['trip']['route_id']
            print(route_id)
            if route_id in self.route_id_to_name:
                print("added a vehicle")
                filtered_json[self.route_id_to_name[route_id]].append(vehicle)
        return filtered_json

    def map_route_id_to_name(self, route_id):
        return self.route_id_to_name.get(route_id, "Uknown Route")

    def load_json_file(self, filename):
        """Tries to load a json file"""
        try:
            with open(filename, "r") as conn:
                json_file = json.load(conn)
                return json_file
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"Unexpected error when loading json file: {e}")
        return json.loads("{}")

if __name__ == "__main__":
    json_processor = JsonProcessor()
    print(json_processor.map_route_id_to_name("4398_84470"))
    print(json.dumps(json_processor.filter_cork_city_routes(json_processor.load_json_file("vehicles.json")), indent=4))

