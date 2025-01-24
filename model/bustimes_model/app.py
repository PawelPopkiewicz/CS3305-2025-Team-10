from flask import render_template, request, jsonify, Flask

app = Flask(__name__)

@app.route("/v1/predictions", methods=["POST"])
def predict_bus():
    json_data = request.get_json()

    response = {
            'message': "Work in progress"
            }
    return jsonify(response)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
