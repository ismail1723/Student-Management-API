from time import time

from fastapi import Request

from logger_config import logger


async def log_requests(request: Request, call_next):

    start_time = time()

    logger.info(
        f"Request Started | {request.method} {request.url.path}"
    )

    response = await call_next(request)

    process_time = time() - start_time

    response.headers["X-Process-Time"] = str(
        round(process_time, 4)
    )

    logger.info(
        f"Request Completed | "
        f"{request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Time: {round(process_time,4)} sec"
    )

    return response