"""
API endpoints, main entry point for the docker container
"""

from flask import render_template, request, jsonify, Flask
import json
from GTFS_Realtime.mongo_funcs import MongoManager

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
    print("entered the mongo_contents_test route")
    mm = MongoManager()
    print("testing the mongodb")
    mongo_contents = mm.get_mongo_test()
    return render_template("mongo_contents.html", jsonfile=json.dumps(mongo_contents))


@app.route("/mongo_contents", methods=["GET"])
def mongo_contents():
    """Return page containing the sample contents of the mongo_db database, for testing purposes"""
    print("entered the real deal")
    mm = MongoManager()
    mm.make_skeleton()
    print("made skeleton")
    mongo_contents = mm.get_mongo()
    print("fetched data")
    return render_template("mongo_contents.html", jsonfile=json.dumps(mongo_contents))
