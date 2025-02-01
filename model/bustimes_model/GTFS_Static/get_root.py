"""
Simple functions which returns the project root
"""

import os
from pathlib import Path
from dotenv import load_dotenv


def get_root():
    """Returns project root"""
    load_dotenv()
    return Path(os.getenv("PROJECT_ROOT")).resolve()


if __name__ == "__main__":
    print(get_root())
