from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router
from app.db.session import get_db
from app.core.providers import seed_internal_providers
from app.services.tool_manager import seed_builtin_tools

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
def health_check():
    return {"status": "ok", "version": settings.VERSION}


@app.on_event("startup")
def startup_upsert_tools():
    db = next(get_db())
    try:
        seed_internal_providers(db)
        seed_builtin_tools(db)
    finally:
        db.close()
