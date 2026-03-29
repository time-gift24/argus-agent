from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.auth.deps import get_current_user_id
from app.db.session import get_db
from app.models.tool import Tool
from app.schemas.tool import ToolRead, ToolCreate, ToolList

router = APIRouter()


@router.get("/", response_model=ToolList)
def list_tools(db: Session = Depends(get_db)):
    tools = db.query(Tool).all()
    return ToolList(data=[ToolRead.model_validate(t) for t in tools])


@router.post("/", response_model=ToolRead, status_code=201)
def create_tool(
    body: ToolCreate,
    _: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    if db.query(Tool).filter(Tool.name == body.name).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tool with this name already exists",
        )
    tool = Tool(**body.model_dump(), is_builtin=False)
    db.add(tool)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tool with this name already exists",
        ) from exc
    db.refresh(tool)
    return tool


@router.delete("/{tool_id}", status_code=204)
def delete_tool(
    tool_id: str,
    _: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    if tool.is_builtin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete builtin tools",
        )
    db.delete(tool)
    db.commit()
