from src.utils.git_utils import clone_or_pull_repo
from src.loader.load_swagger import load_swagger
from src.loader.load_backend_code import extract_routes_from_backend, extract_routes_ai
from src.ai.predict_divergence import compare_api_contract
import shutil

def run_comparison(git_repo: str, swagger_source: str) -> dict:
    """
    Full pipeline:
    1. Fetch backend repo
    2. Load Swagger
    3. Extract routes
    4. Compare
    """

    repo_path = "backend_code"

    # Cleanup to avoid conflicts
    shutil.rmtree(repo_path, ignore_errors=True)

    clone_or_pull_repo(git_repo, repo_path)

    swagger = load_swagger(swagger_source)

    # hybrid extraction
    routes_simple = extract_routes_from_backend(repo_path)
    routes_ai = extract_routes_ai(repo_path)

    all_routes = {
        "pattern_routes": routes_simple,
        "ai_routes": routes_ai
    }

    comparison = compare_api_contract(swagger, all_routes)

    return comparison
