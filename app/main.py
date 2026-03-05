from fastapi import FastAPI, Request
import os
import time
import logging

log_file = "app_logs.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
)

logger = logging.getLogger("taskflow-api")

app = FastAPI(title="TaskFlow API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"{process_time:.4f}s"
    )
    return response

@app.get("/health")
def health():
    logger.info("Health check endpoint accessed")
    return {
        "status": "ok",
        "environment": os.getenv("ENVIRONMENT", "development"),
    }