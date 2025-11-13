import os
import json
import requests
from datetime import datetime

def execute_generated_tests(testcases_path: str, base_url: str = "http://127.0.0.1:8000") -> str:
    """
    Executes generated test cases (from Gemini output JSON).
    Returns the path to the execution report.
    """
    try:
        # Read test cases
        with open(testcases_path, "r") as f:
            testcases = json.load(f)

        results = []
        for test in testcases:
            endpoint = test.get("endpoint")
            method = test.get("method", "GET").upper()
            expected_status = 404 if "404" in " ".join(test.get("steps", [])).lower() else 200
            url = f"{base_url}{endpoint}"
            result = {"endpoint": endpoint, "method": method, "status": None, "result": None, "details": ""}

            try:
                # Perform API request
                response = requests.request(method, url, timeout=5)
                result["status"] = response.status_code

                # Check if expected status matches
                if response.status_code == expected_status:
                    result["result"] = "PASS"
                else:
                    result["result"] = "FAIL"
                    result["details"] = f"Expected {expected_status}, got {response.status_code}"

            except Exception as e:
                result["result"] = "ERROR"
                result["details"] = str(e)

            results.append(result)

        # Save report
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs("reports/executions", exist_ok=True)
        report_path = f"reports/executions/execution_{timestamp}.json"
        with open(report_path, "w") as f:
            json.dump(results, f, indent=4)

        print(f"✅ Test execution completed. Report saved at: {report_path}")
        return report_path

    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return None
