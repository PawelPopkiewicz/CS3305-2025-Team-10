"""
Provides api for inference container
"""

import uuid
from functools import wraps
from flask import jsonify, Flask, request

from inference.bus_time_inference import BusTimesInference

app = Flask(__name__)
bus_time_inference = BusTimesInference("bus_time_prediction_model.pth")


def general_exception(func):
    """Runs the func inside a try except block, in case of failure it sends the Exception as a response"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return wrapper


@app.route("/predictions", methods=["POST"])
@general_exception
def predict_times():
    """
    Input: Inference input for the model
    Returns: The prediction for the bus route
    """
    trip_data = request.get_json()
    prediction = bus_time_inference.predict_trip(trip_data)
    return jsonify(prediction), 200


@app.route("/predictions/<model_id>", methods=["POST"])
@general_exception
def predict_times_model(model_id):
    """
    Predict the bus times with a specific model
    """
    trip_data = request.get_json()
    # query the inference package
    prediction = {
            "model_id": model_id,
            "error": "work in progress",
            "trip_data": trip_data
            }
    return jsonify(prediction), 200


@app.route("/report", methods=["GET"])
@general_exception
def generate_report():
    """Returns a report with general info about the container"""
    report = {"message": "work in progress"}
    return jsonify(report), 200


@app.route("/training_jobs", methods=["POST"])
@general_exception
def create_training_job():
    """Creates a training job which fetches latest training data and retrains the model"""
    model_id = str(uuid.uuid4())
    # store the model_id in postgresql
    # retrain the model
    response = {
            "model_id": model_id,
            "message": "Training job started"
            }
    return jsonify(response), 202


@app.route("/training_jobs/<model_id>", methods=["GET"])
@general_exception
def get_training_job_info(model_id):
    """returns the info about the model"""
    # get info on model from the postgresql
    status = "Not implemented yet"
    if status is None:
        return jsonify({"error": f"Mode with id {model_id} was not found"}), 404
    model_report = {
            "status": status,
            "model_id": model_id
            }
    return jsonify(model_report), 200
