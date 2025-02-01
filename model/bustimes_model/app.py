"""
API endpoints, main entry point for the docker container
"""

from flask import render_template, request, jsonify, Flask
import json
from GTFS_Realtime.mongo_funcs import MongoManager
from GTFS_Realtime.fetch_store import VehicleUpdates

app = Flask(__name__)


@app.route("/v1/predictions", methods=["POST"])
def predict_bus():
    """
    Input: Inference input for the model
    Returns: The prediction for the bus route
    """
    json_data = request.get_json()

    response = {
            'message': "Work in progress"
            }
    return jsonify(response)


@app.route("/", methods=["GET"])
def index():
    """Returnsn main index page, mainly for testing connection"""
    return render_template("index.html")


@app.route("/mongo_contents_test", methods=["GET"])
def mongo_contents_test():
    """Return page containing the sample contents of the mongo_db database, for testing purposes"""
    mm = MongoManager()
    mongo_contents = mm.get_mongo_test()
    return render_template("mongo_contents.html", jsonfile=json.dumps(mongo_contents))


@app.route("/mongo_contents", methods=["GET"])
def mongo_contents():
    """Return page containing the sample contents of the mongo_db database, for testing purposes"""
    mm = MongoManager()
    mongo_contents = mm.get_mongo()
    return render_template("mongo_contents.html", jsonfile=json.dumps(mongo_contents, indent=4))


@app.route("/update_vehicles", methods=["GET"])
def update_vehicles():
    """Fetches the vehicles api data and updates the mongodb with it"""
    vu = VehicleUpdates()
    return jsonify(vu.update_trips())

@app.route("/delete_vehicles", methods=["GET"])
def delete_vehicles():
    mm = MongoManager()
    mm.delete_documents()
