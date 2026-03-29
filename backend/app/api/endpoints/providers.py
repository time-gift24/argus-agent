"""Provider endpoints: user providers and internal providers."""

from __future__ import annotations

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user_id
from app.core.config import settings
from app.core.crypto import decrypt, encrypt
from app.db.session import get_db
from app.models.user import Provider, ProviderKind, UserProvider
from app.schemas.user import (
    DefaultUpdate,
    ProviderConfigInput,
    ProviderCreate,
    ProviderDetailRead,
    ProviderRead,
    ProviderTestResult,
    ProviderUpdate,
    UserProviderRead,
)
from app.services.provider_test import test_config_connectivity, test_provider_connectivity

router = APIRouter(tags=["providers"])


def _get_user_provider_association(db: Session, user_id: str, provider_id: str) -> UserProvider:
    assoc = (
        db.query(UserProvider)
        .filter(UserProvider.user_id == user_id, UserProvider.provider_id == provider_id)
        .first()
    )
    if not assoc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    return assoc


def _build_provider_detail(provider: Provider) -> ProviderDetailRead:
    try:
        config_json = decrypt(provider.config, settings.aes_key_bytes)
        config = ProviderConfigInput.model_validate(json.loads(config_json))
    except Exception as exc:  # pragma: no cover - defensive guard for corrupted data
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Provider config is corrupted",
        ) from exc

    return ProviderDetailRead(
        id=provider.id,
        name=provider.name,
        kind=provider.kind.value,
        created_at=provider.created_at,
        updated_at=provider.updated_at,
        config=config,
    )


# ── Test config (no provider needed) ──────────────────────────────────────────


@router.post(
    "/providers/test-config",
    response_model=ProviderTestResult,
    name="test_provider_config",
)
def test_provider_config(
    config: ProviderConfigInput,
    _: str = Depends(get_current_user_id),
) -> ProviderTestResult:
    """Test connectivity with raw config (for create/edit forms)."""
    return test_config_connectivity(config.model_dump())


# ── Internal providers ────────────────────────────────────────────────────────


@router.get("/internal-providers", response_model=list[ProviderRead], name="list_internal_providers")
def list_internal_providers(
    _: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> list[ProviderRead]:
    """List all internal providers (config never returned)."""
    providers = (
        db.query(Provider)
        .filter(Provider.kind == ProviderKind.INTERNAL)
        .order_by(Provider.name)
        .all()
    )
    return [ProviderRead.model_validate(p) for p in providers]


# ── User providers ───────────────────────────────────────────────────────────


@router.get("/providers", response_model=list[UserProviderRead], name="list_user_providers")
def list_user_providers(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> list[UserProviderRead]:
    """List current user's provider associations."""
    associations = (
        db.query(UserProvider)
        .filter(UserProvider.user_id == user_id)
        .order_by(UserProvider.created_at.desc())
        .all()
    )
    result = []
    for assoc in associations:
        p = assoc.provider
        result.append(UserProviderRead(
            id=p.id,
            name=p.name,
            kind=p.kind.value,
            is_default=assoc.is_default,
            created_at=assoc.created_at,
        ))
    return result


@router.post(
    "/providers",
    response_model=ProviderRead,
    status_code=status.HTTP_201_CREATED,
    name="create_user_provider",
)
def create_user_provider(
    data: ProviderCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ProviderRead:
    """Create a user provider (config is encrypted before storage)."""
    # Encrypt config
    config_json = json.dumps(data.config.model_dump(), separators=(",", ":"))
    encrypted_config = encrypt(config_json, settings.aes_key_bytes)

    # Create provider
    provider = Provider(
        name=data.name,
        kind=ProviderKind.USER,
        config=encrypted_config,
    )
    db.add(provider)
    db.flush()  # get provider.id

    # Check if this is the user's first provider → set as default
    existing_count = db.query(UserProvider).filter(UserProvider.user_id == user_id).count()
    user_provider = UserProvider(
        user_id=user_id,
        provider_id=provider.id,
        is_default=(existing_count == 0),
    )
    db.add(user_provider)
    db.commit()
    db.refresh(provider)

    return ProviderRead.model_validate(provider)


@router.get("/providers/{provider_id}", response_model=ProviderDetailRead, name="get_user_provider")
def get_user_provider(
    provider_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ProviderDetailRead:
    """Return a user provider with decrypted config for editing."""
    assoc = _get_user_provider_association(db, user_id, provider_id)
    return _build_provider_detail(assoc.provider)


@router.patch("/providers/{provider_id}", response_model=ProviderRead, name="update_user_provider")
def update_user_provider(
    provider_id: str,
    data: ProviderUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ProviderRead:
    """Update a user provider and replace its encrypted config."""
    assoc = _get_user_provider_association(db, user_id, provider_id)
    provider = assoc.provider
    if provider.kind == ProviderKind.INTERNAL:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update internal provider")

    provider.name = data.name
    config_json = json.dumps(data.config.model_dump(), separators=(",", ":"))
    provider.config = encrypt(config_json, settings.aes_key_bytes)

    db.add(provider)
    db.commit()
    db.refresh(provider)
    return ProviderRead.model_validate(provider)


@router.delete("/providers/{provider_id}", status_code=status.HTTP_204_NO_CONTENT, name="delete_user_provider")
def delete_user_provider(
    provider_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:
    """Delete a user-provider association (not the Provider itself)."""
    assoc = (
        db.query(UserProvider)
        .filter(UserProvider.user_id == user_id, UserProvider.provider_id == provider_id)
        .first()
    )
    if not assoc:
        # Check if it exists but belongs to another user
        provider = db.get(Provider, provider_id)
        if not provider:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
        if provider.kind == ProviderKind.INTERNAL:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete internal provider")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not associated with user")

    # If deleting the default provider, reassign default to most recent remaining
    if assoc.is_default:
        remaining = (
            db.query(UserProvider)
            .filter(UserProvider.user_id == user_id, UserProvider.provider_id != provider_id)
            .order_by(UserProvider.created_at.desc())
            .first()
        )
        if remaining:
            remaining.is_default = True

    db.delete(assoc)
    db.commit()


@router.put(
    "/providers/{provider_id}/default",
    response_model=UserProviderRead,
    name="set_default_provider",
)
def set_default_provider(
    provider_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> UserProviderRead:
    """Set a provider as the user's default."""
    target = (
        db.query(UserProvider)
        .filter(UserProvider.user_id == user_id, UserProvider.provider_id == provider_id)
        .first()
    )
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not associated with user")

    # Clear all defaults for this user
    db.query(UserProvider).filter(UserProvider.user_id == user_id).update({"is_default": False})

    # Set new default
    target.is_default = True
    db.add(target)
    db.commit()
    db.refresh(target)

    p = target.provider
    return UserProviderRead(
        id=p.id,
        name=p.name,
        kind=p.kind.value,
        is_default=target.is_default,
        created_at=target.created_at,
    )


@router.post(
    "/providers/{provider_id}/test",
    response_model=ProviderTestResult,
    name="test_user_provider",
)
def test_user_provider(
    provider_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ProviderTestResult:
    """Test connectivity of a user provider."""
    assoc = (
        db.query(UserProvider)
        .filter(UserProvider.user_id == user_id, UserProvider.provider_id == provider_id)
        .first()
    )
    if not assoc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")

    provider = assoc.provider
    if provider.kind == ProviderKind.INTERNAL:
        return ProviderTestResult(success=False, message="内部提供商不支持测试")

    return test_provider_connectivity(provider)
