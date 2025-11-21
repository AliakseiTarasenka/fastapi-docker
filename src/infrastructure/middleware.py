import logging
import time
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.requests import Request

from config.settings import Config

logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def get_allowed_hosts() -> List[str]:
    if Config.ENVIRONMENT == "development":
        return ["127.0.0.1", "localhost"]
    if Config.ENVIRONMENT == "staging":
        return [
            "https://staging.domain.com",
            "https://www.staging.domain.com",
        ]
    else:
        return [
            "https://domain.com",
            "https://www.domain.com",
        ]


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)
        processing_time = time.time() - start_time

        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time}s"

        print(message)
        return response

    # Cross-Origin Resource Sharing tells which origins, methods, and headers are permitted to make requests to your API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=get_allowed_hosts())
