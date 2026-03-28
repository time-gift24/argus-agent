"""User profile endpoints: GET /me, PATCH /me."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user_id
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserPatch, UserRead

router = APIRouter(tags=["users"])


@router.get("/me", response_model=UserRead, name="get_me")
def get_me(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> UserRead:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead.model_validate(user)


@router.patch("/me", response_model=UserRead, name="patch_me")
def patch_me(
    data: UserPatch,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> UserRead:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if data.name is not None:
        user.name = data.name
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user)
