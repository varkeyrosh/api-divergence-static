import json
import yaml
import requests
from pathlib import Path

def load_swagger(source: str) -> dict:
    """
    Load Swagger spec from:
    - Local file
    - URL
    - GitHub repo (auto-scans recursively for swagger/openapi files)
    """

    def is_valid_swagger(content: str):
        """Basic check to ensure file contains Swagger or OpenAPI structure."""
        return any(key in content for key in ["openapi", "swagger", "paths"])

    # Case 1: Hosted Swagger file (URL)
    if source.startswith("http://") or source.startswith("https://"):
        response = requests.get(source)
        response.raise_for_status()
        text = response.text

        if not is_valid_swagger(text):
            raise ValueError(f"URL does not appear to be a valid Swagger file: {source}")

        try:
            return response.json()
        except Exception:
            return yaml.safe_load(text)

    # Case 2: GitHub repository (auto-scan)
    if "github.com" in source:
        if source.endswith(".git"):
            source = source[:-4]

        # Convert to GitHub API path
        api_url = source.replace("github.com", "api.github.com/repos") + "/contents"
        print(f"Scanning GitHub repo for Swagger files: {api_url}")

        def recursive_scan(api_url):
            response = requests.get(api_url)
            response.raise_for_status()
            for item in response.json():
                if item["type"] == "file" and item["name"].lower().endswith((".json", ".yaml", ".yml")):
                    file_resp = requests.get(item["download_url"])
                    content = file_resp.text
                    if is_valid_swagger(content):
                        print(f"✅ Found Swagger file: {item['path']}")
                        try:
                            return json.loads(content)
                        except Exception:
                            return yaml.safe_load(content)
                elif item["type"] == "dir":
                    sub = recursive_scan(item["url"])
                    if sub:
                        return sub
            return None

        result = recursive_scan(api_url)
        if not result:
            raise ValueError("No valid Swagger file found in GitHub repo.")
        return result

    # Case 3: Local file
    file = Path(source)
    if file.exists():
        text = file.read_text(encoding="utf-8")
        if not is_valid_swagger(text):
            raise ValueError(f"File {source} does not appear to contain a valid Swagger spec.")
        if source.endswith(".json"):
            return json.loads(text)
        return yaml.safe_load(text)

    raise ValueError(f"Swagger file not found or unsupported format: {source}")
