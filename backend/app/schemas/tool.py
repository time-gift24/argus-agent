from datetime import datetime
from pydantic import BaseModel


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


class ToolList(BaseModel):
    data: list[ToolRead]
