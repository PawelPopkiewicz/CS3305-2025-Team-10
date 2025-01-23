import json
from gtfsr import GTFSR

class JsonProcesser():

    def __init__(self):
        self.gtfsr = GTFSR()
        self.route_id_to_name = {}
        try:
            with open("route_id_to_route_name.txt", "r") as routes:
                for line in routes:
                    route_id, route_name = line.strip("\n").split(",")
                    self.route_id_to_name[route_id] = route_name
        except Exception as e: 
            print(e)

    def filter_cork_city_routes(self, json):
        filtered_json = {}
        for route_name in self.route_id_to_name.values():
            filtered_json[route_name] = []
        print(filtered_json)
        for vehicle in dict(json)['entity']:
            route_id =  vehicle['vehicle']['trip']['route_id']            
            if route_id in self.route_id_to_name.keys():
                filtered_json[self.route_id_to_name[route_id]].append(vehicle)
        return filtered_json
        
    def map_route_id_to_name(self, route_id):
        return self.route_id_to_name[route_id]

    def load_json_file(self, filename):
        try:
            with open(filename, "r") as conn:
                json_file = json.load(conn)
                return json_file
        except Exception as e:
            print(e)

if __name__ == "__main__":
    json_processer = JsonProcesser()
    print(json_processer.map_route_id_to_name("4398_84470"))
    print(json.dumps(json_processer.filter_cork_city_routes(json_processer.load_json_file("vehicles.json")), indent=4))

