from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, VARCHAR
from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), unique=True, )
    username = Column(String(200), unique=True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    password = Column(String(500))
    is_active = Column(Boolean, default=True)
    role = Column(String(200))

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(String(200))
    priority = Column(String(200))
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
