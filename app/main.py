from fastapi import FastAPI

from app.middleware import logging_middleware
from app.api.health import router as health_router

from app.core.logger import logger
# from app.middleware.logging_middleware import log_requests

app = FastAPI(title="TaskFlow API")

app.middleware("http")(logging_middleware.log_requests)

app.include_router(health_router)