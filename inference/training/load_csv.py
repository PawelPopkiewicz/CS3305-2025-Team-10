"""
Load the csv dataset into a pandas dataframe
"""

import pandas as pd

from .get_root import get_root


def load_csv(csv_filename: str) -> pd.DataFrame:
    """Loads the csv dataset into a pandas df"""
    training_dir = get_root / "training_data"
    csv_filename += ".csv"
    df = pd.read_csv(training_dir / csv_filename)

    if "stop_id" in df.columns:
        df = df.drop(columns=["stop_id"])

    return df
