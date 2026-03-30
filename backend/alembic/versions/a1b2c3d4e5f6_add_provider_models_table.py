"""add provider_models table

Revision ID: a1b2c3d4e5f6
Revises: 85222bba3a92
Create Date: 2026-03-29 12:00:00.000000

"""
import base64
import json
import uuid
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.core.crypto import decrypt, encrypt


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "85222bba3a92"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create provider_models table
    op.create_table(
        "provider_models",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider_id", sa.String(36), sa.ForeignKey("providers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("provider_id", "name", name="uq_provider_model_name"),
    )
    op.create_index("ix_provider_model_provider_id", "provider_models", ["provider_id"])
    _create_default_model_unique_index()

    # 2. Data migration: extract model from encrypted config → provider_models
    _migrate_models_from_config()


def downgrade() -> None:
    _drop_default_model_unique_index()
    op.drop_index("ix_provider_model_provider_id", table_name="provider_models")
    op.drop_table("provider_models")


def _migrate_models_from_config() -> None:
    """Migrate model field from encrypted config to provider_models table."""
    import os

    conn = op.get_bind()
    aes_key_b64 = os.environ.get("AES_KEY", "")
    provider_count = _count_encrypted_provider_configs(conn)
    if not aes_key_b64:
        if provider_count > 0:
            raise RuntimeError("AES_KEY is required to migrate existing provider model data")
        return

    try:
        aes_key = base64.b64decode(aes_key_b64)
        if len(aes_key) != 32:
            raise ValueError("AES_KEY must decode to 32 bytes")
    except Exception as exc:
        if provider_count > 0:
            raise RuntimeError("AES_KEY is invalid; cannot migrate existing provider model data") from exc
        return

    providers = conn.execute(
        sa.text("SELECT id, config FROM providers WHERE config IS NOT NULL AND config != ''")
    ).fetchall()

    now_utc = datetime.now(timezone.utc)
    for provider_id, config_b64 in providers:
        try:
            config_json = decrypt(config_b64, aes_key)
            config = json.loads(config_json)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to decrypt provider config for provider {provider_id} during model migration"
            ) from exc

        model_name = str(config.pop("model", "")).strip()
        if not model_name:
            continue

        # Insert into provider_models
        model_id = str(uuid.uuid4())
        conn.execute(
            sa.text(
                "INSERT INTO provider_models (id, provider_id, name, is_default, created_at, updated_at) "
                "VALUES (:id, :provider_id, :name, 1, :created_at, :updated_at)"
            ),
            {
                "id": model_id,
                "provider_id": provider_id,
                "name": model_name,
                "created_at": now_utc,
                "updated_at": now_utc,
            },
        )

        # Re-encrypt config without model field
        new_config_json = json.dumps(config, separators=(",", ":"))
        new_config_b64 = encrypt(new_config_json, aes_key)
        conn.execute(
            sa.text("UPDATE providers SET config = :config WHERE id = :id"),
            {"config": new_config_b64, "id": provider_id},
        )


def _count_encrypted_provider_configs(conn) -> int:
    """Count provider rows that require encrypted-config inspection."""
    return conn.execute(
        sa.text("SELECT COUNT(*) FROM providers WHERE config IS NOT NULL AND config != ''")
    ).scalar_one()


def _create_default_model_unique_index() -> None:
    """Ensure each provider has at most one default model."""
    conn = op.get_bind()
    dialect = conn.dialect.name
    if dialect == "sqlite":
        conn.execute(
            sa.text(
                "CREATE UNIQUE INDEX uq_provider_default_model_per_provider "
                "ON provider_models (provider_id) WHERE is_default = 1"
            )
        )
    elif dialect == "postgresql":
        conn.execute(
            sa.text(
                "CREATE UNIQUE INDEX uq_provider_default_model_per_provider "
                "ON provider_models (provider_id) WHERE is_default"
            )
        )
    else:
        raise RuntimeError(
            f"Unsupported dialect '{dialect}' for partial unique index on provider_models.is_default"
        )


def _drop_default_model_unique_index() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DROP INDEX IF EXISTS uq_provider_default_model_per_provider"))
