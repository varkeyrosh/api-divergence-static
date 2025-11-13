import json
import os
import re
from pathlib import Path
import os
import google.generativeai as genai



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


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_routes_ai(folder_path: str) -> list:
    """
    Uses Gemini Pro to read the entire backend code directory
    and extract API endpoints even if patterns fail.
    """

    all_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith((".js", ".ts", ".py", ".java", ".go")):
                full_path = os.path.join(root, file)
                all_files.append({
                    "path": full_path,
                    "content": open(full_path, "r", encoding="utf-8", errors="ignore").read()
                })

    prompt = f"""
    You are an expert backend analyst.
    Extract all API endpoints and HTTP methods from this backend codebase.

    Output only JSON list like:
    [
       {{ "method": "GET", "path": "/users" }},
       ...
    ]

    Codebase:
    {all_files}
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except:
        text = response.text
        start = text.find("[")
        end = text.rfind("]") + 1
        return json.loads(text[start:end])
