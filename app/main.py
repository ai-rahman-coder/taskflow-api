from fastapi import FastAPI
import os

app = FastAPI(title="TaskFlow API")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": "1.0.2"
    }