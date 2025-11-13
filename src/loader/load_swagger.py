import json
import yaml
from pathlib import Path

def load_swagger(file_path: str) -> dict:
    """
    Load OpenAPI/Swagger spec from JSON or YAML.

    Args:
        file_path (str): Path to the swagger file

    Returns:
        dict: Parsed Swagger as Python dictionary
    """

    file = Path(file_path)

    if not file.exists():
        raise FileNotFoundError(f"Swagger file not found: {file_path}")

    # Parse JSON
    if file.suffix in [".json"]:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)

    # Parse YAML
    if file.suffix in [".yaml", ".yml"]:
        with open(file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    raise ValueError("Unsupported Swagger file format. Use .json or .yaml")
