from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class LLMProviderBase(BaseModel):
    name: str = Field(..., max_length=128)
    api_base: Optional[str] = Field(None, max_length=512)
    api_key: Optional[str] = Field(None, max_length=512)
    models: List[str] = []


class LLMProviderCreate(LLMProviderBase):
    pass


class LLMProviderUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=128)
    api_base: Optional[str] = Field(None, max_length=512)
    api_key: Optional[str] = Field(None, max_length=512)
    models: Optional[List[str]] = None
    is_active: Optional[bool] = None


class LLMProviderRead(LLMProviderBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
