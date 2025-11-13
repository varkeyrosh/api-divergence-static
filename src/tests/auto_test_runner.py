import json
import requests
from datetime import datetime
import os

def run_generated_tests(testcase_path: str, base_url: str = "http://127.0.0.1:8000") -> dict:
    """
    Executes AI-generated test cases and returns a structured report.
    """
    with open(testcase_path, "r") as f:
        testcases = json.load(f)

    results = []
    for case in testcases:
        endpoint = case.get("endpoint")
        method = case.get("method", "GET").upper()
        steps = case.get("steps", [])
        url = f"{base_url}{endpoint}"
        status = "PENDING"
        details = ""

        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, json={})
            elif method == "PUT":
                response = requests.put(url, json={})
            elif method == "DELETE":
                response = requests.delete(url)
            else:
                response = requests.request(method, url)

            # Evaluate based on expectation heuristics
            if "404" in steps[-1]:
                passed = response.status_code == 404
            else:
                passed = response.status_code != 404

            status = "PASS" if passed else "FAIL"
            details = f"Expected: {'404' if '404' in steps[-1] else '!=404'}, Got: {response.status_code}"

        except Exception as e:
            status = "ERROR"
            details = str(e)

        results.append({
            "endpoint": endpoint,
            "method": method,
            "status": status,
            "details": details
        })

    # Save report
    os.makedirs("reports/executions", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_path = f"reports/executions/execution_report_{timestamp}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"✅ Execution completed. Report saved at: {out_path}")
    return results


if __name__ == "__main__":
    latest_test = sorted(os.listdir("reports/testcases"))[-1]
    run_generated_tests(os.path.join("reports/testcases", latest_test))
