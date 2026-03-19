from fastapi import APIRouter
import os

from app.core.logger import logger
from app.schemas.health_schema import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health():
    logger.info("Health check endpoint accessed")
    return HealthResponse(
        status="ok",
        environment = os.getenv("ENVIRONMENT", "development")
    )