from fastapi import FastAPI, Request
from src.services.compare_service import run_comparison
from src.services.webhook_handler import handle_github_webhook

app = FastAPI()

@app.post("/compare")
async def compare_api(data: dict):
    return run_comparison(
        git_repo=data["git_repo"],
        swagger_source=data["swagger"]
    )

@app.post("/webhook/github")
async def github_webhook(request: Request):
    payload = await request.json()
    return handle_github_webhook(payload)
