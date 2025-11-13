import google.generativeai as genai
import os
import json

# Load API key from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def compare_api_contract(swagger_spec: dict, backend_routes: list) -> dict:
    """
    Uses Gemini Pro to compare Swagger API spec with backend routes.
    Produces a structured JSON report of divergences.
    """

    prompt = f"""
    You are an API contract validation expert.

    Compare the following:
    - Swagger/OpenAPI spec (FULL JSON below)
    - Backend implemented routes (Python list below)

    Identify:
    1. Missing endpoints (in backend but present in Swagger)
    2. Extra endpoints (present in backend but not in Swagger)
    3. Method mismatches
    4. Parameter mismatches
    5. Request body mismatches
    6. Response schema mismatches
    7. Status code mismatches

    Provide the output in STRICT JSON with keys:
    {{
        "missing_endpoints": [],
        "extra_endpoints": [],
        "method_mismatches": [],
        "parameter_mismatches": [],
        "request_body_mismatches": [],
        "response_mismatches": [],
        "status_code_mismatches": []
    }}

    Swagger Spec:
    {json.dumps(swagger_spec, indent=2)}

    Backend Routes:
    {json.dumps(backend_routes, indent=2)}
    """

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except Exception:
        text = response.text
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
