from fastapi import Request
import time

from app.core.logger import logger

async def log_requests(request: Request, call_next):
    start_time = time.time()
    client_ip = request.client.host

    logger.info(f"Incoming request: {client_ip} {request.method} {request.url.path}")

    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Request failed")
        raise

    process_time = time.time() - start_time
    logger.info(
        f"Completed request: {client_ip} {request.method} {request.url.path} "
        f"{response.status_code} {process_time:.4f}s"
    )
    return response