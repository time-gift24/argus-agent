"""Provider endpoints: user providers, internal providers, and provider models."""

from __future__ import annotations

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user_id
from app.core.config import settings
from app.core.crypto import decrypt, encrypt
from app.db.session import get_db
from app.models.user import Provider, ProviderKind, ProviderModel, UserProvider
from app.schemas.user import (
    DefaultUpdate,
    ProviderConfigInput,
    ProviderCreate,
    ProviderDetailRead,
    ProviderModelCreate,
    ProviderModelRead,
    ProviderRead,
    ProviderTestResult,
    ProviderUpdate,
    TestConfigInput,
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


def _get_user_provider(db: Session, user_id: str, provider_id: str) -> Provider:
    """Get a provider owned by the user (via association)."""
    _get_user_provider_association(db, user_id, provider_id)
    return db.get(Provider, provider_id)


def _create_provider_models(db: Session, provider_id: str, model_names: list[str]) -> None:
    """Create provider model rows, marking the first model as default."""
    for index, model_name in enumerate(model_names):
        db.add(
            ProviderModel(
                provider_id=provider_id,
                name=model_name,
                is_default=(index == 0),
            )
        )


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
    body: TestConfigInput,
    _: str = Depends(get_current_user_id),
) -> ProviderTestResult:
    """Test connectivity with raw config (for create/edit forms). Model is a top-level field."""
    return test_config_connectivity(body.model_dump())


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
    config_json = json.dumps(data.config.model_dump(), separators=(",", ":"))
    encrypted_config = encrypt(config_json, settings.aes_key_bytes)

    provider = Provider(
        name=data.name,
        kind=ProviderKind.USER,
        config=encrypted_config,
    )
    db.add(provider)
    db.flush()

    existing_count = db.query(UserProvider).filter(UserProvider.user_id == user_id).count()
    user_provider = UserProvider(
        user_id=user_id,
        provider_id=provider.id,
        is_default=(existing_count == 0),
    )
    db.add(user_provider)

    if data.models:
        _create_provider_models(db, provider.id, data.models)

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
        provider = db.get(Provider, provider_id)
        if not provider:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
        if provider.kind == ProviderKind.INTERNAL:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete internal provider")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not associated with user")

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

    db.query(UserProvider).filter(UserProvider.user_id == user_id).update({"is_default": False})

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
    """Test connectivity of a user provider's default model."""
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

    default_model = (
        db.query(ProviderModel)
        .filter(ProviderModel.provider_id == provider_id, ProviderModel.is_default == True)
        .first()
    )
    if not default_model:
        return ProviderTestResult(success=False, message="该 Provider 尚未配置模型")

    return test_provider_connectivity(provider, default_model.name)


# ── Provider Models ──────────────────────────────────────────────────────────


@router.get(
    "/providers/{provider_id}/models",
    response_model=list[ProviderModelRead],
    name="list_provider_models",
)
def list_provider_models(
    provider_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> list[ProviderModelRead]:
    """List all models for a provider."""
    _get_user_provider_association(db, user_id, provider_id)
    models = (
        db.query(ProviderModel)
        .filter(ProviderModel.provider_id == provider_id)
        .order_by(ProviderModel.created_at)
        .all()
    )
    return [ProviderModelRead.model_validate(m) for m in models]


@router.post(
    "/providers/{provider_id}/models",
    response_model=ProviderModelRead,
    status_code=status.HTTP_201_CREATED,
    name="add_provider_model",
)
def add_provider_model(
    provider_id: str,
    data: ProviderModelCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ProviderModelRead:
    """Add a model to a provider. First model auto-set as default."""
    _get_user_provider_association(db, user_id, provider_id)

    existing = (
        db.query(ProviderModel)
        .filter(ProviderModel.provider_id == provider_id, ProviderModel.name == data.name)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"模型 '{data.name}' 已存在",
        )

    is_first = db.query(ProviderModel).filter(ProviderModel.provider_id == provider_id).count() == 0

    model = ProviderModel(
        provider_id=provider_id,
        name=data.name,
        is_default=is_first,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return ProviderModelRead.model_validate(model)


@router.delete(
    "/providers/{provider_id}/models/{model_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_provider_model",
)
def delete_provider_model(
    provider_id: str,
    model_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:
    """Delete a model from a provider. Reassigns default if needed."""
    _get_user_provider_association(db, user_id, provider_id)

    model = db.get(ProviderModel, model_id)
    if not model or model.provider_id != provider_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="模型不存在")

    was_default = model.is_default
    db.delete(model)
    db.flush()

    if was_default:
        new_default = (
            db.query(ProviderModel)
            .filter(ProviderModel.provider_id == provider_id)
            .order_by(ProviderModel.created_at.desc())
            .first()
        )
        if new_default:
            new_default.is_default = True

    db.commit()


@router.put(
    "/providers/{provider_id}/models/{model_id}/default",
    response_model=ProviderModelRead,
    name="set_default_provider_model",
)
def set_default_provider_model(
    provider_id: str,
    model_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ProviderModelRead:
    """Set a model as the default for its provider."""
    _get_user_provider_association(db, user_id, provider_id)

    model = db.get(ProviderModel, model_id)
    if not model or model.provider_id != provider_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="模型不存在")

    db.query(ProviderModel).filter(ProviderModel.provider_id == provider_id).update({"is_default": False})
    model.is_default = True
    db.add(model)
    db.commit()
    db.refresh(model)
    return ProviderModelRead.model_validate(model)


@router.post(
    "/providers/{provider_id}/models/{model_id}/test",
    response_model=ProviderTestResult,
    name="test_provider_model",
)
def test_provider_model(
    provider_id: str,
    model_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ProviderTestResult:
    """Test connectivity of a specific model under a provider."""
    _get_user_provider_association(db, user_id, provider_id)

    model = db.get(ProviderModel, model_id)
    if not model or model.provider_id != provider_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="模型不存在")

    provider = db.get(Provider, provider_id)
    if not provider or provider.kind == ProviderKind.INTERNAL:
        return ProviderTestResult(success=False, message="内部提供商不支持测试")

    return test_provider_connectivity(provider, model.name)
