"""
Gateway providing connection to frontend
"""

from flask import jsonify, Flask, Response

app = Flask(__name__)


@app.route("/v1/test", methods=["GET"])
def test_route():
    """
    test route
    """
    response = {
            'message': "Work in progress"
            }
    return jsonify(response)
