from fastapi import FastAPI, Request
from src.services.compare_service import run_comparison

app = FastAPI()


@app.post("/compare")
async def compare_api(request: Request):
    """
    Accepts JSON body:
    {
        "git_repo": "<GitHub Repo URL>",
        "swagger": "<Swagger JSON path or URL>"
    }
    """
    body = await request.json()
    git_repo = body.get("git_repo")
    swagger_source = body.get("swagger")

    return run_comparison(repo_url=git_repo, swagger_source=swagger_source)
