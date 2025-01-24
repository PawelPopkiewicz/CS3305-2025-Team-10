import urllib.request, json

class GTFSR:

    def __init__(self):
        self.base_url ="https://api.nationaltransport.ie/gtfsr/v2/"
        self.json_format = "?format=json"
        self.api_key = "92aebfe6cc0045b7a5effb1ca9e171b5"

    def fetch_gtfsr(self):
        return self.fetch_endpoint("gtfsr")

    def fetch_vehicles(self):
        return self.fetch_endpoint("Vehicles")

    def fetch_tripUpdates(self):
        return self.fetch_endpoint("TripUpdates")

    def fetch_endpoint(self, endpoint):
        try: 
            url = self.base_url+endpoint+self.json_format
            
            hdr ={
            # Request headers
            'Cache-Control': 'no-cache',
            'x-api-key': self.decrypt_api_key(self.api_key),
            }

            req = urllib.request.Request(url, headers=hdr)

            req.get_method = lambda: 'GET'
            response = urllib.request.urlopen(req)
            response_data = response.read().decode('utf-8')
            json_data = json.loads(response_data)
            return json_data

        except Exception as e:
            print(e)

    def print_json(self, json_data):
        print(json.dumps(json_data, indent=4))

    def decrypt_api_key(self, encrypted_key):
        # implement decryption
        decrypted_key = encrypted_key
        return decrypted_key

    def create_json_file(self, filename, json_data):
        try:
            with open(filename, "w") as json_file:
                json.dump(json_data, json_file)
        except Exception as e:
            print(e)



if __name__ == "__main__":
    gtfsr = GTFSR()
    json_data = gtfsr.fetch_vehicles()
    #gtfsr.print_json(json_data)
    gtfsr.create_json_file("vehicles.json", json_data)


