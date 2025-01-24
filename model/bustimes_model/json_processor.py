import os
import json
from gtfsr import GTFSR

class JsonProcessor():

    def __init__(self):
        self.gtfsr = GTFSR()
        self.route_id_to_name = {}
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            route_file = os.path.join(base_dir, "route_id_to_route_name.txt")
            with open(route_file, "r") as routes:
                for line in routes:
                    route_id, route_name = line.strip("\n").split(",")
                    self.route_id_to_name[route_id] = route_name
        except FileNotFoundError as e:
            print("Route file not found: %s" % (s))
        except Exception as e: 
            print("Error initializing JsonProcessor: %s" % (s))

    def filter_cork_city_routes(self, json_data):
        filtered_json = {route_name:[] for route_name in self.route_id_to_name.values()}
        for vehicle in json_data.get('entity', []):
            route_id =  vehicle['vehicle']['trip']['route_id']            
            if route_id in self.route_id_to_name:
                filtered_json[self.route_id_to_name[route_id]].append(vehicle)
        return filtered_json
        
    def map_route_id_to_name(self, route_id):
        return self.route_id_to_name.get(route_id, "Uknown Route")

    def load_json_file(self, filename):
        try:
            with open(filename, "r") as conn:
                json_file = json.load(conn)
                return json_file
        except FileNotFoundError as e:
            print("File not found: %s" % (e))
        except json.JSONDecodeError as e:
            print("Error decoding JSON: %s" % (e))
        except Exception as e:
            print("Unexpected error when loading json file: %s" % (e))


if __name__ == "__main__":
    json_processor = JsonProcessor()
    print(json_processor.map_route_id_to_name("4398_84470"))
    print(json.dumps(json_processor.filter_cork_city_routes(json_processor.load_json_file("vehicles.json")), indent=4))

