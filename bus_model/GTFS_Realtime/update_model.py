import requests
from ..gtfsr import GTFSR


def update_model() -> dict:
    """Fetches the latest vehicle data and sends it to main Flask server"""
    vehicle_data = GTFSR.fetch_vehicles()
    try:
        r = requests.post("http://localhost:5002/update", json=vehicle_data)
        return 0 if r.text == "Success" else 1
    except Exception as e:
        return 1    # Hidden Error

if __name__ == "__main__":
    update_model()