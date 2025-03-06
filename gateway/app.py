"""
Gateway providing connection to frontend
"""
from flask import Flask, abort, jsonify
import requests
import os
import datetime

import json

app = Flask(__name__)

# Backend API base URL

BUS_MODEL_URI = os.getenv("BUS_MODEL_URI")

DEBUG = True
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, flush=True)

tripInfo = [{'id': 1, 'code': "2222", 'name': "Patrick Street", 'arrival': "14:44"},
            {'id': 2, 'code': "3333", 'name': "University College Cork", 'arrival': "14:56"}]


@app.route("/v1/test", methods=["GET"])
def test_route():
    """
    test route
    """
    response = {
        'message': "Hello World"
    }
    return response


@app.route("/v1/test_bus", methods=["GET"])
def test_bus():
    """
    test bus route
    """
    try:
        response = requests.get(f"{BUS_MODEL_URI}/")
        if response.status_code == 200:
            return response.json()          # Standard response
        elif response.status_code == 404:
            return abort(404)               # Not found
        else:
            debug_print("Failed to fetch buses", e)
            return abort(500, "Failed to fetch buses")
    except requests.exceptions.RequestException as e:
        debug_print("Failed to fetch buses", e)
        return abort(500, "Failed to fetch buses")  # Any other status code

@app.route("/v1/routes", methods=["GET"])
def get_all_routes():
    """
    get all routes
    """
    try:
        response = requests.get(f"{BUS_MODEL_URI}/v1/route")
        if response.status_code == 200:
            return response.json()          # Standard response
        elif response.status_code == 404:
            return abort(404)               # Not found
        else:
            debug_print("Failed to fetch routes", e)
            return abort(500, "Failed to fetch routes")
    except requests.exceptions.RequestException as e:
        debug_print("Failed to fetch routes", e)
        return abort(500, "Failed to fetch routes")

@app.route('/v1/stops', methods=['GET'])
def get_stops():
    """Fetches the details and location of all stops."""

    try:
        response = requests.get(f"{BUS_MODEL_URI}/v1/stops")
        if response.status_code == 200:
            # Print formatted result
            return response.json()         # Standard response
        elif response.status_code == 404:
            return abort(404)               # Not found
        else:
            debug_print("Failed to fetch stops", e)
            return abort(500, "Failed to fetch stops")  # Any other status code
    except requests.exceptions.RequestException as e:
        debug_print("Failed to fetch stops", e)
        return abort(500, "Failed to fetch stops")      # Any other exception


@app.route('/v1/arrivals/<string:stop_id>', methods=['GET'])
def stop_arrivals(stop_id: str):
    """Fetches the predicted arrival times for each bus at the given stop."""

    try:
        response = requests.get(f"{BUS_MODEL_URI}/v1/stop/arrivals/{stop_id}")
        if response.status_code == 200:
            data = [{
                "id": bus["id"],
                "route": bus["route"],
                "headsign": bus["headsign"],
                "arrival": datetime.datetime.fromtimestamp(bus["arrival"]).strftime('%H:%M'),
                } for bus in response.json()]
            return data                     # Standard response
        elif response.status_code == 404:
            return abort(404)               # Not found
        else:
            # Any other status code
            debug_print("Failed to fetch buses for the given stop", e)
            return abort(500, "Failed to fetch buses for the given stop")
    except requests.exceptions.RequestException as e:
        debug_print("Failed to fetch buses for the given stop", e)
        return abort(500, "Failed to fetch buses for the given stop")


@app.route('/v1/buses', methods=['GET'])
def get_buses():
    """Fetches details for all buses, including location."""

    try:
        response = requests.get(f"{BUS_MODEL_URI}/v1/bus")
        if response.status_code == 200:
            return response.json()          # Standard response
        elif response.status_code == 404:
            return abort(404)               # Not found
        else:
            debug_print("Failed to fetch all buses", e)
            return abort(500, "Failed to fetch all buses")
    except requests.exceptions.RequestException as e:
        debug_print("Failed to fetch all buses", e)
        return abort(500, "Failed to fetch all buses")


@app.route('/v1/trips/<string:bus_id>', methods=['GET'])
def get_trips(bus_id: str):
    """Fetches predicted times and stops for a bus."""

    try:
        response = requests.get(f"{BUS_MODEL_URI}/v1/bus/{bus_id}")
        if response.status_code == 200:
            data = [{
                "id": stop["id"], 
                "code": stop["code"], 
                "name": stop["name"], 
                "arrival": datetime.datetime.fromtimestamp(stop["arrival"]).strftime('%H:%M'),
                } for stop in response.json()]
            return data                     # Standard response
        elif response.status_code == 404:
            return abort(404)               # Not found
        else:
            debug_print("Failed to fetch trip info", e)
            return abort(500, "Failed to fetch trip info")
    except requests.exceptions.RequestException as e:
        debug_print("Failed to fetch trip info", e)
        return abort(500, "Failed to fetch trip info")


@app.errorhandler(500)
def internal_server_error(e):
    """500 Error Handler"""
    return {"error_code": 500, "error_message": e.description}, 500


@app.errorhandler(404)
def page_not_found(e):
    """404 Error Handler"""
    return {"error_code": 404, "error_message": "Page not found"}, 404
