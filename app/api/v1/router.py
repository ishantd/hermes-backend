from fastapi.routing import APIRouter

from app.api.v1.auth.controllers import router as auth_router
from app.api.v1.monitoring.controllers import router as monitoring_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(monitoring_router, tags=["monitoring"])
api_router.include_router(auth_router, tags=["auth"], prefix="/auth")
