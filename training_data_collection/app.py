"""
API endpoints, main entry point for the docker container
"""

from flask import Flask, Response, jsonify, render_template, request

from GTFS_Realtime.fetch_store import VehicleUpdates

app = Flask(__name__)
vu = VehicleUpdates()


@app.route("/", methods=["GET"])
def default():
    """Returns a simple json to check the connection is OK"""
    return jsonify({"connection": "OK"})


@app.route("/html", methods=["GET"])
def index():
    """Returns main index page, mainly for testing connection"""
    return render_template("index.html")


# @app.route("/test", methods=["GET"])
# def get_trips_test():
#     """Return page containing the sample contents of the mongo_db database, for testing purposes"""
#     mm = MongoManager()
#     mongo_contents = mm.get_trips_test()
#     mm.close_connection()
#     return jsonify(mongo_contents)


@app.route("/report", methods=["GET"])
def report():
    """Generates the report on collection of data"""
    collection_report = vu.generate_report()
    return jsonify(collection_report)


@app.route("/trips", methods=["GET"])
def get_trips():
    """Return contents of the mongo_db database"""
    mongo_contents = vu.get_trips()
    return jsonify(mongo_contents)


@app.route("/html/trips", methods=["GET"])
def get_html_trips():
    """Return page containing the contents of the mongo_db database"""
    mongo_contents = vu.get_trips_str()
    return Response(mongo_contents, mimetype="application/json")


@app.route("/trips", methods=["POST"])
def update_trips():
    """Fetches the vehicles api data and updates the mongodb with it"""
    try:
        fetch_update_report = vu.fetch_update_trips()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return fetch_update_report


@app.route("/trips", methods=["PUT"])
def recieve_vehicle_update():
    """Receives the json file from the GTFS /vehicles api"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "Invalid JSON or empty payload"}), 400
        put_report = vu.update_trips(json_data)
        return jsonify(put_report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/trips", methods=["DELETE"])
def delete_trips():
    """Deletes the entire mongodb
    Not implemented yet"""
    delete_report = vu.delete_trips()
    return jsonify(delete_report), 400


@app.route("/route_id_to_name", methods=["PUT"])
def receive_route_id_to_name():
    """Receives the route_id_to_name dictionary"""
    try:
        route_id_to_name = request.get_json()
        if not route_id_to_name:
            return jsonify({"error": "Invalid JSON or empty payload"}), 400
        vu.update_route_id_to_name(route_id_to_name)
        return jsonify({"message": "updated route_id_to_name"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
