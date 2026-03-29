from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router
from app.services.tool_manager import ToolManager
from app.db.base_class import Base
from app.db.session import SessionLocal
from app.models.tool import Tool
from app.tools import BUILTIN_TOOLS

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
    tm = ToolManager.get_instance()
    for module_path in BUILTIN_TOOLS:
        tm.register(module_path)

    db = SessionLocal()
    try:
        # Keep startup resilient on a fresh database before migrations are applied.
        Base.metadata.create_all(bind=db.get_bind(), tables=[Tool.__table__])
        for name in tm.list_names():
            meta = tm._registry[name][1]
            record = db.query(Tool).filter(Tool.name == name).first()
            if record:
                record.description = meta["description"]
                record.argus_schema = meta["argus_schema"]
            else:
                db.add(Tool(**meta, is_builtin=True))
        db.commit()
    finally:
        db.close()
