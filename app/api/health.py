from fastapi import APIRouter
import os

from app.core.logger import logger

router = APIRouter()

@router.get("/health")
def health():
    logger.info("Health check endpoint accessed")
    return {
        "status": "ok",
        "environment": os.getenv("ENVIRONMENT", "development"),
    }