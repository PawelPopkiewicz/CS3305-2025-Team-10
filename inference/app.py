"""
Provides api for inference container
"""

from flask import render_template, jsonify, Flask, Response

app = Flask(__name__)


@app.route("/v1/predictions", methods=["POST"])
def predict_bus():
    """
    Input: Inference input for the model
    Returns: The prediction for the bus route
    """
    response = {
            'message': "Work in progress"
            }
    return jsonify(response)
