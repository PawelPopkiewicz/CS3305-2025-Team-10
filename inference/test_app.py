"""
Really primitive testing of the route
"""

import requests
import json

# URL of the route
url = 'http://localhost:5001/predictions'  # Replace with the correct URL if different

# Example JSON data to test the route (modify this based on the actual structure required by your route)
test_trips = [{'trip_id': '4497_67055', 'start_time': '17:00:00', 'start_date': '20250306', 'schedule_relationship': 'SCHEDULED', 'route_id': '4497_87351', 'direction_id': 1, 'vehicle_updates': [{'latitude': 51.7338715, 'longitude': -8.48255062, 'timestamp': 1741280802}, {'latitude': 51.7396965, 'longitude': -8.48602581, 'timestamp': 1741280919}, {'latitude': 51.7602119, 'longitude': -8.49677944, 'timestamp': 1741281071}, {'latitude': 51.7707, 'longitude': -8.49569321, 'timestamp': 1741281162}]}]

for trip_data in test_trips:

    # Send POST request to the Flask server
    response = requests.post(url, json=trip_data)

    # Print status code and response body
    if response.status_code == 200:
        print("Prediction successful")
        print(f"Response JSON: {response.json()}")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response Body: {response.text}")
