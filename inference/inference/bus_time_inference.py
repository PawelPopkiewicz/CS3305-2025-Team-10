"""
Provides a class which holds the loaded model
"""

import torch
import pandas as pd
import numpy as np

from .json_to_csv import process_json
from .model import BusTimeEncoderDecoder
from .get_root import get_root

class BusTimesInference():
    """
    Class holding the bus time prediction model
    Offering prediction method
    """

    def __init__(self, model_filename):
        # Load the model and preprocessing objects
        model_path = get_root() / "models" / model_filename
        checkpoint = torch.load(model_path, weights_only=False)

        # Create model
        self.trip_feature_dim = len(checkpoint['route_encoder'].categories_[0]) + len(checkpoint['day_encoder'].categories_[0])  # routes + days
        self.hidden_dim = 100
        self.model = BusTimeEncoderDecoder(self.trip_feature_dim, self.hidden_dim)
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
        day_df = pd.DataFrame([[day]], column=['day'])
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
                observed_df[['stop_distance']])
        observed_scheduled_times = self.scheduled_time_scaler.transform(
                observed_df[['scheduled_stop_time']])
        observed_residual_times = self.residual_time_scaler.transform(
                observed_df[['residual_stop_time']])

        observed_times = torch.tensor(
                observed_times, dtype=torch.float32).unsqueeze(0)
        observed_distances = torch.tensor(
                observed_distances, dtype=torch.float32).unsqueeze(0)
        observed_scheduled_times = torch.tensor(
                observed_scheduled_times, dtype=torch.float32).unsqueeze(0)
        observed_residual_times = torch.tensor(
                observed_residual_times, dtype=torch.float32).unsqueeze(0)

        return observed_times, observed_distances, observed_scheduled_times, observed_residual_times

    def get_target_data(self, remaining_df):
        """Extract the stop features for target"""
        target_times = self.time_scaler.transform(
                remaining_df[['time']])
        target_distances = self.distance_scaler.transform(
                remaining_df[['stop_distance']])
        target_scheduled_times = self.scheduled_time_scaler.transform(
                remaining_df[['scheduled_stop_time']])

        target_times = torch.tensor(
                target_times, dtype=torch.float32).unsqueeze(0)
        target_distances = torch.tensor(
                target_distances, dtype=torch.float32).unsqueeze(0)
        target_scheduled_times = torch.tensor(
                target_scheduled_times, dtype=torch.float32).unsqueeze(0)

        return target_times, target_distances, target_scheduled_times

    def split_dataframes(self, new_trip_data):
        """Splits the dataframe to observed and target"""
        observed_df = new_trip_data[~new_trip_data['residual_stop_time'].isna()]
        remaining_df = new_trip_data[new_trip_data['residual_stop_time'].isna()]
        if observed_df.empty or remaining_df.empty:
            print("Error: No observed stops or no remaining stops to predict")
            return [None, None]
        return observed_df, remaining_df

    def add_predicted_residuals_to_df(self, remaining_df, predicted_time_residuals):
        """Adds predicted time residuals to the remaining_df"""
        # Convert predictions back to original scale
        predicted_time_residuals_np = predicted_time_residuals.numpy().reshape(-1, 1)
        predicted_time_residuals_orig = self.residual_time_scaler.inverse_transform(predicted_time_residuals_np).flatten()

        # Add predictions to the dataframe
        remaining_df['predicted_time'] = predicted_time_residuals_orig
        return remaining_df

    def combine_dfs(self, observed_df, remaining_df):
        """Concat the dfs"""
        all_stops_df = pd.concat([
            observed_df,
            remaining_df
        ])
        return all_stops_df

    def predict_trip(self, json_data):
        """
        Predict the bus trip for the next target stops
        """
        trip_data = process_json(json_data)
        observed_df, remaining_df = self.split_dataframes(trip_data)
        if observed_df is None or remaining_df is None:
            return None
        trip_features = self.get_trip_features(trip_data)
        observed_times, observed_distances, observed_scheduled_times, observed_residual_times = self.get_observed_data(observed_df)
        target_times, target_distances, target_scheduled_times = self.get_target_data(remaining_df)

        with torch.no_grad():
            predicted_time_residuals = self.model(trip_features,
                                             observed_times, observed_distances, observed_scheduled_times, observed_residual_times,
                                             target_times, target_distances, target_scheduled_times)
        remaining_df = self.add_predicted_residuals_to_df(remaining_df, predicted_time_residuals)
        all_stops_df = self.combine_dfs(observed_df, remaining_df)
        return all_stops_df.to_dict(orient="records")
