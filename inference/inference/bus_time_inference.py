"""
Provides a class which holds the loaded model
"""
import warnings
warnings.filterwarnings("ignore")

import torch
import pandas as pd
import numpy as np

from preprocessing.trip_to_stop_times import TripGenerator

from .model import BusTimeEncoderDecoder
from .get_root import get_root

class BusTimesInference():
    """
    Class holding the bus time prediction model
    Offering prediction method
    """

    HIDDEN_DIM = 120
    OVERLAP = 3

    def __init__(self, model_filename):
        # Load the model and preprocessing objects
        model_path = get_root() / "models" / model_filename
        checkpoint = torch.load(model_path, weights_only=False)

        # Create model
        self.trip_feature_dim = len(checkpoint['route_encoder'].categories_[0]) + len(checkpoint['day_encoder'].categories_[0])  # routes + days
        self.model = BusTimeEncoderDecoder(self.trip_feature_dim, self.HIDDEN_DIM)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()

        # Get the preprocessing objects
        self.route_encoder = checkpoint['route_encoder']
        self.day_encoder = checkpoint['day_encoder']
        self.time_scaler = checkpoint['time_scaler']
        self.distance_scaler = checkpoint['distance_scaler']
        self.scheduled_time_scaler = checkpoint['scheduled_time_scaler']
        self.residual_time_scaler = checkpoint['residual_time_scaler']

    def get_trip_features(self, new_trip_data):
        """Prepares the trip_features"""
        # Extract trip details
        # trip_id = new_trip_data['id'].iloc[0]
        route_name = new_trip_data['route_name'].iloc[0]
        day = new_trip_data['day'].iloc[0]

        # Prepare features
        # One-hot encode route
        route_name_df = pd.DataFrame([[route_name]], columns=['route_name'])
        route_encoded = self.route_encoder.transform(route_name_df)[0]

        # One-hot encode day
        day_df = pd.DataFrame([[day]], columns=['day'])
        day_encoded = self.day_encoder.transform(day_df)[0]

        # Trip features
        trip_features = np.concatenate([
            route_encoded,
            day_encoded
        ])
        trip_features = torch.tensor(trip_features, dtype=torch.float32).unsqueeze(0)
        return trip_features

    def get_observed_data(self, observed_df):
        """Extract the stop features for observed"""
        observed_times = self.time_scaler.transform(
                observed_df[['time']])
        observed_distances = self.distance_scaler.transform(
                observed_df[['distance_to_stop']])
        observed_scheduled_times = self.scheduled_time_scaler.transform(
                observed_df[['time_to_stop']])
        observed_residual_times = self.residual_time_scaler.transform(
                observed_df[['residual_stop_time']])

        observed_times = torch.tensor(
                observed_times, dtype=torch.float32).transpose(0, 1)
        observed_distances = torch.tensor(
                observed_distances, dtype=torch.float32).transpose(0, 1)
        observed_scheduled_times = torch.tensor(
                observed_scheduled_times, dtype=torch.float32).transpose(0, 1)
        observed_residual_times = torch.tensor(
                observed_residual_times, dtype=torch.float32).transpose(0, 1)

        return observed_times, observed_distances, observed_scheduled_times, observed_residual_times

    def get_target_data(self, remaining_df):
        """Extract the stop features for target"""
        target_times = self.time_scaler.transform(
                remaining_df[['time']])
        target_distances = self.distance_scaler.transform(
                remaining_df[['distance_to_stop']])
        target_scheduled_times = self.scheduled_time_scaler.transform(
                remaining_df[['time_to_stop']])

        target_times = torch.tensor(
                target_times, dtype=torch.float32).transpose(0, 1)
        target_distances = torch.tensor(
                target_distances, dtype=torch.float32).transpose(0, 1)
        target_scheduled_times = torch.tensor(
                target_scheduled_times, dtype=torch.float32).transpose(0, 1)

        return target_times, target_distances, target_scheduled_times

    def split_dataframes(self, new_trip_data):
        """Splits the dataframe to observed and target"""
        observed_df = new_trip_data[~new_trip_data['residual_stop_time'].isna()]
        remaining_df = new_trip_data[new_trip_data['residual_stop_time'].isna()]
        if observed_df.empty or remaining_df.empty:
            return [None, None]
        return observed_df, remaining_df

    def add_overlap(self, observed_df, remaining_df):
        """Add the overlapping stops from observed to remaining"""
        overlap_rows = observed_df.tail(self.OVERLAP)
        remaining_df = pd.concat([overlap_rows, remaining_df], ignore_index=True)
        return remaining_df

    def remove_overlap(self, predicted_time_residuals):
        """Remove the overlapped predicted stops"""
        return predicted_time_residuals[self.OVERLAP:]

    def rescale_predictions(self, predicted_time_residuals):
        """Convert predicted times back to scale"""
        # Convert predictions back to original scale
        predicted_time_residuals_np = predicted_time_residuals.numpy().reshape(-1, 1)
        predicted_time_residuals_orig = self.residual_time_scaler.inverse_transform(predicted_time_residuals_np).flatten()
        return predicted_time_residuals_orig

    def predict_trip(self, trip):
        """
        Predict the bus trip for the next target stops
        """
        if not trip.inference_eligible():
            raise ValueError("Trip did not pass enough stops (3)")
        observed_df, remaining_df = trip.observed_df, trip.target_df
        if observed_df is None or remaining_df is None:
            raise ValueError("Failed in resolving the dataframes")
        remaining_df = self.add_overlap(observed_df, remaining_df)
        trip_features = self.get_trip_features(pd.concat([observed_df, remaining_df]))
        observed_times, observed_distances, observed_scheduled_times, observed_residual_times = self.get_observed_data(observed_df)
        target_times, target_distances, target_scheduled_times = self.get_target_data(remaining_df)
        with torch.no_grad():
            predicted_time_residuals = self.model(trip_features,
                                             observed_times, observed_distances, observed_scheduled_times, observed_residual_times,
                                             target_times, target_distances, target_scheduled_times)
        predicted_time_residuals = self.rescale_predictions(predicted_time_residuals)
        # predicted_time_residuals = predicted_time_residuals# .squeeze(0)
        predicted_time_residuals = self.remove_overlap(predicted_time_residuals)
        trip.add_predictions(predicted_time_residuals)
        return True


if __name__ == "__main__":
    from .process_json import process_json
    bus_time_inference = BusTimesInference("bus_time_prediction_model_3.pth")
    trip = {'trip_id': '4497_66378', 'start_time': '10:50:00', 'start_date': '20250307', 'schedule_relationship': 'SCHEDULED', 'route_id': '4497_87351', 'direction_id': 0, 'vehicle_updates': [{'latitude': 51.8992348, 'longitude': -8.46604156, 'timestamp': 1741342091}, {'latitude': 51.8992348, 'longitude': -8.46604156, 'timestamp': 1741342182}, {'latitude': 51.8992348, 'longitude': -8.46604156, 'timestamp': 1741342242}, {'latitude': 51.8992348, 'longitude': -8.46604156, 'timestamp': 1741342304}, {'latitude': 51.8992348, 'longitude': -8.46604156, 'timestamp': 1741342364}, {'latitude': 51.8992348, 'longitude': -8.46604156, 'timestamp': 1741342425}, {'latitude': 51.8992348, 'longitude': -8.46604156, 'timestamp': 1741342546}, {'latitude': 51.8992348, 'longitude': -8.46604156, 'timestamp': 1741342780}]}
    trip = process_json(trip)
    if trip is None:
        raise ValueError("Invalid trip data")
    bus_time_inference.predict_trip(trip)
    json_prediction = {
            "stops": trip.display_df().to_dict("records"),
            "delay": trip.current_delay,
            "trip_id": trip.trip_id
            }
    import json
    print(json.dumps(json_prediction, indent=4))
