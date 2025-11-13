import os
import json
from datetime import datetime
from src.loader.load_swagger import load_swagger
from src.loader.load_backend_code import extract_routes_ai
from src.utils.git_utils import clone_or_pull_repo
from src.ai.predict_divergence import compare_api_contract
from src.ai.generate_testcases import generate_test_cases_from_divergence
from src.services.run_tests import execute_generated_tests


def run_comparison(repo_url: str, swagger_source: str) -> dict:
    """
    Main function to compare Swagger API spec with backend code routes.
    1. Pulls or clones the Git repo.
    2. Extracts backend routes.
    3. Compares them with Swagger using Gemini.
    4. Generates divergence report & test cases.
    5. Executes generated tests automatically.
    """

    print(f"📦 Starting API divergence comparison for repo: {repo_url}")

    # Step 1: Clone or pull the latest repo
    local_repo_path = os.path.join(os.getcwd(), "cloned_repo")
    repo_path = clone_or_pull_repo(repo_url, local_repo_path)
    print(f"✅ Repo synced at: {repo_path}")

    # Step 2: Load Swagger file
    swagger = load_swagger(swagger_source)
    print("✅ Swagger loaded successfully")

    # Step 3: Extract backend routes
    all_routes = extract_routes_ai(repo_path)
    print(f"✅ Extracted backend routes: {len(all_routes)} endpoints found")

    # Step 4: Compare using Gemini AI
    print("🤖 Running Gemini divergence analysis...")
    comparison = compare_api_contract(swagger, all_routes)

    # Step 5: Save divergence report
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    divergence_path = f"reports/report_{timestamp}.json"
    with open(divergence_path, "w") as f:
        json.dump(comparison, f, indent=4)
    print(f"✅ Divergence report saved at: {divergence_path}")

    # Step 6: Generate test cases based on divergence
    print("🧠 Generating test cases from divergences...")
    testcases = generate_test_cases_from_divergence(comparison)
    os.makedirs("reports/testcases", exist_ok=True)
    testcases_path = f"reports/testcases/testcases_{timestamp}.json"
    with open(testcases_path, "w") as f:
        json.dump(testcases, f, indent=4)
    print(f"✅ Test cases saved at: {testcases_path}")

    # Step 7: Execute generated test cases
    print("🧪 Executing generated test cases...")
    execution_report = execute_generated_tests(testcases_path)
    print(f"🧾 Execution report generated: {execution_report}")

    # Step 8: Combine final summary
    summary = {
        "repo_url": repo_url,
        "divergence_report": divergence_path,
        "testcases_report": testcases_path,
        "execution_report": execution_report,
        "divergences_found": len(comparison.get("missing_endpoints", []))
        + len(comparison.get("extra_endpoints", []))
        + len(comparison.get("method_mismatches", []))
        + len(comparison.get("parameter_mismatches", []))
        + len(comparison.get("request_body_mismatches", []))
        + len(comparison.get("response_mismatches", []))
        + len(comparison.get("status_code_mismatches", [])),
        "testcases_generated": len(testcases),
    }

    print(f"✅ Process completed for repo: {repo_url}")
    return summary
