"""
API endpoints, main entry point for the docker container
"""

from flask import render_template, jsonify, Flask, Response
from GTFS_Realtime.mongo_funcs import MongoManager
from GTFS_Realtime.fetch_store import VehicleUpdates

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Returns main index page, mainly for testing connection"""
    return render_template("index.html")


@app.route("/trips_test", methods=["GET"])
def get_trips_test():
    """Return page containing the sample contents of the mongo_db database, for testing purposes"""
    mm = MongoManager()
    mongo_contents = mm.get_trips_test()
    mm.close_connection()
    return jsonify(mongo_contents)


@app.route("/trips", methods=["GET"])
def get_trips():
    """Return page containing the sample contents of the mongo_db database, for testing purposes"""
    mm = MongoManager()
    mongo_contents = mm.get_trips()
    mm.close_connection()
    return Response(mongo_contents, mimetype="application/json")


@app.route("/trips", methods=["POST"])
def update_trips():
    """Fetches the vehicles api data and updates the mongodb with it"""
    vu = VehicleUpdates()
    return jsonify(vu.update_trips())


@app.route("/trips", methods=["DELETE"])
def delete_trips():
    """Deletes the entire mongodb"""
    mm = MongoManager()
    mm.delete_trips()
    mm.close_connection()
    return jsonify({"delete": "ok"})
