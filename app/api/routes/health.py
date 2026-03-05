from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/health")
async def health():
    return {
        "status": "ok",
        "environment": os.getenv("ENVIRONMENT", "development"),
    }