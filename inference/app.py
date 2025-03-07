"""
Provides api for inference container
"""

import uuid
from functools import wraps
from flask import jsonify, Flask, request

from inference.bus_time_inference import BusTimesInference
from inference.process_json import process_json

app = Flask(__name__)
bus_time_inference = BusTimesInference("bus_time_prediction_model_3.pth")


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
    trip = process_json(trip_data)
    if trip is None:
        raise ValueError("Invalid trip data")
    bus_time_inference.predict_trip(trip)
    json_prediction = {
            "stops": trip.display_df().to_dict("records"),
            "delay": trip.current_delay,
            "trip_id": trip.trip_id
            }
    return jsonify(json_prediction), 200


@app.route("/predictions/test", methods=["GET"])
@general_exception
def test_prediction():
    """Test prediction"""
    trip = {'trip_id': '4497_67055', 'start_time': '17:00:00', 'start_date': '20250306', 'schedule_relationship': 'SCHEDULED', 'route_id': '4497_87351', 'direction_id': 1, 'vehicle_updates': [{'latitude': 51.7338715, 'longitude': -8.48255062, 'timestamp': 1741280802}, {'latitude': 51.7396965, 'longitude': -8.48602581, 'timestamp': 1741280919}, {'latitude': 51.7602119, 'longitude': -8.49677944, 'timestamp': 1741281071}, {'latitude': 51.7707, 'longitude': -8.49569321, 'timestamp': 1741281162}]}
    trip = process_json(trip)
    if trip is None:
        raise ValueError("Invalid trip data")
    print("predicting...")
    predicted = bus_time_inference.predict_trip(trip)
    if not predicted:
        raise ValueError("Unable to make an prediction")
    json_prediction = {
            "stops": trip.display_df().to_dict("records"),
            "delay": trip.current_delay,
            "trip_id": trip.trip_id
            }
    return jsonify(json_prediction), 200


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


@app.route("/training_jobs", methods=["GET"])
@general_exception
def get_training_jobs_info():
    """returns the information about training jobs and models"""
