from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    lname: str
    fname: str
    password: str

class TODOBase (BaseModel):
    text: str
    completed: bool

class TODO(TODOBase):
    owner_id: int

    class Config:
        orm_mode = True

class TODOResponse(TODO):
    id: int

class TODOUpdate(TODOBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    email: Optional[str] = None
