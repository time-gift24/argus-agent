from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ToolRead(BaseModel):
    id: str
    name: str
    description: str
    argus_schema: dict
    system_prompt: str | None = None
    turnend_prompt: str | None = None
    is_builtin: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ToolCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    description: str = Field(..., min_length=1)
    argus_schema: dict[str, Any]
    system_prompt: str | None = None
    turnend_prompt: str | None = None


class ToolList(BaseModel):
    data: list[ToolRead]
