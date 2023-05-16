from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from models import Todos, Users
from database import SessionLocal
from .auth import get_current_user, authorize_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=3, max_length=100)
    new_password: str = Field(min_length=3, max_length=100)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/",status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authorization Failed")
    user = db.query(Users).filter(Users.id == user.get("id")).first()

    return user


@router.put("/change_password", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency, change_password_form: ChangePasswordRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authorization Failed")
    user = db.query(Users).filter(Users.id == user.get("id")).first()
    validation = authorize_user(user.username, change_password_form.current_password, db)
    if validation is None:
        raise HTTPException(status_code=401, detail="current password is not valid")

    user.password = bcrypt_context.hash(change_password_form.new_password)
    db.add(user)
    db.commit()
    return "password got changed"

