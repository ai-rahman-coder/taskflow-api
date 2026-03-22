from fastapi import FastAPI

from app.middleware import logging_middleware
from app.api.health import router as health_router
from app.api.tasks import router as tasks_router

app = FastAPI(title="TaskFlow API")

app.middleware("http")(logging_middleware.log_requests)

app.include_router(health_router)
app.include_router(tasks_router)