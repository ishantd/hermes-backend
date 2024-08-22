from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import app.constants as constants
from app.api.v1.router import api_router
from app.settings import settings


def get_app() -> FastAPI:
    """
    Application factory.
    Get FastAPI application.

    This is the main constructor of a fastapi application.

    :return: application.
    """

    app = FastAPI(
        title="hermes",
        description="hermes API - artisan assignment",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        default_response_class=UJSONResponse,
    )

    allowed_origins = [
        settings.frontend_url,
    ]

    if settings.env in [constants.DEVELOPMENT, constants.TESTING]:
        allowed_origins.append("http://localhost:3000")

    default_headers_allowed = ["Content-Type", "Authorization", "X-Workspace-Code"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=default_headers_allowed,
    )

    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

    app.include_router(router=api_router)

    return app
