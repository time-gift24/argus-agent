from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.tool import Tool
from app.schemas.tool import ToolRead, ToolList

router = APIRouter()


@router.get("/", response_model=ToolList)
def list_tools(db: Session = Depends(get_db)):
    tools = db.query(Tool).all()
    return ToolList(data=[ToolRead.model_validate(t) for t in tools])
