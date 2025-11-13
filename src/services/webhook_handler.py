from src.services.compare_service import run_comparison

def handle_github_webhook(payload: dict):
    """
    Triggered automatically on each GitHub push event.
    """

    repo_url = payload["repository"]["clone_url"]

    # Swagger should be stored in repo OR a fixed URL
    swagger_source = "swagger/swagger.yaml"

    result = run_comparison(repo_url, swagger_source)

    return result
