from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, VARCHAR
from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, )
    username = Column(String(50), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    password = Column(String(50))
    is_active = Column(Boolean, default=True)
    role = Column(String(50))

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description = Column(String(50))
    priority = Column(String(50))
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
