from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from models import Users

router = APIRouter()


class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/auth/")
async def create_user(create_user_request: CreateUserRequest):
    user = Users(
        email= create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        password=create_user_request.password,
        role=create_user_request.role,
        is_active=True,
    )
    return user

