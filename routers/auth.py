from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

router = APIRouter()

SECRET_KEY = "449640aec2bdc59c201c898a8c88971c18d19a682a344da84e6a94af8ac56364"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authorize_user(username: str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.password):
        return None

    return user


def create_access_token(username:str,user_id: int,  expiration_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.utcnow() + expiration_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    user = Users(
        email= create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active=True,
    )

    db.add(user)
    db.commit()


@router.post("/token")
async def login_for_access_token(db: db_dependency,
                                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authorize_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, detail="password is wrong")

    token = create_access_token(user.username, user.id, expiration_delta=timedelta(minutes=20))
    token_resp = {"token_type": "Bearer", "token":token}
    return token_resp

