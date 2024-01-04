from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    lname = Column(String)
    fname = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    todos = relationship("TODO", back_populates="owner")

class TODO(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="todos")
    