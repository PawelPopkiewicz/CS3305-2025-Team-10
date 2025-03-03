"""
Prepares the inputs in the form of a numpy ndarray from pandas dataframe
"""

from typing import List

import pandas as pd
import numpy as np


def prepare_trip_sequences(df: pd.DataFrame,
                           encoder_timesteps: int,
                           decoder_timesteps: int,
                           feature_cols: List[str],
                           target_cols: str) -> (np.ndarray, np.ndarray, np.ndarray):
    """
    Group the dataframe by the id, sort by timestamp to ensure monotocity and create sliding window
    """
    encoder_inputs = []
    decoder_inputs = []
    decoder_targets = []

    grouped = df.groupby("id")
    for _, group in grouped:
        group = group.sort_values(by="stop_time").reset_index(drop=True)
        for col in ["direction", "is_rush_hour", "is_weekday"]:
            if col in group.columns:
                group[col] = group[col].astype(int)

        data = group[feature_cols].values
        targets = group[target_cols].values

        n = len(group)

        if n < encoder_timesteps + decoder_timesteps:
            continue

        for i in range(encoder_timesteps, n - decoder_timesteps + 1):
            enc_seq = data[i - encoder_timesteps: i]
            dec_target = targets[i: i + decoder_timesteps]
            encoder_inputs.append(enc_seq)
            decoder_targets.append(dec_target)
            decoder_inputs.append(np.zeros((decoder_timesteps, 1)))

    X_enc = np.array(encoder_inputs)
    X_dec = np.array(decoder_inputs)
    y_dec = np.array(decoder_targets)

    return X_enc, X_dec, y_dec
