from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.llm_provider_service import LLMProviderService
from app.schemas.llm_provider import LLMProviderCreate, LLMProviderUpdate, LLMProviderRead

router = APIRouter(prefix="/llm-providers", tags=["LLM Providers"])


@router.get("", response_model=List[LLMProviderRead])
def list_providers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return LLMProviderService(db).list(skip=skip, limit=limit)


@router.post("", response_model=LLMProviderRead, status_code=status.HTTP_201_CREATED)
def create_provider(data: LLMProviderCreate, db: Session = Depends(get_db)):
    svc = LLMProviderService(db)
    if svc.get_by_name(data.name):
        raise HTTPException(status_code=400, detail="Provider name already exists")
    return svc.create(data)


@router.get("/{provider_id}", response_model=LLMProviderRead)
def get_provider(provider_id: str, db: Session = Depends(get_db)):
    provider = LLMProviderService(db).get(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


@router.patch("/{provider_id}", response_model=LLMProviderRead)
def update_provider(provider_id: str, data: LLMProviderUpdate, db: Session = Depends(get_db)):
    provider = LLMProviderService(db).update(provider_id, data)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_provider(provider_id: str, db: Session = Depends(get_db)):
    if not LLMProviderService(db).delete(provider_id):
        raise HTTPException(status_code=404, detail="Provider not found")
