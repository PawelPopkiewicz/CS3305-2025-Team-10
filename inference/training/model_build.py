"""
Code to build the encoder decoder model
"""

import pandas as pd
import numpy as np

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, TimeDistributed
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import Adam


def build_seq2seq_model(encoder_timesteps: int,
                        num_features: int,
                        decoder_timesteps: int,
                        latent_dim: int = 64) -> Model:
    """Creates a sequence to sequence model"""
    # Encoder
    encoder_inputs = Input(shape=(encoder_timesteps, num_features), name="encoder_inputs")
    encoder_lstm = LSTM(latent_dim, return_state=True, name="encoder_lstm")
    _, state_h, state_c = encoder_lstm(encoder_inputs)
    encoder_states = [state_h, state_c]

    # Decoder
    decoder_inputs = Input(shape=(decoder_timesteps, 1), name="decoder_inputs")
    decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True, name="decoder_lstm")
    decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
    decoder_dense = TimeDistributed(Dense(1), name="decoder_dense")
    decoder_outputs = decoder_dense(decoder_outputs)

    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
    model.compile(optimizer=Adam(), loss="mse")
    return model
