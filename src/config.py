from pathlib import Path

# Set the folder where data files will be stored
BASE_DIRECTORY = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = BASE_DIRECTORY / "data"
# create the folder if it doesn't exist and don't give error if it's already there
DATA_DIRECTORY.mkdir(exist_ok=True)

DEFAULT_START = "2021-01-01"
DEFAULT_END = "2025-01-01"