from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from models import Todos
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get("/todo/{todo_id}")
async def read_by_id(todo_id: int, db: db_dependency):
    todo_models = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_models is not None:
        return todo_models
    raise HTTPException(status_code=404, detail="Todos not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit()


@router.put("/update-todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def create_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todos not found")

    todo_model.description = todo_request.description
    todo_model.title = todo_request.title
    todo_model.complete = todo_request.complete
    todo_model.priority = todo_request.priority

    db.add(todo_model)
    db.commit()


@router.delete("/delete-todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def create_todo(db: db_dependency, todo_id: int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todos not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()
