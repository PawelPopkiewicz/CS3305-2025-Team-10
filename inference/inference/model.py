"""
Define the bus time model
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from tqdm import tqdm


class BusTimeEncoder(nn.Module):
    """
    Encoder for the bus time prediction
    Encodes the observed trips
    Effectively cutting of the unimportant info from them
    """

    def __init__(self, trip_feature_dim, hidden_dim):
        super(BusTimeEncoder, self).__init__()
        self.hidden_dim = hidden_dim

        # Process trip features
        self.trip_fc = nn.Sequential(
            nn.Linear(trip_feature_dim, hidden_dim),
            nn.ReLU()
        )

        # Process observed stops
        self.stop_embedding = nn.Linear(4, hidden_dim)  # time, distance, scheduled, residual

        # LSTM to process the sequence of stops
        self.lstm = nn.LSTM(hidden_dim, hidden_dim, batch_first=True)

    def forward(self, trip_features, observed_times, observed_distances, observed_scheduled_times, observed_residual_times):
        """Forward pass"""
        # Process trip features
        print(f"features shape: {trip_features.shape}")
        trip_embedding = self.trip_fc(trip_features)
        print(f"trip_embedding shape: {trip_embedding.shape}")

        # Combine distance and time for each stop
        batch_size = observed_distances.size(0)
        seq_length = observed_distances.size(1)
        observed_features = torch.stack([observed_times, observed_distances, observed_scheduled_times, observed_residual_times], dim=2)
        print(f"shape of observed_features [1, seq_len, 4]: {observed_features.shape}")

        # Process each stop
        observed_embedded = self.stop_embedding(observed_features)
        print(f"observed_embedded shape: {observed_embedded.shape}")
        # Initialize hidden state with trip features
        h0 = trip_embedding.repeat(1, batch_size, 1)
        # h0 = trip_embedding.unsqueeze(0)
        c0 = torch.zeros_like(h0)
        print(f"h0 shape: {h0.shape}, c0 shape: {c0.shape}")

        # Process the sequence
        output, (hn, cn) = self.lstm(observed_embedded, (h0, c0))

        return output, (hn, cn)

class BusTimeDecoder(nn.Module):
    """
    Bus time decoder
    Decodes the hidden context vector from encoder
    Also overlaps with the already seen data
    """

    def __init__(self, hidden_dim, output_dim=1):
        super(BusTimeDecoder, self).__init__()
        self.hidden_dim = hidden_dim

        # Embedding for target residuals
        self.stop_embedding = nn.Linear(3, hidden_dim)

        # LSTM for decoding
        self.lstm = nn.LSTM(hidden_dim, hidden_dim, batch_first=True)

        # Output layer
        self.fc_out = nn.Linear(hidden_dim, output_dim)

    def forward(self, target_times, target_distances, target_scheduled_times, encoder_hidden):
        """Forward pass"""

        target_features = torch.stack([target_times, target_distances, target_scheduled_times], dim=2)
        # Embed the target distances
        #target_residuals = target_residuals.unsqueeze(2) # Add feature dimension

        target_embedded = self.stop_embedding(target_features)

        # Use encoder's hidden state
        output, _ = self.lstm(target_embedded, encoder_hidden)

        # Generate time predictions
        residual_pred = self.fc_out(output)

        return residual_pred.squeeze(2)

class BusTimeEncoderDecoder(nn.Module):
    """Encoder decoder for bus time prediction"""

    def __init__(self, trip_feature_dim, hidden_dim):
        super(BusTimeEncoderDecoder, self).__init__()
        self.encoder = BusTimeEncoder(trip_feature_dim, hidden_dim)
        self.decoder = BusTimeDecoder(hidden_dim)

    def forward(self,
                trip_features,
                observed_times, observed_distances, observed_scheduled_times, observed_residual_times,
                target_times, target_distances, target_scheduled_times):
        """Forward pass"""
        # Encode the observed stops
        _, encoder_hidden = self.encoder(trip_features,
                                         observed_times, observed_distances, observed_scheduled_times, observed_residual_times)

        # Decode to predict target times
        residual_pred = self.decoder(target_times, target_distances, target_scheduled_times, encoder_hidden)

        return residual_pred
