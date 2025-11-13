import os
import re
from pathlib import Path

def extract_routes_from_backend(folder_path: str) -> list:
    """
    Extract API routes from backend code by scanning for common patterns.
    Supports Node.js (Express), Python (Flask/FastAPI), etc.

    Args:
        folder_path (str): path to backend code folder

    Returns:
        list: list of route definitions found
    """

    patterns = [
        r"@app\.get\(['\"](.*?)['\"]",        # Flask / FastAPI
        r"@app\.post\(['\"](.*?)['\"]",
        r"@app\.put\(['\"](.*?)['\"]",
        r"@app\.delete\(['\"](.*?)['\"]",

        r"router\.get\(['\"](.*?)['\"]",     # Express JS
        r"router\.post\(['\"](.*?)['\"]",
        r"router\.put\(['\"](.*?)['\"]",
        r"router\.delete\(['\"](.*?)['\"]",
    ]

    routes = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith((".js", ".ts", ".py")):  # languages we care about
                full_path = Path(root) / file
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    for pattern in patterns:
                        matches = re.findall(pattern, content)
                        for m in matches:
                            routes.append(m)

    return list(set(routes))  # unique values
