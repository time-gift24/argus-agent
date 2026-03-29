import uuid as _uuid
from sqlalchemy import Column, String, Text, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base, TimestampMixin


class Tool(Base, TimestampMixin):
    __tablename__ = "tools"

    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(_uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    argus_schema: Mapped[dict] = mapped_column(JSON, nullable=False)
    system_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    turnend_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_builtin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
