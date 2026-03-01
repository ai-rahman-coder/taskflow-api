from fastapi import FastAPI, Request
import os
import time

app = FastAPI(title="TaskFlow API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    print("Middleware: before")
    response = await call_next(request)
    print("Middleware: after")
    process_time = time.time() - start_time
    print(
        f"{request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"{process_time:.4f}s"
    )
    return response

@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": os.getenv("ENVIRONMENT", "development"),
    }