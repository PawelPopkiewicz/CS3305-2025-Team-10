"""
Gateway providing connection to frontend
"""

from flask import jsonify, Flask, Response
# from flask import request
# import requests
# from flask_cors import CORS

app = Flask(__name__)

# Backend API base URL
BACKEND_API_URL = "http://127.0.0.1:5002"

# CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

stops = [{"id": 1, "name": "Patrick Street", "lat": "-51.1242", "lon": "43.1242"},
	{"id": 2, "name": "University College Cork", "lat": "-51.2242", "lon": "43.2242"}]

arrivingBuses = [{'id':5, 'route': "220", "headsign": "MTU", "arrival": "14:44"}, 
                 {'id':6, 'route': "220x", "headsign": "UCC", "arrival": "14:56"}]

buses = [{'id':5, 'route': "220", "headsign": "MTU", 'direction':0, "lat": "-51.1242", "lon": "43.1242"},
         {'id':6, 'route': "220x", "headsign": "UCC", 'direction':1, "lat": "-51.1442", "lon": "43.2142"}]

tripInfo = [{'id':1, 'name': "Patrick Street", 'arrival': "14:44"},
            {'id':2, 'name': "University College Cork", 'arrival': "14:56"}]

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



@app.route('/v1/getStops', methods=['GET'])
def getStops():
#     try:
#         response = requests.get(f"{BACKEND_API_URL}/v1/getStops")
#         return jsonify(response.json()), response.status_code
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": "Failed to fetch stops", "details": str(e)}), 500
        return jsonify(stops)

@app.route('/v1/getArrivingBuses/<int:id>', methods=['GET'])
def getArrivingBuses(id):
#     try:
#         response = requests.get(f"{BACKEND_API_URL}/v1/getArrivingBuses/{id}")
#         return jsonify(response.json()), response.status_code
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": "Failed to fetch arriving buses", "details": str(e)}), 500
        return jsonify(arrivingBuses[id])

@app.route('/v1/getBuses', methods=['GET'])
def getBuses():
#     try:
#         response = requests.get(f"{BACKEND_API_URL}/v1/getBuses")
#         return jsonify(response.json()), response.status_code
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": "Failed to fetch buses", "details": str(e)}), 500
        return jsonify(buses)

@app.route('/v1/getTripInfo/<int:id>', methods=['GET'])
def getTripInfo(id):
#     try:
#         response = requests.get(f"{BACKEND_API_URL}/v1/getTripInfo/{id}")
#         return jsonify(response.json()), response.status_code
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": "Failed to fetch trip info", "details": str(e)}), 500
        return jsonify(tripInfo[id])


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5004)