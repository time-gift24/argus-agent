from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.providers import seed_internal_providers
from app.db.session import get_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Seed internal providers on startup."""
    db = next(get_db())
    try:
        seed_internal_providers(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

# CORS: in dev mode allow all origins; in production use explicit allowlist
_cors_origins = ["*"] if settings.is_dev_mode else settings.cors_origins
if _cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins,
        allow_credentials=not settings.is_dev_mode,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "X-Dev-User"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
