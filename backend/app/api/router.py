from fastapi import APIRouter
from app.api.endpoints import llm_providers

api_router = APIRouter()

api_router.include_router(llm_providers.router)
