from flask import Flask, g, abort, jsonify
import time
from gtfsr import GTFSR, StaticGTFSR
import bus_model
from GTFS_Static.db_funcs import get_route_id_to_name_dict
app = Flask(__name__)
load_before = time.time()
# StaticGTFSR.load_all_files()
print(f"Loaded in {time.time() - load_before} seconds")
print("Loaded")


@app.before_request
def before_request():
    """Timing Debug"""
    g.start_time = time.time()

@app.teardown_request
def teardown_request(execution=None):
    """Timing Debug"""
    diff = time.time() - g.start_time
    print(f"Request took {diff} seconds")

@app.route("/")
def test():
    return "Hello, World!"

@app.route("/vehicle")
def vehicles():
    """Directly fetches and returns the live vehicles data."""
    return GTFSR.fetch_vehicles()

@app.route("/stop")
def stops():  
    """Fetches and returns information of all stops."""
    return [stop.get_info() for stop in bus_model.Stop._all.values()]

@app.route("/stop/<stop_id>")
def stop(stop_id):
    """Fetches information for a specific stop based on stop_id or stop_code."""
    if len(stop_id) > 8:    # stop_id
        return generic_get_or_404(bus_model.Stop, stop_id)
    else:   # stop_code
        return bus_model.search_attribute(bus_model.Stop, "stop_code", stop_id)[0].get_info()

@app.route("/trip/<trip_id>")
def trips(trip_id):    
    """Fetches information for a specific trip based on trip_id."""
    return generic_get_or_404(bus_model.Trip, trip_id)

@app.route("/trip/cork")
def cork_stops():
    """Fetches all trips that are in Cork."""
    cork_routes = ["201", "202", "203", "205", "206", "207", "208", "209", "212", "213",
                    "214", "215", "216", "219", "220", "223", "225", "226", "209A", "215A",
                    "207A", "226X", "202A", "225L", "220X", "223X"]
    cork_agency_id = bus_model.search_attribute(bus_model.Agency, "agency_name", "Bus Éireann")[0].agency_id
    cork_route_ids = [route.route_id for route in bus_model.Route._all.values() if route.agency.agency_id == cork_agency_id and route.route_short_name in cork_routes]
    return bus_model.Trip.filter_by_routes(cork_route_ids)

@app.route("/agency/<agency_id>")
def agency(agency_id):
    """Fetches information for a specific agency based on agency_id."""
    return generic_get_or_404(bus_model.Agency, agency_id)

@app.route("/route/<route_id>")
def route(route_id):
    """Fetches information for a specific route based on route_id."""
    return generic_get_or_404(bus_model.Route, route_id)

@app.route("/route/search/<route_name>")
def route_search(route_name):
    """Fetches all routes that match the route_name keyword."""
    return [route.get_info() for route in bus_model.Route._all.values() if route_name in route.route_short_name]

@app.route("/shape/<shape_id>")
def shape(shape_id):
    """Fetches information for a specific shape based on shape_id."""
    return generic_get_or_404(bus_model.Shape, shape_id)

@app.route("/bus/<bus_id>")
def bus(bus_id):
    """Fetches information for a specific bus based on bus_id."""
    return generic_get_or_404(bus_model.Bus, int(bus_id))

@app.route("/route_id_to_name")
def route_id_to_name():
    """Fetches a mapping between route_id to route names"""
    return jsonify(get_route_id_to_name_dict())

@app.errorhandler(500)
def internal_server_error(e) -> dict:
    """500 Error Handler"""
    return {"error_code": 500, "error_message": "Internal Server Error"}, 500

@app.errorhandler(404)
def page_not_found(e) -> dict:
    """404 Error Handler"""
    return {"error_code": 404, "error_message": "Page not found"}, 404

def generic_get_or_404(cls, id_: str) -> dict:
    """Generic function to get info dict of any of the classes else raise a 404 error"""
    if obj := cls._all.get(id_, None):
        return obj.get_info()
    else:
        abort(404)
