from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import LLMProvider
from app.schemas.llm_provider import LLMProviderCreate, LLMProviderUpdate


class LLMProviderService:
    def __init__(self, db: Session):
        self.db = db

    def list(self, skip: int = 0, limit: int = 100) -> List[LLMProvider]:
        return self.db.query(LLMProvider).offset(skip).limit(limit).all()

    def get(self, id: str) -> Optional[LLMProvider]:
        return self.db.query(LLMProvider).filter(LLMProvider.id == id).first()

    def get_by_name(self, name: str) -> Optional[LLMProvider]:
        return self.db.query(LLMProvider).filter(LLMProvider.name == name).first()

    def create(self, data: LLMProviderCreate) -> LLMProvider:
        provider = LLMProvider(**data.model_dump())
        self.db.add(provider)
        self.db.commit()
        self.db.refresh(provider)
        return provider

    def update(self, id: str, data: LLMProviderUpdate) -> Optional[LLMProvider]:
        provider = self.get(id)
        if not provider:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(provider, key, value)
        self.db.commit()
        self.db.refresh(provider)
        return provider

    def delete(self, id: str) -> bool:
        provider = self.get(id)
        if not provider:
            return False
        self.db.delete(provider)
        self.db.commit()
        return True
