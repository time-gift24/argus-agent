"""Internal provider definitions and seeding logic.

Kind.INTERNAL providers are defined here as code, then upserted on startup.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.crypto import encrypt
from app.models.user import Provider, ProviderKind


@dataclass
class InternalProviderDefinition:
    """Definition of an internal provider (code-as-config)."""

    name: str
    config: dict = field(default_factory=dict)  # e.g. {"model": "gpt-4o"}


# Internal providers defined in code.
# Add new ones here — they will be upserted on every startup.
INTERNAL_PROVIDERS: list[InternalProviderDefinition] = [
    InternalProviderDefinition(
        name="argus-internal-default",
        config={},
    ),
]


def seed_internal_providers(db: Session) -> None:
    """
    Upsert all Kind.INTERNAL providers.

    Called on application startup via lifespan event.
    """
    for defn in INTERNAL_PROVIDERS:
        existing = db.query(Provider).filter(
            Provider.name == defn.name,
            Provider.kind == ProviderKind.INTERNAL,
        ).first()

        if existing:
            # Already exists — do not overwrite (preserve config if manually changed)
            continue

        # Encrypt empty config (for future extensibility — all config is encrypted)
        config_json = __import__("json").dumps(defn.config, separators=(",", ":"))
        encrypted = encrypt(config_json, settings.aes_key_bytes)

        provider = Provider(
            name=defn.name,
            kind=ProviderKind.INTERNAL,
            config=encrypted,
        )
        db.add(provider)

    db.commit()
