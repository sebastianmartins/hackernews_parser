import json
from pathlib import Path
from typing import Any


def load_json(data_path: Path) -> Any:
    """
    Load and parse the JSON data from the file.

    Returns:
        Any: The parsed JSON data
    """
    with open(data_path, "r") as f:
        return json.load(f)
