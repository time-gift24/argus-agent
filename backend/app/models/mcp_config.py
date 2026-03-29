import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class McpTransport(str, enum.Enum):
    STDIO = "stdio"
    HTTP = "http"
    SSE = "sse"


class McpConfigKind(str, enum.Enum):
    USER = "user"
    GLOBAL = "global"


class McpServerConfig(Base):
    __tablename__ = "mcp_server_configs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    transport: Mapped[McpTransport] = mapped_column(Enum(McpTransport), nullable=False)

    # stdio fields
    command: Mapped[str | None] = mapped_column(String(512), nullable=True)
    args: Mapped[list | None] = mapped_column(JSON, nullable=True)
    env: Mapped[str | None] = mapped_column(Text, nullable=True)  # AES-256-GCM encrypted

    # http/sse fields
    url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    headers: Mapped[str | None] = mapped_column(Text, nullable=True)  # AES-256-GCM encrypted

    # ownership
    kind: Mapped[McpConfigKind] = mapped_column(
        Enum(McpConfigKind), nullable=False, default=McpConfigKind.USER
    )
    user_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utc_now, onupdate=_utc_now
    )

    __table_args__ = (
        Index("ix_mcp_config_user_id", "user_id"),
    )

    user: Mapped["User | None"] = relationship()  # noqa: F821
