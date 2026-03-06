from fastapi import FastAPI, Request
import os
import time

from app.core.logger import logger
from app.middleware.logging_middleware import log_requests

app = FastAPI(title="TaskFlow API")

app.middleware("http")(log_requests)

@app.get("/health")
def health():
    logger.info("Health check endpoint accessed")
    return {
        "status": "ok",
        "environment": os.getenv("ENVIRONMENT", "development"),
    }