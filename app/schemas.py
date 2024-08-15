from pydantic import BaseModel, EmailStr
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


############# User schemas

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


# create schema (pydantic model) that extends BaseModel class (defines shape of data)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


#### this is response model
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
