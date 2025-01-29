"""
Filters the response json data
"""

import os
import json
from db_funcs import get_route_id_to_name_dict
from gtfsr import GTFSR


class JsonProcessor():
    """Processes json data"""

    def __init__(self):
        self.gtfsr = GTFSR()
        self.route_id_to_name = get_route_id_to_name_dict()

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

    def filter_vehicles(self, vehicles_json):
        """filters the vehicles.json to only cork city"""
        entities = vehicles_json.get("entity", [])
        entity_count = len(entities)
        for i in range(len(entities)-1, -1, -1):
            route_id = entities[i]["vehicle"]["trip"]["route_id"]
            if route_id not in self.route_id_to_name:
                entities.pop(i)
        print(f"Removed {entity_count - len(entities)} out of {entity_count}, {len(entities)} remaining")

    def filter_tripUpdates(self, tripUpdates_json):
        """Filter the tripUpdates json to include only cork city"""
        entities = tripUpdates_json.get("entity", [])
        entity_count = len(entities)
        for i in range(len(entities)-1, -1, -1):
            route_id = entities[i]["trip_update"]["trip"]["route_id"]
            if route_id not in self.route_id_to_name:
                entities.pop(i)
        print(f"Removed {entity_count - len(entities)} out of {entity_count}, {len(entities)} remaining")

    def convert_vehicles(self, vehicles_json):
        """Converts the raw vehicles.json data into the data which could would be stored"""


    def convert_tripUpdates(self, tripUdates_json):
        """Converts the raw tripUpdates.json data into storable format"""

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

    def print_json(self, json_data):
        """prints json data to stdout"""
        print(json.dumps(json_data, indent=4))

    def create_json_file(self, json_data, filename):
        """creates a json file from the provided dict"""
        try:
            with open(filename, "w", encoding="utf-8") as conn:
                json.dump(json_data, conn)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except TypeError as e:
            print(f"Dump was not possible: {e}")
        except Exception as e:
            print("Unexpected error occured: {e}")


if __name__ == "__main__":
    json_processor = JsonProcessor()
    tu_json = json_processor.load_json_file("tripUpdates.json")
    json_processor.filter_tripUpdates(tu_json)
    json_processor.filter_tripUpdates(tu_json)
    json_processor.create_json_file(tu_json, "filtered_tripUpdates.json")
    v_json = json_processor.load_json_file("vehicles.json")
    json_processor.filter_vehicles(v_json)
    json_processor.filter_vehicles(v_json)
    json_processor.create_json_file(v_json, "filtered_vehicles.json")
