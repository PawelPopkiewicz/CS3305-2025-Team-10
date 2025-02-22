"""
Main functions handling fetching and processing data
"""

from .fetch_training_data import fetch_training_data
from .json_to_csv import create_csv


RAW_TRAINING_DATA_FILENAME = "raw_training_data"
CSV_DATASET = "bus_times_dataset"

def fetch_convert_training_data():
    """Fetches the data from training_data_collection
    Converts it to a csv"""
    fetch_training_data(RAW_TRAINING_DATA_FILENAME)
    create_csv(RAW_TRAINING_DATA_FILENAME, CSV_DATASET)


if __name__ == "__main__":
    fetch_convert_training_data()
