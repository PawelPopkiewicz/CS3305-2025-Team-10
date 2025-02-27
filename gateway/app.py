"""
Gateway providing connection to frontend
"""
from flask import jsonify, Flask

# from flask import request
# import requests
# from flask_cors import CORS

app = Flask(__name__)

# Backend API base URL
BACKEND_API_URL = "http://127.0.0.1:5002"

# CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins


stops = [
    {"id": 1, "name": "Patrick Street", "code": "2021", "lat": 51.8983, "lon": -8.4731},
    {"id": 2, "name": "University College Cork", "code": "2022", "lat": 51.8935, "lon": -8.4919},
    {"id": 3, "name": "Kent Station", "code": "2023", "lat": 51.9043, "lon": -8.4695},
    {"id": 4, "name": "Mahon Point", "code": "2024", "lat": 51.9005, "lon": -8.4652},
    {"id": 5, "name": "Blackpool", "code": "2025", "lat": 51.9123, "lon": -8.4734},
    {"id": 6, "name": "Douglas", "code": "2026", "lat": 51.8772, "lon": -8.4351},
    {"id": 7, "name": "Wilton", "code": "2027", "lat": 51.8841, "lon": -8.5112},
    {"id": 8, "name": "Ballincollig", "code": "2028", "lat": 51.8865, "lon": -8.5703},
]

arrivingBuses = [{'id': 5, 'route': "220", "headsign": "MTU", "arrival": "14:44"},
                 {'id': 6, 'route': "220x", "headsign": "UCC", "arrival": "14:56"}]


buses = [
    {'id': 5, 'route': "220", "headsign": "MTU", 'direction': 0, "lat": 51.8983, "lon": -8.4731},
    {'id': 6, 'route': "220x", "headsign": "UCC", 'direction': 1, "lat": 51.8935, "lon": -8.4919},
    {'id': 7, 'route': "215", "headsign": "Mahon Point", 'direction': 0, "lat": 51.9005, "lon": -8.4652},
    {'id': 8, 'route': "208", "headsign": "Lotabeg", 'direction': 1, "lat": 51.9021, "lon": -8.4789},
    {'id': 9, 'route': "205", "headsign": "Kent Station", 'direction': 0, "lat": 51.9043, "lon": -8.4695},
    {'id': 10, 'route': "203", "headsign": "Bishopstown", 'direction': 1, "lat": 51.8927, "lon": -8.4861},
]


tripInfo = [{'id':1, 'code': "2222", 'name': "Patrick Street", 'arrival': "14:44"},
            {'id':2, 'code': "3333", 'name': "University College Cork", 'arrival': "14:56"}]

@app.route("/v1/test", methods=["GET"])
def test_route():
    """
    test route
    """
    response = {
            'message': "Work in progress"
            }
    return jsonify(response)


# @app.after_request
# def add_cors_headers(response):
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
#     response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#     return response



@app.route('/v1/stops', methods=['GET'])
def get_stops():
#     try:
#         response = requests.get(f"{BACKEND_API_URL}/v1/stops")
#         return jsonify(response.json()), response.status_code
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": "Failed to fetch stops", "details": str(e)}), 500
        return jsonify(stops)

@app.route('/v1/arrivals/<int:id>', methods=['GET'])
def get_arrivals(id):
#     try:
#         response = requests.get(f"{BACKEND_API_URL}/v1/getArrivingBuses/{id}")
#         return jsonify(response.json()), response.status_code
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": "Failed to fetch arriving buses", "details": str(e)}), 500
        return jsonify(arrivingBuses[id])

@app.route('/v1/buses', methods=['GET'])
def get_buses():
#     try:
#         response = requests.get(f"{BACKEND_API_URL}/v1/buses")
#         return jsonify(response.json()), response.status_code
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": "Failed to fetch buses", "details": str(e)}), 500
        return jsonify(buses)

@app.route('/v1/trips/<int:id>', methods=['GET'])
def get_trips(id):
    if id < 10:
        return  [{'id':1, 'code': "2222", 'name': "Patrick Street", 'arrival': "14:44"},
                 {'id':2, 'code': "3333", 'name': "University College Cork", 'arrival': "14:56"}]
        #     try:
        #         response = requests.get(f"{BACKEND_API_URL}/v1/getTripInfo/{id}")
        #         return jsonify(response.json()), response.status_code
        #     except requests.exceptions.RequestException as e:
        #         return jsonify({"error": "Failed to fetch trip info", "details": str(e)}), 500
    return jsonify(tripInfo[id])


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5004)