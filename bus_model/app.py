from flask import Flask, g, abort, jsonify, request
import time, datetime
from gtfsr import GTFSR, StaticGTFSR, BustimesAPI
import bus_model
from GTFS_Static.db_funcs import get_route_id_to_name_dict

app = Flask(__name__)
load_before = time.time()
StaticGTFSR.load_all_files()


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

@app.route("/v1/vehicle")
def vehicles():
    """Directly fetches and returns the live vehicles data."""
    return GTFSR.fetch_vehicles()

@app.route("/v1/stop", methods=["GET"])
def stops():  
    """Fetches and returns information of all stops."""
    return [stop.get_info() for stop in bus_model.Stop._all.values()]

@app.route("/v1/stop/<string:stop_id>")
def stop(stop_id):
    """Fetches information for a specific stop based on stop_id or stop_code."""
    if len(stop_id) > 8:    # stop_id
        return generic_get_or_404(bus_model.Stop, stop_id)
    else:   # stop_code
        return bus_model.search_attribute(bus_model.Stop, "stop_code", stop_id)[0].get_info()

@app.route("/v1/trip/<string:trip_id>")
def trips(trip_id):    
    """Fetches information for a specific trip based on trip_id."""
    return generic_get_or_404(bus_model.Trip, trip_id)

@app.route("/v1/trip/cork")
def cork_stops():
    """Fetches all trips that are in Cork."""
    cork_routes = ["201", "202", "203", "205", "206", "207", "208", "209", "212", "213",
                    "214", "215", "216", "219", "220", "223", "225", "226", "209A", "215A",
                    "207A", "226X", "202A", "225L", "220X", "223X"]
    cork_agency_id = bus_model.search_attribute(bus_model.Agency, "agency_name", "Bus Éireann")[0].agency_id
    cork_route_ids = [route.route_id for route in bus_model.Route._all.values() if route.agency.agency_id == cork_agency_id and route.route_short_name in cork_routes]
    return bus_model.Trip.filter_by_routes(cork_route_ids)

@app.route("/v1/agency/<string:agency_id>")
def agency(agency_id):
    """Fetches information for a specific agency based on agency_id."""
    return generic_get_or_404(bus_model.Agency, agency_id)

@app.route("/v1/route/<string:route_id>")
def route(route_id):
    """Fetches information for a specific route based on route_id."""
    return generic_get_or_404(bus_model.Route, route_id)

@app.route("/v1/route/search/<string:route_name>")
def route_search(route_name):
    """Fetches all routes that match the route_name keyword."""
    return [route.get_info() for route in bus_model.Route._all.values() if route_name in route.route_short_name]

@app.route("/v1/shape/<string:shape_id>")
def shape(shape_id):
    """Fetches information for a specific shape based on shape_id."""
    return generic_get_or_404(bus_model.Shape, shape_id)

@app.route("/v1/bus/<string:bus_id>")
def bus(bus_id):
    """Fetches information for a specific bus based on bus_id."""
    all_stops: list = []
    bus_obj = bus_model.Bus._all.get(bus_id, None)
    if bus_obj:
        trip = bus_model.Trip._all.get(bus_obj.latest_trip, None)
        if trip:
            stop_timestamps = trip.get_schedule_times()
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            for stop, timestamp in stop_timestamps.get(today, []):
                data = {
                        "stop_id": stop.stop_id,
                        "stop_code": stop.stop_code,
                        "stop_name": stop.stop_name,
                        "arrival": timestamp
                        }
                all_stops.append(data)
            return {"stops": all_stops}
    return abort(404)


@app.route("/v1/bus")
def buses():
    """Fetches information for all buses."""
    return bus_model.Bus.get_all_buses()

@app.route("/v1/route_id_to_name")
def route_id_to_name():
    """Fetches a mapping between route_id to route names"""
    return jsonify(get_route_id_to_name_dict())

@app.route("/v1/update_realtime", methods=["GET"])
def update_realtime():
    """Takes the fetched data and populates the model."""
    data = GTFSR.fetch_vehicles()
    entities = data.get("entity", [])
    if entities:
        for entity in entities:
            try:
                trip_id = entity["vehicle"]["trip"]["trip_id"]
                route_id = entity["vehicle"]["trip"]["route_id"]
                vehicle_id = entity["vehicle"]["vehicle"]["id"]
                timestamp = int(entity["vehicle"]["timestamp"])
                latitude = float(entity["vehicle"]["position"]["latitude"])
                longitude = float(entity["vehicle"]["position"]["longitude"])
                bus = bus_model.Bus._all.get(vehicle_id, None)
                if bus:
                    bus.add_live_update(trip_id=trip_id, route_id=route_id, timestamp=timestamp, latitude=latitude, longitude=longitude)
            except KeyError as e:
                print(f"KeyError: {e}")
                continue
    return "Success"

@app.route("/v1/update_static", methods=["GET"])
def update_static():
    """Takes the fetched data and populates the model."""
    StaticGTFSR.load_all_files()
    return "Success"

@app.route("/v1/update_bus", methods=["GET"])
def update_bus():
    """Updates the bus data."""
    data = BustimesAPI.fetch_vehicles()
    if data:
        for bus in data:
            cleaned_slug = bus["slug"].replace("ie-", "")
            bus_obj = bus_model.Bus(slug=cleaned_slug) if cleaned_slug not in bus_model.Bus._all else bus_model.Bus._all[cleaned_slug]
            v_type = bus.get("vehicle_type") or {}
            bus_obj.set_details(
                reg=bus.get("reg", ""),
                fleet_code=bus.get("fleet_code", ""),
                name=v_type.get("name", ""),
                style=v_type.get("style", ""),
                fuel=v_type.get("fuel", ""),
                double_decker=v_type.get("double_decker", ""),
                coach=v_type.get("coach", ""),
                electric=v_type.get("electric", ""),
                livery=bus.get("livery", {}),
                withdrawn=bus.get("withdrawn", ""),
                special_features=bus.get("special_features", "")
            )
        return "Success"
    return "Failed"

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

update_bus()    # Update the bus data on startup
update_realtime()    # Update the realtime data on startup
print(f"Loaded in {time.time() - load_before} seconds")
print("Loaded")