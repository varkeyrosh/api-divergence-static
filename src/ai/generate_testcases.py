import json
import re
import google.generativeai as genai
import os

# Configure Gemini model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

def extract_json_from_response(raw_output: str):
    """
    Extracts and cleans JSON content from Gemini responses.
    Handles both markdown code fences (```json ... ```) and plain text JSON.
    """
    if not raw_output:
        return {"error": "Empty response from model"}

    # Match JSON code block in markdown
    match = re.search(r'```json(.*?)```', raw_output, re.DOTALL)
    if match:
        cleaned = match.group(1).strip()
    else:
        # Try to find any JSON-like content even without code fences
        match = re.search(r'(\[.*\]|\{.*\})', raw_output, re.DOTALL)
        cleaned = match.group(1).strip() if match else raw_output.strip()

    try:
        return json.loads(cleaned)
    except Exception:
        return {"error": "Model output not JSON", "raw": raw_output}


def generate_test_cases_from_divergence(divergence_report):
    """
    Generates test cases using Gemini based on the divergence report.
    Input: divergence_report (dict)
    Output: list of generated test cases or error
    """

    prompt = f"""
    You are an expert QA automation engineer. Given the following API divergence report, 
    generate a set of test cases in pure JSON format (no markdown, no text).
    Each test case should include:
    - endpoint
    - method
    - purpose
    - steps (array of strings describing what to do)

    Example output:
    [
      {{
        "endpoint": "/hello",
        "method": "GET",
        "purpose": "Verify 404 for missing endpoint",
        "steps": [
          "Send GET request to /hello",
          "Expect status 404 Not Found"
        ]
      }}
    ]

    Here is the divergence report:
    {json.dumps(divergence_report, indent=2)}
    """

    try:
        response = model.generate_content(prompt)
        raw_output = ""

        # Gemini API response format can differ based on SDK version
        if hasattr(response, "text"):
            raw_output = response.text
        elif hasattr(response, "candidates"):
            raw_output = response.candidates[0].content.parts[0].text
        else:
            raw_output = str(response)

        test_cases = extract_json_from_response(raw_output)
        return test_cases

    except Exception as e:
        return {"error": f"Failed to generate test cases: {str(e)}"}
