from flask import Flask, request, redirect, abort
from gtfsr import GTFSR

app = Flask(__name__)

@app.route("/")
def test():
    return "Hello, World!"

@app.route("/vehicles")
def vehicles():
    return GTFSR.fetch_vehicles()