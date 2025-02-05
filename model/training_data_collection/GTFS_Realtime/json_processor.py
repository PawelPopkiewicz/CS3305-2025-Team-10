"""
Filters the response json data
"""

import json
from .gtfsr import GTFSR
from GTFS_Static.db_funcs import get_route_id_to_name_dict
from .get_root import get_root


class JsonProcessor():
    """Processes json data"""

    def __init__(self):
        self.gtfsr = GTFSR()
        self.route_id_to_name = get_route_id_to_name_dict()

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

    def load_json_file(self, filename):
        """Tries to load a json file"""
        try:
            root = get_root()
            with open(root / "GTFS_Realtime" / "json_files" / filename, "r", encoding="utf-8") as conn:
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
            root = get_root()
            with open(root / "GTFS_Realtime" / "json_files" / filename, "w", encoding="utf-8") as conn:
                json.dump(json_data, conn)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except TypeError as e:
            print(f"Dump was not possible: {e}")
        except Exception as e:
            print(f"Unexpected error occured: {e}")


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
