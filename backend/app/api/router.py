from fastapi import APIRouter

from app.api.endpoints import auth, mcp_configs, providers, tools, users

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(providers.router)
api_router.include_router(tools.router, prefix="/tools", tags=["tools"])
api_router.include_router(mcp_configs.router)
